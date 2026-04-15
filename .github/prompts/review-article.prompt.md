---
description: "既存のブログ記事をレビューし、技術的正確性・文体・構成のフィードバックを提供する。"
agent: "blog-reviewer"
argument-hint: "レビュー対象の記事ファイルパス"
tools: [read, search, web]
---

指定された記事ファイルを `.github/skills/article-reviewer/` スキルの手順に従ってレビューしてください。

- 著者の文体ガイド（`.github/skills/blog-writer/references/style-guide.md`）と既存記事を参照して文体を把握する
- レビューチェックリスト（`.github/skills/article-reviewer/references/review-checklist.md`）に基づいてチェックする
- 🔴 要修正 / 🟡 改善推奨 / 🟢 良い点 の 3 段階で結果を出力する
- **修正は行わず、指摘事項のリストのみを出力する**
