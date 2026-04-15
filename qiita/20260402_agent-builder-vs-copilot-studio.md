---
title: "Microsoft 365 Copilot ライセンスで作るエージェント ― Agent Builder と Copilot Studio の違いと使い分け（2026年4月版）"
tags:
  - Microsoft365
  - Copilot
  - CopilotStudio
  - PowerPlatform
  - AI
private: true
---

## はじめに

Microsoft 365 Copilot ライセンスを持っていると、**Agent Builder（エージェント ビルダー）** と **Copilot Studio** の 2 つのツールを使ってエージェントを作成することが出来ます。どちらもエージェントを構築できますが、対象ユーザー・機能・ガバナンスの面で大きく異なります。

本記事では、両者の違いと使い分けのポイントを整理します。

:::note info
この記事は 2026 年 4 月時点の情報に基づいています。2025 年後半〜2026 年にかけて Agent Builder・Copilot Studio ともに大幅なアップデートが行われており、以前の記事から内容を更新しています。
:::

## Agent Builder とは

Agent Builder は **Microsoft 365 Copilot アプリ内** に組み込まれたエージェント作成機能です。以下の場所からアクセスできます。

- microsoft365.com/chat
- office.com/chat
- Microsoft Teams（デスクトップ / Web）

自然言語でインストラクションを記述し、ナレッジソースを指定するだけで、コード不要でエージェントを構築できます。

### Agent Builder の主な機能（2026年4月時点）

- **自然言語によるエージェント作成（推奨）** ― 会話形式で意図を伝えるだけで、名前・説明・指示・ナレッジソース・スタータープロンプトが自動構成される
- **テンプレートからの構築** ― 特定ユースケース向けのテンプレートが用意されており、カスタマイズして使える
- **Code Interpreter** ― データ分析やチャート作成が可能
- **Image Generator** ― AI による画像生成
- **AI によるアイコン生成** ― エージェントのアイコンを AI で自動生成、ライブラリから選択、または手動アップロード
- **ナレッジソース（最大 20 件）** ― SharePoint サイト・フォルダ・ファイル、Copilot Connectors、Web コンテンツなど。Microsoft 365 Copilot アドオンライセンスがあれば、Teams チャットや Outlook メールなどの個人データもグラウンディング可能

:::note warn
モバイル版では Agent Builder は現時点では利用できません。また、Teams Chat でのエージェント利用は不可です。
:::

## Copilot Studio とは

Copilot Studio は [copilotstudio.microsoft.com](https://copilotstudio.microsoft.com) で利用できる **スタンドアロンの Web ポータル** です。マルチステップ ワークフロー、外部 API 連携、カスタム コネクタ、Azure AI サービス統合など、より高度なシナリオに対応します。

2025 年後半からのアップデートで、MCP サーバー対応、A2A プロトコル対応、Computer-Using Agents、マルチエージェント オーケストレーションなど、エージェントプラットフォームとしての機能が大幅に強化されています。

### Copilot Studio の最近のアップデート

| 時期 | 主な変更 |
| --- | --- |
| 2025年8月 | Code Interpreter GA、MCP サーバー接続のガイド付き体験 |
| 2025年9月 | Computer-Using Agents (CUA) プレビュー、Client SDK |
| 2025年10月 | GPT-4o 廃止 → GPT-4.1 がデフォルトに、MCP サーバーからの動的コンテンツ取得、ROI 分析 |
| 2025年11月 | GPT-5 Chat GA、マルチエージェント オーケストレーション、Agent Builder → Copilot Studio コピー機能、MCP コンポーネントコレクション |
| 2026年1月 | VS Code 拡張機能 GA、エージェント評価の拡張（プレビュー）、CUA に Cloud PC プーリング対応 |
| 2026年2月 | Claude Sonnet 4.5 / Claude Opus 4.6 が GA、A2A プロトコル対応（プレビュー）、プロンプトビルダー拡張 |
| 2026年3月 | Work IQ ツール（プレビュー） |

## 機能比較

| 比較項目 | Agent Builder | Copilot Studio |
| --- | --- | --- |
| **アクセスポイント** | Microsoft 365 Copilot アプリ | copilotstudio.microsoft.com |
| **想定ユーザー** | インフォメーション ワーカー（IT 部門以外も含む） | メーカー（市民開発者）・プロ開発者 |
| **エージェントの対象** | 自分自身、または小規模チーム | 部署全体・組織全体・外部顧客 |
| **エージェントの種類** | 組織ナレッジを活用した軽量 Q&A エージェント | マルチステップ ワークフローやビジネス システム統合を伴う複雑なエージェント |
| **主な機能** | ・自然言語によるオーサリング<br>・テンプレートからの構築<br>・Microsoft Graph ベースの Q&A<br>・Code Interpreter / Image Generator<br>・AI アイコン生成<br>・ユーザーの Microsoft 365 アクセス許可を尊重 | ・広範囲への公開（外部含む）<br>・マルチステップ ロジック・承認・分岐ワークフロー<br>・AI モデル選択（GPT-5、Claude 等）<br>・MCP サーバー / A2A プロトコル対応<br>・Computer-Using Agents (CUA)<br>・マルチエージェント オーケストレーション<br>・プリビルド / カスタム コネクタによる外部データ接続<br>・自律エージェント機能<br>・ALM（バージョン管理、dev/test/prod 環境、RBAC、テレメトリ） |
| **AI モデル** | Microsoft 365 Copilot オーケストレーター・基盤モデル | GPT-4.1（デフォルト）、GPT-5 Chat/Reasoning、Claude Sonnet 4.5/4.6、Claude Opus 4.6 等を選択可能 |
| **管理・ガバナンス** | Microsoft 365 管理センター | Power Platform 管理センター（よりきめ細かい制御） |

## Copilot Studio で追加された注目機能

### MCP（Model Context Protocol）サーバー対応

Copilot Studio のエージェントから **MCP サーバーに接続** して、ファイル、データベースレコード、API レスポンスなどの動的コンテンツをリアルタイムで取得することが出来ます。Microsoft のプリビルト MCP コネクタとカスタム MCP サーバーの両方に対応しており、ツール単位で選択的に有効/無効を切り替えられます。

### A2A（Agent-to-Agent）プロトコル対応（プレビュー）

Copilot Studio のエージェントから **A2A プロトコル経由で外部エージェントに接続** することが出来ます。接続先には以下が含まれます。

- 同一エージェント内の子エージェント
- 環境内の他の Copilot Studio エージェント
- Microsoft Foundry エージェント（プレビュー）
- Fabric Data エージェント（プレビュー）
- Microsoft 365 Agents SDK エージェント（プレビュー）
- A2A プロトコル対応の外部エージェント（プレビュー）

### Computer-Using Agents（CUA）（プレビュー）

ビジョン + 推論を組み合わせた CUA が **Windows デスクトップアプリと Web アプリを自動操作** します。レガシーシステムの操作自動化など、API が存在しないシナリオで威力を発揮します。

- 対応モデル: OpenAI の CUA モデル、Anthropic Claude Sonnet 4.5
- Cloud PC プーリング、セッションリプレイ付き監査ログ、組み込みクレデンシャルに対応
- 1 ステップ = 5 Copilot Credits で課金

### マルチエージェント オーケストレーション

複数の特化エージェントにタスクを分散させるオーケストレーションが可能です。Fabric Data Agent を含む複数のエージェントを連携させ、専門性の異なるタスクを適切なエージェントに振り分けることが出来ます。

### AI モデルの選択

Copilot Studio ではエージェントごとに AI モデルを選択することが出来ます。

| モデル | ステータス |
| --- | --- |
| GPT-4.1 | **デフォルト**（GA） |
| GPT-5 Chat | **GA**（全リージョン） |
| GPT-5 Reasoning / Auto | **プレビュー** |
| GPT-5.3 Chat / GPT-5.4 Reasoning | **Experimental**（Early access） |
| Claude Sonnet 4.5 / 4.6 | **GA**（Cross-geo） |
| Claude Opus 4.6 | **GA**（Cross-geo） |
| Grok 4.1 Fast | **Experimental**（Early access） |

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
- **Code Interpreter** でデータ分析やチャート作成をさせたい

**具体的なユースケース例：**

- プロジェクト FAQ ボット ― プロジェクト ドキュメントをもとによくある質問に回答
- 製品ドキュメント アシスタント ― 社内の製品マニュアルや Wiki から情報を検索
- オンボーディング エージェント ― 新メンバーが社内ナレッジ ベースから回答を得る
- データ分析エージェント ― Excel や CSV データの分析・チャート作成

### Copilot Studio を選ぶケース

- 部署・組織全体、または **外部顧客** 向けにエージェントを展開したい
- **マルチステップのワークフロー**（承認フロー、分岐ロジックなど）が必要
- Microsoft 365 以外の外部システムや API と **統合** したい
- **MCP サーバー** や **A2A プロトコル** で外部エージェント・ツールと連携したい
- **Computer-Using Agents** でデスクトップ アプリの操作を自動化したい
- **AI モデルを選択** したい（GPT-5、Claude など）
- **エンタープライズ レベルのガバナンス**（ALM、DLP、環境分離など）が求められる

**具体的なユースケース例：**

- カスタマー サポート エージェント ― サポート チケットの作成、人間へのエスカレーション
- IT ヘルプデスク トリアージ ― 社員からの IT リクエストを受け付け、適切なサポート チームに振り分け
- 営業アシスタント（CRM 連携） ― 売上データの取得、メモ作成、承認ワークフローの起動
- レガシーシステム自動化 ― API のないデスクトップアプリの操作を CUA で自動化
- マルチエージェント連携 ― 複数の専門エージェントを組み合わせた業務プロセスの自動化

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

### Microsoft Agent 365（2026年5月 GA 予定）

組織内の **全 AI エージェントを一元管理** するプラットフォームとして Microsoft Agent 365 が登場予定です。

- **Microsoft Entra Agent ID** ― 各エージェントに固有の ID を付与し、ID / ライフサイクル / アクセス管理を一元化
- **エージェントマップ** ― エージェント・人・データの接続を可視化し、リアルタイム監視
- **相互運用性** ― MCP インターフェースと SDK を通じた一貫したツール連携
- **セキュリティ統合** ― Microsoft Purview（データ保護・監査）、Microsoft Defender（脅威検出・対応）と統合

Agent Builder で作ったエージェントも Copilot Studio で作ったエージェントも、Microsoft Agent 365 による統合的なガバナンスの対象に含まれるようになります。

## Agent Builder → Copilot Studio への移行

Agent Builder で作ったエージェントは、後から **Copilot Studio にコピー** できます（2025年11月に導入）。Agent Builder で始めて、要件が複雑になった時点で Copilot Studio に移行する「スモールスタート」のアプローチも有効です。

コピーすると、エージェントのコア構成とインストラクションが引き継がれ、Copilot Studio 側で以下の機能を追加できます。

- ライフサイクル管理（バージョン管理、環境分離、段階的リリース）
- 利用状況の監視・分析ダッシュボード
- エンタープライズ ガバナンス（ロールベースのアクセス、データ ポリシー、コンプライアンス チェック）
- 外部 API やエンタープライズ システムとの高度な統合
- MCP サーバー / A2A プロトコルを使った外部エージェント連携
- AI モデルの選択・カスタマイズ

詳細は公式ドキュメント「[エージェントを Copilot Studio にコピーする](https://learn.microsoft.com/microsoft-365-copilot/extensibility/copy-agent-to-copilot-studio)」を参照してください。

## ライセンスとコスト

### ライセンスオプション

| オプション | Agent Builder | Copilot Studio | 備考 |
| --- | --- | --- | --- |
| **Microsoft 365 Copilot アドオンライセンス** | ✅ | ✅ | 拡張機能（Copilot Connectors、エージェント、プラグイン）の追加料金なし |
| **Microsoft 365 Copilot Chat（従量課金）** | ✅（一部機能） | ✅ | 指示 + 公開 Web のナレッジのみなら無料。SharePoint 等の共有データ利用は従量課金 |
| **Microsoft Agent 365（2026年5月 GA 予定）** | ✅ | ✅ | ユーザー単位ライセンス。Microsoft 365 E7 にも含まれる |

### Copilot Credits

2025 年 9 月から、課金単位が旧「メッセージ」から **Copilot Credits** に変更されています。Copilot Credits はエージェントが情報取得・応答・アクション実行に要する時間と労力を測定する共通通貨です。

- **プリペイド**: Microsoft 365 管理センターから購入
- **Pay-as-you-go**: Azure サブスクリプション連携で月末精算
- **Pre-Purchase Plan**: 1 年間の前払いオプション（Azure ポータルから）

:::note info
Microsoft 365 Copilot ライセンス所持者が Copilot Chat / Teams / SharePoint でエージェントを使用する場合、classic answers・generative answers・Graph tenant grounding の利用は**ゼロレート**（追加課金なし）です。
:::

## まとめ

| 選択基準 | Agent Builder | Copilot Studio |
| --- | --- | --- |
| すばやく Q&A ボットを作りたい | ⭐ おすすめ | |
| コードなしで完結したい | ⭐ おすすめ | |
| データ分析・チャート作成（Code Interpreter） | ⭐ おすすめ | |
| 小規模チーム向け | ⭐ おすすめ | |
| 組織全体・外部向けに展開 | | ⭐ おすすめ |
| 外部システム連携・ワークフロー | | ⭐ おすすめ |
| MCP / A2A で外部エージェント連携 | | ⭐ おすすめ |
| Computer-Using Agents（デスクトップ自動化） | | ⭐ おすすめ |
| AI モデルを選択したい | | ⭐ おすすめ |
| エンタープライズ ガバナンス | | ⭐ おすすめ |
| 段階的に規模拡大したい | まず Agent Builder で開始 → 必要に応じて Copilot Studio にコピー | |

**迷ったら、まず Agent Builder で小さく始めてみましょう。** 要件が拡大した時点で Copilot Studio にコピーして拡張できるため、作り直す必要はありません。

2025 年後半から 2026 年にかけて、Copilot Studio は MCP / A2A / CUA / マルチエージェントと、エージェントプラットフォームとしての進化が著しいです。個人的には、まずは Agent Builder で軽く触ってみて、より高度なシナリオが必要になったら Copilot Studio に移行するのが良いと思います。

それでは、良いエージェント開発ライフを！

## 参考リンク

- [Agent Builder in Microsoft 365 Copilot](https://learn.microsoft.com/microsoft-365-copilot/extensibility/agent-builder)
- [エージェントを構築する Microsoft 365 Copilot と Copilot Studio を選択する](https://learn.microsoft.com/microsoft-365-copilot/extensibility/copilot-studio-experience)
- [Choose the right tool to build your declarative agent](https://learn.microsoft.com/microsoft-365-copilot/extensibility/declarative-agent-tool-comparison)
- [Copy an agent to Copilot Studio](https://learn.microsoft.com/microsoft-365-copilot/extensibility/copy-agent-to-copilot-studio)
- [Copilot Studio の新機能](https://learn.microsoft.com/microsoft-copilot-studio/whats-new)
- [Copilot Studio の AI モデル選択](https://learn.microsoft.com/microsoft-copilot-studio/authoring-select-agent-model)
- [MCP サーバーコンポーネントの追加](https://learn.microsoft.com/microsoft-copilot-studio/mcp-add-components-to-agent)
- [A2A プロトコルで外部エージェントに接続](https://learn.microsoft.com/microsoft-copilot-studio/authoring-add-other-agents)
- [Computer-Using Agents](https://learn.microsoft.com/microsoft-copilot-studio/computer-use)
- [ライセンスとコストの考慮事項](https://learn.microsoft.com/microsoft-365-copilot/extensibility/cost-considerations)
- [Microsoft Agent 365 概要](https://learn.microsoft.com/microsoft-agent-365/overview)
