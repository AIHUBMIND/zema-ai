# Tests Folder Documentation

## Purpose
The `tests/` folder contains all test files for the Zema AI project. Tests ensure code quality and functionality correctness.

## Folder Structure

### `conftest.py`
Pytest configuration file. Defines shared fixtures and test configuration.

### `test_config.py`
Tests for configuration module. Tests Settings class, default values, validation.

### `unit/`
Unit tests for individual components. Tests each module in isolation.

### `integration/`
Integration tests for component interactions. Tests how modules work together.

### `hardware/`
Hardware-specific tests. Tests camera, audio devices, etc.

### `fixtures/`
Test fixtures and mock data. Reusable test data and mock objects.

## Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_config.py

# Run with coverage
pytest --cov=src tests/
```

## Test Structure
- Unit tests: Test individual functions/classes
- Integration tests: Test component interactions
- Hardware tests: Test hardware-specific functionality
- Fixtures: Shared test data and mocks

