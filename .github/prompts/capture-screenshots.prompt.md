---
description: "記事の撮影計画に沿ってスクリーンショットを撮影・マスクし、記事に差し込む。"
agent: "agent"
argument-hint: "対象の記事ファイル（例: drafts/20261123_copilot-studio-agent-flows.md）"
---

`.github/skills/article-screenshots/SKILL.md` の手順に従って、指定された記事のスクリーンショットを用意してください。

- 記事ファイルが指定されていない場合は、現在のブランチで変更されている `drafts/*.md` を対象にする。
- 撮影には `.vscode/mcp.json` の Playwright MCP を使う。サインインが必要な場合は、ブラウザーを開いたまま私に依頼して待つ。
- マスク処理は ms-tech-validation スキルの `mask.py` を使い、出力画像は必ず目視で確認する。
- 最後に、撮影済み / 未撮影の一覧と公開前チェックの結果を報告する。コミット・push は私が指示したときだけ行う。
