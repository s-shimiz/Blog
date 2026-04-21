---
title: Microsoft 365 Copilot ライセンスで作るエージェント ― Agent Builder と Copilot Studio の違いと使い分け
tags:
  - PowerPlatform
  - Microsoft365
  - copilot
  - CopilotStudio
private: true
updated_at: '2026-04-21T16:26:44+09:00'
id: 58341a8471839e4d7ad3
organization_url_name: null
slide: false
ignorePublish: false
---

## はじめに

Microsoft 365 Copilot ライセンスを持っていると、**Agent Builder（エージェント ビルダー）** と **Copilot Studio** の 2 つのツールを使ってエージェントを作成できます。どちらもエージェントを構築できますが、対象ユーザー・機能・ガバナンスの面で大きく異なります。

本記事では、両者の違いと使い分けのポイントを整理します。

## Agent Builder とは

Agent Builder は **Microsoft 365 Copilot アプリ内** に組み込まれたエージェント作成機能です。以下の場所からアクセスできます。

- microsoft365.com/chat
- office.com/chat
- Microsoft Teams（デスクトップ / Web）

自然言語でインストラクションを記述し、（管理者の設定や課金構成に応じて）Web サイト、SharePoint のファイル、コネクタ（Graph コネクタなど）をナレッジとして指定するだけで、コード不要でエージェントを構築できます。

## Copilot Studio とは

Copilot Studio は [copilotstudio.microsoft.com](https://copilotstudio.microsoft.com) で利用できる **スタンドアロンの Web ポータル** です。マルチステップ ワークフロー、外部 API 連携、カスタム コネクタ、Azure AI サービス統合など、より高度なシナリオに対応します。

## 機能比較

| 比較項目 | Agent Builder | Copilot Studio |
| --- | --- | --- |
| **アクセスポイント** | Microsoft 365 Copilot アプリ | copilotstudio.microsoft.com |
| **想定ユーザー** | インフォメーション ワーカー（IT 部門以外も含む） | メーカー（市民開発者）・プロ開発者 |
| **エージェントの対象** | 自分自身、または小規模チーム | 部署全体・組織全体・外部顧客 |
| **エージェントの種類** | 組織ナレッジを活用した軽量 Q&A エージェント | マルチステップ ワークフローやビジネス システム統合を伴う複雑なエージェント |
| **主な機能** | ・自然言語によるオーサリング<br>・Microsoft Graph ベースの Q&A<br>・ユーザーの Microsoft 365 アクセス許可を尊重<br>・Microsoft 365 Copilot オーケストレーター・基盤モデルを使用 | ・広範囲への公開（外部含む）<br>・マルチステップ ロジック・承認・分岐ワークフロー<br>・高度な AI モデルと Azure AI サービスの統合<br>・プリビルド / カスタム コネクタによる外部データ接続<br>・自律エージェント機能<br>・ALM（バージョン管理、dev/test/prod 環境、RBAC、テレメトリ） |
| **管理・ガバナンス** | Microsoft 365 管理センター | Power Platform 管理センター（よりきめ細かい制御） |

## どちらを選ぶべきか ― 判断フロー

使用するツールを選ぶ際は、次の 4 つの観点を検討します。

1. **対象ユーザー** ― 誰がエージェントを使うか？
2. **展開スコープ** ― どの範囲に共有するか？
3. **機能** ― エージェントにどんなタスクを実行させるか？
4. **ガバナンスのニーズ** ― アプリケーション ライフサイクル管理（ALM）が必要か？

### Agent Builder を選ぶケース

- 自分やチーム用に **すばやく** エージェントを作りたい
- SharePoint のドキュメントやメールの内容に基づいた **Q&A ボット** を構築したい
- コードは書きたくない（自然言語だけで完結させたい）

**具体的なユースケース例：**

- プロジェクト FAQ ボット ― プロジェクト ドキュメントをもとによくある質問に回答
- 製品ドキュメント アシスタント ― 社内の製品マニュアルや Wiki から情報を検索
- オンボーディング エージェント ― 新メンバーが社内ナレッジ ベースから回答を得る

### Copilot Studio を選ぶケース

- 部署・組織全体、または **外部顧客** 向けにエージェントを展開したい
- **マルチステップのワークフロー**（承認フロー、分岐ロジックなど）が必要
- Microsoft 365 以外の外部システムや API と **統合** したい
- **エンタープライズ レベルのガバナンス**（ALM、DLP、環境分離など）が求められる

**具体的なユースケース例：**

- カスタマー サポート エージェント ― サポート チケットの作成、人間へのエスカレーション
- IT ヘルプデスク トリアージ ― 社員からの IT リクエストを受け付け、適切なサポート チームに振り分け
- 営業アシスタント（CRM 連携） ― 売上データの取得、メモ作成、承認ワークフローの起動

## ガバナンスの違い

### Agent Builder のガバナンス原則

- **新しい特権なし** ― エージェントは既存の Microsoft 365 アクセス許可を尊重。ユーザーがアクセスできない SharePoint サイトや Teams チャネルのコンテンツは表示されない
- **組み込みの監査** ― 標準監査ログ、アクティビティ レポート、DLP/アイテム保持ポリシーがそのまま適用
- **管理** ― Microsoft 365 管理センター > **Copilot** > **Agents** で、エージェントの表示・有効/無効・ブロック・削除・従量課金制の設定などが可能

### Copilot Studio のガバナンス原則

- **構造化開発（ALM）** ― dev / test / prod 環境の分離
- **コネクタ ガバナンス** ― 接続先システムを管理者が制御
- **環境レベルのポリシー** ― DLP、ロールベースのアクセス制御、監査を環境単位で適用
- **柔軟な展開** ― Teams、Web サイト、カスタム エンドポイントへきめ細かいアクセス制御で公開
- **開発・発行の監視** ― 組織のアプリ カタログへの発行に管理者承認が必要
- **管理** ― Power Platform 管理センターでエージェント環境・コネクタ・ライフサイクル ポリシー・テレメトリを管理

## Agent Builder → Copilot Studio への移行

Agent Builder で作ったエージェントは、後から **Copilot Studio にコピー** できます。Agent Builder で始めて、要件が複雑になった時点で Copilot Studio に移行する「スモールスタート」のアプローチも有効です。

コピーすると、エージェントのコア構成とインストラクションが引き継がれ、Copilot Studio 側で以下の機能を追加できます。

- ライフサイクル管理（バージョン管理、環境分離、段階的リリース）
- 利用状況の監視・分析ダッシュボード
- エンタープライズ ガバナンス（ロールベースのアクセス、データ ポリシー、コンプライアンス チェック）
- 外部 API やエンタープライズ システムとの高度な統合

詳細は公式ドキュメント「[エージェントを Copilot Studio にコピーする](https://learn.microsoft.com/microsoft-365-copilot/extensibility/copy-agent-to-copilot-studio)」を参照してください。

## ライセンス要件

| 条件 | Agent Builder | Copilot Studio |
| --- | --- | --- |
| Microsoft 365 Copilot アドオン ライセンス | ✅ 利用可能 | ✅ 利用可能 |
| Copilot Credits / 従量課金 | ✅ 利用可能 | ✅ 利用可能 |
| 無料（指示 + 公開 Web のナレッジのみ） | ✅ 利用可能 | ❌ |

Microsoft 365 Copilot ライセンスがあれば、どちらのツールも追加費用なしで利用できます。

## まとめ

| 選択基準 | Agent Builder | Copilot Studio |
| --- | --- | --- |
| すばやく Q&A ボットを作りたい | ⭐ おすすめ | |
| コードなしで完結したい | ⭐ おすすめ | |
| 小規模チーム向け | ⭐ おすすめ | |
| 組織全体・外部向けに展開 | | ⭐ おすすめ |
| 外部システム連携・ワークフロー | | ⭐ おすすめ |
| エンタープライズ ガバナンス | | ⭐ おすすめ |
| 段階的に規模拡大したい | まず Agent Builder で開始 → 必要に応じて Copilot Studio にコピー | |

**迷ったら、まず Agent Builder で小さく始めてみましょう。** 要件が拡大した時点で Copilot Studio にコピーして拡張できるため、作り直す必要はありません。

## 参考リンク

- [エージェントを構築するMicrosoft 365 CopilotとCopilot Studioを選択する](https://learn.microsoft.com/microsoft-365-copilot/extensibility/copilot-studio-experience)
- [Agent Builder in Microsoft 365 Copilot](https://learn.microsoft.com/microsoft-365-copilot/extensibility/agent-builder)
- [Copy an agent to Copilot Studio](https://learn.microsoft.com/microsoft-365-copilot/extensibility/copy-agent-to-copilot-studio)
- [Copilot Studio でエージェントを構築する](https://learn.microsoft.com/microsoft-copilot-studio/microsoft-copilot-extend-copilot-extensions)
