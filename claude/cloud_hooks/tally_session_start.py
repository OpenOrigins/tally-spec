"""Forward Claude Code's command-only SessionStart event to Tally."""

import json
import os
import pathlib
import sys
import urllib.request

URL = os.environ.get("TALLY_HOOK_URL", "https://api.prod.openorigins.com/v1/tally/logs")


def read_json(path: pathlib.Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return value if isinstance(value, dict) else {}


def billing_type() -> str:
    """"api", "subscription" or "unknown", by Claude Code's credential precedence (as tally-claude)."""
    env = os.environ.get
    enabled = lambda key: env(key, "") not in ("", "0", "false")
    config_dir = env("CLAUDE_CONFIG_DIR")
    home = pathlib.Path.home()
    state = read_json(pathlib.Path(config_dir).expanduser() / ".claude.json" if config_dir else home / ".claude.json")
    user_dir = pathlib.Path(config_dir).expanduser() if config_dir else home / ".claude"
    project_dir = pathlib.Path(env("CLAUDE_PROJECT_DIR") or os.getcwd()) / ".claude"
    settings = [
        read_json(path)
        for path in (user_dir / "settings.json", project_dir / "settings.json", project_dir / "settings.local.json")
    ]

    if any(enabled(key) for key in ("CLAUDE_CODE_USE_BEDROCK", "CLAUDE_CODE_USE_VERTEX", "CLAUDE_CODE_USE_FOUNDRY")):
        return "api"
    if env("ANTHROPIC_AUTH_TOKEN"):
        return "api"
    key = env("ANTHROPIC_API_KEY")
    # A key declined at Claude Code's prompt isn't used; it's remembered by its last 20 characters.
    if key and key[-20:] not in ((state.get("customApiKeyResponses") or {}).get("rejected") or []):
        return "api"
    if any(item.get("apiKeyHelper") for item in settings):
        return "api"
    if env("CLAUDE_CODE_OAUTH_TOKEN"):
        return "subscription"
    if state.get("primaryApiKey"):
        return "api"
    if isinstance(state.get("oauthAccount"), dict) or enabled("CLAUDE_CODE_REMOTE"):
        return "subscription"
    return "unknown"


def main() -> None:
    key = os.environ.get("OO_API_KEY")
    if not key:
        raise SystemExit("OO_API_KEY is required for the Tally SessionStart hook")

    body = sys.stdin.buffer.read()
    try:
        payload = json.loads(body)
    except ValueError:
        payload = None
    if isinstance(payload, dict):
        payload["billing_type"] = billing_type()
        body = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        URL,
        data=body,
        headers={"Content-Type": "application/json", "x-api-key": key},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=10):
        pass


if __name__ == "__main__":
    main()
