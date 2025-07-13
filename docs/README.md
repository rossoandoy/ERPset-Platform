# ERPset - ERP導入支援プラットフォーム

## プロジェクト概要

ERPsetは、「Fit to Standard」原則によるERP導入の全工程支援プラットフォームです。要件定義から移行・本稼働まで一貫した自動化により、遅延リスク・混乱リスク・開発コストを最小化します。

## 主要機能

- **インテリジェントヒアリング**: 標準機能から逆算した効率的なヒアリングリスト自動生成
- **セットアップ定義自動化**: ヒアリング結果に基づく設定内容の自動定義
- **GAP分析・要件定義**: 標準機能とのGAPを自動検出し、システム化要件を定義
- **移行支援ツール**: データ・業務・システム移行の統合支援
- **マスタ登録ファイル生成**: ERP製品へのインポート用ファイル自動生成

## 技術スタック（段階的選定）

### Phase 1 - MVP
```yaml
frontend:
  framework: "Next.js 15 + TypeScript"
  styling: "Tailwind CSS"
  state_management: "Zustand"
  
backend:
  language: "Python (API連携・AI処理)"
  api: "FastAPI"
  
infrastructure:
  containerization: "Docker + Docker Compose"
  development: "Turbopack + ESLint"
```

## 開発フェーズ

| フェーズ | 期間 | 主要タスク | 状況 | MVP範囲 |
|---------|------|-----------|-----|--------|
| Phase 1 | 3-4ヶ月 | MVP: 単一ERP×単一業務 | 🔄 準備中 | Salesforce Sales Cloud限定 |
| Phase 2 | 3ヶ月 | GAP分析・移行設計連携 | 📋 計画中 | 移行ツール基礎 |
| Phase 3 | 4ヶ月 | 複数業務領域拡張 | 📋 計画中 | 5業務領域対応 |
| Phase 4 | 4ヶ月 | 移行ツール統合 | 📋 計画中 | 統合プラットフォーム |
| Phase 5 | 6ヶ月 | マルチERP・セルフサービス化 | 📋 計画中 | SaaS型提供 |

**総開発期間**: 20-21ヶ月  
**開発方針**: 実装ファースト・段階的詳細化

## プロジェクト構造

```
ERPset/
├── docs/                   # プロジェクト管理文書
├── phase1/                 # MVP: 単一ERP×単一業務
├── phase2/                 # GAP分析・移行設計連携
├── phase3/                 # 複数業務領域拡張
├── phase4/                 # 移行ツール統合
├── phase5/                 # マルチERP・セルフサービス化
└── legacy-tool/            # 既存erp-hearing-tool保管
```

## ドキュメントナビゲーション

### 全体構想・管理
- [📋 プロジェクト全体構想](./project-overview.md)
- [🏗️ 技術アーキテクチャ](./technical-architecture.md)
- [🗓️ 開発ロードマップ](./development-roadmap.md)
- [📊 プロジェクト管理計画](./project-management-plan.md)
- [📝 作業記録](./work-log.md)

### 要件・仕様文書
- [📝 機能要求仕様書](./functional-requirements.md)
- [⚙️ 非機能要求仕様書](./non-functional-requirements.md)

### 開発・運用文書
- [🔧 環境構築ガイド](./setup-guide.md)
- [🧪 品質保証・テスト戦略](./quality-assurance.md)

### 過去の構想・参考資料
- [💡 ERP導入ツール構想 with Claude](./ERP導入ツール構想withClaude.md)
- [💡 ERP導入ツール構想 with GPT](./ERP導入ツール構想withGPT.md)
- [💡 ERP導入ツール構想 with Gemini](./ERP導入ツール構想withGemini.md)
- [🏗️ プラットフォーム・ブループリント with Claude](./ERP導入支援プラットフォーム・ブループリントwithClaude.md)
- [🏗️ プラットフォーム・ブループリント with GPT](./ERP導入支援プラットフォーム・ブループリントwithGPT.md)
- [🏗️ プラットフォーム・ブループリント with Gemini](./ERP導入支援プラットフォーム・ブループリントwithGemini.md)
- [📝 初期ツールアイデア](./ERPseToolIdea.md)

### フェーズ別文書
- [🚀 Phase 1: MVP開発](../phase1/) - Salesforce Sales Cloud限定MVP
  - [📋 Phase 1概要](../phase1/README.md)
  - [🔧 技術仕様書](../phase1/docs/technical-spec.md)
  - [🌐 API設計書](../phase1/docs/api-design.md)
  - [🗄️ データベース設計書](../phase1/docs/database-design.md)
- [📈 Phase 2: GAP分析拡張](../phase2/) - 移行設計連携
- [🎯 Phase 3: 業務領域拡張](../phase3/) - 5業務領域対応
- [🔗 Phase 4: 移行ツール統合](../phase4/) - 統合プラットフォーム
- [☁️ Phase 5: マルチERP対応](../phase5/) - SaaS型提供

### レガシーシステム
- [Legacy Tool: erp-hearing-tool](../legacy-tool/) - 既存実装保管

## クイックスタート

### 前提条件
- Docker & Docker Compose
- Node.js 18+ (フロントエンド開発用)
- Python 3.9+ (バックエンド開発用)

### セットアップ手順
```bash
# 1. リポジトリクローン
git clone <repository-url>
cd ERPset

# 2. ブランチ切り替え
git checkout test-phasing

# 3. Phase 1 開発環境構築
cd phase1
# （Phase 1実装後に詳細手順追加予定）

# 4. レガシーツール参照
cd legacy-tool/erp-hearing-tool
docker-compose up -d
# アクセス: http://localhost:3000
```

## 開発方針・特徴

### 実装ファースト原則
- Phase N完全実装 → Phase N+1詳細設計
- 実装で得た知見をすべての文書に反映
- 理論と実装の乖離を最小化

### 段階的価値提供
- 各フェーズで明確な価値提供
- MVP重視・スコープ調整可能設計
- 継続的改善・フィードバック反映

### 品質重視
- 各段階での完全性確保
- 技術的負債の蓄積防止
- 文書と実装の双方向更新

## コントリビューション

プロジェクトの進捗状況や変更提案は、各フェーズの要件定義書・SOW文書を参照してください。
現在はtest-phasingブランチでのフェーズ分け開発リファクタリング中です。

## サポート・お問い合わせ

技術的な質問や課題については、各フェーズのドキュメントまたは開発チームまでお問い合わせください。

---
**最終更新**: 2025-07-13  
**プロジェクト状況**: Phase 1 準備中（フェーズ分け開発移行完了）  
**次回マイルストーン**: MVP範囲確定・Phase 1詳細設計