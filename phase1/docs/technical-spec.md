# Phase 1 技術仕様書

## 1. 技術仕様概要

### 1.1 仕様書の目的・範囲

本文書は、ERPset Phase 1 MVPの技術仕様を詳細に定義し、開発チームが一貫した実装を行うための技術ガイドラインを提供します。

**対象範囲**:
- システムアーキテクチャ・コンポーネント設計
- フロントエンド・バックエンド技術仕様
- データモデル・API設計詳細
- Salesforce連携・知識ベース実装

**対象読者**:
- 開発チーム（フロントエンド・バックエンド・フルスタック）
- テックリード・アーキテクト
- QAエンジニア・DevOpsエンジニア

### 1.2 システム構成概要

#### アーキテクチャパターン
```
クライアント・サーバー・マイクロサービス準備アーキテクチャ

┌─────────────────────────────────────────────────────────┐
│                    Client Layer                        │
│  ┌─────────────────┐  ┌─────────────────────────────┐  │
│  │   Web Browser   │  │     Mobile (Future)        │  │
│  │  (Next.js SPA)  │  │                             │  │
│  └─────────────────┘  └─────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                              ↕ HTTPS/WSS
┌─────────────────────────────────────────────────────────┐
│                  Application Layer                     │
│  ┌─────────────────┐  ┌─────────────────────────────┐  │
│  │  Next.js SSR    │  │     FastAPI Service         │  │
│  │   (Frontend)    │  │      (Backend API)          │  │
│  └─────────────────┘  └─────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────┐
│                    Data Layer                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐   │
│  │ PostgreSQL  │ │   Redis     │ │   File Storage  │   │
│  │ (Primary)   │ │  (Cache)    │ │     (S3)        │   │
│  └─────────────┘ └─────────────┘ └─────────────────┘   │
└─────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────┐
│                External Services                       │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐   │
│  │ Salesforce  │ │    Auth0    │ │   Monitoring    │   │
│  │    APIs     │ │   (Future)  │ │   (DataDog)     │   │
│  └─────────────┘ └─────────────┘ └─────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

#### コンポーネント役割分担
```yaml
component_responsibilities:
  frontend_nextjs:
    role: "ユーザーインターフェース・体験"
    responsibilities:
      - "SPA・SSR・SEO最適化"
      - "状態管理・フォーム処理"
      - "API通信・エラーハンドリング"
      - "レスポンシブ・アクセシビリティ"
  
  backend_fastapi:
    role: "ビジネスロジック・データ処理"
    responsibilities:
      - "RESTful API・認証認可"
      - "ヒアリング生成・セットアップ定義ロジック"
      - "Salesforce API連携"
      - "知識ベース管理・検索"
  
  postgresql:
    role: "メインデータストア"
    responsibilities:
      - "ユーザー・プロジェクト・知識ベースデータ"
      - "ACID特性・トランザクション管理"
      - "全文検索・複雑クエリ"
  
  redis:
    role: "キャッシュ・セッション管理"
    responsibilities:
      - "API レスポンスキャッシュ"
      - "JWT セッション管理"
      - "一時データ・状態管理"
```

## 2. フロントエンド技術仕様

### 2.1 Next.js アプリケーション設計

#### プロジェクト構造
```
frontend/
├── src/
│   ├── app/                    # App Router (Next.js 13+)
│   │   ├── (auth)/            # 認証ルートグループ
│   │   │   ├── login/
│   │   │   └── register/
│   │   ├── dashboard/         # ダッシュボード
│   │   ├── projects/          # プロジェクト管理
│   │   │   ├── [id]/         # 動的ルート
│   │   │   └── new/
│   │   ├── knowledge/         # 知識ベース管理
│   │   ├── api/               # API Routes (サーバー関数)
│   │   ├── globals.css        # グローバルスタイル
│   │   ├── layout.tsx         # ルートレイアウト
│   │   └── page.tsx           # ホームページ
│   ├── components/            # UIコンポーネント
│   │   ├── ui/               # 基本UIコンポーネント
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Modal.tsx
│   │   │   └── Table.tsx
│   │   ├── forms/            # フォームコンポーネント
│   │   │   ├── ProjectForm.tsx
│   │   │   └── HearingForm.tsx
│   │   ├── layout/           # レイアウトコンポーネント
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Footer.tsx
│   │   └── domain/           # ドメイン固有コンポーネント
│   │       ├── ProjectCard.tsx
│   │       └── HearingList.tsx
│   ├── lib/                  # ユーティリティ・設定
│   │   ├── api.ts            # API クライアント
│   │   ├── auth.ts           # 認証ユーティリティ
│   │   ├── utils.ts          # 共通ユーティリティ
│   │   └── validations.ts    # バリデーションスキーマ
│   ├── hooks/                # カスタムReactフック
│   │   ├── useAuth.ts
│   │   ├── useProjects.ts
│   │   └── useHearing.ts
│   ├── store/                # Zustand状態管理
│   │   ├── authStore.ts
│   │   ├── projectStore.ts
│   │   └── uiStore.ts
│   └── types/                # TypeScript型定義
│       ├── api.ts
│       ├── auth.ts
│       └── project.ts
├── public/                   # 静的リソース
│   ├── images/
│   └── icons/
├── tests/                    # テストファイル
│   ├── __mocks__/
│   ├── components/
│   ├── pages/
│   └── e2e/
├── .env.local               # 環境変数
├── next.config.js          # Next.js設定
├── tailwind.config.js      # Tailwind CSS設定
├── package.json
└── README.md
```

#### 状態管理設計（Zustand）
```typescript
// src/store/authStore.ts
interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
}

// src/store/projectStore.ts
interface ProjectState {
  projects: Project[];
  currentProject: Project | null;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  fetchProjects: () => Promise<void>;
  createProject: (data: CreateProjectData) => Promise<void>;
  updateProject: (id: string, data: UpdateProjectData) => Promise<void>;
  deleteProject: (id: string) => Promise<void>;
  setCurrentProject: (project: Project) => void;
}

// src/store/hearingStore.ts
interface HearingState {
  hearingList: HearingItem[];
  responses: HearingResponse[];
  generationProgress: number;
  isGenerating: boolean;
  
  // Actions
  generateHearingList: (projectId: string, scope: ProjectScope) => Promise<void>;
  saveResponse: (itemId: string, response: any) => Promise<void>;
  submitAllResponses: (projectId: string) => Promise<void>;
}
```

#### API通信設計（TanStack Query）
```typescript
// src/lib/api.ts
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,        // 5分間フレッシュ
      cacheTime: 10 * 60 * 1000,       // 10分間キャッシュ
      retry: 3,
      retryDelay: attemptIndex => Math.min(1000 * 2 ** attemptIndex, 30000),
    },
  },
});

// API クライアント設計
class ApiClient {
  private baseURL: string;
  private authToken: string | null = null;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  setAuthToken(token: string) {
    this.authToken = token;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.authToken) {
      headers.Authorization = `Bearer ${this.authToken}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      throw new ApiError(response.status, await response.text());
    }

    return response.json();
  }

  // プロジェクト関連API
  async getProjects(): Promise<Project[]> {
    return this.request<Project[]>('/api/v1/projects');
  }

  async createProject(data: CreateProjectData): Promise<Project> {
    return this.request<Project>('/api/v1/projects', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // ヒアリング関連API
  async generateHearingList(
    projectId: string,
    scope: ProjectScope
  ): Promise<HearingListResponse> {
    return this.request<HearingListResponse>('/api/v1/hearing/generate', {
      method: 'POST',
      body: JSON.stringify({ projectId, scope }),
    });
  }
}
```

### 2.2 UIコンポーネント設計

#### デザインシステム
```typescript
// src/lib/design-system.ts
export const designTokens = {
  colors: {
    primary: {
      50: '#eff6ff',
      500: '#3b82f6',
      600: '#2563eb',
      700: '#1d4ed8',
    },
    gray: {
      50: '#f9fafb',
      100: '#f3f4f6',
      500: '#6b7280',
      900: '#111827',
    },
    semantic: {
      success: '#10b981',
      warning: '#f59e0b',
      error: '#ef4444',
      info: '#3b82f6',
    },
  },
  spacing: {
    xs: '0.25rem',   // 4px
    sm: '0.5rem',    // 8px
    md: '1rem',      // 16px
    lg: '1.5rem',    // 24px
    xl: '2rem',      // 32px
  },
  typography: {
    fontFamily: {
      sans: ['Inter', 'system-ui', 'sans-serif'],
      mono: ['JetBrains Mono', 'monospace'],
    },
    fontSize: {
      xs: '0.75rem',
      sm: '0.875rem',
      base: '1rem',
      lg: '1.125rem',
      xl: '1.25rem',
      '2xl': '1.5rem',
    },
  },
};

// 基本UIコンポーネント例
// src/components/ui/Button.tsx
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  leftIcon,
  rightIcon,
  children,
  className,
  disabled,
  ...props
}) => {
  const baseClasses = 'inline-flex items-center justify-center font-medium rounded-md transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none';
  
  const variantClasses = {
    primary: 'bg-primary text-primary-foreground hover:bg-primary/90',
    secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
    outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
    ghost: 'hover:bg-accent hover:text-accent-foreground',
  };
  
  const sizeClasses = {
    sm: 'h-9 px-3 text-sm',
    md: 'h-10 px-4 py-2',
    lg: 'h-11 px-8',
  };

  return (
    <button
      className={cn(
        baseClasses,
        variantClasses[variant],
        sizeClasses[size],
        className
      )}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
      {leftIcon && !isLoading && <span className="mr-2">{leftIcon}</span>}
      {children}
      {rightIcon && <span className="ml-2">{rightIcon}</span>}
    </button>
  );
};
```

#### フォーム処理設計
```typescript
// src/components/forms/ProjectForm.tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const projectSchema = z.object({
  name: z.string().min(1, '프로젝트명은 필수입니다').max(100),
  description: z.string().max(500).optional(),
  erpType: z.literal('salesforce'),
  businessDomain: z.enum(['sales', 'service', 'marketing']),
  scope: z.object({
    leadManagement: z.boolean(),
    opportunityManagement: z.boolean(),
    accountManagement: z.boolean(),
  }),
});

type ProjectFormData = z.infer<typeof projectSchema>;

export const ProjectForm: React.FC<ProjectFormProps> = ({ onSubmit }) => {
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors, isSubmitting },
  } = useForm<ProjectFormData>({
    resolver: zodResolver(projectSchema),
    defaultValues: {
      erpType: 'salesforce',
      businessDomain: 'sales',
      scope: {
        leadManagement: true,
        opportunityManagement: true,
        accountManagement: false,
      },
    },
  });

  const watchedScope = watch('scope');

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div>
        <Label htmlFor="name">프로젝트명 *</Label>
        <Input
          id="name"
          {...register('name')}
          error={errors.name?.message}
        />
      </div>

      <div>
        <Label htmlFor="description">설명</Label>
        <Textarea
          id="description"
          {...register('description')}
          error={errors.description?.message}
        />
      </div>

      <div>
        <Label>업무 범위</Label>
        <div className="space-y-2">
          <Checkbox
            {...register('scope.leadManagement')}
            label="리드 관리"
          />
          <Checkbox
            {...register('scope.opportunityManagement')}
            label="상담 관리"
          />
          <Checkbox
            {...register('scope.accountManagement')}
            label="거래처 관리"
          />
        </div>
      </div>

      <Button type="submit" isLoading={isSubmitting}>
        프로젝트 생성
      </Button>
    </form>
  );
};
```

## 3. バックエンド技術仕様

### 3.1 FastAPI アプリケーション設計

#### プロジェクト構造
```
backend/
├── app/
│   ├── api/                   # API エンドポイント
│   │   ├── deps.py           # 依存関係注入
│   │   ├── __init__.py
│   │   └── v1/               # APIバージョン1
│   │       ├── __init__.py
│   │       ├── auth.py       # 認証エンドポイント
│   │       ├── projects.py   # プロジェクト管理
│   │       ├── hearing.py    # ヒアリング機能
│   │       ├── knowledge.py  # 知識ベース
│   │       └── health.py     # ヘルスチェック
│   ├── core/                 # コア設定・ユーティリティ
│   │   ├── __init__.py
│   │   ├── config.py         # 設定管理
│   │   ├── database.py       # DB接続・セッション
│   │   ├── security.py       # JWT・パスワード暗号化
│   │   ├── logging.py        # ログ設定
│   │   └── exceptions.py     # カスタム例外
│   ├── models/               # データベースモデル
│   │   ├── __init__.py
│   │   ├── base.py          # ベースモデル
│   │   ├── user.py          # ユーザーモデル
│   │   ├── project.py       # プロジェクトモデル
│   │   ├── knowledge.py     # 知識ベースモデル
│   │   └── hearing.py       # ヒアリングモデル
│   ├── schemas/              # Pydanticスキーマ
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── hearing.py
│   │   └── knowledge.py
│   ├── services/             # ビジネスロジック
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── project_service.py
│   │   ├── hearing_generator.py
│   │   ├── setup_generator.py
│   │   └── salesforce_client.py
│   ├── utils/                # ユーティリティ
│   │   ├── __init__.py
│   │   ├── email.py
│   │   ├── file_utils.py
│   │   └── date_utils.py
│   └── main.py               # FastAPIアプリケーション
├── alembic/                  # データベースマイグレーション
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── tests/                    # テストファイル
│   ├── __init__.py
│   ├── conftest.py          # テスト設定・フィクスチャ
│   ├── test_api/
│   ├── test_services/
│   └── test_utils/
├── scripts/                  # 実行スクリプト
│   ├── setup_db.py
│   ├── seed_data.py
│   └── migrate.py
├── requirements.txt          # 依存関係
├── requirements-dev.txt      # 開発依存関係
├── alembic.ini              # Alembic設定
├── pyproject.toml           # プロジェクト設定
└── README.md
```

#### FastAPI アプリケーション設定
```python
# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import time
import logging

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.exceptions import CustomException
from app.api.v1 import auth, projects, hearing, knowledge, health

# ログ設定
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ERPset API",
    description="ERP導入支援プラットフォーム API",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# セキュリティ・ミドルウェア
if settings.TRUSTED_HOSTS:
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=settings.TRUSTED_HOSTS
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# カスタムミドルウェア
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response

# 例外ハンドラー
@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error_code": exc.error_code},
    )

# ルーター登録
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(hearing.router, prefix="/api/v1/hearing", tags=["hearing"])
app.include_router(knowledge.router, prefix="/api/v1/knowledge", tags=["knowledge"])

@app.on_event("startup")
async def startup_event():
    logger.info("ERPset API starting up...")
    # データベース接続確認
    # 外部サービス接続確認
    # キャッシュ初期化

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("ERPset API shutting down...")
    # リソースクリーンアップ
```

#### 設定管理
```python
# app/core/config.py
from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # アプリケーション設定
    APP_NAME: str = "ERPset"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    
    # データベース設定
    DATABASE_URL: str
    DATABASE_TEST_URL: Optional[str] = None
    
    # Redis設定
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT設定
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    JWT_REFRESH_EXPIRE_DAYS: int = 30
    
    # CORS設定
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    TRUSTED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    
    # Salesforce設定
    SALESFORCE_CLIENT_ID: str
    SALESFORCE_CLIENT_SECRET: str
    SALESFORCE_INSTANCE_URL: str = "https://test.salesforce.com"
    
    # ファイルアップロード設定
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_FOLDER: str = "uploads"
    
    # ログ設定
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # 外部サービス設定
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# グローバル設定インスタンス
settings = Settings()
```

### 3.2 ビジネスロジック設計

#### ヒアリング生成サービス
```python
# app/services/hearing_generator.py
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.knowledge import SalesforceFunction, HearingItem
from app.schemas.hearing import HearingListRequest, HearingListResponse
from app.services.salesforce_client import SalesforceClient
import logging

logger = logging.getLogger(__name__)

class HearingGeneratorService:
    def __init__(self, db: Session):
        self.db = db
        self.salesforce_client = SalesforceClient()

    async def generate_hearing_list(
        self, 
        request: HearingListRequest
    ) -> HearingListResponse:
        """
        プロジェクトスコープに基づいてヒアリングリストを自動生成
        """
        try:
            # 1. スコープに関連するSalesforce機能を抽出
            relevant_functions = await self._get_relevant_functions(
                request.business_modules,
                request.business_requirements
            )
            
            # 2. 機能毎のヒアリング項目を取得
            hearing_items = []
            for function in relevant_functions:
                items = await self._get_hearing_items_for_function(function.id)
                hearing_items.extend(items)
            
            # 3. 優先順位付け・重複排除
            prioritized_items = self._prioritize_and_deduplicate(hearing_items)
            
            # 4. カバレッジスコア計算
            coverage_score = self._calculate_coverage_score(
                request.business_requirements,
                prioritized_items
            )
            
            # 5. 生成理由・説明を付与
            generation_rationale = self._generate_rationale(
                relevant_functions,
                prioritized_items
            )
            
            logger.info(f"Generated {len(prioritized_items)} hearing items with coverage score {coverage_score}")
            
            return HearingListResponse(
                hearing_items=prioritized_items,
                coverage_score=coverage_score,
                total_items=len(prioritized_items),
                estimated_time_minutes=len(prioritized_items) * 2,  # 項目あたり2分想定
                generation_rationale=generation_rationale,
                success=True
            )
            
        except Exception as e:
            logger.error(f"Failed to generate hearing list: {str(e)}")
            raise HearingGenerationError(f"ヒアリングリスト生成に失敗しました: {str(e)}")

    async def _get_relevant_functions(
        self, 
        business_modules: List[str],
        business_requirements: List[str]
    ) -> List[SalesforceFunction]:
        """ビジネス要求に関連するSalesforce機能を抽出"""
        
        query = self.db.query(SalesforceFunction).filter(
            SalesforceFunction.module.in_(business_modules)
        )
        
        # ビジネス要求による絞り込み
        if business_requirements:
            requirement_filters = []
            for req in business_requirements:
                requirement_filters.append(
                    SalesforceFunction.keywords.contains(req)
                )
            query = query.filter(or_(*requirement_filters))
        
        functions = query.all()
        
        # 依存関係を考慮した機能追加
        additional_functions = await self._get_dependent_functions(functions)
        
        return functions + additional_functions

    async def _get_hearing_items_for_function(
        self, 
        function_id: str
    ) -> List[Dict[str, Any]]:
        """指定機能のヒアリング項目を取得"""
        
        items = self.db.query(HearingItem).filter(
            HearingItem.salesforce_function_id == function_id
        ).order_by(HearingItem.display_order).all()
        
        return [
            {
                "id": item.id,
                "function_id": item.salesforce_function_id,
                "question": item.question,
                "answer_type": item.answer_type,
                "answer_options": item.answer_options,
                "is_required": item.is_required,
                "category": item.category,
                "priority": item.priority,
                "estimated_time_minutes": item.estimated_time_minutes,
            }
            for item in items
        ]

    def _prioritize_and_deduplicate(
        self, 
        hearing_items: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """ヒアリング項目の優先順位付けと重複排除"""
        
        # 重複排除（質問内容の類似性チェック）
        unique_items = self._remove_duplicates(hearing_items)
        
        # 優先順位付け（必須項目・ビジネス影響度・実装容易性）
        prioritized = sorted(unique_items, key=lambda x: (
            -x.get("is_required", 0),      # 必須項目を優先
            -x.get("priority", 0),         # 優先度スコア
            x.get("estimated_time_minutes", 0)  # 所要時間の短い順
        ))
        
        return prioritized

    def _calculate_coverage_score(
        self, 
        business_requirements: List[str],
        hearing_items: List[Dict[str, Any]]
    ) -> float:
        """ビジネス要求に対するカバレッジスコア計算"""
        
        if not business_requirements:
            return 1.0
        
        covered_requirements = set()
        
        for item in hearing_items:
            # ヒアリング項目がカバーする要求を特定
            for req in business_requirements:
                if req.lower() in item.get("question", "").lower():
                    covered_requirements.add(req)
        
        coverage_score = len(covered_requirements) / len(business_requirements)
        return round(coverage_score, 3)
```

#### セットアップ定義生成サービス
```python
# app/services/setup_generator.py
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.hearing import HearingResponse
from app.schemas.setup import SetupDefinitionRequest, SetupDefinitionResponse
import logging

logger = logging.getLogger(__name__)

class SetupDefinitionGenerator:
    def __init__(self, db: Session):
        self.db = db

    async def generate_setup_definition(
        self,
        project_id: str,
        hearing_responses: List[Dict[str, Any]]
    ) -> SetupDefinitionResponse:
        """
        ヒアリング回答に基づいてSalesforceセットアップ定義を自動生成
        """
        try:
            # 1. プロジェクト情報取得
            project = self._get_project(project_id)
            
            # 2. ヒアリング回答を解析・構造化
            structured_responses = self._structure_responses(hearing_responses)
            
            # 3. Salesforce設定値を推論・生成
            salesforce_config = await self._generate_salesforce_config(
                project, 
                structured_responses
            )
            
            # 4. 設定値の妥当性検証
            validation_results = self._validate_configuration(salesforce_config)
            
            # 5. セットアップ定義書フォーマット生成
            setup_document = self._format_setup_document(
                project,
                salesforce_config,
                validation_results
            )
            
            # 6. GAP要件特定
            gap_requirements = await self._identify_gap_requirements(
                structured_responses,
                salesforce_config
            )
            
            logger.info(f"Generated setup definition for project {project_id}")
            
            return SetupDefinitionResponse(
                project_id=project_id,
                setup_document=setup_document,
                salesforce_configuration=salesforce_config,
                gap_requirements=gap_requirements,
                validation_results=validation_results,
                generated_at=datetime.utcnow(),
                success=True
            )
            
        except Exception as e:
            logger.error(f"Failed to generate setup definition: {str(e)}")
            raise SetupGenerationError(f"セットアップ定義生成に失敗しました: {str(e)}")

    async def _generate_salesforce_config(
        self,
        project: Project,
        responses: Dict[str, Any]
    ) -> Dict[str, Any]:
        """ヒアリング回答からSalesforce設定値を推論"""
        
        config = {
            "lead_management": self._generate_lead_config(responses),
            "opportunity_management": self._generate_opportunity_config(responses),
            "account_management": self._generate_account_config(responses),
            "workflow_automation": self._generate_workflow_config(responses),
            "data_validation": self._generate_validation_rules(responses),
        }
        
        return config

    def _generate_lead_config(self, responses: Dict[str, Any]) -> Dict[str, Any]:
        """Lead管理設定生成"""
        
        lead_config = {
            "lead_sources": [],
            "lead_statuses": [],
            "assignment_rules": [],
            "conversion_criteria": {},
        }
        
        # Lead Sourceの設定
        if "lead_sources" in responses:
            lead_config["lead_sources"] = [
                {
                    "name": source,
                    "is_active": True,
                    "default_rating": self._infer_rating(source)
                }
                for source in responses["lead_sources"]
            ]
        
        # Lead Statusの設定
        if "lead_process" in responses:
            statuses = responses["lead_process"].get("stages", [])
            lead_config["lead_statuses"] = [
                {
                    "name": status,
                    "sort_order": idx + 1,
                    "is_converted": status.lower() in ["qualified", "converted"]
                }
                for idx, status in enumerate(statuses)
            ]
        
        return lead_config
```

## 4. データベース設計詳細

### 4.1 データモデル設計

#### ベースモデル
```python
# app/models/base.py
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
```

### 4.2 パフォーマンス最適化

#### インデックス戦略
```sql
-- プロジェクト検索最適化
CREATE INDEX idx_projects_user_status ON projects(user_id, status);
CREATE INDEX idx_projects_created_at ON projects(created_at DESC);

-- 知識ベース検索最適化
CREATE INDEX idx_salesforce_functions_module ON salesforce_functions(module);
CREATE INDEX idx_salesforce_functions_keywords_gin ON salesforce_functions USING gin(keywords);

-- ヒアリング項目検索最適化
CREATE INDEX idx_hearing_items_function_id ON hearing_items(salesforce_function_id);
CREATE INDEX idx_hearing_items_category ON hearing_items(category);

-- 全文検索インデックス
CREATE INDEX idx_salesforce_functions_search ON salesforce_functions 
USING gin(to_tsvector('english', function_name || ' ' || description));
```

## 5. 関連文書・参照

### 5.1 Phase 1設計文書

- [📋 Phase 1概要](../README.md)
- [🌐 API設計書](./api-design.md)
- [🗄️ データベース設計書](./database-design.md)
- [⚡ Salesforce知識ベース設計](./salesforce-knowledge.md)
- [🚀 デプロイ・運用ガイド](./deployment-guide.md)

### 5.2 全体プロジェクト文書

- [📋 プロジェクト全体構想](../../docs/project-overview.md)
- [🏗️ 技術アーキテクチャ](../../docs/technical-architecture.md)
- [📝 機能要求仕様書](../../docs/functional-requirements.md)
- [⚙️ 非機能要求仕様書](../../docs/non-functional-requirements.md)
- [🧪 品質保証・テスト戦略](../../docs/quality-assurance.md)

### 5.3 開発・運用文書

- [🔧 環境構築ガイド](../../docs/setup-guide.md)
- [📊 プロジェクト管理計画](../../docs/project-management-plan.md)

### 5.4 外部技術参照

- [Next.js 13+ Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- [Salesforce REST API Documentation](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/)

---
**最終更新**: 2025-07-13  
**文書バージョン**: 1.0  
**技術責任者**: テックリード  
**次回レビュー**: 実装開始時（技術選定・アーキテクチャ確定）