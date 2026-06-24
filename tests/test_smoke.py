import os


def test_backend_pycache_exists():
    assert os.path.isdir("backend/__pycache__"), "backend/__pycache__ should exist"



def test_backend_routes_exists():
    assert os.path.isdir("backend/routes"), "backend/routes should exist"


def test_frontend_lockfile_exists():
    assert os.path.isfile("frontend/package-lock.json"), "frontend/package-lock.json should exist"


def test_license_present():
    assert os.path.isfile("LICENSE"), "LICENSE file should be present in repo root"
