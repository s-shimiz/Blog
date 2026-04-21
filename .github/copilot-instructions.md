# Copilot Instructions — M365 Copilot & Copilot Studio ブログ

## プロジェクト概要

Microsoft 365 Copilot および Copilot Studio に関する技術ブログ記事の原稿を管理するリポジトリ。
記事は **Qiita** に投稿する。Qiita CLI で投稿・管理を行う。

## ディレクトリ構成

```
public/            # Qiita 用の記事（Qiita CLI の管理ディレクトリ。投稿済み記事のみ配置）
drafts/            # 下書き・執筆中の記事（投稿準備ができたら public/ に移動）
images/            # 記事で使用するスクリーンショット・図
images/verification/ # 検証テストのスクリーンショット
verification/      # Copilot Studio 検証レポート
snippets/          # 記事内で参照するコードスニペット
scripts/           # MD→PPTX 変換などのユーティリティ
Template/          # PowerPoint テンプレート
```

## ファイル命名規則

- **Qiita**: `public/yyyymmdd_slug.md`（例: `20260217_agent-builder-vs-copilot-studio.md`）
- **下書き**: `drafts/yyyymmdd_slug.md`（投稿準備ができたら `public/` に移動）

## 執筆規約

1. **言語**: 日本語で執筆する
2. **見出し**: `##` から始める（`#` は Qiita/Zenn がタイトルに使用）
3. **画像**: `images/<記事slug>/` 配下に配置し、相対パスで参照
4. **コードブロック**: 言語を必ず指定する（`power-fx`, `json`, `typescript`, `python`, `yaml` など）
5. **Microsoft 製品名**: 正式名称を使う（例: ✅ `Microsoft 365 Copilot` / ❌ `M365 Copilot`、ただし記事内で初出以降は `Copilot` と略記可）
6. **スクリーンショット**: UI 操作の手順記事では必ず添付する
7. **対象読者**: Copilot / Power Platform に興味がある日本語話者の開発者・IT 管理者
8. **技術的正確性**: 公式ドキュメント（learn.microsoft.com）の情報に基づくこと

## 関連カスタマイズ

- **記事テンプレート・文体ルール・執筆ワークフロー**: `.github/skills/blog-writer/` スキルを参照
- **レビュー観点**: `.github/skills/article-reviewer/` スキルを参照
- **Copilot Studio 検証**: `.github/skills/copilot-studio-verifier/` スキルを参照
