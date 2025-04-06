# RunningGPT Test Plan

## 1. Overview
This document outlines the testing strategy for RunningGPT, including both manual and automated testing procedures.

## 2. Test Environment Setup

### 2.1 Prerequisites
- Python 3.11 or 3.12
- Virtual environment (.venv)
- All dependencies installed from requirements.txt
- Sample workout data in workout_reports and workout_plots directories

### 2.2 Test Mode
RunningGPT includes a test mode that can be activated using the `--test` flag:
```bash
python gui/main.py --test
```

The test mode provides the following features:
- Skips authentication process
- Loads existing workout data
- Jumps directly to the results page
- Displays workout cards and analysis
- Pre-initializes AI Assistant

## 3. Test Cases

### 3.1 GUI Testing

#### 3.1.1 Normal Mode
1. **Authentication**
   - Test valid credentials
   - Test invalid credentials
   - Test network connectivity issues

2. **Activity Selection**
   - Test running activity selection
   - Test cycling activity selection
   - Test swimming activity selection

3. **Workout Processing**
   - Test single workout processing
   - Test multiple workout processing
   - Test workout data visualization

4. **AI Assistant Integration**
   - Test chat functionality
   - Test workout analysis
   - Test training recommendations

#### 3.1.2 Test Mode
1. **Direct Results Access**
   - Verify automatic loading of workout data
   - Verify correct display of workout cards
   - Verify plot generation and display

2. **AI Assistant Pre-initialization**
   - Verify AI Assistant availability
   - Test chat functionality without authentication
   - Test workout analysis in test mode

### 3.2 Data Processing Testing

1. **FIT File Processing**
   - Test FIT file download
   - Test FIT to CSV conversion
   - Verify data integrity

2. **Analysis Generation**
   - Test workout statistics calculation
   - Test plot generation
   - Test report generation

### 3.3 Error Handling

1. **Network Issues**
   - Test behavior with no internet connection
   - Test behavior with slow connection
   - Test reconnection handling

2. **Data Issues**
   - Test handling of corrupted FIT files
   - Test handling of incomplete workout data
   - Test handling of missing metrics

## 4. Unit Testing

### 4.1 Unit Test Framework
RunningGPT uses pytest as the primary unit testing framework. Unit tests are located in the `tests/` directory and follow the naming convention `test_*.py`.

### 4.2 Test Structure
```
tests/
├── __init__.py
├── conftest.py                  # Shared fixtures
├── test_ai_assistant.py         # AI Assistant tests
├── test_analysis_running_CSV.py # CSV analysis tests
├── test_decode_fit.py           # FIT file decoding tests
├── test_garminconnect.py        # Garmin Connect API tests
├── test_get_workouts_data.py    # Workout data retrieval tests
└── cassettes/                   # VCR cassettes for API mocking
```

### 4.3 Running Unit Tests

#### Windows
```powershell
# Make sure you're in your virtual environment
.\.venv\Scripts\activate

# Set environment variable and run tests
$env:GARMINTOKENS="C:\Users\$env:USERNAME\.garminconnect"; python -m pytest tests/

# Run specific test file
python -m pytest tests/test_ai_assistant.py

# Run with coverage report
python -m pytest --cov=. tests/
```

#### Linux/macOS
```bash
# Set environment variable
export GARMINTOKENS=~/.garminconnect

# Run all tests
python -m pytest tests/

# Run with coverage report
python -m pytest --cov=. tests/
```

### 4.4 Test Dependencies
Unit tests require additional packages:
```bash
pip install pytest pytest-vcr pytest-cov coverage
```

### 4.5 Mocking External Services
Tests use VCR.py to record and replay HTTP interactions:
- First run: Records actual API calls
- Subsequent runs: Uses recorded responses
- Ensures tests are deterministic and don't require internet connection

### 4.6 Key Unit Test Areas

1. **AI Assistant Tests**
   - Test message analysis
   - Test workout recommendations
   - Test error handling
   - Test context management

2. **Data Processing Tests**
   - Test FIT file parsing
   - Test CSV conversion
   - Test statistics calculation
   - Test plot generation

3. **API Integration Tests**
   - Test Garmin Connect authentication
   - Test workout data retrieval
   - Test error handling for API failures

4. **GUI Component Tests**
   - Test window creation
   - Test API exposure to JavaScript
   - Test event handling
   - Test test mode functionality

### 4.7 Test Fixtures
Common test fixtures are defined in `conftest.py`:
- Mock Garmin Connect client
- Sample workout data
- Temporary directories for test outputs
- Environment variable setup

### 4.8 Continuous Integration
Unit tests are automatically run on:
- Pull requests to main branch
- Daily scheduled builds
- Before each release

## 5. Test Execution

### 5.1 Manual Testing
1. Run the application in normal mode
2. Complete each step of the wizard
3. Verify all features and functionality
4. Document any issues or bugs

### 5.2 Test Mode Testing
1. Run the application with --test flag
2. Verify automatic loading of workout data
3. Test AI Assistant functionality
4. Verify all visualizations and reports

## 6. Test Results

### 6.1 Documentation
- Record all test results
- Document any bugs or issues
- Note performance metrics
- Track test coverage

### 6.2 Bug Reporting
- Use issue tracking system
- Include steps to reproduce
- Attach relevant logs
- Provide system information

## 7. Test Schedule

### 7.1 Regular Testing
- Run full test suite before each release
- Perform weekly regression testing
- Conduct monthly performance testing

### 7.2 Continuous Integration
- Automated tests on pull requests
- Daily build verification
- Weekly integration testing

## 8. Test Tools

### 8.1 Required Tools
- Python testing frameworks
- Browser developer tools
- Network monitoring tools
- Performance profiling tools

### 8.2 Test Data
- Sample workout files
- Test user accounts
- Mock API responses
- Test environment configurations

## 9. Test Maintenance

### 9.1 Test Updates
- Update test cases for new features
- Maintain test documentation
- Review and update test data
- Optimize test performance

### 9.2 Test Environment
- Keep test environment updated
- Maintain test data freshness
- Update dependencies regularly
- Monitor test execution times 

## 10. Version History
| Version | Date | Description | Author |
|---------|------|-------------|---------|
| 1.0 | 2025-04-04 | Initial test plan | QA Lead | 
| 1.1 | 2025-04-05 | Added Test mode | QA Lead | 