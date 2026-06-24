// Jest configuration for frontend tests
module.exports = {
  testEnvironment: 'jsdom',
  roots: ['<rootDir>'],
  testMatch: ['**/test_frontend_unit.js', '**/test_frontend_integration.js'],
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    '\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$': '<rootDir>/__mocks__/fileMock.js',
  },
  setupFilesAfterEnv: ['<rootDir>/setup.js'],
  collectCoverageFrom: [
    '../frontend/src/**/*.{js,jsx}',
    '!../frontend/src/index.js',
    '!../frontend/src/reportWebVitals.js',
  ],
  coverageThreshold: {
    global: {
      branches: 50,
      functions: 50,
      lines: 50,
      statements: 50,
    },
  },
  transform: {
    '^.+\\.[jt]sx?$': 'babel-jest',
  },
  moduleDirectories: ['node_modules', '../frontend/src'],
  testTimeout: 5000,
  verbose: true,
};
