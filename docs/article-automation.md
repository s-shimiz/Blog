# 記事作成の自動化（ネタ出し〜レビュー〜スクショ〜投稿）

毎週 1 本の記事を、AI と著者の分担で仕上げて Qiita に投稿するための仕組みです。
著者がやることは「ネタを選ぶ」「レビューしてコメントする」「スクショ撮影を実行する」「マージする」の 4 つです。

## 全体の流れ

```text
[毎週月曜 9:00 JST]  weekly-ideas.yml   ／   [任意のタイミング] 「/ideas テーマ」コメント・Run workflow
  ① AI がネタ候補 5 件を Issue にする（ラベル: article-idea）
        │ 著者: 自分のアイデアがあれば「/add-idea タイトル」で候補に追加（何件でも）
        │ 著者: Issue に「/write 2」とコメント（2 行目以降に補足を書ける）
        ▼
  ② article-commands.yml（write）
     AI が drafts/yyyymmdd_slug.md と撮影計画 .shot-plan.md を作成
     → PR を作成（ラベル: article-draft）→ 自動レビューを PR にコメント
        │ 著者: PR を読み「/revise 修正指示や感想」とコメント（何度でも）
        ▼
  ③ article-commands.yml（/revise）
     AI がフィードバックを反映してコミット → 反映結果と再レビューをコメント
     （レビューだけやり直したいときは「/review」）
        │ 著者: ローカルの VS Code で /capture-screenshots を実行し、PR ブランチに push
        ▼
  ④ スクショ撮影（ローカル）
     Playwright MCP で撮影 → ms-tech-validation の mask.py で機密情報を隠す
     → images/<slug>/ に保存 → 記事中の <!-- SHOT: ... --> を画像に置き換え
        │ 著者: PR に「/publish」とコメント（限定共有のままなら「/publish private」）
        ▼
  ⑤ article-commands.yml（/publish）
     公開前チェック → 記事を public/ に移動、private を設定、画像を GitHub の URL に変換
        │ 著者: PR をマージ（ここが最終承認）
        ▼
  ⑥ publish.yml（既存）が Qiita に投稿
```

## 構成ファイル

| ファイル | 役割 |
|---------|------|
| `.github/workflows/weekly-ideas.yml` | ネタ候補 Issue の作成（毎週の自動実行・手動実行・`/ideas` から呼び出し） |
| `.github/workflows/article-commands.yml` | `/ideas` `/add-idea` `/write` `/revise` `/review` `/publish` コマンドの処理 |
| `.github/actions/copilot-run/action.yml` | Copilot CLI を権限を絞って実行する共通処理 |
| `.github/automation/prompts/*.md` | AI への指示（ネタ出し・下書き・レビュー・修正） |
| `scripts/blog_automation.py` | 記事ファイルの特定、公開前チェック、public/ への移動 |
| `.github/skills/article-screenshots/SKILL.md` | 撮影・マスク・記事への差し込み手順 |
| `.github/prompts/capture-screenshots.prompt.md` | VS Code で撮影を始めるプロンプト |
| `.github/prompts/apply-feedback.prompt.md` | `/revise` のローカル版 |
| `.vscode/mcp.json` | Playwright MCP（Edge・専用プロファイル） |

## 初期設定

### 1. GitHub 側

1. **Copilot CLI 用のトークン**: fine-grained personal access token を作成し、**Copilot Requests** 権限を付ける。
   リポジトリの **Settings > Secrets and variables > Actions** に `COPILOT_PAT` として登録する。
   - 個人リポジトリなので `GITHUB_TOKEN` ではなく PAT を使います。AI の利用分は PAT の持ち主の Copilot プランから消費されます。
2. **`QIITA_TOKEN`** が登録済みか確認する（既存の publish.yml が使用）。
3. **Settings > Actions > General > Workflow permissions** で次を有効にする。
   - Read and write permissions
   - Allow GitHub Actions to create and approve pull requests（PR の自動作成に必要）
4. これらのファイルを `main` ブランチにマージする（`issue_comment` と `schedule` は `main` のワークフローだけが動きます）。
5. **Actions > Article ideas > Run workflow** で 1 回手動実行し、Issue ができることを確認する。

### 2. ローカル側（スクショ撮影）

1. Node.js 20 以上と Python、Pillow（`pip install Pillow`）を用意する。
2. VS Code で `.vscode/mcp.json` の `playwright` サーバーを起動する。
3. 初回だけ、Playwright が開いた Edge で Microsoft 365 / Copilot Studio に手動でサインインする（MFA を含む）。
   以降は `~/.playwright-blog-edge-profile` にセッションが残ります。
4. ms-tech-validation スキルの場所が既定（`C:\Users\MODAdministrator\.scout\m-skills\ms-tech-validation`）と違う場合は、
   環境変数 `MS_TECH_VALIDATION_SKILL` にパスを設定する。

## 使い方のポイント

- **コマンドはリポジトリのオーナーのコメントだけ**に反応します（他人のコメントによる AI の誤作動を防ぐため）。

### ネタ出しを好きなタイミングで行う

- **コメントで**: どの Issue でもよいので `/ideas` とコメントすると、新しいネタ候補 Issue が作られます。
  テーマを指定するとそれに沿った候補になります（2 行目以降に条件を書いても可）。

  ```text
  /ideas Copilot Studio のナレッジ連携
  初心者向けで、画面操作が多いもの
  ```

- **Actions 画面から**: **Actions > Article ideas > Run workflow** で、テーマ（任意）を入力して実行します。
  CLI なら `gh workflow run weekly-ideas.yml -f theme="Copilot Studio のナレッジ連携"`。

### 自分のアイデアを追加する

- ネタ候補 Issue に `/add-idea タイトル` とコメントすると、**次の番号の候補として Issue 本文に追加**されます。
  2 行目以降はメモとして残り、`/write` で下書きを作るときに最優先で反映されます。

  ```text
  /add-idea Teams 会議の要約を Copilot で自動化してみた
  実際に社内の定例で試した流れで書きたい
  画面多め
  ```

- 自分で作った普通の Issue に `/add-idea` しても使えます（`article-idea` ラベルが自動で付き、`/write` できるようになります）。
  ネタのストック用 Issue を 1 つ作っておき、思いついたら追加していく使い方もできます。

### レビューと修正
- PR 上のコマンドは、GitHub の **Conversation** タブのコメントだけでなく、VS Code（GitHub Pull Requests 拡張機能）の PR 画面下部のコメント欄からも送れます。
  VS Code から送ったコメントは GitHub ではレビューとして扱われるため、👀 の代わりに「受け付けました」というコメントが付きます。
- `/revise` には修正指示だけでなく感想も書けます。例:

  ```text
  /revise
  - 「はじめに」が硬いので、もう少しくだけた感じに
  - 手順 3 のところは実際にやるとエラーになりやすいので注意書きを入れて
  - まとめの最後の一言はいい感じ！
  ```

- 公開前チェック（`python scripts/blog_automation.py check <記事>`）は、フロントマター、仮テキスト、
  見出しレベル、コードブロックの言語指定、画像の有無、**未撮影のプレースホルダー**を確認します。
- `/publish` は `../images/...` の画像を `https://raw.githubusercontent.com/<repo>/main/images/...` に置き換えます。
  Qiita から画像が見えるのは**リポジトリが公開されている場合だけ**です。
- `images/_raw/` はマスク前の画像なので Git に含めません（`.gitignore` 済み）。

## 制約と注意

- **GitHub Models は 2026-07-30 に提供終了**したため、Actions 内の AI には Copilot CLI（`copilot -p`）を使っています。
- AI に許可しているのはファイルの書き込みと読み取り系コマンド、learn.microsoft.com へのアクセスだけです。`git push` や PR の作成はワークフローの決まった手順で行います。
- AI のレビューは公式情報との照合が不十分なことがあります。技術的な事実の最終確認は著者が行ってください。
- スケジュール実行は混雑時に遅れることがあります。公開リポジトリで 60 日間動きがないと、スケジュール実行は自動で止まります。
- スクショ撮影はクラウドでは行いません（M365 のサインインと MFA が必要で、認証情報をクラウドに置かないため）。
