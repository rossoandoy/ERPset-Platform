# ERPset Phase 1 - Quick Start Guide

## 🚀 開発環境クイックスタート

### 前提条件
- Docker Desktop
- Git
- Node.js 18+ (ローカル開発用)
- Python 3.11+ (ローカル開発用)

### 1分でスタート
```bash
# 1. リポジトリクローン・ブランチ切り替え
git clone <repository-url>
cd ERPset/phase1
git checkout test-phasing

# 2. 自動セットアップ実行
./scripts/setup-dev.sh

# 3. ブラウザでアクセス
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000/docs
```

## 📊 利用可能サービス

| サービス | URL | 説明 |
|---------|-----|-----|
| **Frontend** | http://localhost:3000 | Next.js Webアプリ |
| **Backend API** | http://localhost:8000 | FastAPI REST API |
| **API文書** | http://localhost:8000/docs | Swagger UI |
| **PostgreSQL** | localhost:5432 | メインデータベース |
| **Redis** | localhost:6379 | キャッシュ・セッション |

### 管理ツール（オプション）
```bash
# 管理ツール付きで起動
docker-compose --profile tools up -d
```

| ツール | URL | ログイン |
|-------|-----|---------|
| **pgAdmin** | http://localhost:5050 | admin@erpset.local / admin123 |
| **Redis Commander** | http://localhost:8081 | - |

## 🛠️ 開発コマンド

### Docker操作
```bash
# サービス起動
docker-compose up -d

# ログ確認
docker-compose logs -f

# サービス停止
docker-compose down

# 特定サービス再起動
docker-compose restart backend

# コンテナ内アクセス
docker-compose exec backend bash
docker-compose exec frontend sh
```

### データベース操作
```bash
# マイグレーション実行
docker-compose exec backend alembic upgrade head

# サンプルデータ投入
docker-compose exec backend python /app/scripts/seed-data.py

# データベースリセット
docker-compose down -v
docker-compose up -d
```

### 開発作業
```bash
# バックエンド開発
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# フロントエンド開発
cd frontend
npm install
npm run dev

# テスト実行
cd backend && pytest
cd frontend && npm test
```

## 📁 プロジェクト構造

```
phase1/
├── docs/                    # 設計文書
│   ├── technical-spec.md    # 技術仕様書
│   ├── api-design.md        # API設計書
│   ├── database-design.md   # DB設計書
│   └── ...
├── frontend/                # Next.js アプリ
├── backend/                 # FastAPI アプリ
├── shared/                  # 共通定義
├── scripts/                 # 運用スクリプト
├── docker-compose.yml       # 開発環境
├── .env.example            # 環境変数テンプレート
└── README.md               # 本ファイル
```

## ⚙️ 設定・カスタマイズ

### 環境変数設定
```bash
# 環境設定ファイル作成
cp .env.example .env.local

# 重要な設定項目を確認・更新
vim .env.local
```

### 主要設定項目
- `SECRET_KEY`: アプリケーション秘密鍵
- `DATABASE_URL`: PostgreSQL接続文字列
- `REDIS_URL`: Redis接続文字列
- `CORS_ORIGINS`: フロントエンドOrigin設定

## 🧪 テスト・品質確認

### バックエンドテスト
```bash
cd backend

# 単体テスト
pytest

# カバレッジ付きテスト
pytest --cov=app --cov-report=html

# 型チェック
mypy app/

# コード品質
black . && isort . && flake8
```

### フロントエンドテスト
```bash
cd frontend

# 単体テスト
npm test

# E2Eテスト
npx playwright test

# 型チェック
npm run type-check

# Lint・フォーマット
npm run lint && npm run format
```

## 🔧 トラブルシューティング

### よくある問題

**ポート衝突エラー**
```bash
# 使用中ポート確認
lsof -i :3000
lsof -i :8000
lsof -i :5432

# Docker完全リセット
docker-compose down -v
docker system prune -a
```

**データベース接続エラー**
```bash
# PostgreSQL状態確認
docker-compose exec postgres pg_isready -U erpset_user -d erpset_dev

# ログ確認
docker-compose logs postgres
```

**依存関係エラー**
```bash
# Node.js依存関係リビルド
docker-compose exec frontend npm ci

# Python依存関係更新
docker-compose exec backend pip install -r requirements.txt --force-reinstall
```

### パフォーマンス最適化
```bash
# Docker BuildKit有効化
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

# イメージ軽量化
docker-compose build --no-cache
```

## 📚 開発リソース

### 技術文書
- [📋 Phase 1概要](./README.md)
- [🔧 技術仕様書](./docs/technical-spec.md)
- [🌐 API設計書](./docs/api-design.md)
- [🗄️ データベース設計書](./docs/database-design.md)

### 外部ドキュメント
- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Compose Reference](https://docs.docker.com/compose/)

### 開発支援
- **Backend API**: http://localhost:8000/docs (Swagger UI)
- **Frontend Storybook**: http://localhost:6006 (実装後)
- **Database Schema**: http://localhost:5050 (pgAdmin)

---

**最終更新**: 2025-07-13  
**開発環境**: Docker Compose  
**サポート**: 開発チーム