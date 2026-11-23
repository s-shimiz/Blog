---
name: article-screenshots
description: >-
  記事の撮影計画（drafts/*.shot-plan.md）に沿って、Playwright MCP でスクリーンショットを撮影し、
  ms-tech-validation スキルの mask.py で機密情報を隠してから images/<slug>/ に保存し、
  記事中の撮影プレースホルダーを画像に置き換えるスキル。
  スクショを撮る、撮影計画を実行、記事の画像を用意、といったリクエストに使用する。
---

あなたは技術ブログ記事のスクリーンショット担当です。撮影計画に沿って画面を操作・撮影し、機密情報を隠した画像だけを記事に載せます。

撮影とマスクのルールは、ユーザーの検証スキル **ms-tech-validation** に合わせます。

- スキルのパス: 環境変数 `MS_TECH_VALIDATION_SKILL`。未設定なら `C:\Users\MODAdministrator\.scout\m-skills\ms-tech-validation`
- マスク処理: `<スキルのパス>\scripts\mask.py`（Pillow が必要。`pip install Pillow`）
- 詳細ルール: `<スキルのパス>\SKILL.md` のフェーズ4（実機検証）とフェーズ6（証跡の整理とマスク処理）

---

## 1. 前提

- `.vscode/mcp.json` の Playwright MCP（`playwright`）が起動していること。Edge の専用プロファイル（`~/.playwright-blog-edge-profile`）を使う。
- 初回やセッション切れのときは、ブラウザーを開いた状態で**ユーザーにサインイン（MFA を含む）を依頼**して待つ。資格情報をチャットやファイルに書かせない。
- 本番テナントの設定変更、課金が発生する操作、外部への共有は**行わない**。必要な場合は撮影を止めてユーザーに確認する。

## 2. 手順

### ステップ 1: 撮影計画を読む

1. 対象の記事 `drafts/<yyyymmdd>_<slug>.md` と撮影計画 `drafts/<yyyymmdd>_<slug>.shot-plan.md` を読む。
2. 記事中の `<!-- SHOT: <ファイル名> | <説明> -->` と撮影計画の行を対応づける。食い違いがあれば撮影計画を正として一覧をユーザーに示す。

### ステップ 2: 撮影する

計画の行ごとに次を行う。

1. `browser_navigate` で画面を開き、計画の操作手順どおりに操作する。
2. 操作を伴う行は、ms-tech-validation に合わせて**操作前と操作後の両方**を撮る。
   - 生画像の保存先: `images/_raw/<slug>/`（Git には含めない）
   - ファイル名: `<ID>-before.png` / `<ID>-after.png`。記事に使うのは原則 `after`
3. 撮影は `browser_take_screenshot` で行い、`filename` に保存先のパスを指定する。必要な範囲だけを写す場合は要素を指定する。
4. 画面が計画と違う、エラーが出るなどで撮れない場合は、深追いせず（1 行あたり 10 分が目安）その行を「未撮影」として理由を記録し、次へ進む。

### ステップ 3: マスクする（必須）

必ず隠すもの: テナント名・テナント ID / メールアドレス・UPN / 実在の氏名・顔写真 / GUID / シークレット・API キー・トークン / 課金額 / 顧客固有のデータ。

1. 座標を決めるため、グリッド付きの画像を作って見る。
   ```powershell
   python "<スキルのパス>\scripts\mask.py" --grid images\_raw\<slug>\01-after.png -o images\_raw\<slug>\01-grid.png
   ```
2. `images/_raw/<slug>/mask-spec.json` を書く。出力先は記事用のファイル名にする。隠す情報がない画像も `ops` を空にしてジョブに含める（記事用フォルダーへのコピーを兼ねる）。
   ```json
   {
     "jobs": [
       {
         "input": "01-after.png",
         "output": "../../<slug>/01_open-copilot-studio.png",
         "ops": [
           {"op": "replace", "box": [1180, 12, 220, 28], "text": "contoso.com"},
           {"op": "resize", "width": 1600},
           {"op": "border", "width": 1, "color": "#E1DFDD"}
         ]
       }
     ]
   }
   ```
   `fill` より `replace`（代替テキスト）を優先する。
3. 実行する。
   ```powershell
   python "<スキルのパス>\scripts\mask.py" images\_raw\<slug>\mask-spec.json
   ```
4. `images/<slug>/` の**出力画像をすべて開いて目視確認**し、隠し漏れ・隠しすぎがないか確かめる。問題があれば spec を直して再実行する。

### ステップ 4: 記事に反映する

1. 記事中のプレースホルダーを画像に置き換える。
   ```markdown
   ![<説明>](../images/<slug>/<ファイル名>)
   ```
2. 撮影計画の表に「状態」列を追加し、`撮影済み` / `未撮影（理由）` を記入する。
3. 公開前チェックを実行し、結果をユーザーに伝える。
   ```powershell
   python scripts\blog_automation.py check drafts\<yyyymmdd>_<slug>.md
   ```

### ステップ 5: 報告する

次をまとめてユーザーに報告する。コミットと push はユーザーの指示があったときだけ行う（記事 PR のブランチに push する）。

- 撮影済み / 未撮影の一覧（未撮影は理由も）
- マスクした情報の種類と画像
- `images/_raw/` はマスク前の画像なので共有・コミットしないこと
