---
description: "Zenn 記事の作成・編集時に適用。Zenn フロントマター、topics 規約、命名規則、Zenn 固有記法を含む。Use when: Zenn 記事を書く、articles/ 配下のファイルを編集"
applyTo: "articles/**/*.md"
---

# Zenn 記事ルール

## フロントマター

記事の先頭には必ず以下の形式の YAML フロントマターを付ける。

```yaml
---
title: "記事のタイトル"
emoji: "😸"
type: "tech"
topics: [microsoft365, copilot, copilotstudio]
published: true
publication_name: "microsoft"
---
```

- `title`: 記事の内容が伝わる日本語のタイトル。シリーズ記事は `"タイトル - シリーズ名 そのN"` の形式
- `emoji`: 記事を表す絵文字を 1 つ選ぶ。猫系（😸😽）をよく使うが、内容に合った絵文字でもよい
- `type`: 技術記事は `"tech"`、アイデア系は `"idea"`
- `topics`: 小文字で記事に関連するタグを**最大 5 つ**（例: `[csharp, dotnet, azure, ai, agent]`）
- `published`: 下書きは `false`、公開時に `true`
- `publication_name`: 常に `"microsoft"` を設定する

## ファイル命名

- ケバブケース（小文字・ハイフン区切り）（例: `mcp-azurefunctions.md`）
- シリーズ記事は `シリーズ名-001.md` のように 3 桁の連番を付ける

## Zenn 固有の記法

### リンクカード

URL を独立した行に記載すると Zenn が自動的にカード形式で埋め込む。積極的に使う。

```markdown
公式ドキュメントは以下になります。

https://learn.microsoft.com/ja-jp/...
```

### メッセージボックス

```markdown
:::message
この機能はプレビュー版です。本番環境での使用は推奨されていません。
:::

:::message alert
破壊的変更が含まれています。
:::
```

### 画像

```markdown
![代替テキスト](/images/記事のスラッグ/ファイル名.png)
```

### コードブロック（ファイル名付き）

````markdown
```csharp:Program.cs
var builder = WebApplication.CreateBuilder(args);
```
````
