# Phase 1 データベース設計書

## 1. データベース設計概要

### 1.1 設計方針・原則

ERPset Phase 1のデータベース設計は、**スケーラビリティ**と**保守性**を重視し、将来のPhase拡張に対応できる柔軟な構造を採用します。

#### 設計原則
```yaml
database_design_principles:
  normalization:
    - "第3正規形準拠・データ整合性確保"
    - "適切な非正規化・パフォーマンス最適化"
    - "冗長性最小化・ストレージ効率化"
    
  scalability:
    - "水平分割対応・シャーディング準備"
    - "インデックス最適化・クエリ性能確保"
    - "パーティショニング・アーカイブ戦略"
    
  maintainability:
    - "明確な命名規則・テーブル構造"
    - "外部キー制約・参照整合性"
    - "マイグレーション管理・バージョン管理"
    
  extensibility:
    - "Phase 2-5拡張対応・追加フィールド余地"
    - "マルチテナント準備・論理分離"
    - "監査ログ・変更履歴管理"
```

### 1.2 技術スタック・構成

#### データベース技術選定
```yaml
database_stack:
  primary_database: "PostgreSQL 15"
  reasons:
    - "ACID特性・トランザクション安全性"
    - "JSON・配列・全文検索機能"
    - "拡張性・パフォーマンス・エコシステム"
    - "オープンソース・コスト効率"
    
  caching_layer: "Redis 7"
  purposes:
    - "セッション管理・JWTトークン"
    - "APIレスポンスキャッシュ"
    - "一時データ・計算結果"
    
  connection_management:
    pool_size: "20-50接続"
    timeout: "30秒"
    retry_logic: "指数バックオフ"
```

## 2. ER図・データモデル

### 2.1 主要エンティティ関係図

```
┌─────────────────┐     ┌─────────────────────────┐     ┌─────────────────────────┐
│     Users       │ 1:N │       Projects          │ 1:N │    Hearing Sessions     │
│─────────────────│────▶│─────────────────────────│────▶│─────────────────────────│
│ id (PK)         │     │ id (PK)                 │     │ id (PK)                 │
│ email           │     │ name                    │     │ project_id (FK)         │
│ password_hash   │     │ description             │     │ status                  │
│ name            │     │ erp_type                │     │ generated_at            │
│ role            │     │ business_domain         │     │ completion_rate         │
│ created_at      │     │ scope                   │     │ estimated_time          │
│ updated_at      │     │ status                  │     │ metadata                │
│ is_active       │     │ owner_id (FK)           │     └─────────────────────────┘
└─────────────────┘     │ created_at              │              │
                        │ updated_at              │              │ 1:N
                        └─────────────────────────┘              ▼
                                 │                    ┌─────────────────────────┐
                                 │ 1:N                │    Hearing Items        │
                                 ▼                    │─────────────────────────│
                    ┌─────────────────────────┐       │ id (PK)                 │
                    │   Setup Definitions     │       │ session_id (FK)         │
                    │─────────────────────────│       │ salesforce_function_id  │
                    │ id (PK)                 │       │ question                │
                    │ project_id (FK)         │       │ answer_type             │
                    │ configuration           │       │ answer_options          │
                    │ gap_analysis            │       │ is_required             │
                    │ export_formats          │       │ category                │
                    │ generated_at            │       │ priority                │
                    │ data_quality_score      │       │ help_text               │
                    └─────────────────────────┘       └─────────────────────────┘
                                                                │
                                                                │ 1:1
                                                                ▼
                                                   ┌─────────────────────────┐
                                                   │   Hearing Responses     │
                                                   │─────────────────────────│
                                                   │ id (PK)                 │
                                                   │ hearing_item_id (FK)    │
                                                   │ response_value          │
                                                   │ comments                │
                                                   │ confidence_level        │
                                                   │ answered_at             │
                                                   └─────────────────────────┘

┌─────────────────────────┐     ┌─────────────────────────┐     ┌─────────────────────────┐
│  Salesforce Functions   │ 1:N │   Function Categories   │ N:M │    Knowledge Tags       │
│─────────────────────────│────▶│─────────────────────────│◀───▶│─────────────────────────│
│ id (PK)                 │     │ id (PK)                 │     │ id (PK)                 │
│ name                    │     │ name                    │     │ name                    │
│ description             │     │ description             │     │ description             │
│ module                  │     │ module                  │     │ color                   │
│ configuration_template  │     │ parent_id (FK)          │     │ created_at              │
│ hearing_template        │     │ sort_order              │     └─────────────────────────┘
│ is_active               │     │ created_at              │
│ complexity_score        │     └─────────────────────────┘
│ created_at              │
│ updated_at              │
└─────────────────────────┘
```

### 2.2 コアテーブル詳細設計

#### Users（ユーザー管理）
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'consultant', 'viewer')),
    is_active BOOLEAN DEFAULT true,
    email_verified BOOLEAN DEFAULT false,
    last_login_at TIMESTAMP WITH TIME ZONE,
    password_reset_token VARCHAR(255),
    password_reset_expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- インデックス
    INDEX idx_users_email (email),
    INDEX idx_users_role (role),
    INDEX idx_users_active (is_active),
    INDEX idx_users_created_at (created_at)
);
```

#### Projects（プロジェクト管理）
```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    erp_type VARCHAR(50) NOT NULL DEFAULT 'salesforce',
    business_domain VARCHAR(50) NOT NULL CHECK (business_domain IN ('sales', 'service', 'marketing')),
    scope JSONB NOT NULL DEFAULT '{}',
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'completed', 'archived')),
    owner_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    
    -- メタデータ
    client_name VARCHAR(200),
    project_budget DECIMAL(12,2),
    start_date DATE,
    target_go_live DATE,
    
    -- タイムスタンプ
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- インデックス
    INDEX idx_projects_owner (owner_id),
    INDEX idx_projects_status (status),
    INDEX idx_projects_erp_type (erp_type),
    INDEX idx_projects_domain (business_domain),
    INDEX idx_projects_created_at (created_at),
    
    -- 全文検索インデックス
    INDEX idx_projects_search USING gin(to_tsvector('english', name || ' ' || COALESCE(description, '')))
);
```

#### Hearing_Sessions（ヒアリングセッション）
```sql
CREATE TABLE hearing_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'completed', 'archived')),
    
    -- 生成パラメータ
    business_modules JSONB NOT NULL DEFAULT '[]',
    business_requirements JSONB NOT NULL DEFAULT '[]',
    priority_focus VARCHAR(20) DEFAULT 'essential' CHECK (priority_focus IN ('comprehensive', 'essential', 'quick')),
    
    -- 結果データ
    total_items INTEGER DEFAULT 0,
    completed_items INTEGER DEFAULT 0,
    completion_rate DECIMAL(5,4) DEFAULT 0.0,
    coverage_score DECIMAL(5,4),
    estimated_time_minutes INTEGER,
    
    -- メタデータ
    generation_rationale TEXT,
    metadata JSONB DEFAULT '{}',
    
    -- タイムスタンプ
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- インデックス
    INDEX idx_hearing_sessions_project (project_id),
    INDEX idx_hearing_sessions_status (status),
    INDEX idx_hearing_sessions_generated (generated_at),
    INDEX idx_hearing_sessions_completion (completion_rate)
);
```

#### Hearing_Items（ヒアリング項目）
```sql
CREATE TABLE hearing_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES hearing_sessions(id) ON DELETE CASCADE,
    salesforce_function_id UUID REFERENCES salesforce_functions(id),
    
    -- 質問内容
    question TEXT NOT NULL,
    answer_type VARCHAR(20) NOT NULL CHECK (answer_type IN ('text', 'select', 'multiselect', 'number', 'boolean', 'date')),
    answer_options JSONB,
    is_required BOOLEAN DEFAULT false,
    
    -- 分類・優先度
    category VARCHAR(100) NOT NULL,
    priority INTEGER CHECK (priority BETWEEN 1 AND 5),
    estimated_time_minutes INTEGER DEFAULT 5,
    
    -- 補助情報
    help_text TEXT,
    validation_rules JSONB DEFAULT '{}',
    display_order INTEGER,
    
    -- タイムスタンプ
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- インデックス
    INDEX idx_hearing_items_session (session_id),
    INDEX idx_hearing_items_function (salesforce_function_id),
    INDEX idx_hearing_items_category (category),
    INDEX idx_hearing_items_priority (priority),
    INDEX idx_hearing_items_order (display_order),
    
    -- 全文検索
    INDEX idx_hearing_items_search USING gin(to_tsvector('english', question || ' ' || COALESCE(help_text, '')))
);
```

#### Hearing_Responses（ヒアリング回答）
```sql
CREATE TABLE hearing_responses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hearing_item_id UUID NOT NULL REFERENCES hearing_items(id) ON DELETE CASCADE,
    
    -- 回答内容
    response_value JSONB,  -- 型に応じた値格納
    comments TEXT,
    confidence_level VARCHAR(10) CHECK (confidence_level IN ('high', 'medium', 'low')),
    
    -- 回答者情報
    answered_by_id UUID REFERENCES users(id),
    answered_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- 変更履歴
    previous_value JSONB,
    revision_number INTEGER DEFAULT 1,
    
    -- タイムスタンプ
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- インデックス
    INDEX idx_hearing_responses_item (hearing_item_id),
    INDEX idx_hearing_responses_answered_by (answered_by_id),
    INDEX idx_hearing_responses_answered_at (answered_at),
    INDEX idx_hearing_responses_confidence (confidence_level),
    
    -- ユニーク制約（1項目1回答）
    UNIQUE (hearing_item_id)
);
```

### 2.3 知識ベーステーブル

#### Salesforce_Functions（Salesforce機能マスタ）
```sql
CREATE TABLE salesforce_functions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- 基本情報
    name VARCHAR(200) NOT NULL,
    description TEXT,
    module VARCHAR(50) NOT NULL CHECK (module IN ('sales', 'service', 'marketing', 'analytics', 'platform')),
    function_type VARCHAR(50),
    
    -- 設定テンプレート
    configuration_template JSONB DEFAULT '{}',
    hearing_template JSONB DEFAULT '{}',
    setup_requirements JSONB DEFAULT '{}',
    
    -- メタデータ
    complexity_score INTEGER CHECK (complexity_score BETWEEN 1 AND 10),
    implementation_effort_hours INTEGER,
    dependencies JSONB DEFAULT '[]',
    prerequisites JSONB DEFAULT '[]',
    
    -- ステータス
    is_active BOOLEAN DEFAULT true,
    is_standard BOOLEAN DEFAULT true,
    requires_license BOOLEAN DEFAULT false,
    
    -- バージョン管理
    version VARCHAR(20) DEFAULT '1.0',
    effective_from DATE,
    deprecated_at DATE,
    
    -- タイムスタンプ
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- インデックス
    INDEX idx_sf_functions_module (module),
    INDEX idx_sf_functions_type (function_type),
    INDEX idx_sf_functions_active (is_active),
    INDEX idx_sf_functions_complexity (complexity_score),
    
    -- 全文検索
    INDEX idx_sf_functions_search USING gin(to_tsvector('english', name || ' ' || COALESCE(description, '')))
);
```

#### Function_Categories（機能カテゴリ）
```sql
CREATE TABLE function_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    module VARCHAR(50) NOT NULL,
    parent_id UUID REFERENCES function_categories(id),
    sort_order INTEGER DEFAULT 0,
    icon VARCHAR(50),
    color VARCHAR(7),  -- HEXカラーコード
    
    -- タイムスタンプ
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- インデックス
    INDEX idx_categories_module (module),
    INDEX idx_categories_parent (parent_id),
    INDEX idx_categories_order (sort_order)
);
```

#### Knowledge_Tags（知識タグ）
```sql
CREATE TABLE knowledge_tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    color VARCHAR(7) DEFAULT '#6B7280',
    usage_count INTEGER DEFAULT 0,
    
    -- タイムスタンプ
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- インデックス
    INDEX idx_tags_usage (usage_count DESC)
);
```

### 2.4 セットアップ定義テーブル

#### Setup_Definitions（セットアップ定義）
```sql
CREATE TABLE setup_definitions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    
    -- 設定内容
    configuration JSONB NOT NULL DEFAULT '{}',
    validation_rules JSONB DEFAULT '{}',
    workflow_automation JSONB DEFAULT '{}',
    
    -- GAP分析結果
    gap_analysis JSONB DEFAULT '{}',
    identified_gaps INTEGER DEFAULT 0,
    critical_gaps INTEGER DEFAULT 0,
    recommended_solutions JSONB DEFAULT '[]',
    
    -- 品質指標
    data_quality_score DECIMAL(5,4),
    completeness_score DECIMAL(5,4),
    consistency_score DECIMAL(5,4),
    
    -- エクスポート管理
    export_formats JSONB DEFAULT '[]',
    last_exported_at TIMESTAMP WITH TIME ZONE,
    export_version INTEGER DEFAULT 1,
    
    -- メタデータ
    generation_duration_seconds DECIMAL(8,3),
    generation_metadata JSONB DEFAULT '{}',
    
    -- タイムスタンプ
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- インデックス
    INDEX idx_setup_definitions_project (project_id),
    INDEX idx_setup_definitions_generated (generated_at),
    INDEX idx_setup_definitions_quality (data_quality_score)
);
```

### 2.5 中間テーブル・関連テーブル

#### Function_Category_Mappings（機能-カテゴリマッピング）
```sql
CREATE TABLE function_category_mappings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    function_id UUID NOT NULL REFERENCES salesforce_functions(id) ON DELETE CASCADE,
    category_id UUID NOT NULL REFERENCES function_categories(id) ON DELETE CASCADE,
    is_primary BOOLEAN DEFAULT false,
    
    -- タイムスタンプ
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- インデックス・制約
    INDEX idx_func_cat_function (function_id),
    INDEX idx_func_cat_category (category_id),
    UNIQUE (function_id, category_id)
);
```

#### Function_Tag_Mappings（機能-タグマッピング）
```sql
CREATE TABLE function_tag_mappings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    function_id UUID NOT NULL REFERENCES salesforce_functions(id) ON DELETE CASCADE,
    tag_id UUID NOT NULL REFERENCES knowledge_tags(id) ON DELETE CASCADE,
    relevance_score DECIMAL(3,2) DEFAULT 1.0,
    
    -- タイムスタンプ
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- インデックス・制約
    INDEX idx_func_tag_function (function_id),
    INDEX idx_func_tag_tag (tag_id),
    INDEX idx_func_tag_relevance (relevance_score DESC),
    UNIQUE (function_id, tag_id)
);
```

## 3. データベース制約・ルール

### 3.1 外部キー制約

#### 参照整合性管理
```sql
-- カスケード削除設定
-- プロジェクト削除時：ヒアリングセッション・セットアップ定義も削除
-- ヒアリングセッション削除時：ヒアリング項目・回答も削除
-- ユーザー削除制限：プロジェクトオーナーの場合は削除不可

-- 外部キー制約の詳細定義
ALTER TABLE projects 
ADD CONSTRAINT fk_projects_owner 
FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE RESTRICT;

ALTER TABLE hearing_sessions 
ADD CONSTRAINT fk_hearing_sessions_project 
FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE;

ALTER TABLE hearing_items 
ADD CONSTRAINT fk_hearing_items_session 
FOREIGN KEY (session_id) REFERENCES hearing_sessions(id) ON DELETE CASCADE;

ALTER TABLE hearing_responses 
ADD CONSTRAINT fk_hearing_responses_item 
FOREIGN KEY (hearing_item_id) REFERENCES hearing_items(id) ON DELETE CASCADE;
```

### 3.2 チェック制約・検証ルール

#### データ整合性チェック
```sql
-- プロジェクトスコープ検証
ALTER TABLE projects 
ADD CONSTRAINT chk_projects_scope_required 
CHECK (jsonb_typeof(scope) = 'object' AND scope != '{}');

-- ヒアリング完了率検証
ALTER TABLE hearing_sessions 
ADD CONSTRAINT chk_hearing_completion_rate 
CHECK (completion_rate >= 0.0 AND completion_rate <= 1.0);

-- 回答値タイプ検証
ALTER TABLE hearing_responses 
ADD CONSTRAINT chk_response_value_not_null 
CHECK (response_value IS NOT NULL);

-- 複雑度スコア範囲検証
ALTER TABLE salesforce_functions 
ADD CONSTRAINT chk_complexity_score_range 
CHECK (complexity_score BETWEEN 1 AND 10);
```

### 3.3 インデックス戦略

#### パフォーマンス最適化インデックス
```sql
-- 複合インデックス（よく使用されるクエリパターン用）
CREATE INDEX idx_projects_owner_status ON projects(owner_id, status);
CREATE INDEX idx_hearing_items_session_category ON hearing_items(session_id, category);
CREATE INDEX idx_responses_item_answered ON hearing_responses(hearing_item_id, answered_at);

-- 部分インデックス（条件付きインデックス）
CREATE INDEX idx_projects_active ON projects(created_at) WHERE status = 'active';
CREATE INDEX idx_functions_active ON salesforce_functions(name) WHERE is_active = true;

-- JSON フィールドインデックス
CREATE INDEX idx_projects_scope_sales ON projects USING gin((scope->'lead_management'));
CREATE INDEX idx_hearing_metadata ON hearing_sessions USING gin(metadata);
```

## 4. データ型・JSON スキーマ

### 4.1 JSON フィールド定義

#### Project.scope スキーマ
```json
{
  "type": "object",
  "properties": {
    "lead_management": {"type": "boolean"},
    "opportunity_management": {"type": "boolean"},
    "account_management": {"type": "boolean"},
    "contact_management": {"type": "boolean"},
    "quote_management": {"type": "boolean"},
    "custom_objects": {
      "type": "array",
      "items": {"type": "string"}
    },
    "integration_requirements": {
      "type": "array",
      "items": {"type": "string"}
    }
  },
  "required": ["lead_management", "opportunity_management"]
}
```

#### Hearing_Items.answer_options スキーマ
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "value": {"type": "string"},
      "label": {"type": "string"},
      "description": {"type": "string"},
      "is_default": {"type": "boolean"}
    },
    "required": ["value", "label"]
  }
}
```

#### Setup_Definitions.configuration スキーマ
```json
{
  "type": "object",
  "properties": {
    "lead_management": {
      "type": "object",
      "properties": {
        "lead_sources": {"type": "array"},
        "lead_status": {"type": "array"},
        "assignment_rules": {"type": "object"},
        "conversion_process": {"type": "object"}
      }
    },
    "opportunity_management": {
      "type": "object",
      "properties": {
        "stages": {"type": "array"},
        "probability_mapping": {"type": "object"},
        "forecasting_categories": {"type": "array"}
      }
    }
  }
}
```

### 4.2 列挙型・定数定義

#### アプリケーション定数
```sql
-- ユーザーロール
CREATE TYPE user_role AS ENUM ('admin', 'consultant', 'viewer');

-- プロジェクトステータス
CREATE TYPE project_status AS ENUM ('active', 'completed', 'archived');

-- ヒアリング回答タイプ
CREATE TYPE answer_type AS ENUM ('text', 'select', 'multiselect', 'number', 'boolean', 'date');

-- 信頼度レベル
CREATE TYPE confidence_level AS ENUM ('high', 'medium', 'low');

-- Salesforce モジュール
CREATE TYPE salesforce_module AS ENUM ('sales', 'service', 'marketing', 'analytics', 'platform');
```

## 5. マイグレーション戦略

### 5.1 初期データベース構築

#### テーブル作成順序
```sql
-- 1. 基盤テーブル
CREATE TABLE users (...);
CREATE TABLE knowledge_tags (...);

-- 2. マスタテーブル
CREATE TABLE function_categories (...);
CREATE TABLE salesforce_functions (...);

-- 3. プロジェクト関連テーブル
CREATE TABLE projects (...);
CREATE TABLE hearing_sessions (...);
CREATE TABLE hearing_items (...);
CREATE TABLE hearing_responses (...);
CREATE TABLE setup_definitions (...);

-- 4. 関連テーブル
CREATE TABLE function_category_mappings (...);
CREATE TABLE function_tag_mappings (...);

-- 5. インデックス・制約
CREATE INDEX ...;
ALTER TABLE ... ADD CONSTRAINT ...;
```

### 5.2 マスタデータ投入

#### Salesforce機能マスタ初期データ
```sql
-- Sales Cloud 主要機能の投入
INSERT INTO salesforce_functions (name, description, module, configuration_template) VALUES
('Lead Management', 'リード管理機能', 'sales', '{"lead_sources": [], "assignment_rules": {}}'),
('Opportunity Management', '商談管理機能', 'sales', '{"stages": [], "probability_mapping": {}}'),
('Account Management', '取引先管理機能', 'sales', '{"record_types": [], "validation_rules": {}}'),
('Contact Management', '取引先責任者管理', 'sales', '{"contact_roles": [], "relationship_mapping": {}}'),
('Quote Management', '見積管理機能', 'sales', '{"approval_process": [], "pricing_rules": {}}}');

-- カテゴリ分類データ
INSERT INTO function_categories (name, description, module) VALUES
('Customer Lifecycle', '顧客ライフサイクル管理', 'sales'),
('Sales Process', 'セールスプロセス管理', 'sales'),
('Data Management', 'データ管理・品質', 'sales'),
('Automation', '自動化・ワークフロー', 'sales');
```

### 5.3 Phase 2-5 拡張準備

#### 拡張対応設計
```sql
-- 将来のマルチテナント対応準備
ALTER TABLE users ADD COLUMN tenant_id UUID;
ALTER TABLE projects ADD COLUMN tenant_id UUID;

-- 追加ERP対応準備
ALTER TABLE projects ALTER COLUMN erp_type TYPE VARCHAR(100);
CREATE TABLE erp_systems (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    version VARCHAR(50),
    is_supported BOOLEAN DEFAULT true
);

-- 監査ログテーブル準備
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    table_name VARCHAR(100) NOT NULL,
    record_id UUID NOT NULL,
    action VARCHAR(20) NOT NULL,
    old_values JSONB,
    new_values JSONB,
    user_id UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

## 6. パフォーマンス・最適化

### 6.1 クエリ最適化戦略

#### 頻出クエリパターン最適化
```sql
-- プロジェクト一覧取得（ページネーション対応）
EXPLAIN ANALYZE 
SELECT p.*, u.name as owner_name 
FROM projects p 
JOIN users u ON p.owner_id = u.id 
WHERE p.status = 'active' 
ORDER BY p.created_at DESC 
LIMIT 20 OFFSET 0;

-- ヒアリング進捗情報取得
EXPLAIN ANALYZE
SELECT 
    hs.id,
    hs.total_items,
    hs.completed_items,
    hs.completion_rate,
    COUNT(hr.id) as answered_count
FROM hearing_sessions hs
LEFT JOIN hearing_items hi ON hs.id = hi.session_id
LEFT JOIN hearing_responses hr ON hi.id = hr.hearing_item_id
WHERE hs.project_id = '...'
GROUP BY hs.id;
```

### 6.2 インデックス効果測定

#### パフォーマンス監視クエリ
```sql
-- インデックス使用状況確認
SELECT 
    indexname,
    idx_tup_read,
    idx_tup_fetch,
    idx_tup_read / idx_tup_fetch as selectivity
FROM pg_stat_user_indexes 
WHERE schemaname = 'public'
ORDER BY idx_tup_read DESC;

-- スロークエリ特定
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    stddev_time
FROM pg_stat_statements 
WHERE mean_time > 1000  -- 1秒以上
ORDER BY mean_time DESC;
```

### 6.3 パーティショニング戦略

#### 大量データ対応準備
```sql
-- ログテーブルの月次パーティショニング
CREATE TABLE audit_logs_template (
    LIKE audit_logs INCLUDING ALL
) PARTITION BY RANGE (created_at);

-- 月次パーティション例
CREATE TABLE audit_logs_2025_01 PARTITION OF audit_logs_template
FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

-- ヒアリング回答の年次パーティショニング
CREATE TABLE hearing_responses_template (
    LIKE hearing_responses INCLUDING ALL
) PARTITION BY RANGE (answered_at);
```

## 7. セキュリティ・バックアップ

### 7.1 データベースセキュリティ

#### アクセス制御・権限管理
```sql
-- アプリケーション用ロール作成
CREATE ROLE erpset_app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO erpset_app_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO erpset_app_user;

-- 読み取り専用ロール
CREATE ROLE erpset_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO erpset_readonly;

-- レプリケーション用ロール
CREATE ROLE erpset_replica REPLICATION;
```

#### 機密データ保護
```sql
-- パスワードハッシュ化確認
CREATE OR REPLACE FUNCTION validate_password_hash()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.password_hash IS NULL OR length(NEW.password_hash) < 60 THEN
        RAISE EXCEPTION 'Invalid password hash format';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validate_password 
BEFORE INSERT OR UPDATE ON users 
FOR EACH ROW EXECUTE FUNCTION validate_password_hash();
```

### 7.2 バックアップ・災害復旧

#### バックアップ戦略
```yaml
backup_strategy:
  full_backup:
    frequency: "毎日午前3時"
    retention: "30日間"
    compression: "gzip"
    encryption: "AES-256"
    
  incremental_backup:
    frequency: "4時間毎"
    retention: "7日間"
    wal_archiving: "有効"
    
  point_in_time_recovery:
    wal_retention: "24時間"
    recovery_target: "任意時点復旧対応"
    
  testing:
    restore_test: "月次実施"
    recovery_drill: "四半期実施"
```

## 8. 監視・運用

### 8.1 データベース監視

#### パフォーマンス監視指標
```sql
-- 接続数監視
SELECT count(*), state FROM pg_stat_activity GROUP BY state;

-- データベースサイズ監視
SELECT 
    datname,
    pg_size_pretty(pg_database_size(datname)) as size
FROM pg_database;

-- テーブルサイズ監視
SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size(tablename::regclass)) as size
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(tablename::regclass) DESC;
```

### 8.2 メンテナンス・最適化

#### 定期メンテナンスタスク
```sql
-- 統計情報更新
ANALYZE;

-- バキューム実行
VACUUM ANALYZE;

-- インデックス再構築（必要時）
REINDEX DATABASE erpset;

-- 古いデータアーカイブ
DELETE FROM audit_logs WHERE created_at < NOW() - INTERVAL '1 year';
```

## 9. 関連文書・参照

### 9.1 Phase 1設計文書

- [🔧 技術仕様書](./technical-spec.md)
- [🌐 API設計書](./api-design.md)
- [⚡ Salesforce知識ベース設計](./salesforce-knowledge.md)
- [🚀 デプロイ・運用ガイド](./deployment-guide.md)

### 9.2 全体プロジェクト文書

- [📋 プロジェクト全体構想](../../docs/project-overview.md)
- [🏗️ 技術アーキテクチャ](../../docs/technical-architecture.md)
- [📝 機能要求仕様書](../../docs/functional-requirements.md)
- [⚙️ 非機能要求仕様書](../../docs/non-functional-requirements.md)

### 9.3 外部参照・ドキュメント

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Database Design Best Practices](https://www.postgresql.org/docs/current/ddl.html)
- [JSON/JSONB in PostgreSQL](https://www.postgresql.org/docs/current/datatype-json.html)
- [Performance Tuning Guide](https://wiki.postgresql.org/wiki/Performance_Optimization)

---
**最終更新**: 2025-07-13  
**文書バージョン**: 1.0  
**データベース責任者**: バックエンドリード・DBA  
**次回レビュー**: データベース実装開始時（テーブル作成・マイグレーション実行）