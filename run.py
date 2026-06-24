from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
from pathlib import Path


def start_process(cmd, cwd):
    shell = os.name == "nt" and isinstance(cmd, str)
    return subprocess.Popen(
        cmd,
        cwd=str(cwd),
        env=os.environ.copy(),
        shell=shell,
    )


def main():
    root = Path(__file__).resolve().parent

    backend_cmd = [sys.executable, str(root / "backend" / "main.py")]
    frontend_cmd = "npm run dev" if os.name == "nt" else ["npm", "run", "dev"]

    print("Starting backend...")
    backend_proc = start_process(backend_cmd, root)
    print("Starting frontend...")
    frontend_proc = start_process(frontend_cmd, root / "frontend")

    print("\n=== Running ===")
    print("Backend: http://127.0.0.1:8000")
    print("Frontend: http://localhost:5173")
    print("Press Ctrl+C to stop both servers.\n")

    processes = [backend_proc, frontend_proc]

    def terminate():
        for proc in processes:
            if proc and proc.poll() is None:
                proc.terminate()
        time.sleep(1)
        for proc in processes:
            if proc and proc.poll() is None:
                proc.kill()

    try:
        while True:
            for proc in processes:
                if proc.poll() is not None:
                    raise KeyboardInterrupt
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping servers...")
        terminate()
    finally:
        terminate()


if __name__ == "__main__":
    main()
