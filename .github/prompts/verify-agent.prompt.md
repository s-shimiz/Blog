---
description: "Copilot Studio エージェントの検証テストを実行する。テストシナリオの生成からブラウザ自動テスト、スクショ付きレポート生成までを一括で行う。"
agent: "copilot-studio-verifier"
argument-hint: "検証対象のエージェント名またはテスト URL"
tools: [read, edit, search, web]
---

以下の手順で Copilot Studio エージェントの検証テストを実行してください。

1. `.github/skills/copilot-studio-verifier/SKILL.md` を読み込む
2. ユーザーから検証対象のエージェント情報をヒアリングする
   - エージェント名
   - テスト URL（Copilot Studio のテストパネル URL）
   - トピック一覧 / フロー構成 / ナレッジソース（わかる範囲で）
   - 検証の目的と重点ポイント
3. テストシナリオを生成し、ユーザーの承認を得る
4. Playwright MCP でブラウザを起動し、テストを実行する
5. 各シナリオごとにスクリーンショットを取得する
6. 検証レポートを `verification/` ディレクトリに出力する
