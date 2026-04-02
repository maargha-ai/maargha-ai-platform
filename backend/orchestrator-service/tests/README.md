# Testing Guide

This directory contains comprehensive tests for the Maargha Orchestrator service.

## Test Structure

```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── test_logger.py           # Unit tests for logging system
├── test_health.py           # Unit tests for health endpoints
├── test_websocket.py        # Unit tests for WebSocket handlers
├── test_integration.py       # Integration tests for full system
└── pytest.ini             # Pytest configuration
```

## Running Tests

### Prerequisites
```bash
# Install test dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

### Run All Tests
```bash
# Run all tests with coverage
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=app --cov-report=html
```

### Run Specific Test Categories
```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only WebSocket tests
pytest -m websocket

# Run only monitoring tests
pytest -m monitoring
```

### Run Specific Test Files
```bash
# Run logger tests
pytest tests/test_logger.py -v

# Run health tests
pytest tests/test_health.py -v

# Run WebSocket tests
pytest tests/test_websocket.py -v

# Run integration tests
pytest tests/test_integration.py -v
```

## Test Coverage

The test suite covers:
- ✅ Logging system functionality
- ✅ Health check endpoints
- ✅ WebSocket connection handling
- ✅ Performance monitoring
- ✅ API endpoint integration
- ✅ Database connectivity
- ✅ Error handling
- ✅ CORS configuration

## Coverage Reports

After running tests with coverage:
- HTML report: `htmlcov/index.html`
- Terminal coverage: Shown in terminal
- Coverage threshold: 80% minimum

## Test Categories

### Unit Tests (`test_*.py`)
- **test_logger.py**: Tests StructuredLogger, PerformanceMonitor, LoggingMiddleware
- **test_health.py**: Tests health check endpoints and utility functions
- **test_websocket.py**: Tests WebSocket message handling and error scenarios

### Integration Tests (`test_integration.py`)
- **API Integration**: Tests full API request/response cycles
- **WebSocket Integration**: Tests WebSocket upgrade and message flow
- **Database Integration**: Tests database initialization and connectivity
- **Monitoring Integration**: Tests monitoring system integration
- **Error Handling**: Tests graceful error handling across the system

## Mock Strategy

Tests use comprehensive mocking:
- **WebSocket Mocking**: Mock WebSocket connections for isolated testing
- **Database Mocking**: Mock database connections for fast, reliable tests
- **External Service Mocking**: Mock external APIs (Groq, etc.)
- **Logger Mocking**: Mock loggers to verify logging behavior

## Fixtures

Common test fixtures available in `conftest.py`:
- `mock_websocket()`: Pre-configured WebSocket mock
- `mock_performance_monitor()`: Mock performance monitor
- `mock_logger()`: Mock orchestrator logger
- `sample_graph_response()`: Sample AI agent response
- `sample_navigation_response()`: Sample navigation response

## Continuous Integration

Add to your CI/CD pipeline:

```yaml
# GitHub Actions example
- name: Run Tests
  run: |
    pip install -r requirements.txt
    pytest --cov=app --cov-report=xml
- name: Upload Coverage
  uses: codecov/codecov-action@v1
```

## Best Practices

1. **Test Isolation**: Each test is independent and doesn't rely on state
2. **Comprehensive Mocking**: External dependencies are mocked for reliable tests
3. **Error Scenarios**: Both success and failure paths are tested
4. **Performance Testing**: Response times and metrics are validated
5. **Security Testing**: CORS, authentication, and authorization are tested

## Debugging Failed Tests

```bash
# Run with maximum verbosity
pytest -vvs -s tests/test_failing.py

# Run with debugger
pytest --pdb tests/test_failing.py

# Run specific test
pytest tests/test_file.py::TestClass::test_method -vvs
```

## Adding New Tests

1. Create test file following naming convention: `test_<module>.py`
2. Use appropriate markers: `@pytest.mark.unit`, `@pytest.mark.integration`
3. Follow existing patterns for fixtures and mocking
4. Add test documentation and comments
5. Update this README with new test coverage

## Test Data

Tests use realistic but sanitized data:
- Sample user messages
- Mock API responses
- Typical error scenarios
- Edge cases and boundary conditions

## Performance Benchmarks

Some tests include performance assertions:
- Response time limits
- Memory usage monitoring
- Connection limits
- Error rate thresholds
