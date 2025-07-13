# ERPset 環境構築ガイド

## 1. 環境構築概要

### 1.1 目的・対象読者

本ガイドは、ERPsetプラットフォームの開発環境・ステージング環境・本番環境の構築手順を提供します。

**対象読者**:
- 開発者・エンジニア（新規参加メンバー）
- DevOps・インフラエンジニア
- QAエンジニア（テスト環境構築）

### 1.2 環境構成

```
環境階層:
├── ローカル開発環境（個人PC）
├── 開発環境（Development）
├── ステージング環境（Staging）
└── 本番環境（Production）
```

### 1.3 前提条件・必要ツール

#### 必須ソフトウェア
```yaml
required_tools:
  runtime:
    node: "v18.17.0以降（推奨: v20.x）"
    python: "v3.9以降（推奨: v3.11）"
    docker: "v24.0以降"
    docker_compose: "v2.20以降"
    
  development:
    git: "v2.34以降"
    yarn: "v1.22以降（package manager）"
    vscode: "推奨IDE（拡張機能設定含む）"
    
  optional:
    aws_cli: "v2.13以降（本番デプロイ用）"
    terraform: "v1.5以降（インフラ管理）"
    kubectl: "v1.27以降（Kubernetes管理）"
```

#### システム要件
```yaml
system_requirements:
  minimum:
    cpu: "4コア以上"
    memory: "8GB以上"
    storage: "20GB以上の空き容量"
    
  recommended:
    cpu: "8コア以上"
    memory: "16GB以上"
    storage: "50GB以上のSSD"
    
  network:
    internet: "ブロードバンド接続"
    ports: "3000, 8000, 5432, 6379（ローカル開発用）"
```

## 2. ローカル開発環境構築

### 2.1 リポジトリクローン・初期設定

#### Git設定・リポジトリクローン
```bash
# 1. リポジトリクローン
git clone https://github.com/YOUR_ORG/ERPset.git
cd ERPset

# 2. 開発ブランチに切り替え
git checkout test-phasing

# 3. Git設定確認
git config user.name "Your Name"
git config user.email "your.email@company.com"
```

#### プロジェクト構造確認
```bash
# プロジェクト構造表示
tree -L 2 .

# 期待される構造:
# ERPset/
# ├── docs/                   # プロジェクト文書
# ├── phase1/                 # MVP開発
# ├── phase2/                 # GAP分析拡張
# ├── phase3/                 # 業務領域拡張
# ├── phase4/                 # 移行ツール統合
# ├── phase5/                 # マルチERP対応
# ├── legacy-tool/            # 既存ツール保管
# ├── docker-compose.yml      # 開発環境設定
# ├── README.md              # プロジェクト概要
# └── package.json           # 依存関係定義
```

### 2.2 Node.js・Python環境設定

#### Node.js環境構築
```bash
# 1. Node.jsバージョン確認
node --version  # v18.17.0以降
npm --version   # v9.0.0以降

# 2. Yarnインストール（未インストールの場合）
npm install -g yarn

# 3. フロントエンド依存関係インストール
cd phase1/frontend
yarn install

# 4. 開発サーバー起動確認
yarn dev
# http://localhost:3000 でアクセス確認
```

#### Python環境構築
```bash
# 1. Pythonバージョン確認
python3 --version  # v3.9以降

# 2. 仮想環境作成・有効化
cd phase1/backend
python3 -m venv venv

# macOS/Linux:
source venv/bin/activate

# Windows:
# venv\Scripts\activate

# 3. 依存関係インストール
pip install -r requirements.txt

# 4. 開発サーバー起動確認
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# http://localhost:8000/docs でSwagger UI確認
```

### 2.3 データベース・Redis環境

#### Docker Compose環境構築
```bash
# 1. プロジェクトルートに移動
cd ERPset

# 2. 環境変数ファイル作成
cp .env.example .env.local
# .env.localを編集（後述の設定例参照）

# 3. Docker Compose起動
docker-compose -f docker-compose.local.yml up -d

# 4. サービス確認
docker-compose ps

# 期待される出力:
# NAME                    STATUS              PORTS
# erpset-postgres-1       Up 2 minutes        0.0.0.0:5432->5432/tcp
# erpset-redis-1          Up 2 minutes        0.0.0.0:6379->6379/tcp
```

#### データベース初期化・マイグレーション
```bash
# 1. データベース接続確認
psql -h localhost -p 5432 -U erpset_user -d erpset_db
# パスワード: development_password

# 2. Alembicマイグレーション実行
cd phase1/backend
alembic upgrade head

# 3. 初期データ投入
python scripts/seed_data.py

# 4. 接続テスト
python scripts/test_connection.py
```

### 2.4 環境変数設定

#### .env.local設定例
```bash
# アプリケーション設定
APP_NAME=ERPset
APP_VERSION=1.0.0
ENVIRONMENT=local
DEBUG=true

# データベース設定
DATABASE_URL=postgresql://erpset_user:development_password@localhost:5432/erpset_db
DATABASE_TEST_URL=postgresql://erpset_user:development_password@localhost:5432/erpset_test_db

# Redis設定
REDIS_URL=redis://localhost:6379/0

# JWT認証設定
JWT_SECRET_KEY=your-super-secret-jwt-key-for-development
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

# フロントエンド設定
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_ENV=local

# Salesforce連携設定（開発用）
SALESFORCE_CLIENT_ID=your_dev_client_id
SALESFORCE_CLIENT_SECRET=your_dev_client_secret
SALESFORCE_INSTANCE_URL=https://test.salesforce.com

# ログ設定
LOG_LEVEL=DEBUG
LOG_FORMAT=json
```

### 2.5 VS Code環境設定

#### 推奨拡張機能
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.flake8",
    "ms-python.black-formatter",
    "bradlc.vscode-tailwindcss",
    "ms-vscode.vscode-typescript-next",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-eslint",
    "ms-vscode-remote.remote-containers",
    "ms-vscode.vscode-docker"
  ]
}
```

#### Workspace設定
```json
{
  "python.defaultInterpreterPath": "./phase1/backend/venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "editor.formatOnSave": true,
  "eslint.workingDirectories": ["phase1/frontend"],
  "typescript.preferences.includePackageJsonAutoImports": "auto"
}
```

## 3. 開発ワークフロー

### 3.1 日常的な開発手順

#### 開発開始手順
```bash
# 1. 最新コードの取得
git pull origin test-phasing

# 2. 新機能ブランチ作成
git checkout -b feature/US-01-01-project-creation

# 3. 開発環境起動
# Terminal 1: データベース・Redis
docker-compose -f docker-compose.local.yml up

# Terminal 2: バックエンド
cd phase1/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 3: フロントエンド
cd phase1/frontend
yarn dev

# 4. 開発作業・動作確認
# http://localhost:3000 でフロントエンド確認
# http://localhost:8000/docs でAPI確認
```

#### コード品質チェック
```bash
# フロントエンド品質チェック
cd phase1/frontend
yarn lint          # ESLint実行
yarn type-check    # TypeScript型チェック
yarn test          # Jest単体テスト
yarn test:e2e      # Playwright E2Eテスト

# バックエンド品質チェック
cd phase1/backend
black .                    # コードフォーマット
flake8 .                  # Linter実行
pytest                    # 単体テスト
pytest --cov=app          # カバレッジ付きテスト
```

#### コミット・プッシュ手順
```bash
# 1. 変更ファイル確認
git status
git diff

# 2. テスト実行・品質チェック
# （上記の品質チェックコマンド実行）

# 3. ステージング・コミット
git add .
git commit -m "feat: implement project creation UI (US-01-01)

- Add project creation form with validation
- Implement project API endpoints
- Add unit tests for project service
- Update documentation"

# 4. プッシュ・プルリクエスト作成
git push origin feature/US-01-01-project-creation
# GitHub/GitLabでPR作成
```

### 3.2 データベース管理

#### マイグレーション管理
```bash
# 新しいマイグレーション作成
cd phase1/backend
alembic revision --autogenerate -m "Add project table"

# マイグレーション実行
alembic upgrade head

# マイグレーション履歴確認
alembic history

# マイグレーション取り消し
alembic downgrade -1
```

#### テストデータ管理
```bash
# テストデータリセット・再投入
cd phase1/backend
python scripts/reset_test_data.py

# 特定のテストデータ投入
python scripts/seed_projects.py
python scripts/seed_knowledge_base.py

# データベースバックアップ（開発用）
pg_dump -h localhost -p 5432 -U erpset_user erpset_db > backup_$(date +%Y%m%d).sql
```

### 3.3 トラブルシューティング

#### よくある問題・解決策

##### ポート競合エラー
```bash
# Error: Port 3000 is already in use

# 1. 使用中のプロセス確認
lsof -i :3000
netstat -tulpn | grep :3000

# 2. プロセス終了
kill -9 <PID>

# 3. 別ポート使用
yarn dev --port 3001
```

##### データベース接続エラー
```bash
# Error: could not connect to server

# 1. Docker Compose状態確認
docker-compose ps

# 2. PostgreSQLコンテナ再起動
docker-compose restart postgres

# 3. ログ確認
docker-compose logs postgres

# 4. 接続設定確認
cat .env.local | grep DATABASE
```

##### 依存関係エラー
```bash
# Error: Module not found

# Node.js依存関係再インストール
cd phase1/frontend
rm -rf node_modules yarn.lock
yarn install

# Python依存関係再インストール
cd phase1/backend
pip install --force-reinstall -r requirements.txt
```

## 4. ステージング環境

### 4.1 ステージング環境概要

#### 環境目的・用途
```yaml
staging_purpose:
  integration_testing: "フロントエンド・バックエンド統合テスト"
  user_acceptance: "ステークホルダー・ユーザー受入テスト"
  performance_testing: "負荷テスト・性能検証"
  release_validation: "本番リリース前の最終検証"
```

#### インフラ構成
```yaml
staging_infrastructure:
  cloud_provider: "AWS"
  compute: "ECS Fargate（コンテナ）"
  database: "RDS PostgreSQL（db.t3.medium）"
  cache: "ElastiCache Redis（cache.t3.micro）"
  storage: "S3（ドキュメント・ログ保存）"
  monitoring: "CloudWatch・DataDog"
```

### 4.2 ステージング環境デプロイ

#### CI/CDパイプライン
```yaml
ci_cd_pipeline:
  trigger: "test-phasing ブランチへのプッシュ"
  steps:
    1: "コード品質チェック（Lint・Test・Security Scan）"
    2: "Dockerイメージビルド・ECRプッシュ"
    3: "ECSサービス更新・デプロイ"
    4: "ヘルスチェック・スモークテスト"
    5: "Slack通知・デプロイ完了"
```

#### 手動デプロイ手順
```bash
# 1. AWS CLI設定確認
aws configure list
aws sts get-caller-identity

# 2. Dockerイメージビルド
cd ERPset
docker build -t erpset-frontend:staging phase1/frontend/
docker build -t erpset-backend:staging phase1/backend/

# 3. ECRログイン・イメージプッシュ
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.ap-northeast-1.amazonaws.com

docker tag erpset-frontend:staging <ACCOUNT_ID>.dkr.ecr.ap-northeast-1.amazonaws.com/erpset-frontend:staging
docker push <ACCOUNT_ID>.dkr.ecr.ap-northeast-1.amazonaws.com/erpset-frontend:staging

# 4. ECSサービス更新
aws ecs update-service --cluster erpset-staging --service erpset-frontend --force-new-deployment
aws ecs update-service --cluster erpset-staging --service erpset-backend --force-new-deployment

# 5. デプロイ確認
curl -f https://staging.erpset.com/health
```

### 4.3 ステージング環境接続・確認

#### アクセス情報
```yaml
staging_access:
  frontend_url: "https://staging.erpset.com"
  api_url: "https://api-staging.erpset.com"
  api_docs: "https://api-staging.erpset.com/docs"
  
  test_accounts:
    admin: "admin@erpset.com / staging_password_123"
    consultant: "consultant@erpset.com / staging_password_123"
    viewer: "viewer@erpset.com / staging_password_123"
```

#### 動作確認手順
```bash
# 1. ヘルスチェック
curl https://api-staging.erpset.com/health

# 2. 認証API確認
curl -X POST https://api-staging.erpset.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@erpset.com", "password": "staging_password_123"}'

# 3. 知識ベースAPI確認
curl -H "Authorization: Bearer <TOKEN>" \
  https://api-staging.erpset.com/api/v1/knowledge/salesforce-functions

# 4. フロントエンド確認
# ブラウザで https://staging.erpset.com にアクセス
# ログイン・基本操作確認
```

## 5. 本番環境

### 5.1 本番環境概要

#### インフラ構成
```yaml
production_infrastructure:
  availability: "マルチAZ・高可用性構成"
  compute: "ECS Fargate（Auto Scaling）"
  database: "RDS PostgreSQL（Multi-AZ・暗号化）"
  cache: "ElastiCache Redis（Cluster Mode）"
  cdn: "CloudFront（静的コンテンツ配信）"
  security: "WAF・Certificate Manager・Secrets Manager"
```

#### セキュリティ設定
```yaml
production_security:
  network: "VPC・Private Subnet・Security Group"
  ssl_tls: "TLS 1.3・HTTPS強制・HSTS"
  authentication: "JWT・BCrypt・Multi-Factor Authentication"
  data_encryption: "保存時暗号化・転送時暗号化"
  backup: "自動バックアップ・ポイントインタイム復元"
```

### 5.2 本番デプロイメント

#### デプロイ戦略
```yaml
deployment_strategy:
  blue_green: "無停止デプロイメント・即座ロールバック"
  health_check: "ALB・ECSヘルスチェック・カスタムヘルスエンドポイント"
  rollback: "自動ロールバック・手動ロールバック手順"
  
  deployment_phases:
    1: "ステージング環境での最終検証"
    2: "本番環境への段階的デプロイ"
    3: "カナリアリリース（10%→50%→100%）"
    4: "全体切り替え・旧バージョン削除"
```

#### 本番デプロイ手順
```bash
# 1. リリースブランチ作成・確認
git checkout test-phasing
git pull origin test-phasing
git checkout -b release/v1.0.0

# 2. バージョンタグ作成
git tag -a v1.0.0 -m "Release version 1.0.0 - MVP Launch"
git push origin v1.0.0

# 3. 本番環境デプロイ（GitHub Actions）
# タグプッシュで自動トリガー
# または手動実行: GitHub Actions > Deploy to Production

# 4. デプロイ確認・検証
curl https://api.erpset.com/health
# 機能テスト・パフォーマンステスト実行

# 5. リリース完了・通知
# Slack・Email・ステークホルダー通知
```

### 5.3 本番環境監視・運用

#### 監視・アラート
```yaml
production_monitoring:
  uptime: "Pingdom・StatusPage・外形監視"
  performance: "DataDog・CloudWatch・APM"
  errors: "Sentry・ログ監視・アラート通知"
  business_metrics: "GAU・NPS・コンバージョン率"
  
  alert_thresholds:
    response_time: "95%ile > 3秒で警告"
    error_rate: "5分間で3%超過でアラート"
    availability: "2分間ダウンで即座通知"
```

#### バックアップ・災害復旧
```yaml
backup_disaster_recovery:
  database_backup:
    frequency: "自動日次フルバックアップ"
    retention: "30日間保持・長期アーカイブ"
    testing: "月次復元テスト・整合性確認"
    
  application_backup:
    code: "Git・タグ管理・リリースアーカイブ"
    configuration: "Secrets Manager・Parameter Store"
    documents: "S3・バージョン管理・クロスリージョン"
    
  recovery_procedures:
    rto: "目標復旧時間2時間以内"
    rpo: "目標復旧ポイント15分以内"
    playbook: "災害復旧手順書・定期訓練"
```

## 6. 開発ツール・ユーティリティ

### 6.1 便利スクリプト

#### 開発効率化スクリプト
```bash
# scripts/dev-setup.sh - 開発環境一括セットアップ
#!/bin/bash
echo "Setting up ERPset development environment..."
docker-compose -f docker-compose.local.yml up -d
cd phase1/backend && source venv/bin/activate && alembic upgrade head
cd ../frontend && yarn install
echo "Development environment ready!"

# scripts/run-tests.sh - 全テスト実行
#!/bin/bash
echo "Running all tests..."
cd phase1/frontend && yarn test && yarn test:e2e
cd ../backend && pytest --cov=app
echo "All tests completed!"

# scripts/quality-check.sh - コード品質チェック
#!/bin/bash
echo "Running quality checks..."
cd phase1/frontend && yarn lint && yarn type-check
cd ../backend && black . && flake8 . && mypy .
echo "Quality checks completed!"
```

### 6.2 デバッグ・トラブルシューティング

#### ログ確認コマンド
```bash
# アプリケーションログ確認
tail -f phase1/backend/logs/app.log
tail -f phase1/frontend/.next/trace

# Docker Composeログ確認
docker-compose logs -f postgres
docker-compose logs -f redis

# 本番環境ログ確認（AWS）
aws logs tail /aws/ecs/erpset-backend --follow
aws logs tail /aws/ecs/erpset-frontend --follow
```

#### パフォーマンス分析
```bash
# APIパフォーマンス測定
ab -n 100 -c 10 http://localhost:8000/api/v1/health

# データベースパフォーマンス
psql -h localhost -p 5432 -U erpset_user -d erpset_db -c "
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC LIMIT 10;"

# フロントエンドパフォーマンス
yarn build && yarn start
# Lighthouse・DevTools Performance分析
```

## 7. 関連文書・参照

### 7.1 プロジェクト文書

- [📋 プロジェクト全体構想](./project-overview.md)
- [🏗️ 技術アーキテクチャ](./technical-architecture.md)
- [📝 機能要求仕様書](./functional-requirements.md)
- [⚙️ 非機能要求仕様書](./non-functional-requirements.md)

### 7.2 運用・品質文書

- [🧪 品質保証・テスト戦略](./quality-assurance.md)
- [🛡️ セキュリティ・コンプライアンス要件](./security-compliance.md)
- [📊 監視・運用手順](./operations-guide.md)

### 7.3 外部リソース

- [Docker Documentation](https://docs.docker.com/)
- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---
**最終更新**: 2025-07-13  
**文書バージョン**: 1.0  
**メンテナンス責任者**: DevOpsチーム  
**次回更新**: Phase 1開発開始時（環境詳細化）