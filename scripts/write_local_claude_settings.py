#!/usr/bin/env python
import argparse
import json
import os
from pathlib import Path


ENV_KEYS = [
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_BASE_URL",
    "ANTHROPIC_MODEL",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL",
    "ANTHROPIC_DEFAULT_SONNET_MODEL",
    "ANTHROPIC_DEFAULT_OPUS_MODEL",
    "CLAUDE_CODE_EFFORT_LEVEL",
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS",
    "DISABLE_AUTOUPDATER",
    "ENABLE_TOOL_SEARCH",
]

REQUIRED_KEYS = [
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_BASE_URL",
    "ANTHROPIC_MODEL",
]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Write COURSE_DIR/.claude/settings.local.json from current process environment without printing secrets."
    )
    parser.add_argument("course_dir", help="Course root directory")
    args = parser.parse_args()

    missing = [key for key in REQUIRED_KEYS if not os.environ.get(key)]
    if missing:
        print(
            "missing required environment variables: "
            + ", ".join(missing)
            + "\nDo not paste secrets into a Write/Edit payload. Restart Claude with these env values available.",
            flush=True,
        )
        return 2

    env = {key: os.environ[key] for key in ENV_KEYS if os.environ.get(key)}
    settings = {
        "env": env,
        "skipDangerousModePermissionPrompt": True,
        "autoCompactEnabled": False,
    }

    course_dir = Path(args.course_dir).resolve()
    output = course_dir / ".claude" / "settings.local.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {output} (secrets not printed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
