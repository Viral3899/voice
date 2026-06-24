# Test Suite Documentation

This directory contains comprehensive test suites for the Voice AI Agent project. The tests are organized by layer and scope.

## Test Structure

### Backend Tests (Python + pytest)

#### 1. **test_smoke.py** - Smoke Tests
Basic structural tests to verify project setup.
- Verifies directories exist
- Checks for required files
- Validates basic project structure

Run: `pytest tests/test_smoke.py -v`

#### 2. **test_backend_api.py** - API Tests
Integration tests for backend routes and endpoints.
- Tests HTTP endpoints
- Validates request/response handling
- Tests authentication and authorization
- Verifies error handling

Run: `pytest tests/test_backend_api.py -v`

Classes:
- `TestBackendAPI` - Route endpoint tests
- `TestAuthentication` - Auth and token tests
- `TestDataValidation` - Input validation tests
- `TestErrorHandling` - Error scenario tests
- `TestPerformance` - Performance requirement tests

#### 3. **test_backend_unit.py** - Unit Tests
Unit tests for backend components and utilities.
- Audio processing functions
- Speech-to-text conversion
- AI response generation
- Database operations
- Utility functions

Run: `pytest tests/test_backend_unit.py -v`

Classes:
- `TestAudioProcessing` - Audio manipulation tests
- `TestTranscription` - Speech-to-text tests
- `TestAIResponse` - AI response generation tests
- `TestTextToSpeech` - TTS synthesis tests
- `TestDatabaseOperations` - Database CRUD tests
- `TestUtilityFunctions` - Helper function tests
- `TestDataModels` - Model instantiation tests
- `TestCaching` - Cache mechanism tests

#### 4. **test_integration.py** - Integration Tests
End-to-end and integration tests.
- Full voice conversation flows
- Frontend-backend communication
- Data persistence
- External service integration
- Complete user scenarios
- Security tests
- Error recovery

Run: `pytest tests/test_integration.py -v -m integration`

Classes:
- `TestFullVoiceConversationFlow` - Complete conversation cycle
- `TestFrontendBackendIntegration` - API communication
- `TestDataPersistence` - Data storage and retrieval
- `TestExternalIntegrations` - Third-party service integration
- `TestEndToEndScenarios` - Complete user workflows
- `TestPerformanceIntegration` - Performance under load
- `TestSecurityIntegration` - Security measures
- `TestErrorRecovery` - Error recovery mechanisms

#### 5. **conftest.py** - Pytest Fixtures
Shared fixtures and configuration for all backend tests.

Fixtures:
- `mock_database` - Mock database connection
- `mock_audio_file` - Mock audio file
- `mock_user_session` - Mock user session data
- `mock_conversation` - Mock conversation data
- `mock_api_key` - Mock API key
- `mock_config` - Mock configuration
- `temp_audio_file` - Temporary audio file
- `temp_config_file` - Temporary config file
- `event_loop` - Async event loop
- `mock_logger` - Mock logger
- `cli_runner` - CLI test runner
- `http_client` - Mock HTTP client

#### 6. **pytest.ini** - Pytest Configuration
Configuration file for pytest.

### Frontend Tests (JavaScript + Jest)

#### 7. **test_frontend_unit.js** - Frontend Unit Tests
React component unit tests.
- Component rendering
- User interactions
- State management
- Props handling
- Event handling

Run: `npm test` (from frontend directory)

Test Suites:
- Voice Input Component
- Voice Display Component
- Conversation History
- Settings
- Authentication
- API Communication
- UI Integration
- Form Validation
- State Management
- Performance
- Accessibility

#### 8. **test_frontend_integration.js** - Frontend Integration Tests
Frontend user flow and integration tests.
- Complete voice interaction flows
- Session management
- Conversation management
- Backend communication
- User preferences
- Error scenarios
- Performance
- Responsive design
- Accessibility

Run: `npm run test:integration` (from frontend directory)

Test Suites:
- Voice Interaction Flow
- Session Management
- Conversation Management
- Backend Communication
- User Preferences
- Error Scenarios
- Performance and Optimization
- Responsive Design
- Accessibility

#### 9. **jest.config.js** - Jest Configuration
Configuration for Jest test runner.

#### 10. **setup.js** - Jest Setup
Global test setup and mocks for Jest.

## Running Tests

### Run All Tests
```bash
# Backend
pytest -v

# Frontend
npm test
```

### Run Specific Test Suite
```bash
# Smoke tests
pytest tests/test_smoke.py -v

# API tests
pytest tests/test_backend_api.py -v

# Unit tests
pytest tests/test_backend_unit.py -v

# Integration tests
pytest tests/test_integration.py -v

# Only integration tests
pytest tests/test_integration.py -v -m integration

# Only unit tests
pytest tests/test_backend_unit.py -v
```

### Run Tests by Marker
```bash
# Run only slow tests
pytest -v -m slow

# Run everything except slow tests
pytest -v -m "not slow"

# Run integration tests
pytest -v -m integration

# Run end-to-end tests
pytest -v -m e2e

# Run external service tests
pytest -v -m external
```

### Frontend Tests
```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test file
npm test test_frontend_unit.js

# Run in watch mode
npm test -- --watch

# Run integration tests
npm run test:integration
```

## Test Markers (pytest)

- `@pytest.mark.slow` - Slow tests (deselect with `-m "not slow"`)
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.e2e` - End-to-end tests
- `@pytest.mark.external` - Tests requiring external services
- `@pytest.mark.unit` - Unit tests

## Coverage

### Backend Coverage
```bash
pytest --cov=backend --cov-report=html
```

This generates an HTML coverage report in `htmlcov/index.html`.

### Frontend Coverage
```bash
npm test -- --coverage
```

## Writing New Tests

### Backend (pytest)
1. Create a test file: `test_<module>.py`
2. Import pytest
3. Create test classes with `Test` prefix
4. Create test methods with `test_` prefix
5. Use fixtures from `conftest.py`
6. Add appropriate markers

Example:
```python
import pytest

@pytest.mark.unit
def test_something(mock_database):
    # Arrange
    # Act
    # Assert
    pass
```

### Frontend (Jest)
1. Add tests to `test_frontend_*.js` files
2. Use describe/test blocks
3. Import needed components
4. Use Jest matchers

Example:
```javascript
test('should do something', () => {
  // Arrange
  // Act
  // Assert
  expect(result).toBe(expected);
});
```

## Test Conventions

### Naming
- Test files: `test_<feature>.py` or `<feature>.test.js`
- Test classes: `Test<Feature>`
- Test methods: `test_<specific_behavior>`

### Structure
1. **Arrange** - Set up test data and conditions
2. **Act** - Execute the code being tested
3. **Assert** - Verify the results

### Best Practices
- One assertion concept per test
- Clear, descriptive test names
- Use fixtures to reduce duplication
- Mock external dependencies
- Keep tests focused and fast
- Avoid testing implementation details

## CI/CD Integration

These tests are designed to run in CI/CD pipelines:

```bash
# Run all tests with coverage
pytest -v --cov=backend --cov-report=xml && npm test -- --coverage
```

## Troubleshooting

### Backend Issues
- Missing fixtures: Check `conftest.py`
- Import errors: Verify `sys.path` in conftest
- Database errors: Use mock_database fixture

### Frontend Issues
- Missing modules: Run `npm install`
- Jest not found: Check jest.config.js
- Test timeouts: Increase timeout in jest.config.js

## TODO: Implement Tests

When implementing actual source code, fill in the test bodies with real implementations that:
- Set up test data
- Call the function/method
- Assert on results
- Clean up resources

Each test class has multiple test methods ready to be implemented with actual test logic.
