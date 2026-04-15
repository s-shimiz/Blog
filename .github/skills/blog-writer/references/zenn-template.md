# Zenn 記事テンプレート

## フロントマター

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

### フィールド説明

| フィールド | 説明 |
|-----------|------|
| `title` | 日本語のタイトル。シリーズ記事は `"タイトル - シリーズ名 そのN"` |
| `emoji` | 記事を表す絵文字を 1 つ。猫系（😸😽）をよく使うが、内容に合ったものでもよい |
| `type` | 技術記事は `"tech"`、アイデア系は `"idea"` |
| `topics` | 小文字で関連タグを**最大 5 つ** |
| `published` | 下書きは `false`、公開時に `true` |
| `publication_name` | 常に `"microsoft"` |

## ファイル命名

`articles/slug.md`（ケバブケース）

例: `articles/mcp-azurefunctions.md`

シリーズ記事: `articles/semantic-kernel-001.md`

## 記事テンプレート

```markdown
---
title: ""
emoji: "😸"
type: "tech"
topics: []
published: false
publication_name: "microsoft"
---

## はじめに

（この記事で何をやるか、動機や背景を 2〜4 文で簡潔に）

## 本文

（本文）

## まとめ

（振り返りと今後の展望）
```

## Zenn 固有の記法

### リンクカード

URL を独立した行に置くとカード化される。積極的に使う。

```markdown
公式ドキュメントは以下になります。

https://learn.microsoft.com/ja-jp/...
```

### メッセージボックス

```markdown
:::message
補足情報やプレビュー版への注意を書く
:::

:::message alert
破壊的変更や重大な注意事項
:::
```

### 画像

```markdown
![代替テキスト](/images/記事のスラッグ/ファイル名.png)
```

- 画像ファイルは `/images/記事のスラッグ/` ディレクトリに配置する。

### コードブロック（ファイル名付き）

````markdown
```csharp:Program.cs
var builder = WebApplication.CreateBuilder(args);
```
````

### アコーディオン

```markdown
:::details タイトル
折りたたまれた内容
:::
```

### シリーズ記事の注意書き

```markdown
## シリーズ記事

:::message
この記事はプレビュー版の〇〇を基に書かれています。今後のバージョンアップで内容が変わる可能性があります。
:::

- [その1: タイトル](URL)
- [その2: タイトル](URL)
```
