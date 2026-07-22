"""Run the API and web development servers as one interruptible process group."""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def stop(processes: list[subprocess.Popen[bytes]]) -> None:
    """Terminate each development server and any reload child it created."""

    for process in processes:
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)

    deadline = time.monotonic() + 5
    for process in processes:
        if process.poll() is not None:
            continue
        timeout = max(0, deadline - time.monotonic())
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)


def main() -> int:
    api_command = [
        sys.executable,
        "-m",
        "uvicorn",
        "services.api.main:app",
        "--host",
        os.getenv("API_HOST", "127.0.0.1"),
        "--port",
        os.getenv("API_PORT", "8000"),
    ]
    if os.getenv("API_RELOAD", "").lower() in {"1", "true", "yes"}:
        api_command.append("--reload")

    commands = [
        api_command,
        ["npm", "run", "dev", "--workspace", "@tendy-spider/web"],
    ]
    processes: list[subprocess.Popen[bytes]] = []

    try:
        for command in commands:
            processes.append(
                subprocess.Popen(
                    command,
                    cwd=REPOSITORY_ROOT,
                    start_new_session=True,
                )
            )

        while True:
            for process in processes:
                return_code = process.poll()
                if return_code is not None:
                    return return_code
            time.sleep(0.25)
    except KeyboardInterrupt:
        return 130
    finally:
        stop(processes)


if __name__ == "__main__":
    raise SystemExit(main())
