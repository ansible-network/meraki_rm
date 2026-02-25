"""Shared mock server lifecycle utilities.

Used by both the MCP server (``mcp/server.py``) and the CLI
(``cli/main.py``) to auto-start the stateful Flask mock server
for integration testing without a real Meraki API key.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

MOCK_PORT: int = 29443
MOCK_URL: str = f"http://127.0.0.1:{MOCK_PORT}"


def find_project_root() -> Path:
    """Walk up from this file to find the collection root (contains galaxy.yml).

    Returns:
        Path to the project root directory.
    """
    candidate = Path(__file__).resolve().parent
    for _ in range(10):
        if (candidate / "galaxy.yml").exists():
            return candidate
        candidate = candidate.parent
    return Path.cwd()


def start_mock_server() -> subprocess.Popen:
    """Start the mock server as a subprocess.

    Returns:
        The running Popen object.  The caller is responsible for termination.

    Raises:
        SystemExit: If the spec file is missing or the server fails health check.
    """
    root = find_project_root()
    spec = root / "spec3.json"
    if not spec.exists():
        print(
            f"ERROR: spec3.json not found at {spec}",
            file=sys.stderr,
        )
        sys.exit(1)

    proc = subprocess.Popen(
        [
            sys.executable, "-m", "tools.mock_server.server",
            "--spec", str(spec),
            "--port", str(MOCK_PORT),
        ],
        cwd=str(root),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    import urllib.error
    import urllib.request

    for _ in range(30):
        time.sleep(0.5)
        if proc.poll() is not None:
            print(
                f"ERROR: Mock server exited with code {proc.returncode}",
                file=sys.stderr,
            )
            sys.exit(1)
        try:
            urllib.request.urlopen(f"{MOCK_URL}/health", timeout=2)
            print(
                f"Mock server ready on {MOCK_URL} (pid {proc.pid})",
                file=sys.stderr,
            )
            return proc
        except (urllib.error.URLError, OSError):
            continue

    proc.kill()
    print("ERROR: Mock server failed to become healthy", file=sys.stderr)
    sys.exit(1)


def stop_mock_server(proc: subprocess.Popen) -> None:
    """Gracefully terminate a mock server subprocess.

    Args:
        proc: The Popen object returned by ``start_mock_server()``.
    """
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
