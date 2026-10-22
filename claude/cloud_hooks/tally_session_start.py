"""Forward Claude Code's command-only SessionStart event to Tally."""

import os
import sys
import urllib.request

URL = os.environ.get("TALLY_HOOK_URL", "https://api.prod.openorigins.com/v1/tally/logs")


def main() -> None:
    key = os.environ.get("OO_API_KEY")
    if not key:
        raise SystemExit("OO_API_KEY is required for the Tally SessionStart hook")

    request = urllib.request.Request(
        URL,
        data=sys.stdin.buffer.read(),
        headers={"Content-Type": "application/json", "x-api-key": key},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=10):
        pass


if __name__ == "__main__":
    main()
