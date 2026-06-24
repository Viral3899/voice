# Example Frontend Test Scripts

Add these scripts to your `frontend/package.json` to run the test suites:

```json
{
  "name": "voice-ai-agent-frontend",
  "private": true,
  "version": "0.0.1",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "test": "jest --watch",
    "test:run": "jest",
    "test:coverage": "jest --coverage",
    "test:unit": "jest test_frontend_unit.js",
    "test:integration": "jest test_frontend_integration.js",
    "test:ci": "jest --coverage --ci"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@vitejs/plugin-react-swc": "^4.3.1",
    "@testing-library/jest-dom": "^6.1.0",
    "@testing-library/react": "^14.0.0",
    "@testing-library/user-event": "^14.5.0",
    "babel-jest": "^29.7.0",
    "identity-obj-proxy": "^3.0.0",
    "jest": "^29.7.0",
    "jest-environment-jsdom": "^29.7.0",
    "vite": "^8.1.0"
  }
}
```

## Test Scripts Explained

| Script | Purpose |
|--------|---------|
| `npm test` | Run tests in watch mode (best for development) |
| `npm run test:run` | Run tests once (for CI/CD) |
| `npm run test:coverage` | Run tests and generate coverage report |
| `npm run test:unit` | Run only unit tests |
| `npm run test:integration` | Run only integration tests |
| `npm run test:ci` | Run tests optimized for CI environment |

## Installation Steps

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Add Jest devDependencies:
```bash
npm install --save-dev jest @testing-library/react @testing-library/jest-dom babel-jest
```

3. Copy test files to frontend/tests or __tests__ directory

4. Run tests:
```bash
npm test
```
