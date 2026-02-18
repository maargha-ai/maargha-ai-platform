# LINTING AND CODE QUALITY GUIDE

## Overview
This document outlines the comprehensive linting and code quality standards implemented across all Maargha backend services.

## Linting Tools Configured

### 1. **Black** - Code Formatting
- **Purpose**: Automatic code formatting
- **Configuration**: 88 character line length, Python 3.11 target
- **Usage**: `black --check .` (CI) or `black .` (local)

### 2. **isort** - Import Sorting
- **Purpose**: Automatic import sorting
- **Configuration**: Black profile compatibility
- **Usage**: `isort --check-only .` (CI) or `isort .` (local)

### 3. **flake8** - Style Guide Enforcement
- **Purpose**: PEP 8 style guide compliance
- **Configuration**: 88 character line length, ignore E203/W503
- **Usage**: `flake8 .`

### 4. **mypy** - Type Checking
- **Purpose**: Static type checking
- **Configuration**: Strict mode with external library ignores
- **Usage**: `mypy app/` or `mypy user_service/`

### 5. **bandit** - Security Linting
- **Purpose**: Security vulnerability detection
- **Configuration**: Exclude tests, skip common false positives
- **Usage**: `bandit -r app/`

### 6. **pydocstyle** - Documentation Standards
- **Purpose**: Docstring format compliance
- **Configuration**: Google convention with selective ignores
- **Usage**: `pydocstyle .`

### 7. **autoflake** - Dead Code Removal
- **Purpose**: Remove unused imports and variables
- **Configuration**: Preserve init module imports
- **Usage**: `autoflake --in-place --remove-all-unused-imports .`

## Pre-commit Hooks

All services include comprehensive pre-commit configuration that runs:
- ✅ Trailing whitespace removal
- ✅ End-of-file fixer
- ✅ YAML validation
- ✅ Large file detection
- ✅ Merge conflict detection
- ✅ Debug statement detection
- ✅ Black formatting
- ✅ isort import sorting
- ✅ flake8 style checking
- ✅ mypy type checking
- ✅ bandit security scanning
- ✅ pydocstyle documentation checking
- ✅ autoflake dead code removal

## Service-Specific Configurations

### Orchestrator Service (FastAPI)
```yaml
# .pre-commit-config.yaml
# pyproject.toml with FastAPI-specific ignores
```

### Gateway Service (FastAPI)
```yaml
# .pre-commit-config.yaml
# pyproject.toml with gateway-specific ignores
```

### User Service (Django)
```yaml
# .pre-commit-config.yaml
# pyproject.toml with Django-specific ignores
```

## CI/CD Integration

The linting pipeline includes:
1. **Parallel Linting Jobs**: Each service linted independently
2. **Comprehensive Checks**: All linting tools run in CI
3. **Fail Fast**: Any linting failure blocks deployment
4. **Coverage Integration**: Linting passes before testing

## Local Development Setup

### Installation
```bash
# Install pre-commit hooks
pip install pre-commit

# Install hooks in all services
cd backend/orchestrator-service && pre-commit install
cd ../gateway-service && pre-commit install
cd ../user-service && pre-commit install
```

### Manual Linting
```bash
# Format code
black . && isort .

# Check linting
flake8 . && mypy . && bandit -r .

# Clean up dead code
autoflake --in-place --remove-all-unused-imports .
```

## Quality Standards

### Code Style
- **Line Length**: Maximum 88 characters
- **Import Style**: Sorted and grouped
- **Documentation**: Google-style docstrings
- **Type Hints**: Required for all functions

### Security Standards
- **No Hardcoded Secrets**: Bandit scanning
- **SQL Injection Protection**: Django ORM usage
- **Input Validation**: FastAPI request validation
- **Dependency Security**: Regular vulnerability scanning

### Performance Standards
- **Import Optimization**: Remove unused imports
- **Dead Code Elimination**: Automatic cleanup
- **Type Safety**: Strict mypy configuration
- **Documentation Coverage**: Required for public APIs

## Troubleshooting

### Common Issues
1. **Black vs isort conflicts**: Use same profile configuration
2. **mypy false positives**: Add to ignore list in pyproject.toml
3. **bandit test failures**: Exclude test directories
4. **pre-commit hook failures**: Run `pre-commit run --all-files`

### Fix Commands
```bash
# Auto-fix formatting issues
black . && isort .

# Remove unused imports
autoflake --in-place --remove-all-unused-imports .

# Check specific issues
flake8 --select=E203,W503 .
mypy --ignore-missing-imports app/
```

## Quality Metrics

Each service maintains:
- **80% Test Coverage**: Minimum threshold
- **Zero Linting Errors**: CI gate requirement
- **Documentation Coverage**: Public APIs documented
- **Security Score**: Bandit clean scans
- **Type Coverage**: Mypy strict mode

## Benefits

1. **Consistent Code**: Automatic formatting across team
2. **Early Error Detection**: Linting catches issues before runtime
3. **Security Focus**: Automated vulnerability scanning
4. **Developer Productivity**: Pre-commit hooks save time
5. **Quality Gates**: CI/CD ensures standards compliance

## Next Steps

1. **IDE Integration**: Configure editor linting plugins
2. **Team Training**: Ensure everyone understands standards
3. **Regular Updates**: Keep linting tools current
4. **Metrics Tracking**: Monitor code quality over time
