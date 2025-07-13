# ERPset 機能要求仕様書（FRD）

## 1. 文書概要

### 1.1 目的・スコープ

本文書は、ERPsetプラットフォームの機能要求を詳細に定義し、開発チーム・ステークホルダー間の共通理解を確立することを目的とします。

### 1.2 対象読者

- プロダクトマネージャー・プロジェクトオーナー
- 開発チーム（フロントエンド・バックエンド・QA）
- ビジネスアナリスト・UXデザイナー
- 顧客・エンドユーザー代表

### 1.3 文書構成

```
機能要求の階層構造:
├── エピック（Epic）- ビジネス価値単位
├── ユーザーストーリー（User Story）- 利用者視点機能
├── 受入基準（Acceptance Criteria）- 品質・完了定義
└── タスク（Task）- 実装単位
```

## 2. ユーザーペルソナ・利用シナリオ

### 2.1 プライマリペルソナ

#### Salesforce導入コンサルタント（田中 剛）
```yaml
profile:
  role: "シニアSalesforceコンサルタント"
  experience: "Salesforce導入8年・20社経験"
  company: "中堅ITコンサルティング会社"
  
pain_points:
  - "ヒアリング項目作成に毎回3-4時間かかる"
  - "設定漏れによる手戻りが月1-2回発生"
  - "顧客要求とSalesforce機能のGAP分析が属人的"
  
goals:
  - "ヒアリング準備工数を70%削減したい"
  - "設定品質を標準化・安定化したい"
  - "より戦略的なコンサルティングに時間を使いたい"
```

#### 中小企業IT責任者（佐藤 麻衣）
```yaml
profile:
  role: "情報システム部長"
  experience: "IT部門管理5年・業務システム導入3回"
  company: "従業員200名の製造業"
  
pain_points:
  - "Salesforce機能を理解しきれていない"
  - "自社業務との適合性判断が困難"
  - "導入コストが予算に対して高い"
  
goals:
  - "自社に最適な設定を効率的に決めたい"
  - "導入リスクを最小化したい"
  - "将来的な拡張性を確保したい"
```

### 2.2 利用シナリオ

#### メインシナリオ: Salesforce Sales Cloud導入支援
```
1. プロジェクト開始・スコープ設定
   ↓
2. 顧客ビジネス要求ヒアリング
   ↓
3. Salesforce標準機能マッピング
   ↓
4. 詳細ヒアリング実施・回答収集
   ↓
5. セットアップ定義書生成・レビュー
   ↓
6. GAP要件特定・解決策検討
   ↓
7. 最終仕様確定・移行計画策定
```

## 3. Phase 1 MVP機能仕様

### 3.1 エピック1: プロジェクト管理

#### Epic-01: プロジェクト基本管理
**ビジネス価値**: "複数のSalesforce導入プロジェクトを効率的に管理し、進捗・品質を可視化する"

##### US-01-01: プロジェクト作成・設定
```yaml
user_story: |
  Salesforce導入コンサルタントとして、
  新しいプロジェクトを作成し、基本情報を設定することで、
  プロジェクト固有の要件定義作業を開始したい

acceptance_criteria:
  - プロジェクト名・説明・期間を設定できる
  - 対象Salesforce製品（Sales Cloud）を選択できる
  - 導入スコープ（Lead管理、Opportunity管理）を選択できる
  - プロジェクトメンバー（役割付き）を招待できる
  - プロジェクト一覧で進捗状況を確認できる

priority: "Must Have"
story_points: 8
```

##### US-01-02: プロジェクトダッシュボード
```yaml
user_story: |
  プロジェクトマネージャーとして、
  プロジェクトの進捗・課題・品質を一目で把握することで、
  適切な判断・指示を行いたい

acceptance_criteria:
  - ヒアリング進捗率（回答済み/全項目）を表示
  - GAP要件数・解決状況を表示
  - セットアップ定義書の完成度を表示
  - 課題・リスク一覧を表示
  - 次のアクション項目を表示

priority: "Should Have"
story_points: 5
```

### 3.2 エピック2: 知識ベース管理

#### Epic-02: Salesforce知識ベース
**ビジネス価値**: "Salesforce Sales Cloudの標準機能・設定パラメータを体系化し、要件定義の精度・効率を向上させる"

##### US-02-01: Salesforce機能マスタ
```yaml
user_story: |
  システム管理者として、
  Salesforce Sales Cloudの標準機能・設定項目を登録・管理することで、
  正確で最新の知識ベースを維持したい

acceptance_criteria:
  - Lead管理機能（Lead Status、Assignment Rules等）を登録
  - Opportunity管理機能（Stage、Forecast等）を登録
  - Account/Contact管理機能を登録
  - 各機能の設定パラメータ・依存関係を定義
  - 設定項目の説明・制約事項を記載
  - バージョン管理・変更履歴を保持

priority: "Must Have"
story_points: 13
```

##### US-02-02: ヒアリング項目テンプレート
```yaml
user_story: |
  Salesforceコンサルタントとして、
  機能毎の標準ヒアリング項目テンプレートを活用することで、
  ヒアリング漏れを防ぎ、質問品質を向上させたい

acceptance_criteria:
  - Lead管理のヒアリング項目（Lead Source、変換基準等）
  - Opportunity管理のヒアリング項目（Stage定義、確度等）
  - Account階層・取引先責任者のヒアリング項目
  - 回答形式（選択式・記述式・数値等）を定義
  - 必須/任意の設定が可能
  - 業界別バリエーション対応

priority: "Must Have"  
story_points: 8
```

### 3.3 エピック3: ヒアリング生成・実施

#### Epic-03: インテリジェントヒアリング
**ビジネス価値**: "顧客要求とSalesforce標準機能をマッピングし、効率的で漏れのないヒアリングを実現する"

##### US-03-01: ヒアリングリスト自動生成
```yaml
user_story: |
  Salesforceコンサルタントとして、
  プロジェクトスコープに基づいてヒアリングリストが自動生成されることで、
  ヒアリング準備工数を大幅に削減したい

acceptance_criteria:
  - プロジェクトスコープ（Lead管理、Opportunity管理等）を選択
  - 関連するSalesforce機能を自動抽出
  - 機能毎のヒアリング項目を自動組み合わせ
  - 優先順位・カテゴリ別にグルーピング
  - Excel・PDF形式でエクスポート可能
  - 生成理由・根拠を表示

priority: "Must Have"
story_points: 13
```

##### US-03-02: ヒアリング実施・回答管理
```yaml
user_story: |
  Salesforceコンサルタントとして、
  ヒアリング回答を効率的に収集・管理することで、
  後続のセットアップ定義作業をスムーズに進めたい

acceptance_criteria:
  - Webフォームでヒアリング回答を入力
  - 必須項目のバリデーション・エラー表示
  - 中間保存・下書き機能
  - 回答進捗の可視化（完了率表示）
  - コメント・補足情報の追加
  - 回答者別の履歴管理

priority: "Must Have"
story_points: 8
```

### 3.4 エピック4: セットアップ定義・GAP分析

#### Epic-04: 自動セットアップ定義
**ビジネス価値**: "ヒアリング結果からSalesforce設定値を自動推論し、設定漏れ・設定ミスを防止する"

##### US-04-01: セットアップ定義書生成
```yaml
user_story: |
  Salesforceコンサルタントとして、
  ヒアリング結果からセットアップ定義書が自動生成されることで、
  手作業による設定ミス・漏れを防ぎたい

acceptance_criteria:
  - ヒアリング回答を解析してSalesforce設定値を推論
  - Lead Status・Opportunity Stageの設定を自動定義
  - Lead Assignment Rules・Escalation Rulesを生成
  - Account Team・Opportunity Team設定を定義
  - 設定項目の妥当性を自動チェック
  - Excel・PDF形式で出力

priority: "Must Have"
story_points: 21
```

##### US-04-02: GAP要件特定・分析
```yaml
user_story: |
  Salesforceコンサルタントとして、
  標準機能で対応できない要件を自動特定することで、
  GAP分析の精度・効率を向上させたい

acceptance_criteria:
  - 標準機能の範囲外要求を自動検出
  - GAP要件をカテゴリ別（機能・UI・連携等）に分類
  - ビジネス影響度（高・中・低）を評価
  - 解決アプローチ（Apex開発・外部連携等）を提案
  - 工数・コスト見積もりを表示
  - GAP要件一覧をExcel出力

priority: "Should Have"
story_points: 13
```

## 4. Phase 2+ 拡張機能仕様

### 4.1 エピック5: 移行支援連携

#### Epic-05: データ移行マッピング
**ビジネス価値**: "要件定義の成果を移行設計に連携し、データ移行の精度・効率を向上させる"

##### US-05-01: 移行マッピング定義生成
```yaml
user_story: |
  データ移行担当者として、
  要件定義の結果から移行マッピング定義が自動生成されることで、
  移行設計工数を削減し、要件との整合性を保ちたい

acceptance_criteria:
  - セットアップ定義書からSalesforceデータ構造を抽出
  - 移行元システムとのマッピングシート生成
  - データ変換ルールのテンプレート作成
  - 必須項目・制約事項の移行時チェック定義
  - 移行データの妥当性検証ルール生成

priority: "Could Have"
story_points: 21
```

### 4.2 エピック6: マルチクラウド対応

#### Epic-06: Service Cloud拡張
**ビジネス価値**: "Salesforce Service Cloudに対応し、カスタマーサービス業務の要件定義を支援する"

##### US-06-01: Service Cloud知識ベース
```yaml
user_story: |
  Service Cloudコンサルタントとして、
  Service Cloud特有の機能・設定項目を活用することで、
  カスタマーサービス要件定義を効率化したい

acceptance_criteria:
  - Case管理機能（Case Origin、Priority等）を登録
  - Knowledge Base機能の設定項目を定義
  - Entitlement・Service Contract機能を定義
  - CTI連携・Omni-Channel設定を定義

priority: "Could Have"
story_points: 13
```

## 5. 非機能要求との連携

### 5.1 性能要求

#### 応答時間要求
```yaml
performance_requirements:
  hearing_list_generation:
    target: "2秒以内"
    measurement: "プロジェクトスコープ選択→リスト表示"
    
  setup_definition_generation:
    target: "5秒以内"
    measurement: "ヒアリング完了→定義書生成"
    
  gap_analysis:
    target: "3秒以内"
    measurement: "要件入力→GAP要件特定"
```

### 5.2 ユーザビリティ要求

#### UX要求
```yaml
usability_requirements:
  learning_curve:
    target: "新規ユーザーが30分以内で基本操作習得"
    measurement: "チュートリアル完了率・操作成功率"
    
  task_completion:
    target: "ヒアリングリスト生成を3クリック以内で完了"
    measurement: "クリック数・操作時間測定"
    
  error_prevention:
    target: "入力エラー発生率5%以下"
    measurement: "バリデーションエラー・修正回数"
```

## 6. 受入テスト・検証計画

### 6.1 機能受入基準

#### 自動テスト
```yaml
automated_acceptance:
  unit_tests:
    coverage: "80%以上"
    scope: "ビジネスロジック・API"
    
  integration_tests:
    coverage: "主要エンドポイント100%"
    scope: "API・DB連携"
    
  e2e_tests:
    coverage: "クリティカルパス"
    scope: "ユーザージャーニー"
```

#### 手動テスト
```yaml
manual_acceptance:
  user_scenario_tests:
    scope: "エンドツーエンドシナリオ"
    criteria: "ペルソナ毎の利用シナリオ完走"
    
  usability_tests:
    scope: "UI/UX・使い勝手"
    criteria: "ユーザビリティ基準達成"
    
  load_tests:
    scope: "性能・負荷"
    criteria: "性能要求基準達成"
```

### 6.2 ビジネス価値検証

#### 定量的検証
```yaml
quantitative_validation:
  efficiency_gain:
    metric: "ヒアリング準備工数削減率"
    target: "70%削減"
    measurement: "作業時間Before/After比較"
    
  quality_improvement:
    metric: "設定漏れ・ミス発生率"
    target: "50%削減"
    measurement: "レビュー指摘事項数"
    
  user_satisfaction:
    metric: "NPS・満足度スコア"
    target: "NPS 50以上、満足度8.0/10以上"
    measurement: "月次ユーザー調査"
```

## 7. 制約事項・前提条件

### 7.1 技術制約

#### Salesforce API制限
```yaml
salesforce_constraints:
  api_limits:
    daily_limit: "100,000 API calls/日"
    bulk_limit: "10,000 records/batch"
    
  metadata_access:
    scope: "Custom Objects・Fields・Workflows"
    limitation: "Standard Objectの一部制限"
    
  security:
    requirement: "OAuth 2.0認証必須"
    constraint: "IP制限・セッション管理"
```

### 7.2 ビジネス制約

#### Phase 1制約
```yaml
phase1_constraints:
  functional_scope:
    include: "Sales Cloud Lead/Opportunity管理のみ"
    exclude: "Service Cloud・Marketing Cloud・Commerce"
    
  user_scope:
    include: "コンサルタント・社内ユーザー"
    exclude: "エンドカスタマー直接利用"
    
  integration_scope:
    include: "基本的なデータ出力機能"
    exclude: "外部システム連携・リアルタイム同期"
```

## 8. 関連文書・参照

### 8.1 プロジェクト管理文書

- [📋 プロジェクト全体構想](./project-overview.md)
- [🏗️ 技術アーキテクチャ](./technical-architecture.md)
- [🗓️ 開発ロードマップ](./development-roadmap.md)
- [📊 プロジェクト管理計画](./project-management-plan.md)
- [⚙️ 非機能要求仕様書](./non-functional-requirements.md)

### 8.2 Phase 1実装・詳細設計

- [🚀 Phase 1 MVP概要](../phase1/README.md)
- [🔧 技術仕様書](../phase1/docs/technical-spec.md)
- [🌐 API設計書](../phase1/docs/api-design.md)
- [🗄️ データベース設計書](../phase1/docs/database-design.md)

### 8.3 開発・運用関連文書

- [🔧 環境構築ガイド](./setup-guide.md)
- [🧪 品質保証・テスト戦略](./quality-assurance.md)

### 8.4 外部参照

- [Salesforce Developer Documentation](https://developer.salesforce.com/)
- [Salesforce Trailhead - Sales Cloud](https://trailhead.salesforce.com/en/content/learn/trails/getting_started_with_sales_cloud)
- [Salesforce Implementation Guide](https://help.salesforce.com/s/articleView?id=sf.overview_edition_lex_only.htm)

---
**最終更新**: 2025-07-13  
**文書バージョン**: 1.0  
**承認状況**: レビュー待ち  
**次回更新**: Phase 1開発開始時（詳細仕様確定）