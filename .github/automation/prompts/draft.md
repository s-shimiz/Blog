あなたはこのリポジトリの著者として Qiita 記事の下書きを書きます。ユーザーへの質問はせず、自分で判断して最後まで進めてください。

## 入力

- 環境変数 `IDEAS_FILE`: 今週のネタ候補（Issue 本文）
- 環境変数 `IDEA_NUMBER`: 採用するネタの番号
- 環境変数 `EXTRA_NOTE_FILE`: 著者からの追加メモ（空の場合あり）。内容があれば構成に反映する
- 環境変数 `TODAY`: 今日の日付（yyyymmdd）

## 必ず守るルール

- `.github/copilot-instructions.md`、`.github/skills/blog-writer/SKILL.md`、
  `.github/skills/blog-writer/references/style-guide.md`、`.github/skills/blog-writer/references/qiita-template.md`、
  `.github/instructions/qiita-article.instructions.md` を読み、文体・構成・フロントマターに従う。
- 文体の参考として `public/` の既存記事を 1 本以上読む。
- 技術的な内容は learn.microsoft.com の公式情報に基づく。確認できなかった内容は書かないか、
  本文中で「未確認」と分かるようにする。
- フロントマターは `private: true` にする。

## 作成するファイル（この 2 つだけ）

1. `drafts/<TODAY>_<slug>.md` … 記事本文。slug はネタ候補の slug を使う。slug が「未定」の場合（著者のアイデア）は、
   タイトルから英小文字とハイフンのみで決める。候補に「著者メモ」があれば、その内容を最優先で構成に反映する。
2. `drafts/<TODAY>_<slug>.shot-plan.md` … スクリーンショット撮影計画。

### スクリーンショットの扱い

記事中でスクリーンショットを入れたい場所には、画像の代わりに次のプレースホルダーを 1 行で置く。

```text
<!-- SHOT: 01_open-copilot-studio.png | Copilot Studio のホーム画面 -->
```

ファイル名は `<連番2桁>_<英小文字とハイフン>.png`。撮影はあとで著者がローカルで行う。

撮影計画ファイルは次の形式で書く。

```markdown
# 撮影計画: <記事タイトル>

- 記事: drafts/<TODAY>_<slug>.md
- 保存先: images/<slug>/
- 前提: 必要なライセンス・権限・事前に作っておくもの

| ID | ファイル名 | 画面 / URL | 操作手順 | 写す範囲 | マスクが必要な情報 |
|----|-----------|-----------|---------|---------|------------------|
| 01 | 01_open-copilot-studio.png | https://copilotstudio.microsoft.com/ | 1. ... | 画面全体 | テナント名、ユーザー名 |
```

記事中のプレースホルダーと撮影計画の行は 1 対 1 で対応させる。
