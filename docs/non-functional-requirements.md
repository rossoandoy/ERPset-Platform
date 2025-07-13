# ERPset 非機能要求仕様書（NFR）

## 1. 文書概要

### 1.1 目的・スコープ

本文書は、ERPsetプラットフォームの非機能要求（性能・可用性・セキュリティ・拡張性・運用性）を定義し、システム品質の目標値・測定方法・達成手段を明確化します。

### 1.2 対象読者

- アーキテクト・テックリード
- インフラ・DevOpsエンジニア
- QAエンジニア・SREエンジニア
- プロダクトマネージャー・プロジェクトオーナー

### 1.3 品質特性の定義

ISO/IEC 25010品質モデルに基づく8つの品質特性を適用：

```
品質特性マップ:
├── 機能適合性（Functional Suitability）
├── 性能効率性（Performance Efficiency）
├── 互換性（Compatibility）
├── 使用性（Usability）
├── 信頼性（Reliability）
├── セキュリティ（Security）
├── 保守性（Maintainability）
└── 移植性（Portability）
```

## 2. 性能効率性（Performance Efficiency）

### 2.1 応答時間要求

#### フロントエンド応答時間
```yaml
frontend_performance:
  page_load:
    target: "初回ロード3秒以内、リロード1秒以内"
    measurement: "DOMContentLoaded イベント"
    conditions: "標準的なブロードバンド環境"
    
  user_interaction:
    target: "ユーザー操作から画面更新まで0.5秒以内"
    measurement: "クリック→レスポンス表示"
    conditions: "通常負荷時"
    
  form_validation:
    target: "入力検証・エラー表示0.3秒以内"
    measurement: "入力完了→バリデーション結果"
    conditions: "クライアントサイド検証"
```

#### バックエンドAPI応答時間
```yaml
api_performance:
  hearing_list_generation:
    target: "2秒以内（95パーセンタイル）"
    measurement: "API呼び出し→レスポンス返却"
    conditions: "プロジェクトスコープ選択→ヒアリング項目50件"
    
  setup_definition_generation:
    target: "5秒以内（95パーセンタイル）"
    measurement: "ヒアリング回答処理→定義書生成"
    conditions: "回答項目100件→設定値50項目生成"
    
  gap_analysis:
    target: "3秒以内（95パーセンタイル）"
    measurement: "要件分析→GAP要件特定"
    conditions: "要件項目30件→GAP要件10件特定"
    
  knowledge_search:
    target: "1秒以内（99パーセンタイル）"
    measurement: "検索クエリ→結果返却"
    conditions: "全文検索・1,000件知識ベース"
```

### 2.2 スループット要求

#### 同時利用者数
```yaml
concurrent_users:
  phase1_mvp:
    target: "10名同時利用でレスポンス維持"
    measurement: "同時API呼び出し・応答時間劣化率20%以内"
    
  phase2_expansion:
    target: "50名同時利用対応"
    measurement: "負荷テスト・実運用監視"
    
  phase3_commercial:
    target: "200名同時利用対応"
    measurement: "オートスケーリング・負荷分散"
```

#### データ処理能力
```yaml
data_throughput:
  batch_processing:
    target: "知識ベース更新1,000件/分"
    measurement: "バッチジョブ実行時間"
    
  export_performance:
    target: "Excel出力1,000行/5秒以内"
    measurement: "データ抽出→ファイル生成"
    
  import_capacity:
    target: "ヒアリング回答500件/分取り込み"
    measurement: "CSVインポート処理時間"
```

### 2.3 リソース利用効率

#### インフラリソース
```yaml
resource_efficiency:
  cpu_utilization:
    target: "平常時50%以下、ピーク時80%以下"
    measurement: "CloudWatch・Prometheus監視"
    
  memory_usage:
    target: "アプリケーション使用率70%以下"
    measurement: "メモリリーク検出・GC効率"
    
  database_performance:
    target: "クエリ実行時間100ms以内（80%）"
    measurement: "スロークエリログ・実行計画分析"
    
  network_bandwidth:
    target: "API通信データ圧縮率70%以上"
    measurement: "gzip圧縮・レスポンスサイズ"
```

## 3. 信頼性（Reliability）

### 3.1 可用性要求

#### システム稼働率
```yaml
availability:
  service_level:
    target: "99.9%（月間ダウンタイム43分以内）"
    measurement: "外形監視・稼働時間測定"
    exclusion: "計画メンテナンス時間を除く"
    
  recovery_time:
    rto: "目標復旧時間2時間以内"
    rpo: "目標復旧ポイント15分以内"
    measurement: "障害発生→サービス復旧"
    
  maintenance_window:
    scheduled: "月1回・日曜深夜2-4時（2時間以内）"
    emergency: "平日日中可（事前通知・影響最小化）"
```

#### 障害対応・監視
```yaml
monitoring_alerting:
  health_check:
    interval: "30秒間隔での死活監視"
    endpoints: "API・DB・外部サービス連携"
    
  error_rate:
    target: "エラー率1%以下"
    measurement: "HTTP 5xx・アプリケーションエラー"
    alert: "5分間で3%超過時アラート"
    
  response_time:
    threshold: "95パーセンタイル応答時間の150%超過"
    alert: "3分間継続でアラート・エスカレーション"
```

### 3.2 耐障害性・回復性

#### 障害分離・冗長化
```yaml
fault_tolerance:
  service_isolation:
    design: "マイクロサービス間の障害波及防止"
    implementation: "Circuit Breaker・Timeout設定"
    
  data_redundancy:
    database: "Primary-Replica構成・自動フェイルオーバー"
    backup: "日次フルバックアップ・1時間毎増分"
    
  geographic_distribution:
    phase1: "単一AZ・ローカル冗長"
    phase2: "マルチAZ・リージョン内冗長"
    phase3: "マルチリージョン対応検討"
```

#### 災害復旧・事業継続
```yaml
disaster_recovery:
  backup_strategy:
    database: "日次フルバックアップ・30日間保持"
    application: "コンテナイメージ・設定ファイル管理"
    documents: "Git・クラウドストレージ同期"
    
  recovery_procedures:
    documentation: "詳細復旧手順書・定期訓練"
    automation: "インフラ自動復旧・アプリケーション再起動"
    testing: "四半期毎の復旧テスト・手順見直し"
```

## 4. セキュリティ（Security）

### 4.1 認証・認可

#### ユーザー認証
```yaml
authentication:
  method: "JWT（JSON Web Token）ベース認証"
  token_expiry: "アクセストークン60分・リフレッシュトークン30日"
  multi_factor: "Phase 2でMFA対応（TOTP・SMS）"
  
  password_policy:
    length: "最低8文字・推奨12文字以上"
    complexity: "英数字記号組み合わせ・辞書攻撃対策"
    expiry: "90日間・履歴10世代管理"
    
  session_management:
    timeout: "無操作30分でセッション無効化"
    concurrent: "同一ユーザー5セッション上限"
    hijacking: "IP変更・User-Agent変更検出"
```

#### 認可・アクセス制御
```yaml
authorization:
  rbac: "ロールベースアクセス制御（Role-Based Access Control）"
  roles:
    - admin: "全機能・データアクセス"
    - consultant: "プロジェクト管理・要件定義"
    - viewer: "読み取り専用・レポート参照"
    
  resource_access:
    project_isolation: "プロジェクト毎のデータ分離"
    api_authorization: "エンドポイント毎の権限チェック"
    data_filtering: "ユーザー権限に応じたデータフィルタリング"
```

### 4.2 データ保護

#### 暗号化
```yaml
encryption:
  data_at_rest:
    database: "AES-256暗号化（AWS RDS暗号化）"
    files: "S3暗号化・KMS鍵管理"
    sensitive_fields: "PII・機密データの個別暗号化"
    
  data_in_transit:
    https: "TLS 1.3必須・HSTS有効化"
    api_communication: "内部API間もTLS暗号化"
    database_connection: "SSL/TLS接続必須"
    
  key_management:
    rotation: "暗号化鍵90日間隔で自動ローテーション"
    backup: "鍵バックアップ・復旧手順"
    access: "鍵アクセスログ・監査証跡"
```

#### プライバシー保護・GDPR対応
```yaml
privacy_protection:
  pii_handling:
    identification: "個人情報項目の明確な定義・マーキング"
    minimization: "必要最小限のデータ収集・保持"
    anonymization: "分析用データの匿名化・仮名化"
    
  user_rights:
    access: "データポータビリティ・エクスポート機能"
    rectification: "個人情報修正・更新機能"
    erasure: "個人情報削除・忘れられる権利"
    
  consent_management:
    explicit: "明示的同意・用途別同意管理"
    withdrawal: "同意撤回・処理停止機能"
    records: "同意履歴・証跡保持"
```

### 4.3 脆弱性対策・セキュリティ監視

#### アプリケーションセキュリティ
```yaml
application_security:
  input_validation:
    sanitization: "XSS・SQLインジェクション対策"
    csrf_protection: "CSRFトークン・SameSite Cookie"
    rate_limiting: "API呼び出し制限・DDoS対策"
    
  secure_coding:
    static_analysis: "静的コード解析・脆弱性スキャン"
    dependency_scan: "依存ライブラリ脆弱性チェック"
    penetration_test: "年2回のペネトレーションテスト"
    
  security_headers:
    csp: "Content Security Policy設定"
    hsts: "HTTP Strict Transport Security"
    x_frame_options: "Clickjacking対策"
```

#### セキュリティ監視・インシデント対応
```yaml
security_monitoring:
  audit_logging:
    scope: "認証・認可・データアクセス・設定変更"
    retention: "ログ保持期間1年・監査証跡"
    siem: "セキュリティ情報・イベント管理"
    
  threat_detection:
    anomaly: "異常アクセス・行動パターン検出"
    brute_force: "総当たり攻撃検出・アカウントロック"
    data_exfiltration: "大量データアクセス・エクスポート監視"
    
  incident_response:
    playbook: "インシデント対応手順書・エスカレーション"
    notification: "24時間以内の関係者通知"
    forensics: "証跡保全・原因調査・再発防止"
```

## 5. 使用性（Usability）

### 5.1 ユーザビリティ・UX要求

#### 学習容易性
```yaml
learnability:
  onboarding:
    target: "新規ユーザーが30分以内で基本操作習得"
    measurement: "チュートリアル完了率・操作成功率"
    support: "ガイドツアー・ヘルプドキュメント"
    
  intuitive_design:
    navigation: "3クリック以内で目的機能到達"
    consistency: "UI・UXパターンの統一性"
    feedback: "操作結果の明確なフィードバック"
```

#### 効率性・生産性
```yaml
efficiency:
  task_completion:
    hearing_generation: "ヒアリングリスト生成3分以内"
    response_input: "ヒアリング回答入力30項目/15分"
    setup_review: "セットアップ定義書レビュー5分以内"
    
  error_prevention:
    input_validation: "リアルタイム入力検証・エラー防止"
    auto_save: "30秒間隔の自動保存・データ損失防止"
    undo_redo: "操作の取り消し・やり直し機能"
```

### 5.2 アクセシビリティ

#### ウェブアクセシビリティ
```yaml
accessibility:
  wcag_compliance:
    level: "WCAG 2.1 レベルAA準拠"
    testing: "自動テスト・スクリーンリーダー検証"
    
  keyboard_navigation:
    support: "全機能のキーボード操作対応"
    shortcuts: "頻繁操作のショートカット提供"
    
  visual_design:
    contrast: "カラーコントラスト比4.5:1以上"
    text_size: "最小フォントサイズ14px・拡大200%対応"
    responsive: "モバイル・タブレット対応"
```

### 5.3 国際化・多言語対応

#### ローカライゼーション
```yaml
internationalization:
  phase1_scope:
    language: "日本語のみ"
    currency: "日本円（JPY）"
    timezone: "JST（Asia/Tokyo）"
    
  phase3_expansion:
    language: "英語・中国語・韓国語対応"
    currency: "多通貨対応・為替レート連携"
    timezone: "ユーザー設定タイムゾーン"
    
  implementation:
    i18n_framework: "React i18next・多言語リソース"
    date_format: "地域別日付・時刻フォーマット"
    number_format: "数値・通貨フォーマット対応"
```

## 6. 保守性（Maintainability）

### 6.1 コード品質・可読性

#### 開発標準・規約
```yaml
code_quality:
  coding_standards:
    language: "TypeScript ESLint・Python Black"
    naming: "ケース統一・意味のある命名"
    documentation: "JSDoc・docstring・README"
    
  complexity_metrics:
    cyclomatic: "複雑度10以下・関数行数50行以下"
    technical_debt: "SonarQube分析・負債指標管理"
    
  code_review:
    coverage: "全PR必須レビュー・2名以上承認"
    checklist: "機能・性能・セキュリティ観点"
    knowledge_sharing: "ペアプログラミング・定期勉強会"
```

#### テスト・品質保証
```yaml
testing_strategy:
  test_coverage:
    unit: "80%以上・ビジネスロジック100%"
    integration: "主要API・DB連携100%"
    e2e: "クリティカルパス・主要ユーザージャーニー"
    
  test_automation:
    ci_cd: "コミット毎の自動テスト・品質ゲート"
    regression: "リリース前全回帰テスト"
    performance: "負荷テスト・ベンチマーク比較"
```

### 6.2 運用・監視

#### ログ・監視・アラート
```yaml
observability:
  logging:
    structured: "JSON形式・検索可能なログ"
    levels: "ERROR・WARN・INFO・DEBUG"
    retention: "30日間・重要ログ1年間"
    
  metrics:
    application: "ビジネスメトリクス・技術メトリクス"
    infrastructure: "CPU・メモリ・ネットワーク・ディスク"
    user_experience: "ページ表示時間・エラー率"
    
  alerting:
    severity: "Critical・High・Medium・Low"
    escalation: "15分→30分→1時間エスカレーション"
    notification: "Slack・Email・PagerDuty連携"
```

#### デプロイ・リリース管理
```yaml
deployment:
  ci_cd_pipeline:
    automation: "Git push→テスト→ビルド→デプロイ"
    environments: "開発→ステージング→本番"
    rollback: "ワンクリック・自動ロールバック"
    
  release_strategy:
    blue_green: "本番環境無停止デプロイ"
    feature_flags: "機能フラグ・段階的リリース"
    canary: "カナリアリリース・リスク軽減"
```

## 7. 互換性・移植性

### 7.1 システム互換性

#### ブラウザ対応
```yaml
browser_compatibility:
  supported_browsers:
    chrome: "最新版・直前2バージョン"
    firefox: "最新版・直前2バージョン"
    safari: "最新版・直前2バージョン"
    edge: "最新版・直前2バージョン"
    
  mobile_browsers:
    ios_safari: "iOS 14以降"
    android_chrome: "Android 10以降"
    
  testing_strategy:
    automated: "CrossBrowserTesting・BrowserStack"
    manual: "主要環境での手動検証"
```

#### 外部システム連携
```yaml
integration_compatibility:
  salesforce_api:
    versions: "REST API v52.0以降・SOAP API対応"
    authentication: "OAuth 2.0・JWT Bearer"
    rate_limits: "API制限遵守・リトライ制御"
    
  office_integration:
    excel_export: "Excel 2016以降・CSV互換"
    pdf_generation: "PDF/A準拠・印刷最適化"
    
  third_party_services:
    email: "SendGrid・AWS SES"
    storage: "AWS S3・Azure Blob Storage"
    monitoring: "DataDog・New Relic・Prometheus"
```

### 7.2 クラウド・インフラ移植性

#### クラウドプロバイダー対応
```yaml
cloud_portability:
  primary_cloud:
    provider: "AWS（Phase 1-2）"
    services: "ECS・RDS・ElastiCache・S3"
    
  multi_cloud_strategy:
    phase3: "Azure・GCPサポート検討"
    containerization: "Docker・Kubernetes対応"
    infrastructure_as_code: "Terraform・CloudFormation"
    
  vendor_lock_in_avoidance:
    database: "PostgreSQL・オープンソース"
    message_queue: "Redis・Apache Kafka"
    storage: "S3互換API・標準プロトコル"
```

## 8. 測定・監視・改善

### 8.1 非機能要求の測定方法

#### 継続的測定
```yaml
continuous_measurement:
  real_time_monitoring:
    tools: "Prometheus・Grafana・DataDog"
    metrics: "レスポンス時間・エラー率・リソース使用率"
    dashboards: "リアルタイム・履歴・傾向分析"
    
  user_experience_monitoring:
    tools: "Google Analytics・Hotjar・LogRocket"
    metrics: "ページ表示時間・離脱率・操作エラー"
    feedback: "ユーザー満足度・NPS調査"
    
  load_testing:
    tools: "JMeter・k6・Gatling"
    scenarios: "通常負荷・ピーク負荷・ストレステスト"
    frequency: "リリース前・月次定期実行"
```

### 8.2 改善・最適化プロセス

#### 継続的改善
```yaml
continuous_improvement:
  performance_optimization:
    profiling: "APM・コードプロファイリング"
    bottleneck_analysis: "スローQUERY・CPU集約処理特定"
    optimization: "インデックス・キャッシュ・アルゴリズム改善"
    
  capacity_planning:
    trend_analysis: "利用者数・データ量増加予測"
    scaling_strategy: "水平・垂直スケーリング計画"
    cost_optimization: "リソース効率・コスト最適化"
    
  quality_metrics:
    tracking: "品質指標・技術的負債の継続追跡"
    review: "月次品質レビュー・改善計画"
    investment: "技術的負債解消・リファクタリング"
```

## 9. Phase別非機能要求

### 9.1 Phase 1 MVP要求

```yaml
phase1_requirements:
  performance:
    concurrent_users: "10名同時利用"
    response_time: "API 2-5秒・画面表示3秒"
    
  reliability:
    availability: "99%（平日営業時間）"
    recovery: "手動復旧・4時間以内"
    
  security:
    basic_auth: "JWT認証・基本的なアクセス制御"
    https: "TLS暗号化・基本的なセキュリティヘッダー"
    
  scalability:
    architecture: "モノリス許容・マイクロサービス準備"
    database: "単一DB・読み取り専用レプリカ"
```

### 9.2 Phase 2-3 商用化要求

```yaml
commercial_requirements:
  performance:
    concurrent_users: "50-200名同時利用"
    response_time: "API 1-3秒・画面表示2秒"
    
  reliability:
    availability: "99.9%（24時間365日）"
    recovery: "自動復旧・2時間以内"
    
  security:
    enterprise_auth: "MFA・SSO・RBAC"
    compliance: "SOC2・GDPR・セキュリティ監査"
    
  scalability:
    microservices: "マイクロサービス分離・独立デプロイ"
    multi_tenant: "マルチテナント・データ分離"
```

## 10. 関連文書・参照

### 10.1 プロジェクト文書

- [📋 プロジェクト全体構想](./project-overview.md)
- [🏗️ 技術アーキテクチャ](./technical-architecture.md)
- [📝 機能要求仕様書](./functional-requirements.md)
- [🧪 品質保証・テスト戦略](./quality-assurance.md)

### 10.2 運用・セキュリティ文書

- [🔧 環境構築ガイド](./setup-guide.md)
- [🛡️ セキュリティ・コンプライアンス要件](./security-compliance.md)
- [📊 監視・運用手順](./operations-guide.md)

### 10.3 外部参照・標準

- [ISO/IEC 25010 品質モデル](https://www.iso.org/standard/35733.html)
- [WCAG 2.1 ウェブアクセシビリティガイドライン](https://www.w3.org/WAI/WCAG21/quickref/)
- [GDPR データ保護規則](https://gdpr-info.eu/)
- [SOC 2 セキュリティ基準](https://www.aicpa.org/interestareas/frc/assuranceadvisoryservices/aicpasoc2report.html)

---
**最終更新**: 2025-07-13  
**文書バージョン**: 1.0  
**承認状況**: レビュー待ち  
**次回レビュー**: Phase 1開発中（非機能要求検証時）