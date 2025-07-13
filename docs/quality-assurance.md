# ERPset 品質保証・テスト戦略

## 1. 品質保証概要

### 1.1 品質方針・目標

ERPsetプラットフォームの品質保証は、**実装ファースト原則**に基づき、継続的な品質向上と早期欠陥発見を重視します。

#### 品質目標
```yaml
quality_objectives:
  defect_prevention:
    target: "本番環境での致命的欠陥ゼロ"
    measurement: "Critical・High severity バグ件数"
    
  user_satisfaction:
    target: "ユーザー満足度8.0/10以上"
    measurement: "NPS・ユーザーフィードバック"
    
  reliability:
    target: "システム稼働率99.9%以上"
    measurement: "ダウンタイム・パフォーマンス監視"
    
  maintainability:
    target: "コードカバレッジ80%以上・技術的負債最小化"
    measurement: "テストカバレッジ・静的解析指標"
```

### 1.2 品質保証アプローチ

#### Shift-Left戦略
```
品質保証の前倒し:
設計 → 実装 → 単体テスト → 統合テスト → システムテスト → 受入テスト
 ↑      ↑         ↑           ↑            ↑            ↑
品質   コード    自動化      API連携      E2E        ユーザー
設計   レビュー   テスト      テスト      テスト      検証
```

#### 継続的品質改善
```yaml
continuous_improvement:
  daily: "コードレビュー・自動テスト・静的解析"
  weekly: "テストレポート分析・品質メトリクス確認"
  monthly: "品質振り返り・プロセス改善・テスト戦略見直し"
  quarterly: "品質監査・外部評価・ベンチマーク比較"
```

## 2. テスト戦略・アプローチ

### 2.1 テストピラミッド

#### 階層別テスト配分
```
        E2E Tests
       (5% - 手動重点)
      ↗              ↖
 Integration Tests    API Tests
(20% - 自動化)      (25% - 自動化)
  ↗                        ↖
Unit Tests              Component Tests
(40% - 完全自動化)     (10% - 自動化)
```

#### 各階層の役割・責任
```yaml
test_layers:
  unit_tests:
    scope: "関数・メソッド・クラス単位"
    automation: "100%自動化"
    execution: "コミット毎・高速実行"
    responsibility: "開発者"
    
  component_tests:
    scope: "Reactコンポーネント・UIロジック"
    automation: "100%自動化"
    execution: "PR作成時・CI/CD"
    responsibility: "フロントエンド開発者"
    
  integration_tests:
    scope: "API・DB・外部サービス連携"
    automation: "100%自動化"
    execution: "マージ前・デプロイ前"
    responsibility: "バックエンド開発者"
    
  api_tests:
    scope: "RESTful API・GraphQL"
    automation: "100%自動化"
    execution: "ステージング・本番前"
    responsibility: "QAエンジニア"
    
  e2e_tests:
    scope: "ユーザージャーニー・ビジネスシナリオ"
    automation: "70%自動化・30%手動"
    execution: "リリース前・定期実行"
    responsibility: "QAエンジニア・PM"
```

### 2.2 テスト種別・技法

#### 機能テスト
```yaml
functional_testing:
  positive_testing:
    description: "正常系・期待動作確認"
    techniques: "等価分割・境界値分析"
    
  negative_testing:
    description: "異常系・エラーハンドリング"
    techniques: "不正データ・例外ケース"
    
  boundary_testing:
    description: "境界値・限界値テスト"
    techniques: "上限下限・最大最小値"
    
  state_transition:
    description: "状態遷移・ワークフロー"
    techniques: "状態遷移図・遷移表"
```

#### 非機能テスト
```yaml
non_functional_testing:
  performance:
    load_testing: "通常負荷・期待レスポンス確認"
    stress_testing: "限界負荷・システム破綻点確認"
    spike_testing: "急激負荷変動・回復能力確認"
    volume_testing: "大量データ・長時間稼働確認"
    
  security:
    authentication: "認証・認可・セッション管理"
    authorization: "権限制御・アクセス制限"
    data_protection: "暗号化・個人情報保護"
    vulnerability: "脆弱性スキャン・侵入テスト"
    
  usability:
    user_experience: "UI/UX・操作性・直感性"
    accessibility: "アクセシビリティ・WCAG準拠"
    compatibility: "ブラウザ・デバイス互換性"
    localization: "多言語・地域対応"
```

## 3. 自動テスト実装

### 3.1 フロントエンド自動テスト

#### 単体テスト（Jest + React Testing Library）
```typescript
// phase1/frontend/src/components/__tests__/ProjectCard.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { ProjectCard } from '../ProjectCard';

describe('ProjectCard', () => {
  const mockProject = {
    id: '1',
    name: 'Test Project',
    description: 'Test Description',
    status: 'active',
    createdAt: '2025-01-01T00:00:00Z'
  };

  test('renders project information correctly', () => {
    render(<ProjectCard project={mockProject} />);
    
    expect(screen.getByText('Test Project')).toBeInTheDocument();
    expect(screen.getByText('Test Description')).toBeInTheDocument();
    expect(screen.getByText('Active')).toBeInTheDocument();
  });

  test('calls onEdit when edit button is clicked', () => {
    const mockOnEdit = jest.fn();
    render(<ProjectCard project={mockProject} onEdit={mockOnEdit} />);
    
    fireEvent.click(screen.getByRole('button', { name: /edit/i }));
    expect(mockOnEdit).toHaveBeenCalledWith(mockProject.id);
  });

  test('displays correct status badge color', () => {
    render(<ProjectCard project={mockProject} />);
    const statusBadge = screen.getByText('Active');
    
    expect(statusBadge).toHaveClass('bg-green-100', 'text-green-800');
  });
});
```

#### コンポーネント統合テスト
```typescript
// phase1/frontend/src/pages/__tests__/projects.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import ProjectsPage from '../projects';
import { mockApiResponse } from '../../__mocks__/api';

// Mock API
jest.mock('../../lib/api', () => ({
  getProjects: jest.fn()
}));

describe('Projects Page', () => {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } }
  });

  test('displays projects list after loading', async () => {
    mockApiResponse.getProjects.mockResolvedValue({
      data: [
        { id: '1', name: 'Project 1', status: 'active' },
        { id: '2', name: 'Project 2', status: 'completed' }
      ]
    });

    render(
      <QueryClientProvider client={queryClient}>
        <ProjectsPage />
      </QueryClientProvider>
    );

    expect(screen.getByText('Loading...')).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('Project 1')).toBeInTheDocument();
      expect(screen.getByText('Project 2')).toBeInTheDocument();
    });
  });
});
```

#### E2Eテスト（Playwright）
```typescript
// phase1/frontend/e2e/project-management.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Project Management', () => {
  test.beforeEach(async ({ page }) => {
    // ログイン
    await page.goto('/login');
    await page.fill('[data-testid=email]', 'test@example.com');
    await page.fill('[data-testid=password]', 'password123');
    await page.click('[data-testid=login-button]');
    await expect(page).toHaveURL('/dashboard');
  });

  test('creates new project successfully', async ({ page }) => {
    // プロジェクト作成ページに移動
    await page.click('[data-testid=new-project-button]');
    await expect(page).toHaveURL('/projects/new');

    // プロジェクト情報入力
    await page.fill('[data-testid=project-name]', 'E2E Test Project');
    await page.fill('[data-testid=project-description]', 'Test Description');
    await page.selectOption('[data-testid=erp-type]', 'salesforce');
    await page.check('[data-testid=scope-sales]');

    // 作成実行
    await page.click('[data-testid=create-project-button]');

    // 成功確認
    await expect(page).toHaveURL(/\/projects\/\w+/);
    await expect(page.locator('[data-testid=project-title]'))
      .toHaveText('E2E Test Project');
  });

  test('generates hearing list for project', async ({ page }) => {
    // 既存プロジェクトに移動
    await page.goto('/projects/test-project-id');

    // ヒアリングリスト生成
    await page.click('[data-testid=generate-hearing-button]');
    
    // 生成中表示確認
    await expect(page.locator('[data-testid=loading-spinner]'))
      .toBeVisible();

    // 生成完了確認
    await expect(page.locator('[data-testid=hearing-list-table]'))
      .toBeVisible({ timeout: 10000 });
    
    const hearingItems = page.locator('[data-testid=hearing-item]');
    await expect(hearingItems).toHaveCountGreaterThan(0);
  });
});
```

### 3.2 バックエンド自動テスト

#### 単体テスト（pytest）
```python
# phase1/backend/tests/test_services/test_hearing_generator.py
import pytest
from unittest.mock import Mock, patch
from app.services.hearing_generator import HearingGeneratorService
from app.models.project import Project
from app.schemas.hearing import HearingListRequest

@pytest.fixture
def hearing_service():
    return HearingGeneratorService(db=Mock())

@pytest.fixture
def sample_project():
    return Project(
        id="test-project-id",
        name="Test Project",
        erp_type="salesforce",
        business_domain="sales"
    )

class TestHearingGeneratorService:
    def test_generate_hearing_list_success(self, hearing_service, sample_project):
        # Arrange
        request = HearingListRequest(
            erp_type="salesforce",
            business_modules=["sales"],
            business_requirements=["lead_management", "opportunity_tracking"]
        )
        
        with patch.object(hearing_service, '_get_relevant_functions') as mock_functions:
            mock_functions.return_value = [
                {"id": "func-1", "name": "Lead Management", "hearing_items": ["item-1", "item-2"]},
                {"id": "func-2", "name": "Opportunity Tracking", "hearing_items": ["item-3"]}
            ]
            
            # Act
            result = hearing_service.generate_hearing_list(request)
            
            # Assert
            assert result.success is True
            assert len(result.hearing_items) == 3
            assert result.coverage_score > 0.8
            mock_functions.assert_called_once()

    def test_generate_hearing_list_invalid_erp_type(self, hearing_service):
        # Arrange
        request = HearingListRequest(
            erp_type="invalid_erp",
            business_modules=["sales"],
            business_requirements=["lead_management"]
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="Unsupported ERP type"):
            hearing_service.generate_hearing_list(request)

    def test_calculate_coverage_score(self, hearing_service):
        # Arrange
        requirements = ["req1", "req2", "req3"]
        covered_requirements = ["req1", "req2"]
        
        # Act
        score = hearing_service._calculate_coverage_score(requirements, covered_requirements)
        
        # Assert
        assert score == pytest.approx(0.667, rel=1e-2)
```

#### 統合テスト（API・データベース）
```python
# phase1/backend/tests/test_api/test_projects.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.core.database import get_db
from app.models.project import Project
from tests.conftest import override_get_db

client = TestClient(app)

class TestProjectsAPI:
    def test_create_project_success(self, db_session: Session, auth_headers: dict):
        # Arrange
        project_data = {
            "name": "Test Project",
            "description": "Test Description",
            "erp_type": "salesforce",
            "business_domain": "sales"
        }
        
        # Act
        response = client.post("/api/v1/projects", json=project_data, headers=auth_headers)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Project"
        assert data["erp_type"] == "salesforce"
        
        # DB確認
        project = db_session.query(Project).filter(Project.id == data["id"]).first()
        assert project is not None
        assert project.name == "Test Project"

    def test_get_projects_list(self, db_session: Session, auth_headers: dict):
        # Arrange - テストデータ作成
        project1 = Project(name="Project 1", erp_type="salesforce", business_domain="sales")
        project2 = Project(name="Project 2", erp_type="salesforce", business_domain="service")
        db_session.add_all([project1, project2])
        db_session.commit()
        
        # Act
        response = client.get("/api/v1/projects", headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 2

    def test_get_project_not_found(self, auth_headers: dict):
        # Act
        response = client.get("/api/v1/projects/non-existent-id", headers=auth_headers)
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    @pytest.mark.parametrize("invalid_data,expected_error", [
        ({"name": ""}, "Name cannot be empty"),
        ({"name": "Test", "erp_type": "invalid"}, "Invalid ERP type"),
        ({"name": "Test", "erp_type": "salesforce"}, "Business domain is required")
    ])
    def test_create_project_validation_errors(self, invalid_data: dict, expected_error: str, auth_headers: dict):
        # Act
        response = client.post("/api/v1/projects", json=invalid_data, headers=auth_headers)
        
        # Assert
        assert response.status_code == 422
        assert expected_error in str(response.json())
```

### 3.3 パフォーマンステスト

#### 負荷テスト（k6）
```javascript
// phase1/tests/performance/hearing-generation-load.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// カスタムメトリクス
const errorRate = new Rate('errors');
const hearingGenerationTime = new Trend('hearing_generation_duration');

export const options = {
  stages: [
    { duration: '2m', target: 10 }, // 2分で10ユーザーまで上昇
    { duration: '5m', target: 10 }, // 5分間10ユーザー維持
    { duration: '2m', target: 20 }, // 2分で20ユーザーまで上昇
    { duration: '5m', target: 20 }, // 5分間20ユーザー維持
    { duration: '2m', target: 0 },  // 2分で0ユーザーまで下降
  ],
  thresholds: {
    http_req_duration: ['p(95)<3000'], // 95%のリクエストが3秒以内
    errors: ['rate<0.1'],             // エラー率10%未満
    hearing_generation_duration: ['p(90)<5000'], // ヒアリング生成90%が5秒以内
  },
};

export function setup() {
  // 認証トークン取得
  const loginResponse = http.post('http://localhost:8000/auth/login', JSON.stringify({
    email: 'loadtest@example.com',
    password: 'loadtest123'
  }), {
    headers: { 'Content-Type': 'application/json' },
  });
  
  return { token: loginResponse.json('access_token') };
}

export default function(data) {
  const headers = {
    'Authorization': `Bearer ${data.token}`,
    'Content-Type': 'application/json',
  };

  // ヒアリングリスト生成リクエスト
  const hearingPayload = JSON.stringify({
    erp_type: 'salesforce',
    business_modules: ['sales'],
    business_requirements: ['lead_management', 'opportunity_tracking', 'account_management']
  });

  const start = new Date();
  const response = http.post('http://localhost:8000/api/v1/generators/hearing-list', 
    hearingPayload, 
    { headers }
  );
  const duration = new Date() - start;

  // 結果検証
  const success = check(response, {
    'status is 200': (r) => r.status === 200,
    'response has hearing items': (r) => r.json('hearing_items').length > 0,
    'coverage score is valid': (r) => r.json('coverage_score') >= 0.7,
  });

  if (!success) {
    errorRate.add(1);
  }
  
  hearingGenerationTime.add(duration);
  
  sleep(1); // 1秒間隔
}
```

#### ストレステスト（負荷限界確認）
```javascript
// phase1/tests/performance/stress-test.js
export const options = {
  stages: [
    { duration: '5m', target: 50 },   // 通常負荷
    { duration: '10m', target: 100 }, // 高負荷
    { duration: '5m', target: 200 },  // 極高負荷
    { duration: '10m', target: 300 }, // 限界負荷
    { duration: '5m', target: 0 },    // 負荷解除
  ],
  thresholds: {
    http_req_duration: ['p(99)<10000'], // 99%が10秒以内（緩和）
    http_req_failed: ['rate<0.5'],      // 失敗率50%未満
  },
};
```

## 4. 手動テスト・探索的テスト

### 4.1 探索的テスト戦略

#### セッションベース探索的テスト
```yaml
exploratory_testing:
  session_duration: "90分間の集中テストセッション"
  charter: "特定機能・ユーザーシナリオの探索"
  reporting: "発見した問題・改善点・学習事項の記録"
  
  charter_examples:
    - "プロジェクト作成から初回ヒアリング実施までのフロー探索"
    - "異常系データ入力・エラーハンドリングの探索"
    - "モバイルブラウザでの操作性・レスポンシブ対応の探索"
    - "アクセシビリティ・キーボード操作の探索"
```

#### ペルソナベーステスト
```yaml
persona_based_testing:
  consultant_perspective:
    focus: "業務効率・正確性・使いやすさ"
    scenarios: "日常的なコンサルティング業務フロー"
    
  it_manager_perspective:
    focus: "セキュリティ・安定性・管理機能"
    scenarios: "システム導入・ユーザー管理・監査"
    
  end_user_perspective:
    focus: "直感性・学習容易性・エラー回復"
    scenarios: "初回利用・不慣れな操作・困ったときの対処"
```

### 4.2 受入テスト・UAT

#### ユーザー受入テスト手順
```yaml
uat_process:
  preparation:
    environment: "ステージング環境・本番類似データ"
    test_accounts: "実際の役割・権限を反映したテストアカウント"
    scenarios: "実業務を反映したテストシナリオ"
    
  execution:
    participants: "実際のエンドユーザー・ステークホルダー"
    duration: "1週間集中テスト期間"
    support: "開発チーム・QAチームのサポート体制"
    
  criteria:
    functional: "全主要機能の動作確認"
    usability: "ユーザビリティ基準達成"
    performance: "性能要求基準達成"
    business_value: "ビジネス価値・効果の実感"
```

### 4.3 回帰テスト・リリーステスト

#### 回帰テストスイート
```yaml
regression_testing:
  smoke_tests:
    scope: "主要機能の基本動作確認"
    execution: "デプロイ後10分以内"
    automation: "100%自動化"
    
  critical_path:
    scope: "ビジネスクリティカルなユーザージャーニー"
    execution: "リリース前24時間以内"
    automation: "80%自動化・20%手動確認"
    
  full_regression:
    scope: "全機能・エッジケース・互換性"
    execution: "メジャーリリース前"
    automation: "60%自動化・40%手動探索"
```

## 5. 品質メトリクス・KPI

### 5.1 技術品質指標

#### コード品質メトリクス
```yaml
code_quality_metrics:
  test_coverage:
    unit_tests: "目標80%以上・最低70%"
    integration_tests: "主要API100%・DB操作100%"
    e2e_tests: "クリティカルパス100%"
    
  static_analysis:
    complexity: "循環的複雑度10以下"
    duplications: "重複コード5%以下"
    maintainability: "SonarQube Maintainability Rating A"
    
  technical_debt:
    debt_ratio: "技術的負債比率5%以下"
    reliability: "SonarQube Reliability Rating A"
    security: "Security Hotspots 0件"
```

#### 欠陥品質指標
```yaml
defect_metrics:
  defect_density:
    target: "1,000行あたり5件以下"
    measurement: "リリース後6ヶ月間の欠陥数"
    
  defect_severity:
    critical: "0件（本番停止レベル）"
    high: "月5件以下（主要機能影響）"
    medium: "月20件以下（一部機能影響）"
    
  defect_lifecycle:
    detection_time: "90%が開発フェーズ内で発見"
    resolution_time: "Critical 4時間・High 24時間・Medium 1週間"
```

### 5.2 ユーザー体験品質指標

#### パフォーマンス指標
```yaml
performance_metrics:
  core_web_vitals:
    lcp: "Largest Contentful Paint 2.5秒以下"
    fid: "First Input Delay 100ms以下"
    cls: "Cumulative Layout Shift 0.1以下"
    
  api_performance:
    response_time: "95%ile 3秒以下・99%ile 5秒以下"
    throughput: "秒間100リクエスト処理"
    availability: "99.9%稼働率"
```

#### ユーザビリティ指標
```yaml
usability_metrics:
  task_completion:
    success_rate: "主要タスク95%以上完了"
    error_rate: "操作エラー5%以下"
    efficiency: "タスク完了時間ベンチマーク達成"
    
  user_satisfaction:
    nps: "Net Promoter Score 50以上"
    csat: "Customer Satisfaction 8.0/10以上"
    sus: "System Usability Scale 70以上"
```

### 5.3 ビジネス価値指標

#### 効率化効果測定
```yaml
business_metrics:
  productivity_gains:
    hearing_preparation: "工数70%削減（8時間→2.5時間）"
    setup_definition: "工数75%削減（16時間→4時間）"
    gap_analysis: "精度向上90%・時間50%削減"
    
  quality_improvements:
    configuration_errors: "設定ミス50%削減"
    project_delays: "遅延リスク80%削減"
    customer_satisfaction: "顧客満足度20%向上"
    
  cost_benefits:
    consulting_efficiency: "コンサルティング単価30%向上"
    project_success_rate: "成功率85%→95%向上"
    total_cost_reduction: "総導入コスト40%削減"
```

## 6. 品質管理プロセス

### 6.1 品質ゲート・チェックポイント

#### 開発プロセス品質ゲート
```yaml
quality_gates:
  code_commit:
    criteria: "単体テスト通過・Lint規約準拠・コードレビュー完了"
    automation: "pre-commit hooks・CI自動実行"
    
  pull_request:
    criteria: "統合テスト通過・カバレッジ基準達成・2名レビュー承認"
    automation: "GitHub Actions・品質指標自動確認"
    
  deployment:
    criteria: "全テスト通過・セキュリティスキャン完了・性能基準達成"
    automation: "CD pipeline・自動ロールバック"
    
  release:
    criteria: "UAT完了・ステークホルダー承認・運用準備完了"
    manual: "リリース会議・Go/NoGo判定"
```

### 6.2 不具合管理・改善プロセス

#### 不具合ライフサイクル管理
```yaml
defect_management:
  detection:
    sources: "自動テスト・手動テスト・ユーザーレポート・監視アラート"
    triage: "4時間以内の優先度判定・担当者アサイン"
    
  resolution:
    workflow: "分析→修正→テスト→レビュー→リリース"
    tracking: "JIRA・GitHub Issues・進捗可視化"
    
  prevention:
    root_cause: "根本原因分析・再発防止策"
    process_improvement: "テスト強化・品質プロセス改善"
```

#### 継続的改善サイクル
```yaml
continuous_improvement:
  daily:
    standup: "前日の品質課題・当日の品質目標"
    code_review: "品質観点・学習事項共有"
    
  weekly:
    metrics_review: "品質指標・トレンド分析"
    retrospective: "品質課題・改善アクション"
    
  monthly:
    quality_board: "品質状況報告・戦略調整"
    process_audit: "品質プロセス監査・改善"
    
  quarterly:
    quality_planning: "次四半期品質目標・投資計画"
    external_review: "外部品質評価・ベンチマーク"
```

## 7. ツール・インフラ

### 7.1 テストツールスタック

#### 自動テストツール
```yaml
test_automation_tools:
  frontend:
    unit: "Jest + React Testing Library"
    component: "Storybook + Chromatic"
    e2e: "Playwright"
    visual: "Percy・Applitools"
    
  backend:
    unit: "pytest + pytest-cov"
    integration: "pytest + testcontainers"
    api: "pytest + requests"
    load: "k6・Locust"
    
  mobile:
    cross_platform: "Detox（React Native）"
    device_cloud: "BrowserStack・Sauce Labs"
```

#### 品質分析ツール
```yaml
quality_analysis_tools:
  static_analysis:
    code_quality: "SonarQube・CodeClimate"
    security: "Snyk・OWASP ZAP"
    dependencies: "Dependabot・npm audit"
    
  monitoring:
    application: "DataDog・New Relic"
    errors: "Sentry・Bugsnag"
    performance: "Lighthouse・PageSpeed Insights"
    
  reporting:
    test_results: "Allure・Jest HTML Reporter"
    coverage: "Codecov・Coveralls"
    dashboards: "Grafana・Kibana"
```

### 7.2 CI/CDパイプライン品質統合

#### 品質チェック統合
```yaml
cicd_quality_integration:
  pr_checks:
    - lint_and_format
    - unit_tests
    - integration_tests
    - security_scan
    - coverage_check
    
  deployment_checks:
    - e2e_tests
    - performance_tests
    - accessibility_scan
    - security_compliance
    
  post_deployment:
    - smoke_tests
    - monitoring_validation
    - user_metrics_tracking
```

## 8. 関連文書・参照

### 8.1 プロジェクト文書

- [📋 プロジェクト全体構想](./project-overview.md)
- [🏗️ 技術アーキテクチャ](./technical-architecture.md)
- [📝 機能要求仕様書](./functional-requirements.md)
- [⚙️ 非機能要求仕様書](./non-functional-requirements.md)

### 8.2 開発・運用文書

- [🔧 環境構築ガイド](./setup-guide.md)
- [🛡️ セキュリティ・コンプライアンス要件](./security-compliance.md)
- [📊 監視・運用手順](./operations-guide.md)

### 8.3 外部参照・ベストプラクティス

- [Testing Trophy - Kent C. Dodds](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications)
- [Google Testing Blog](https://testing.googleblog.com/)
- [ISTQB Testing Standards](https://www.istqb.org/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

---
**最終更新**: 2025-07-13  
**文書バージョン**: 1.0  
**品質責任者**: QAリード・テックリード  
**次回レビュー**: Phase 1開発開始時（テスト実装・実行開始）