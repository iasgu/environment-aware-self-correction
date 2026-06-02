#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import locale
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


SENSITIVE_MARKERS = ("KEY", "TOKEN", "SECRET", "PASSWORD", "COOKIE", "CREDENTIAL")


def run_command(args: list[str], timeout: int = 5) -> dict:
    try:
        completed = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return {
            "ok": completed.returncode == 0,
            "returncode": completed.returncode,
            "stdout": completed.stdout.strip()[:1000],
            "stderr": completed.stderr.strip()[:1000],
        }
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__ + ": " + str(exc)}


def command_path(name: str) -> str:
    return shutil.which(name) or ""


def safe_env_snapshot(keys: list[str]) -> dict:
    result = {}
    for key in keys:
        value = os.environ.get(key)
        if value is None:
            result[key] = {"present": False}
            continue
        if any(marker in key.upper() for marker in SENSITIVE_MARKERS):
            result[key] = {"present": True, "redacted": True}
        else:
            result[key] = {"present": True, "value": value[:300]}
    return result


def count_non_ascii_paths(root: Path, limit: int) -> dict:
    examples = []
    count = 0
    if not root.exists():
        return {"root_exists": False, "count": 0, "examples": []}
    for path in root.rglob("*"):
        text = str(path)
        if any(ord(ch) > 127 for ch in text):
            count += 1
            if len(examples) < limit:
                examples.append(text)
    return {"root_exists": True, "count": count, "examples": examples}


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe local environment for shell, encoding, tooling, and path risks.")
    parser.add_argument("--project-root", default=".", help="Project root to inspect.")
    parser.add_argument("--path-sample-limit", type=int, default=5, help="Number of non-ASCII path examples.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON.")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    tools = ["python", "git", "docker", "node", "npm", "gh", "powershell", "pwsh", "cmd"]
    payload = {
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "platform": platform.platform(),
        },
        "python": {
            "executable": sys.executable,
            "version": sys.version.replace("\n", " "),
            "filesystem_encoding": sys.getfilesystemencoding(),
            "default_encoding": sys.getdefaultencoding(),
            "preferred_encoding": locale.getpreferredencoding(False),
            "stdin_encoding": getattr(sys.stdin, "encoding", None),
            "stdout_encoding": getattr(sys.stdout, "encoding", None),
            "stderr_encoding": getattr(sys.stderr, "encoding", None),
        },
        "project": {
            "root": str(project_root),
            "cwd": str(Path.cwd()),
            "non_ascii_paths": count_non_ascii_paths(project_root, args.path_sample_limit),
        },
        "tools": {name: command_path(name) for name in tools},
        "environment": safe_env_snapshot(
            [
                "COMSPEC",
                "SHELL",
                "TERM",
                "PYTHONUTF8",
                "PYTHONIOENCODING",
                "PYTHONLEGACYWINDOWSSTDIO",
                "LANG",
                "LC_ALL",
                "FRONTEND_API_PORT",
                "SEARCH_BACKEND_PROVIDER",
                "SEARXNG_URL",
                "GH_TOKEN",
                "GITHUB_TOKEN",
            ]
        ),
        "git": run_command(["git", "status", "--short"], timeout=5) if command_path("git") else {"ok": False, "error": "git not found"},
        "docker": run_command(["docker", "ps", "--format", "{{.Names}}\t{{.Status}}\t{{.Ports}}"], timeout=8)
        if command_path("docker")
        else {"ok": False, "error": "docker not found"},
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
