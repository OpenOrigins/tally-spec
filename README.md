# Tally specification and installation

Public specification, Homebrew cask and standalone Claude Code cloud hooks for
[OpenOrigins Tally](https://openorigins.com/tally).

- [Agent log specification](Tally-SPEC.md) — version 0.2, draft for public comment.
- [Cloud hook setup](claude/cloud_hooks/cloud_hook_installation.md) — the separate
  HTTP-hook option for supported Claude Code cloud sessions.
- [OpenOrigins dashboard](https://dashboard.openorigins.com/) — create an account,
  generate an Agent API key and download the native installer for your platform.

## Downloads — 0.1.18

Generate an Agent API key in the dashboard before opening the native installer.

| Platform | Download |
| --- | --- |
| macOS, Apple Silicon | [tally-macos-arm64.dmg](https://cdn.openorigins.com/releases/v0.1.18/tally-macos-arm64.dmg) |
| macOS, Intel | [tally-macos-x86_64.dmg](https://cdn.openorigins.com/releases/v0.1.18/tally-macos-x86_64.dmg) |
| Windows, x64 | [tally-windows-x86_64.exe](https://cdn.openorigins.com/releases/v0.1.18/tally-windows-x86_64.exe) |
| Linux, x64 | [tally-linux-x86_64](https://cdn.openorigins.com/releases/v0.1.18/tally-linux-x86_64) |
| Python / LangGraph | [tally_langgraph-0.1.2-py3-none-any.whl](https://cdn.openorigins.com/releases/v0.1.18/tally_langgraph-0.1.2-py3-none-any.whl) |
| Claude Code cloud sessions | [tally-claude-cloud-hooks.zip](https://cdn.openorigins.com/releases/v0.1.18/tally-claude-cloud-hooks.zip) |

Verify downloads against [SHA256SUMS](https://cdn.openorigins.com/releases/v0.1.18/SHA256SUMS).
The macOS app and disk images are signed and notarized. The Windows executable
is currently unsigned and may require administrator approval on managed devices.
Open the macOS DMG and drag Tally to Applications; open the Windows executable
directly. On Linux, run `chmod +x tally-linux-x86_64`, then `./tally-linux-x86_64`.
Install the downloaded wheel with
`python -m pip install ~/Downloads/tally_langgraph-0.1.2-py3-none-any.whl`.

After installing the native hooks, restart the selected client. Codex users
must install Codex CLI first, review the OpenOrigins Tally hooks in the CLI and
trust them before reopening Codex Desktop. See the public
[setup guide](https://openorigins.gitbook.io/v1/tally/setup#step-6-connect-your-client).

## Homebrew on macOS

```sh
brew tap openorigins/tally https://github.com/OpenOrigins/tally-spec
brew install --cask openorigins/tally/tally
```

The cask records the release version and separate SHA-256 checksums for Apple
Silicon and Intel installers. Updates are published only after verifying the
release files. Run `brew update` and `brew upgrade --cask openorigins/tally/tally`
to update an installation.

If you already tapped the old Tally source repository, replace the tap checkout.
This keeps the installed app; save any local edits to the old tap first.

```sh
brew untap --force openorigins/tally
brew tap openorigins/tally https://github.com/OpenOrigins/tally-spec
```

## Python / LangGraph

Install the wheel above in your application's environment. Set `TALLY_API_KEY`
to the Agent API key from the dashboard through your environment or secret
manager, then add a fresh callback to each graph invocation:

```python
from tally_langgraph import TallyClient

tally = TallyClient.from_env()
result = graph.invoke(inputs, config={"callbacks": [tally.callback(source="my-app")]})
# At application shutdown:
tally.close(timeout=10)
```

Append the callback if your application already has callbacks. The same
configuration works with `ainvoke()` and `astream()`. The default state directory
is `.tally/langgraph`; exclude `.tally/` from Git and use a persistent local volume
in deployments. Undelivered records stay in its local SQLite outbox for retry.

## Claude Code cloud hooks

The files under `claude/cloud_hooks/` are a separate integration for
single-repository cloud sessions outside Claude Projects. Follow their setup
guide before enabling them. The direct HTTP option does not report token counts
or keep a local delivery queue; use the native installer for local token capture.

`settings.local.json` is an empty template. Keep API keys outside version control.

## Licenses

The specification identifies its license as CC BY 4.0. The cask and cloud-hook
code are distributed under the [Apache License 2.0](LICENSE).
