# Testing Guidelines

## 1. Testing Framework

### 1.1 Primary Tools
- pytest: Main testing framework
- pytest-cov: Code coverage reporting
- pytest-vcr: Recording and replaying HTTP interactions
- pytest-mock: Mocking functionality

### 1.2 Test Organization
```
tests/
├── __init__.py
├── conftest.py           # Shared fixtures
├── test_garmin.py       # Garmin Connect integration tests
├── test_fit.py          # FIT file processing tests
├── test_analysis.py     # Data analysis tests
├── test_integration.py  # End-to-end tests
└── resources/           # Test data
    ├── sample.fit       # Sample FIT file
    ├── mock_responses/  # VCR cassettes
    └── expected/        # Expected output files
```

## 2. Test Categories

### 2.1 Unit Tests
Test individual components in isolation:
```python
def test_garmin_auth():
    """Test Garmin Connect authentication"""
    connector = GarminConnector(TEST_USER, TEST_PASS)
    assert connector.is_authenticated()

def test_fit_decode():
    """Test FIT file decoding"""
    decoder = FitDecoder()
    data = decoder.decode('tests/resources/sample.fit')
    assert 'timestamp' in data.columns
    assert 'heart_rate' in data.columns
```

### 2.2 Integration Tests
Test component interactions:
```python
def test_download_and_decode():
    """Test downloading and decoding FIT file"""
    # Download FIT file
    connector = GarminConnector(TEST_USER, TEST_PASS)
    fit_file = connector.download_activity(TEST_ACTIVITY_ID)
    
    # Decode FIT file
    decoder = FitDecoder()
    data = decoder.decode(fit_file)
    
    # Verify data
    assert data is not None
    assert len(data) > 0
```

### 2.3 End-to-End Tests
Test complete workflows:
```python
def test_full_workflow():
    """Test complete workout analysis workflow"""
    # Setup
    connector = GarminConnector(TEST_USER, TEST_PASS)
    
    # Get recent activities
    activities = connector.get_activities(limit=1)
    
    # Download and process FIT file
    fit_file = connector.download_activity(activities[0]['activityId'])
    workout_data = process_workout(fit_file)
    
    # Generate report
    report = generate_workout_report(workout_data)
    
    # Verify results
    assert os.path.exists(report)
    assert verify_report_content(report)
```

## 3. Test Data Management

### 3.1 Mock Data
```python
@pytest.fixture
def mock_garmin_response():
    """Mock Garmin Connect API response"""
    return {
        'activityId': '12345678',
        'activityName': 'Morning Run',
        'distance': 5000.0,
        'duration': 1800.0,
        'averageHR': 150
    }

@pytest.fixture
def sample_fit_data():
    """Load sample FIT file data"""
    return read_fit_file('tests/resources/sample.fit')
```

### 3.2 VCR Cassettes
```python
@pytest.mark.vcr()
def test_garmin_api():
    """Test Garmin Connect API with recorded responses"""
    connector = GarminConnector(TEST_USER, TEST_PASS)
    activities = connector.get_activities(limit=1)
    assert len(activities) == 1
```

## 4. Test Coverage

### 4.1 Coverage Requirements
- Minimum coverage: 80% for new code
- Critical paths: 100% coverage
- Integration points: 90% coverage

### 4.2 Running Coverage
```bash
# Run tests with coverage
pytest tests/ -v --cov=. --cov-report=term-missing

# Generate HTML report
pytest tests/ -v --cov=. --cov-report=html
```

## 5. Mocking Strategies

### 5.1 API Mocking
```python
def test_garmin_api_error(mocker):
    """Test handling of API errors"""
    # Mock API error response
    mocker.patch('garminconnect.Garmin.get_activities',
                 side_effect=GarminConnectConnectionError)
    
    connector = GarminConnector(TEST_USER, TEST_PASS)
    with pytest.raises(GarminConnectConnectionError):
        connector.get_activities()
```

### 5.2 File System Mocking
```python
def test_fit_file_handling(tmp_path):
    """Test FIT file operations with temporary directory"""
    # Create mock FIT file
    fit_path = tmp_path / "test.fit"
    create_mock_fit_file(fit_path)
    
    # Process file
    result = process_fit_file(fit_path)
    assert result is not None
```

## 6. Test Environment

### 6.1 Configuration
```python
# conftest.py
import pytest

@pytest.fixture(scope='session')
def test_config():
    """Test configuration"""
    return {
        'garmin': {
            'username': 'test_user',
            'password': 'test_pass'
        },
        'storage': {
            'fit_dir': 'tests/resources/fit',
            'report_dir': 'tests/resources/reports'
        }
    }
```

### 6.2 Cleanup
```python
@pytest.fixture(autouse=True)
def cleanup_files():
    """Clean up test files after each test"""
    yield
    # Clean up downloaded files
    for file in glob.glob('tests/resources/temp/*'):
        os.remove(file)
```

## 7. Continuous Integration

### 7.1 Test Automation
```yaml
# .github/workflows/tests.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: |
          pytest tests/ -v --cov=. --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## 8. Version History
| Version | Date | Description | Author |
|---------|------|-------------|---------|
| 1.0 | 2024-03-20 | Initial testing guidelines | Lead Developer |
| 1.1 | 2024-03-21 | Added Garmin Connect testing | Lead Developer | 