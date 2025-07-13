#!/bin/bash

# ERPset Phase 1 Development Environment Setup Script
# Usage: ./scripts/setup-dev.sh

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if script is run from correct directory
check_directory() {
    if [[ ! -f "docker-compose.yml" ]]; then
        log_error "docker-compose.yml not found. Please run this script from the phase1 directory."
        exit 1
    fi
}

# Check required tools
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker Desktop."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose."
        exit 1
    fi
    
    # Check Node.js (for local development)
    if ! command -v node &> /dev/null; then
        log_warning "Node.js is not installed. Some local development features may not work."
    else
        NODE_VERSION=$(node --version)
        log_info "Node.js version: $NODE_VERSION"
    fi
    
    # Check Python (for local development)
    if ! command -v python3 &> /dev/null; then
        log_warning "Python 3 is not installed. Some local development features may not work."
    else
        PYTHON_VERSION=$(python3 --version)
        log_info "Python version: $PYTHON_VERSION"
    fi
    
    log_success "Prerequisites check completed"
}

# Setup environment variables
setup_environment() {
    log_info "Setting up environment variables..."
    
    if [[ ! -f ".env.local" ]]; then
        if [[ -f ".env.example" ]]; then
            cp .env.example .env.local
            log_success "Created .env.local from .env.example"
            log_warning "Please review and update .env.local with your specific configuration"
        else
            log_error ".env.example not found. Cannot create .env.local"
            exit 1
        fi
    else
        log_info ".env.local already exists"
    fi
}

# Create required directories
create_directories() {
    log_info "Creating required directories..."
    
    directories=(
        "backend/app"
        "backend/tests"
        "backend/alembic/versions"
        "frontend/src"
        "frontend/public"
        "shared/schemas"
        "shared/types"
        "scripts"
        "uploads"
        "logs"
    )
    
    for dir in "${directories[@]}"; do
        mkdir -p "$dir"
        log_info "Created directory: $dir"
    done
    
    log_success "Directory structure created"
}

# Setup backend development files
setup_backend() {
    log_info "Setting up backend development files..."
    
    # Create requirements.txt if it doesn't exist
    if [[ ! -f "backend/requirements.txt" ]]; then
        cat > backend/requirements.txt << 'EOF'
# ERPset Backend Dependencies

# FastAPI and ASGI
fastapi==0.104.1
uvicorn[standard]==0.24.0
gunicorn==21.2.0

# Database
sqlalchemy==2.0.23
alembic==1.13.0
asyncpg==0.29.0
psycopg2-binary==2.9.9

# Redis
redis==5.0.1
hiredis==2.2.3

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Validation & Serialization
pydantic==2.5.0
pydantic-settings==2.1.0

# HTTP Client
httpx==0.25.2
aiohttp==3.9.1

# Development & Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
black==23.11.0
isort==5.12.0
flake8==6.1.0
mypy==1.7.1

# Monitoring
structlog==23.2.0
sentry-sdk[fastapi]==1.38.0

# Environment
python-dotenv==1.0.0
EOF
        log_success "Created backend/requirements.txt"
    fi
    
    # Create Dockerfile.dev for backend
    if [[ ! -f "backend/Dockerfile.dev" ]]; then
        cat > backend/Dockerfile.dev << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Development command with auto-reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
EOF
        log_success "Created backend/Dockerfile.dev"
    fi
}

# Setup frontend development files
setup_frontend() {
    log_info "Setting up frontend development files..."
    
    # Create package.json if it doesn't exist
    if [[ ! -f "frontend/package.json" ]]; then
        cat > frontend/package.json << 'EOF'
{
  "name": "erpset-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  },
  "dependencies": {
    "next": "15.0.0",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "@tanstack/react-query": "5.0.0",
    "zustand": "4.5.0",
    "react-hook-form": "7.51.0",
    "zod": "3.22.0",
    "@hookform/resolvers": "3.3.0",
    "tailwindcss": "3.4.0",
    "autoprefixer": "10.4.0",
    "postcss": "8.4.0",
    "lucide-react": "0.300.0",
    "clsx": "2.0.0",
    "tailwind-merge": "2.0.0"
  },
  "devDependencies": {
    "typescript": "5.4.0",
    "@types/node": "20.0.0",
    "@types/react": "18.2.0",
    "@types/react-dom": "18.2.0",
    "eslint": "8.57.0",
    "eslint-config-next": "15.0.0",
    "@typescript-eslint/parser": "6.0.0",
    "@typescript-eslint/eslint-plugin": "6.0.0",
    "prettier": "3.1.0",
    "prettier-plugin-tailwindcss": "0.5.0",
    "jest": "29.7.0",
    "jest-environment-jsdom": "29.7.0",
    "@testing-library/react": "14.1.0",
    "@testing-library/jest-dom": "6.1.0",
    "@testing-library/user-event": "14.5.0",
    "@playwright/test": "1.40.0"
  },
  "engines": {
    "node": ">=18.17.0"
  }
}
EOF
        log_success "Created frontend/package.json"
    fi
    
    # Create Dockerfile.dev for frontend
    if [[ ! -f "frontend/Dockerfile.dev" ]]; then
        cat > frontend/Dockerfile.dev << 'EOF'
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production=false

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Development command
CMD ["npm", "run", "dev"]
EOF
        log_success "Created frontend/Dockerfile.dev"
    fi
}

# Setup database initialization
setup_database() {
    log_info "Setting up database initialization..."
    
    if [[ ! -f "scripts/init-db.sql" ]]; then
        cat > scripts/init-db.sql << 'EOF'
-- ERPset Database Initialization Script

-- Create database (if not exists)
SELECT 'CREATE DATABASE erpset_dev'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'erpset_dev')\gexec

-- Create test database
SELECT 'CREATE DATABASE erpset_test'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'erpset_test')\gexec

-- Connect to main database
\c erpset_dev;

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- Create application user with appropriate permissions
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'erpset_app_user') THEN
        CREATE ROLE erpset_app_user;
    END IF;
END
$$;

-- Grant necessary permissions
GRANT USAGE ON SCHEMA public TO erpset_app_user;
GRANT CREATE ON SCHEMA public TO erpset_app_user;

-- Connect to test database and set up similarly
\c erpset_test;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

GRANT USAGE ON SCHEMA public TO erpset_app_user;
GRANT CREATE ON SCHEMA public TO erpset_app_user;
EOF
        log_success "Created scripts/init-db.sql"
    fi
}

# Start Docker services
start_services() {
    log_info "Starting Docker services..."
    
    # Pull latest images
    docker-compose pull
    
    # Build and start services
    docker-compose up -d --build
    
    # Wait for services to be healthy
    log_info "Waiting for services to start..."
    sleep 10
    
    # Check if services are running
    if docker-compose ps | grep -q "Up"; then
        log_success "Docker services started successfully"
    else
        log_error "Some services failed to start. Check logs with: docker-compose logs"
        exit 1
    fi
}

# Display helpful information
show_info() {
    log_success "ERPset Phase 1 development environment setup completed!"
    echo ""
    log_info "Available services:"
    echo "  - Frontend:    http://localhost:3000"
    echo "  - Backend API: http://localhost:8000"
    echo "  - API Docs:    http://localhost:8000/docs"
    echo "  - PostgreSQL:  localhost:5432"
    echo "  - Redis:       localhost:6379"
    echo ""
    log_info "Optional management tools (run with --profile tools):"
    echo "  - pgAdmin:         http://localhost:5050"
    echo "  - Redis Commander: http://localhost:8081"
    echo ""
    log_info "Useful commands:"
    echo "  - View logs:           docker-compose logs -f"
    echo "  - Stop services:       docker-compose down"
    echo "  - Restart service:     docker-compose restart <service>"
    echo "  - Run with tools:      docker-compose --profile tools up -d"
    echo "  - Access backend:      docker-compose exec backend bash"
    echo "  - Access frontend:     docker-compose exec frontend sh"
    echo ""
    log_warning "Don't forget to:"
    echo "  1. Review and update .env.local with your configuration"
    echo "  2. Set up your IDE/editor with project workspace"
    echo "  3. Install local development dependencies if needed"
}

# Main execution
main() {
    log_info "Starting ERPset Phase 1 development environment setup..."
    
    check_directory
    check_prerequisites
    setup_environment
    create_directories
    setup_backend
    setup_frontend
    setup_database
    start_services
    show_info
    
    log_success "Setup completed successfully! 🚀"
}

# Run main function
main "$@"