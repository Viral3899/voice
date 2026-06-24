"""
Smoke tests for basic project structure verification
"""
import os


def test_backend_pycache_exists():
    assert os.path.isdir("backend/__pycache__"), "backend/__pycache__ should exist"


def test_backend_routes_exists():
    assert os.path.isdir("backend/routes"), "backend/routes should exist"


def test_frontend_lockfile_exists():
    assert os.path.isfile("frontend/package-lock.json"), "frontend/package-lock.json should exist"


def test_license_present():
    assert os.path.isfile("LICENSE"), "LICENSE file should be present in repo root"


def test_backend_structure():
    """Verify backend directory structure"""
    assert os.path.isdir("backend"), "backend directory should exist"
    assert os.path.isdir("backend/routes"), "backend/routes directory should exist"


def test_frontend_structure():
    """Verify frontend directory structure"""
    assert os.path.isdir("frontend"), "frontend directory should exist"
    assert os.path.isfile("frontend/package.json"), "frontend/package.json should exist"


def test_tests_directory():
    """Verify tests directory exists"""
    assert os.path.isdir("tests"), "tests directory should exist"


def test_test_files_exist():
    """Verify all test files are present"""
    test_files = [
        "tests/test_smoke.py",
        "tests/test_backend_api.py",
        "tests/test_backend_unit.py",
        "tests/test_integration.py",
        "tests/conftest.py",
        "tests/pytest.ini"
    ]
    for test_file in test_files:
        assert os.path.isfile(test_file), f"{test_file} should exist"
