"""Run the full project test suite and frontend test commands.

This runner is intentionally minimal because the repository does not contain
backend application source files, only compiled Python cache files and tests.

- Backend tests: runs pytest for the entire repository.
- Frontend tests: runs npm test in the frontend directory.

Note: `npm test` requires frontend dependencies to be installed first.
"""

import os
import subprocess
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")


def run_pytest():
    print("Running backend tests with pytest...")
    result = subprocess.run([sys.executable, "-m", "pytest", "-v"], cwd=ROOT_DIR)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def find_npm_command():
    npm_cmd = "npm"
    if os.name == "nt":
        npm_cmd = "npm.cmd"

    for path_dir in os.environ.get("PATH", "").split(os.pathsep):
        candidate = os.path.join(path_dir, npm_cmd)
        if os.path.isfile(candidate):
            return candidate
    return npm_cmd


def run_frontend_tests():
    print("Running frontend tests with npm...")
    if not os.path.isdir(FRONTEND_DIR):
        print("Skipping frontend tests: frontend directory not found.")
        return
    npm_cmd = [find_npm_command(), "test"]
    result = subprocess.run(npm_cmd, cwd=FRONTEND_DIR)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def print_usage():
    print("Usage:")
    print("  python run.py           # run backend and frontend tests")
    print("  python run.py all       # run backend and frontend tests")
    print("  python run.py backend   # run backend tests only")
    print("  python run.py frontend  # run frontend tests only")


def main():
    mode = "all"
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()

    if mode in {"all", ""}:
        run_pytest()
        run_frontend_tests()
    elif mode == "backend":
        run_pytest()
    elif mode == "frontend":
        run_frontend_tests()
    else:
        print(f"Unknown mode: {mode}\n")
        print_usage()
        raise SystemExit(1)

    print("All configured checks completed successfully.")


if __name__ == "__main__":
    main()
