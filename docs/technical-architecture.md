# ERPset 技術アーキテクチャ

## 1. アーキテクチャ概要

### 1.1 設計原則

ERPsetプラットフォームは以下の設計原則に基づいて構築されます：

#### コア原則
- **段階的詳細化**: Phase毎に技術選択を最適化、過度な先行設計を回避
- **疎結合・高凝集**: モジュール間のAPI連携により拡張性とメンテナンス性を確保
- **知識ベース中心**: 構造化された知識データが競争優位の核心
- **実装ファースト**: 理論より実装、実装から学んだ知見で設計を改善

#### 非機能要件
- **可用性**: 99.9%（月間ダウンタイム43分以内）
- **性能**: 応答時間2秒以内（ヒアリングリスト生成）
- **拡張性**: 水平スケーリング対応、マルチテナント架構
- **セキュリティ**: SOC2 Type2準拠、GDPR対応

### 1.2 全体システム構成

```
┌─────────────────────────────────────────────────────────────────┐
│                        ERPset Platform                         │
├─────────────────────────────────────────────────────────────────┤
│                      API Gateway Layer                         │
│  Authentication | Rate Limiting | Routing | Monitoring         │
├─────────────────────────────────────────────────────────────────┤
│  Frontend Layer │              Backend Services                │
│                 │                                              │
│  Next.js Web    │  Requirements    │    Migration             │
│  Application    │  Definition      │    Support               │
│                 │  Service         │    Service               │
│                 │                  │                          │
│  React Admin    │  Knowledge       │    Integration           │
│  Dashboard      │  Base            │    Adapter               │
│                 │  Service         │    Service               │
├─────────────────────────────────────────────────────────────────┤
│                      Data Layer                                │
│  PostgreSQL  │  Redis Cache  │  File Storage  │  Vector DB    │
│  (Core Data) │  (Sessions)   │  (Documents)   │  (Knowledge)  │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Phase 1 MVP アーキテクチャ

### 2.1 技術スタック選定理由

#### フロントエンド: Next.js 15 + TypeScript
**選定理由**:
- **開発速度**: React Serverコンポーネントによる高速開発
- **SEO対応**: SSRによる検索エンジン最適化
- **TypeScript**: 型安全性による品質向上
- **エコシステム**: 豊富なライブラリとツール群

**主要ライブラリ**:
```json
{
  "dependencies": {
    "next": "^15.0.0",
    "react": "^18.3.0",
    "typescript": "^5.4.0",
    "tailwindcss": "^3.4.0",
    "zustand": "^4.5.0",
    "@tanstack/react-query": "^5.0.0",
    "react-hook-form": "^7.51.0",
    "zod": "^3.22.0"
  }
}
```

#### バックエンド: Python + FastAPI
**選定理由**:
- **AI/ML統合**: 豊富なAI/MLライブラリとの親和性
- **開発生産性**: Pythonの可読性と開発速度
- **API性能**: FastAPIの高性能・自動ドキュメント生成
- **型安全**: Pydanticによる型検証

**主要フレームワーク・ライブラリ**:
```python
dependencies = [
    "fastapi[all]==0.104.1",
    "sqlalchemy==2.0.25",
    "alembic==1.13.1",
    "pydantic==2.5.0",
    "pandas==2.1.4",
    "langchain==0.1.0",
    "openai==1.7.0",
    "redis==5.0.1",
    "pytest==7.4.3"
]
```

#### データベース: PostgreSQL + Redis
**PostgreSQL**: 
- ACID特性による高い整合性
- JSON型によるスキーマ柔軟性
- 高性能全文検索（pg_trgm）

**Redis**:
- セッション管理・キャッシュ
- リアルタイム通知（Pub/Sub）
- レート制限実装

### 2.2 詳細アーキテクチャ設計

#### フロントエンド構成
```
src/
├── app/                    # Next.js App Router
│   ├── (auth)/            # 認証ルート
│   ├── dashboard/         # ダッシュボード
│   ├── projects/          # プロジェクト管理
│   └── api/               # API Routes
├── components/            # UIコンポーネント
│   ├── ui/               # 基本UIコンポーネント
│   ├── forms/            # フォームコンポーネント
│   └── charts/           # チャート・グラフ
├── lib/                  # ユーティリティ
│   ├── api/              # API クライアント
│   ├── store/            # Zustand ストア
│   └── utils/            # 共通関数
└── types/                # TypeScript型定義
```

#### バックエンド構成
```
app/
├── api/                  # API エンドポイント
│   ├── v1/              # APIバージョン管理
│   │   ├── projects/    # プロジェクト関連API
│   │   ├── requirements/ # 要件定義API
│   │   └── knowledge/   # 知識ベースAPI
├── core/                # コア機能
│   ├── config/          # 設定管理
│   ├── database/        # DB接続・セッション
│   ├── security/        # 認証・認可
│   └── logging/         # ログ管理
├── models/              # データモデル
│   ├── database/        # SQLAlchemyモデル
│   └── schemas/         # Pydanticスキーマ
├── services/            # ビジネスロジック
│   ├── requirements/    # 要件定義サービス
│   ├── knowledge/       # 知識ベースサービス
│   └── generators/      # 自動生成エンジン
└── tests/               # テストコード
```

## 3. データモデル設計

### 3.1 コアエンティティ

#### プロジェクト管理
```sql
-- プロジェクト
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    erp_type VARCHAR(50) NOT NULL, -- 'Salesforce', 'SAP', 'Oracle', etc.
    business_domain VARCHAR(50) NOT NULL, -- 'Sales', 'Service', 'Marketing', etc.
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- プロジェクトメンバー
CREATE TABLE project_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id),
    user_id UUID NOT NULL,
    role VARCHAR(50) NOT NULL, -- 'admin', 'consultant', 'viewer'
    joined_at TIMESTAMP DEFAULT NOW()
);
```

#### 知識ベース
```sql
-- ERP機能マスタ
CREATE TABLE erp_functions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    erp_type VARCHAR(50) NOT NULL,
    module VARCHAR(50) NOT NULL,
    function_code VARCHAR(100) NOT NULL,
    function_name VARCHAR(255) NOT NULL,
    description TEXT,
    configuration_params JSONB,
    dependencies JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ヒアリング項目マスタ
CREATE TABLE hearing_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    erp_function_id UUID REFERENCES erp_functions(id),
    item_code VARCHAR(100) NOT NULL,
    question TEXT NOT NULL,
    answer_type VARCHAR(20) NOT NULL, -- 'text', 'select', 'checkbox'
    answer_options JSONB,
    is_required BOOLEAN DEFAULT false,
    display_order INTEGER DEFAULT 0
);
```

#### 要件定義データ
```sql
-- ヒアリング結果
CREATE TABLE hearing_responses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id),
    hearing_item_id UUID REFERENCES hearing_items(id),
    response_value JSONB NOT NULL,
    respondent_role VARCHAR(50),
    responded_at TIMESTAMP DEFAULT NOW()
);

-- セットアップ定義
CREATE TABLE setup_definitions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id),
    erp_function_id UUID REFERENCES erp_functions(id),
    parameter_name VARCHAR(255) NOT NULL,
    parameter_value JSONB NOT NULL,
    derivation_rule TEXT,
    status VARCHAR(20) DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT NOW()
);

-- GAP要件
CREATE TABLE gap_requirements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id),
    gap_type VARCHAR(50) NOT NULL, -- 'functional', 'technical', 'integration'
    gap_description TEXT NOT NULL,
    business_impact VARCHAR(20), -- 'high', 'medium', 'low'
    solution_approach JSONB,
    status VARCHAR(20) DEFAULT 'identified',
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 3.2 インデックス戦略

```sql
-- パフォーマンス最適化インデックス
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_erp_functions_type_module ON erp_functions(erp_type, module);
CREATE INDEX idx_hearing_responses_project ON hearing_responses(project_id);
CREATE INDEX idx_setup_definitions_project ON setup_definitions(project_id);

-- 全文検索インデックス
CREATE INDEX idx_erp_functions_search ON erp_functions 
USING gin(to_tsvector('japanese', function_name || ' ' || description));
```

## 4. API設計

### 4.1 RESTful API設計原則

#### URL構造
```
/api/v1/projects                    # プロジェクト一覧・作成
/api/v1/projects/{id}               # プロジェクト詳細・更新・削除
/api/v1/projects/{id}/hearings      # ヒアリング管理
/api/v1/projects/{id}/setup         # セットアップ定義
/api/v1/projects/{id}/gaps          # GAP要件

/api/v1/knowledge/erp-functions     # ERP機能マスタ
/api/v1/knowledge/hearing-items     # ヒアリング項目
/api/v1/generators/hearing-list     # ヒアリングリスト生成
/api/v1/generators/setup-definition # セットアップ定義生成
```

#### 標準レスポンス形式
```json
{
  "success": true,
  "data": {
    // 実際のデータ
  },
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  },
  "meta": {
    "timestamp": "2025-07-13T10:00:00Z",
    "version": "1.0"
  }
}
```

### 4.2 主要APIエンドポイント

#### ヒアリングリスト生成API
```python
@router.post("/generators/hearing-list")
async def generate_hearing_list(
    request: HearingListRequest,
    db: Session = Depends(get_db)
) -> HearingListResponse:
    """
    プロジェクトスコープに基づくヒアリングリスト自動生成
    """
    service = HearingGeneratorService(db)
    return await service.generate_hearing_list(
        erp_type=request.erp_type,
        business_modules=request.business_modules,
        business_requirements=request.business_requirements
    )
```

#### セットアップ定義生成API
```python
@router.post("/generators/setup-definition")
async def generate_setup_definition(
    project_id: UUID,
    request: SetupDefinitionRequest,
    db: Session = Depends(get_db)
) -> SetupDefinitionResponse:
    """
    ヒアリング結果に基づくセットアップ定義自動生成
    """
    service = SetupGeneratorService(db)
    return await service.generate_setup_definition(
        project_id=project_id,
        hearing_responses=request.hearing_responses
    )
```

## 5. セキュリティ設計

### 5.1 認証・認可

#### JWT認証
```python
# JWT設定
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60
JWT_REFRESH_EXPIRE_DAYS = 30

# 権限管理
class Permission(str, Enum):
    PROJECT_READ = "project:read"
    PROJECT_WRITE = "project:write"
    PROJECT_ADMIN = "project:admin"
    KNOWLEDGE_READ = "knowledge:read"
    KNOWLEDGE_WRITE = "knowledge:write"
```

#### ロールベースアクセス制御（RBAC）
```python
ROLE_PERMISSIONS = {
    "viewer": [
        Permission.PROJECT_READ,
        Permission.KNOWLEDGE_READ
    ],
    "consultant": [
        Permission.PROJECT_READ,
        Permission.PROJECT_WRITE,
        Permission.KNOWLEDGE_READ
    ],
    "admin": [
        Permission.PROJECT_ADMIN,
        Permission.KNOWLEDGE_WRITE
    ]
}
```

### 5.2 データ保護

#### 機密データ暗号化
- **保存時暗号化**: AES-256による機密フィールド暗号化
- **転送時暗号化**: TLS 1.3必須、HSTS有効化
- **バックアップ暗号化**: AWS S3/Azure Blob暗号化ストレージ

#### 個人情報保護
```python
# 個人情報マスキング
@dataclass
class PersonalInfo:
    email: str = field(metadata={"pii": True})
    name: str = field(metadata={"pii": True})
    
    def to_masked_dict(self) -> dict:
        return {
            "email": mask_email(self.email),
            "name": mask_name(self.name)
        }
```

## 6. 拡張性・運用設計

### 6.1 水平スケーリング

#### マイクロサービス分離点
```yaml
# Phase 2以降の分離計画
services:
  requirements-service:
    description: "要件定義・ヒアリング関連機能"
    database: "requirements_db"
    
  knowledge-service:
    description: "知識ベース・ERP機能マスタ"
    database: "knowledge_db"
    
  migration-service:
    description: "移行支援機能（Phase 2以降）"
    database: "migration_db"
    
  generator-service:
    description: "自動生成エンジン"
    database: "shared"
```

#### キャッシュ戦略
```python
# Redis キャッシュ設計
CACHE_KEYS = {
    "erp_functions": "erp_funcs:{erp_type}:{module}",  # TTL: 1時間
    "hearing_items": "hearing_items:{function_id}",   # TTL: 30分
    "user_sessions": "session:{user_id}",             # TTL: 60分
}
```

### 6.2 監視・ログ

#### ログ戦略
```python
# 構造化ログ
import structlog

logger = structlog.get_logger()

# 業務ログ
logger.info(
    "hearing_list_generated",
    project_id=project_id,
    erp_type=erp_type,
    module=module,
    item_count=len(hearing_items),
    generation_time_ms=elapsed_time
)
```

#### メトリクス監視
```yaml
# Prometheus メトリクス
custom_metrics:
  - hearing_list_generation_duration_seconds
  - setup_definition_generation_duration_seconds  
  - knowledge_base_search_duration_seconds
  - active_projects_total
  - gap_requirements_by_type
```

## 7. Phase 2+ 拡張アーキテクチャ

### 7.1 移行支援ツール統合

#### データ連携アーキテクチャ
```
要件定義DB ──→ Message Queue ──→ 移行支援DB
     │                              │
     └─── Event Sourcing ─────────── │
                                    │
移行マッピング ←─── API Gateway ←─────┘
自動生成
```

#### イベント駆動設計
```python
# イベント定義
class SetupDefinitionUpdated(BaseEvent):
    project_id: UUID
    function_id: UUID
    old_parameters: dict
    new_parameters: dict
    
# イベントハンドラ
async def handle_setup_definition_updated(
    event: SetupDefinitionUpdated
):
    # 移行マッピングの更新通知
    await migration_service.notify_parameter_change(
        project_id=event.project_id,
        changes=compare_parameters(
            event.old_parameters,
            event.new_parameters
        )
    )
```

### 7.2 AI/ML機能統合

#### 知識ベース拡張
```python
# ベクトル検索（Phase 3+）
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

class KnowledgeVectorStore:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = Chroma(
            embedding_function=self.embeddings
        )
    
    async def semantic_search(
        self, 
        query: str, 
        erp_type: str
    ) -> List[ERPFunction]:
        """セマンティック検索による機能推薦"""
        results = await self.vectorstore.similarity_search(
            query, 
            filter={"erp_type": erp_type}
        )
        return [self._to_erp_function(r) for r in results]
```

## 8. 関連文書

### プロジェクト管理
- [📋 プロジェクト全体構想](./project-overview.md)
- [🗓️ 開発ロードマップ](./development-roadmap.md)
- [📊 プロジェクト管理計画](./project-management-plan.md)
- [📝 作業記録](./work-log.md)

### 実装関連
- [Phase 1: MVP開発](../phase1/)
- [Phase 2: GAP分析拡張](../phase2/)
- [Phase 3: 業務領域拡張](../phase3/)
- [Phase 4: 移行ツール統合](../phase4/)
- [Phase 5: マルチERP対応](../phase5/)

### 参考資料
- [🏗️ プラットフォーム・ブループリント with Claude](./ERP導入支援プラットフォーム・ブループリントwithClaude.md)
- [🏗️ プラットフォーム・ブループリント with GPT](./ERP導入支援プラットフォーム・ブループリントwithGPT.md)

---
**最終更新**: 2025-07-13  
**文書バージョン**: 1.0  
**技術レビュー**: 実施待ち