# LINTING AND CODE QUALITY GUIDE

## Overview
This document outlines the linting and code quality standards implemented across all Maargha backend services.

## Linting Tools Configured

### 1. **pylint** - Code Quality Analysis
- **Purpose**: Comprehensive code quality checking, error detection, and style enforcement
- **Configuration**: 88 character line length, selective rule disables
- **Usage**: `pylint app/` or `pylint user_service/`

#### Disabled Rules
- `C0114`: missing-module-docstring
- `C0115`: missing-class-docstring  
- `C0116`: missing-function-docstring
- `R0903`: too-few-public-methods

#### Design Limits
- Max arguments: 10
- Max locals: 15
- Max returns: 6
- Max branches: 12
- Max statements: 50
- Max parents: 7
- Max attributes: 7

## Testing

### 2. **pytest** - Testing Framework
- **Purpose**: Unit and integration testing
- **Configuration**: Coverage reporting with 40% minimum threshold
- **Usage**: `pytest --cov=app --cov-report=xml --cov-fail-under=40`

## CI/CD Integration

The linting pipeline includes:
1. **Parallel Linting Jobs**: Each service linted independently with pylint
2. **Testing Jobs**: Each service tested with pytest and coverage
3. **Fail Fast**: Any linting or testing failure blocks deployment
4. **Coverage Integration**: Coverage reports uploaded to Codecov

## Service-Specific Configurations

### Orchestrator Service (FastAPI)
```toml
[tool.pylint.messages_control]
disable = [
    "C0114",  # missing-module-docstring
    "C0115",  # missing-class-docstring
    "C0116",  # missing-function-docstring
    "R0903",  # too-few-public-methods
]

[tool.pylint.format]
max-line-length = 88
```

### Gateway Service (FastAPI)
```toml
[tool.pylint.messages_control]
disable = [
    "C0114",  # missing-module-docstring
    "C0115",  # missing-class-docstring
    "C0116",  # missing-function-docstring
    "R0903",  # too-few-public-methods
    "R0915",  # too-many-statements
    "R0801",  # duplicate-code
    "W0718",  # broad-exception-caught
    "W0611",  # unused-import
    "C0411",  # import-outside-toplevel
    "W0707",  # raise-missing-from
    "W1514",  # wrong-import-order
]

[tool.pylint.format]
max-line-length = 88
```

### User Service (Django)
```toml
[tool.pylint.messages_control]
disable = [
    "C0114",  # missing-module-docstring
    "C0115",  # missing-class-docstring
    "C0116",  # missing-function-docstring
    "R0903",  # too-few-public-methods
]

[tool.pylint.format]
max-line-length = 88
```

## Local Development Setup

### Installation
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run linting manually
pylint app/  # or pylint user_service/
```

### Testing
```bash
# Run tests with coverage
pytest --cov=app --cov-report=xml --cov-fail-under=40
```

## Quality Standards

### Code Style
- **Line Length**: Maximum 88 characters
- **Error Detection**: Pylint comprehensive checking
- **Test Coverage**: Minimum 40% threshold

## Troubleshooting

### Common Issues
1. **Pylint false positives**: Add to disable list in pyproject.toml
2. **Test failures**: Check test environment setup
3. **Coverage below threshold**: Add more tests or adjust threshold

### Fix Commands
```bash
# Check specific issues
pylint --disable=all --enable=E1131 app/

# Run specific tests
pytest tests/test_specific.py -v
```

## Quality Metrics

Each service maintains:
- **40% Test Coverage**: Minimum threshold
- **Zero Pylint Errors**: CI gate requirement
- **Clean Builds**: All linting passes before deployment

## Benefits

1. **Consistent Code**: Pylint enforces quality standards
2. **Early Error Detection**: Linting catches issues before runtime
3. **Quality Gates**: CI/CD ensures standards compliance
4. **Simplified Workflow**: Focused tooling reduces complexity
