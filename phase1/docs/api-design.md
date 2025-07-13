# Phase 1 API設計書

## 1. API設計概要

### 1.1 設計方針・原則

ERPset Phase 1 APIは、RESTful設計原則に基づき、直感的で拡張性の高いAPIを提供します。

#### 設計原則
```yaml
api_design_principles:
  restful_design:
    - "HTTPメソッドの適切な使用（GET・POST・PUT・DELETE）"
    - "リソース指向URL設計"
    - "ステートレス通信"
    
  consistency:
    - "命名規則・レスポンス形式の統一"
    - "エラーハンドリング・ステータスコードの統一"
    - "認証・認可方式の統一"
    
  developer_experience:
    - "自動生成API文書（Swagger UI）"
    - "明確なエラーメッセージ"
    - "バージョン管理・後方互換性"
    
  performance:
    - "ページネーション・フィルタリング対応"
    - "適切なキャッシュ設定"
    - "レスポンス時間2-5秒以内"
```

### 1.2 API構成概要

#### ベースURL・バージョニング
```yaml
api_structure:
  base_url: "https://api.erpset.com"
  version: "v1"
  full_path: "https://api.erpset.com/api/v1/"
  
  versioning_strategy:
    - "URLパスバージョニング（/api/v1/）"
    - "メジャーバージョンのみ（v1, v2, ...）"
    - "後方互換性6ヶ月間保証"
```

#### リソース概要
```yaml
api_resources:
  authentication:
    base_path: "/auth"
    description: "ユーザー認証・JWT管理"
    
  projects:
    base_path: "/projects"
    description: "プロジェクト管理・CRUD操作"
    
  hearing:
    base_path: "/hearing"
    description: "ヒアリング生成・回答管理"
    
  knowledge:
    base_path: "/knowledge"
    description: "Salesforce知識ベース管理"
    
  health:
    base_path: "/health"
    description: "システムヘルスチェック"
```

## 2. 認証・認可API

### 2.1 認証エンドポイント

#### POST /api/v1/auth/login
```yaml
endpoint: "POST /api/v1/auth/login"
description: "ユーザーログイン・JWT発行"
authentication: "不要"

request:
  content_type: "application/json"
  schema:
    type: "object"
    required: ["email", "password"]
    properties:
      email:
        type: "string"
        format: "email"
        example: "user@example.com"
      password:
        type: "string"
        minLength: 8
        example: "password123"

responses:
  200:
    description: "ログイン成功"
    schema:
      type: "object"
      properties:
        access_token:
          type: "string"
          description: "JWT アクセストークン"
          example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        refresh_token:
          type: "string"
          description: "リフレッシュトークン"
        token_type:
          type: "string"
          example: "Bearer"
        expires_in:
          type: "integer"
          description: "トークン有効期限（秒）"
          example: 3600
        user:
          $ref: "#/components/schemas/User"
  
  400:
    description: "バリデーションエラー"
    schema:
      $ref: "#/components/schemas/ValidationError"
  
  401:
    description: "認証失敗"
    schema:
      type: "object"
      properties:
        detail:
          type: "string"
          example: "メールアドレスまたはパスワードが正しくありません"
        error_code:
          type: "string"
          example: "INVALID_CREDENTIALS"
```

#### POST /api/v1/auth/refresh
```yaml
endpoint: "POST /api/v1/auth/refresh"
description: "アクセストークン更新"
authentication: "不要（リフレッシュトークン必要）"

request:
  content_type: "application/json"
  schema:
    type: "object"
    required: ["refresh_token"]
    properties:
      refresh_token:
        type: "string"
        description: "有効なリフレッシュトークン"

responses:
  200:
    description: "トークン更新成功"
    schema:
      type: "object"
      properties:
        access_token:
          type: "string"
        expires_in:
          type: "integer"
  
  401:
    description: "リフレッシュトークン無効"
    schema:
      type: "object"
      properties:
        detail:
          type: "string"
          example: "リフレッシュトークンが無効または期限切れです"
```

#### POST /api/v1/auth/logout
```yaml
endpoint: "POST /api/v1/auth/logout"
description: "ログアウト・トークン無効化"
authentication: "必要（JWT）"

responses:
  200:
    description: "ログアウト成功"
    schema:
      type: "object"
      properties:
        message:
          type: "string"
          example: "ログアウトしました"
```

### 2.2 ユーザー情報API

#### GET /api/v1/auth/me
```yaml
endpoint: "GET /api/v1/auth/me"
description: "現在のユーザー情報取得"
authentication: "必要（JWT）"

responses:
  200:
    description: "ユーザー情報取得成功"
    schema:
      $ref: "#/components/schemas/User"
```

## 3. プロジェクト管理API

### 3.1 プロジェクト一覧・詳細

#### GET /api/v1/projects
```yaml
endpoint: "GET /api/v1/projects"
description: "プロジェクト一覧取得"
authentication: "必要（JWT）"

parameters:
  query:
    - name: "page"
      type: "integer"
      default: 1
      description: "ページ番号"
    - name: "limit"
      type: "integer"
      default: 20
      maximum: 100
      description: "1ページあたりの件数"
    - name: "status"
      type: "string"
      enum: ["active", "completed", "archived"]
      description: "ステータスフィルタ"
    - name: "search"
      type: "string"
      description: "プロジェクト名・説明での検索"

responses:
  200:
    description: "プロジェクト一覧取得成功"
    schema:
      type: "object"
      properties:
        items:
          type: "array"
          items:
            $ref: "#/components/schemas/Project"
        pagination:
          $ref: "#/components/schemas/Pagination"
        total:
          type: "integer"
          description: "総件数"
```

#### GET /api/v1/projects/{project_id}
```yaml
endpoint: "GET /api/v1/projects/{project_id}"
description: "プロジェクト詳細取得"
authentication: "必要（JWT）"

parameters:
  path:
    - name: "project_id"
      type: "string"
      format: "uuid"
      required: true
      description: "プロジェクトID"

responses:
  200:
    description: "プロジェクト詳細取得成功"
    schema:
      $ref: "#/components/schemas/ProjectDetail"
  
  404:
    description: "プロジェクトが見つからない"
    schema:
      $ref: "#/components/schemas/NotFoundError"
```

### 3.2 プロジェクト作成・更新

#### POST /api/v1/projects
```yaml
endpoint: "POST /api/v1/projects"
description: "新規プロジェクト作成"
authentication: "必要（JWT）"

request:
  content_type: "application/json"
  schema:
    $ref: "#/components/schemas/CreateProjectRequest"

responses:
  201:
    description: "プロジェクト作成成功"
    schema:
      $ref: "#/components/schemas/Project"
    headers:
      Location:
        description: "作成されたプロジェクトのURL"
        schema:
          type: "string"
  
  400:
    description: "バリデーションエラー"
    schema:
      $ref: "#/components/schemas/ValidationError"
```

#### PUT /api/v1/projects/{project_id}
```yaml
endpoint: "PUT /api/v1/projects/{project_id}"
description: "プロジェクト更新"
authentication: "必要（JWT・プロジェクトアクセス権限）"

parameters:
  path:
    - name: "project_id"
      type: "string"
      format: "uuid"
      required: true

request:
  content_type: "application/json"
  schema:
    $ref: "#/components/schemas/UpdateProjectRequest"

responses:
  200:
    description: "プロジェクト更新成功"
    schema:
      $ref: "#/components/schemas/Project"
```

## 4. ヒアリング機能API

### 4.1 ヒアリングリスト生成

#### POST /api/v1/hearing/generate
```yaml
endpoint: "POST /api/v1/hearing/generate"
description: "ヒアリングリスト自動生成"
authentication: "必要（JWT）"

request:
  content_type: "application/json"
  schema:
    type: "object"
    required: ["project_id", "business_modules"]
    properties:
      project_id:
        type: "string"
        format: "uuid"
        description: "対象プロジェクトID"
      business_modules:
        type: "array"
        items:
          type: "string"
          enum: ["sales", "service", "marketing"]
        description: "対象業務モジュール"
        example: ["sales"]
      business_requirements:
        type: "array"
        items:
          type: "string"
        description: "具体的なビジネス要求"
        example: ["lead_management", "opportunity_tracking"]
      priority_focus:
        type: "string"
        enum: ["comprehensive", "essential", "quick"]
        default: "essential"
        description: "生成方針"

responses:
  200:
    description: "ヒアリングリスト生成成功"
    schema:
      type: "object"
      properties:
        request_id:
          type: "string"
          description: "生成リクエストID"
        hearing_items:
          type: "array"
          items:
            $ref: "#/components/schemas/HearingItem"
        coverage_score:
          type: "number"
          minimum: 0
          maximum: 1
          description: "要求カバレッジスコア"
          example: 0.85
        total_items:
          type: "integer"
          description: "総ヒアリング項目数"
        estimated_time_minutes:
          type: "integer"
          description: "予想所要時間（分）"
        generation_rationale:
          type: "string"
          description: "生成根拠・説明"
        metadata:
          type: "object"
          properties:
            salesforce_functions_used:
              type: "array"
              items:
                type: "string"
              description: "使用されたSalesforce機能一覧"
            generation_timestamp:
              type: "string"
              format: "date-time"
  
  400:
    description: "リクエストエラー"
    schema:
      $ref: "#/components/schemas/ValidationError"
  
  422:
    description: "生成処理エラー"
    schema:
      type: "object"
      properties:
        detail:
          type: "string"
          example: "指定された業務モジュールに対応する知識ベースが見つかりません"
        error_code:
          type: "string"
          example: "INSUFFICIENT_KNOWLEDGE_BASE"
```

### 4.2 ヒアリング回答管理

#### GET /api/v1/hearing/projects/{project_id}/responses
```yaml
endpoint: "GET /api/v1/hearing/projects/{project_id}/responses"
description: "プロジェクトのヒアリング回答一覧取得"
authentication: "必要（JWT・プロジェクトアクセス権限）"

parameters:
  path:
    - name: "project_id"
      type: "string"
      format: "uuid"
  query:
    - name: "status"
      type: "string"
      enum: ["pending", "completed", "all"]
      default: "all"

responses:
  200:
    description: "ヒアリング回答一覧取得成功"
    schema:
      type: "object"
      properties:
        project_id:
          type: "string"
        responses:
          type: "array"
          items:
            $ref: "#/components/schemas/HearingResponse"
        completion_rate:
          type: "number"
          description: "回答完了率"
          example: 0.75
        summary:
          type: "object"
          properties:
            total_items:
              type: "integer"
            completed_items:
              type: "integer"
            pending_items:
              type: "integer"
```

#### POST /api/v1/hearing/projects/{project_id}/responses
```yaml
endpoint: "POST /api/v1/hearing/projects/{project_id}/responses"
description: "ヒアリング回答保存・更新"
authentication: "必要（JWT・プロジェクトアクセス権限）"

request:
  content_type: "application/json"
  schema:
    type: "object"
    required: ["responses"]
    properties:
      responses:
        type: "array"
        items:
          type: "object"
          required: ["hearing_item_id", "response_value"]
          properties:
            hearing_item_id:
              type: "string"
              format: "uuid"
            response_value:
              oneOf:
                - type: "string"
                - type: "number"
                - type: "boolean"
                - type: "array"
                  items:
                    type: "string"
            comments:
              type: "string"
              description: "回答に関するコメント"
            confidence_level:
              type: "string"
              enum: ["high", "medium", "low"]
              description: "回答の確信度"

responses:
  200:
    description: "回答保存成功"
    schema:
      type: "object"
      properties:
        saved_count:
          type: "integer"
          description: "保存された回答数"
        completion_rate:
          type: "number"
          description: "更新後の完了率"
        validation_errors:
          type: "array"
          items:
            type: "object"
            properties:
              hearing_item_id:
                type: "string"
              error_message:
                type: "string"
```

## 5. セットアップ定義生成API

### 5.1 セットアップ定義生成

#### POST /api/v1/setup/generate
```yaml
endpoint: "POST /api/v1/setup/generate"
description: "セットアップ定義書自動生成"
authentication: "必要（JWT）"

request:
  content_type: "application/json"
  schema:
    type: "object"
    required: ["project_id"]
    properties:
      project_id:
        type: "string"
        format: "uuid"
      generation_options:
        type: "object"
        properties:
          include_validation_rules:
            type: "boolean"
            default: true
          include_workflow_automation:
            type: "boolean"
            default: true
          output_formats:
            type: "array"
            items:
              type: "string"
              enum: ["json", "excel", "pdf"]
            default: ["json"]

responses:
  200:
    description: "セットアップ定義生成成功"
    schema:
      type: "object"
      properties:
        project_id:
          type: "string"
        setup_definition:
          type: "object"
          description: "生成されたセットアップ定義"
          properties:
            lead_management:
              $ref: "#/components/schemas/LeadSetupConfig"
            opportunity_management:
              $ref: "#/components/schemas/OpportunitySetupConfig"
            account_management:
              $ref: "#/components/schemas/AccountSetupConfig"
            data_validation:
              $ref: "#/components/schemas/ValidationRulesConfig"
            workflow_automation:
              $ref: "#/components/schemas/WorkflowConfig"
        gap_analysis:
          type: "object"
          properties:
            identified_gaps:
              type: "array"
              items:
                $ref: "#/components/schemas/GapRequirement"
            gap_summary:
              type: "object"
              properties:
                total_gaps:
                  type: "integer"
                critical_gaps:
                  type: "integer"
                recommended_solutions:
                  type: "array"
                  items:
                    type: "string"
        export_urls:
          type: "object"
          properties:
            excel_download:
              type: "string"
              format: "uri"
            pdf_download:
              type: "string"
              format: "uri"
        metadata:
          type: "object"
          properties:
            generated_at:
              type: "string"
              format: "date-time"
            generation_duration_seconds:
              type: "number"
            data_quality_score:
              type: "number"
              minimum: 0
              maximum: 1
```

## 6. 知識ベース管理API

### 6.1 Salesforce機能検索

#### GET /api/v1/knowledge/salesforce/functions
```yaml
endpoint: "GET /api/v1/knowledge/salesforce/functions"
description: "Salesforce機能検索"
authentication: "必要（JWT）"

parameters:
  query:
    - name: "module"
      type: "string"
      enum: ["sales", "service", "marketing", "analytics"]
      description: "業務モジュールフィルタ"
    - name: "search"
      type: "string"
      description: "機能名・説明での検索"
    - name: "tags"
      type: "array"
      items:
        type: "string"
      description: "タグフィルタ"
    - name: "page"
      type: "integer"
      default: 1
    - name: "limit"
      type: "integer"
      default: 20

responses:
  200:
    description: "機能検索成功"
    schema:
      type: "object"
      properties:
        functions:
          type: "array"
          items:
            $ref: "#/components/schemas/SalesforceFunction"
        pagination:
          $ref: "#/components/schemas/Pagination"
        search_metadata:
          type: "object"
          properties:
            query:
              type: "string"
            total_results:
              type: "integer"
            search_time_ms:
              type: "number"
```

#### GET /api/v1/knowledge/salesforce/functions/{function_id}
```yaml
endpoint: "GET /api/v1/knowledge/salesforce/functions/{function_id}"
description: "Salesforce機能詳細取得"
authentication: "必要（JWT）"

parameters:
  path:
    - name: "function_id"
      type: "string"
      format: "uuid"

responses:
  200:
    description: "機能詳細取得成功"
    schema:
      allOf:
        - $ref: "#/components/schemas/SalesforceFunction"
        - type: "object"
          properties:
            configuration_details:
              type: "object"
              description: "詳細設定情報"
            related_functions:
              type: "array"
              items:
                $ref: "#/components/schemas/SalesforceFunction"
            hearing_items:
              type: "array"
              items:
                $ref: "#/components/schemas/HearingItem"
```

## 7. ファイル管理API

### 7.1 ドキュメント出力・ダウンロード

#### GET /api/v1/files/exports/{export_id}
```yaml
endpoint: "GET /api/v1/files/exports/{export_id}"
description: "生成済みファイルダウンロード"
authentication: "必要（JWT）"

parameters:
  path:
    - name: "export_id"
      type: "string"
      format: "uuid"
      description: "エクスポートファイルID"

responses:
  200:
    description: "ファイルダウンロード成功"
    content:
      application/vnd.openxmlformats-officedocument.spreadsheetml.sheet:
        schema:
          type: "string"
          format: "binary"
      application/pdf:
        schema:
          type: "string"
          format: "binary"
    headers:
      Content-Disposition:
        description: "ファイル名設定"
        schema:
          type: "string"
          example: "attachment; filename=\"setup-definition-20250713.xlsx\""
  
  404:
    description: "ファイルが見つからない・期限切れ"
    schema:
      $ref: "#/components/schemas/NotFoundError"
```

## 8. システム管理API

### 8.1 ヘルスチェック

#### GET /health
```yaml
endpoint: "GET /health"
description: "システムヘルスチェック"
authentication: "不要"

responses:
  200:
    description: "システム正常"
    schema:
      type: "object"
      properties:
        status:
          type: "string"
          example: "healthy"
        timestamp:
          type: "string"
          format: "date-time"
        version:
          type: "string"
          example: "1.0.0"
        checks:
          type: "object"
          properties:
            database:
              type: "object"
              properties:
                status:
                  type: "string"
                  example: "healthy"
                response_time_ms:
                  type: "number"
            redis:
              type: "object"
              properties:
                status:
                  type: "string"
                  example: "healthy"
            salesforce_api:
              type: "object"
              properties:
                status:
                  type: "string"
                  example: "healthy"
```

#### GET /health/detailed
```yaml
endpoint: "GET /health/detailed"
description: "詳細ヘルスチェック"
authentication: "必要（管理者権限）"

responses:
  200:
    description: "詳細ヘルス情報"
    schema:
      type: "object"
      properties:
        system_info:
          type: "object"
          properties:
            uptime_seconds:
              type: "number"
            memory_usage:
              type: "object"
            cpu_usage:
              type: "number"
        dependencies:
          type: "object"
          properties:
            database:
              type: "object"
              properties:
                connection_pool:
                  type: "object"
                query_performance:
                  type: "object"
            external_apis:
              type: "object"
              properties:
                salesforce:
                  type: "object"
                  properties:
                    api_limits:
                      type: "object"
                    last_successful_call:
                      type: "string"
                      format: "date-time"
```

## 9. データスキーマ定義

### 9.1 共通スキーマ

#### User
```yaml
User:
  type: "object"
  properties:
    id:
      type: "string"
      format: "uuid"
    email:
      type: "string"
      format: "email"
    name:
      type: "string"
    role:
      type: "string"
      enum: ["admin", "consultant", "viewer"]
    is_active:
      type: "boolean"
    created_at:
      type: "string"
      format: "date-time"
    last_login_at:
      type: "string"
      format: "date-time"
      nullable: true
```

#### Project
```yaml
Project:
  type: "object"
  properties:
    id:
      type: "string"
      format: "uuid"
    name:
      type: "string"
      maxLength: 100
    description:
      type: "string"
      maxLength: 500
      nullable: true
    erp_type:
      type: "string"
      enum: ["salesforce"]
    business_domain:
      type: "string"
      enum: ["sales", "service", "marketing"]
    scope:
      type: "object"
      properties:
        lead_management:
          type: "boolean"
        opportunity_management:
          type: "boolean"
        account_management:
          type: "boolean"
    status:
      type: "string"
      enum: ["active", "completed", "archived"]
    owner_id:
      type: "string"
      format: "uuid"
    created_at:
      type: "string"
      format: "date-time"
    updated_at:
      type: "string"
      format: "date-time"
```

#### HearingItem
```yaml
HearingItem:
  type: "object"
  properties:
    id:
      type: "string"
      format: "uuid"
    salesforce_function_id:
      type: "string"
      format: "uuid"
    question:
      type: "string"
      description: "ヒアリング質問文"
    answer_type:
      type: "string"
      enum: ["text", "select", "multiselect", "number", "boolean", "date"]
    answer_options:
      type: "array"
      items:
        type: "string"
      nullable: true
      description: "選択肢（select・multiselectの場合）"
    is_required:
      type: "boolean"
    category:
      type: "string"
      description: "質問カテゴリ"
    priority:
      type: "integer"
      minimum: 1
      maximum: 5
      description: "優先度（1=低、5=高）"
    estimated_time_minutes:
      type: "integer"
      description: "予想回答時間（分）"
    help_text:
      type: "string"
      nullable: true
      description: "回答補助説明"
```

### 9.2 リクエスト・レスポンススキーマ

#### CreateProjectRequest
```yaml
CreateProjectRequest:
  type: "object"
  required: ["name", "erp_type", "business_domain", "scope"]
  properties:
    name:
      type: "string"
      minLength: 1
      maxLength: 100
      description: "プロジェクト名"
    description:
      type: "string"
      maxLength: 500
      description: "プロジェクト説明"
    erp_type:
      type: "string"
      enum: ["salesforce"]
      description: "対象ERP"
    business_domain:
      type: "string"
      enum: ["sales", "service", "marketing"]
      description: "主要業務領域"
    scope:
      type: "object"
      required: ["lead_management", "opportunity_management"]
      properties:
        lead_management:
          type: "boolean"
          description: "リード管理機能"
        opportunity_management:
          type: "boolean"
          description: "商談管理機能"
        account_management:
          type: "boolean"
          description: "取引先管理機能"
```

#### Pagination
```yaml
Pagination:
  type: "object"
  properties:
    page:
      type: "integer"
      minimum: 1
      description: "現在のページ番号"
    limit:
      type: "integer"
      minimum: 1
      maximum: 100
      description: "1ページあたりの件数"
    total_pages:
      type: "integer"
      description: "総ページ数"
    has_next:
      type: "boolean"
      description: "次のページが存在するか"
    has_previous:
      type: "boolean"
      description: "前のページが存在するか"
```

#### ValidationError
```yaml
ValidationError:
  type: "object"
  properties:
    detail:
      type: "string"
      description: "エラーメッセージ"
    validation_errors:
      type: "array"
      items:
        type: "object"
        properties:
          field:
            type: "string"
            description: "エラーが発生したフィールド"
          message:
            type: "string"
            description: "フィールド固有のエラーメッセージ"
          code:
            type: "string"
            description: "エラーコード"
```

## 10. エラーハンドリング・ステータスコード

### 10.1 HTTPステータスコード使用指針

```yaml
status_codes:
  2xx_success:
    200: "リクエスト成功・レスポンスボディあり"
    201: "リソース作成成功・Locationヘッダー含む"
    204: "処理成功・レスポンスボディなし"
  
  4xx_client_errors:
    400: "リクエスト形式エラー・バリデーションエラー"
    401: "認証失敗・トークン無効"
    403: "認可失敗・権限不足"
    404: "リソースが見つからない"
    409: "リソース競合（重複作成等）"
    422: "セマンティックエラー（ビジネスルール違反）"
    429: "レート制限超過"
  
  5xx_server_errors:
    500: "サーバー内部エラー"
    502: "外部サービス接続エラー"
    503: "サービス一時停止・メンテナンス中"
```

### 10.2 エラーレスポンス形式

#### 標準エラーレスポンス
```json
{
  "detail": "エラーの詳細説明",
  "error_code": "ERROR_CODE",
  "timestamp": "2025-07-13T10:00:00Z",
  "path": "/api/v1/projects",
  "request_id": "req-123456789"
}
```

#### バリデーションエラーレスポンス
```json
{
  "detail": "入力データにエラーがあります",
  "error_code": "VALIDATION_ERROR",
  "validation_errors": [
    {
      "field": "name",
      "message": "プロジェクト名は必須です",
      "code": "REQUIRED"
    },
    {
      "field": "email",
      "message": "有効なメールアドレスを入力してください",
      "code": "INVALID_FORMAT"
    }
  ],
  "timestamp": "2025-07-13T10:00:00Z"
}
```

## 11. API認証・セキュリティ

### 11.1 JWT認証仕様

#### JWTペイロード構造
```json
{
  "sub": "user-uuid",
  "email": "user@example.com",
  "role": "consultant",
  "iat": 1626123456,
  "exp": 1626127056,
  "jti": "jwt-id"
}
```

#### 認証ヘッダー形式
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 11.2 レート制限

```yaml
rate_limiting:
  global:
    requests_per_minute: 100
    burst_limit: 20
  
  endpoint_specific:
    auth_login:
      requests_per_minute: 5
      description: "ブルートフォース攻撃防止"
    
    hearing_generation:
      requests_per_minute: 10
      description: "重い処理の制限"
    
    file_download:
      requests_per_minute: 30
      description: "帯域幅制限"
```

## 12. API使用例・サンプルコード

### 12.1 認証フロー例

```javascript
// ログイン
const loginResponse = await fetch('/api/v1/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'consultant@example.com',
    password: 'password123'
  })
});

const { access_token, user } = await loginResponse.json();

// 認証が必要なAPIリクエスト
const projectsResponse = await fetch('/api/v1/projects', {
  headers: {
    'Authorization': `Bearer ${access_token}`,
    'Content-Type': 'application/json'
  }
});

const projects = await projectsResponse.json();
```

### 12.2 プロジェクト作成からヒアリング生成まで

```javascript
// 1. プロジェクト作成
const newProject = await fetch('/api/v1/projects', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'ABC商事 Salesforce導入',
    description: '営業効率化を目的としたSalesforce Sales Cloud導入',
    erp_type: 'salesforce',
    business_domain: 'sales',
    scope: {
      lead_management: true,
      opportunity_management: true,
      account_management: false
    }
  })
});

const project = await newProject.json();

// 2. ヒアリングリスト生成
const hearingResponse = await fetch('/api/v1/hearing/generate', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    project_id: project.id,
    business_modules: ['sales'],
    business_requirements: [
      'lead_management', 
      'opportunity_tracking',
      'sales_forecasting'
    ],
    priority_focus: 'essential'
  })
});

const hearingList = await hearingResponse.json();
console.log(`${hearingList.total_items}項目のヒアリングリストを生成`);
```

## 13. 関連文書・参照

### 13.1 Phase 1設計文書

- [🔧 技術仕様書](./technical-spec.md)
- [🗄️ データベース設計書](./database-design.md)
- [⚡ Salesforce知識ベース設計](./salesforce-knowledge.md)
- [🚀 デプロイ・運用ガイド](./deployment-guide.md)

### 13.2 全体プロジェクト文書

- [📋 プロジェクト全体構想](../../docs/project-overview.md)
- [📝 機能要求仕様書](../../docs/functional-requirements.md)
- [⚙️ 非機能要求仕様書](../../docs/non-functional-requirements.md)

### 13.3 外部API参照

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAPI 3.0 Specification](https://swagger.io/specification/)
- [Salesforce REST API Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/)

---
**最終更新**: 2025-07-13  
**文書バージョン**: 1.0  
**API責任者**: バックエンドリード  
**次回レビュー**: API実装開始時（エンドポイント仕様確定）