#!/usr/bin/env python
import os
import subprocess
import sys
import tempfile
from pathlib import Path

if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: invoke-python-hook.py <hook.py>", file=sys.stderr)
        return 2

    hook_path = Path(sys.argv[1]).resolve()
    payload = sys.stdin.read().lstrip("\ufeff")
    fd, temp_path = tempfile.mkstemp(suffix=".json")
    os.close(fd)

    try:
        Path(temp_path).write_text(payload, encoding="utf-8")
        return subprocess.run(
            [sys.executable, "-X", "utf8", str(hook_path), "--payload-file", temp_path],
            check=False,
        ).returncode
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
