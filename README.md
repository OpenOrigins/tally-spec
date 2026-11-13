# Tally specification and installation

Public specification, Homebrew cask and standalone Claude Code cloud hooks for
[OpenOrigins Tally](https://openorigins.com/tally).

- [Agent log specification](Tally-SPEC.md) — version 0.2, draft for public comment.
- [Cloud hook setup](claude/cloud_hooks/cloud_hook_installation.md) — the separate
  HTTP-hook option for supported Claude Code cloud sessions.
- [OpenOrigins dashboard](https://dashboard.openorigins.com/) — create an account,
  generate an Agent API key and download the Tally desktop app.

## Downloads

Install the **Tally desktop app**. It includes the hooks and sets them up for
Claude Code, Codex and Cursor; there's nothing else to install. Linux has no
desktop app yet and uses the integration installer below.

Tally 0.1.21 is available for macOS and Linux. Windows remains on its previous release.
Generate an Agent API key in the dashboard before connecting your agents.

| Platform | Download |
| --- | --- |
| macOS desktop, Apple Silicon | [tally-desktop-macos-arm64.dmg](https://cdn.openorigins.com/releases/desktop-v0.1.21/tally-desktop-macos-arm64.dmg) |
| macOS desktop, Intel | [tally-desktop-macos-x86_64.dmg](https://cdn.openorigins.com/releases/desktop-v0.1.21/tally-desktop-macos-x86_64.dmg) |
| Windows desktop, x64 | [tally-desktop-windows-x86_64.zip](https://cdn.openorigins.com/releases/desktop-v0.1.20/tally-desktop-windows-x86_64.zip) |
| Linux integration installer, x64 | [tally-linux-x86_64](https://cdn.openorigins.com/releases/v0.1.21/tally-linux-x86_64) |
| Python / LangGraph | [tally_langgraph-0.1.3-py3-none-any.whl](https://cdn.openorigins.com/releases/v0.1.21/tally_langgraph-0.1.3-py3-none-any.whl) |
| Claude Code cloud sessions | [tally-claude-cloud-hooks.zip](https://cdn.openorigins.com/releases/v0.1.21/tally-claude-cloud-hooks.zip) |

Verify the 0.1.21 downloads against the [desktop](https://cdn.openorigins.com/releases/desktop-v0.1.21/SHA256SUMS) or [integration](https://cdn.openorigins.com/releases/v0.1.21/SHA256SUMS) checksums.
For Windows, use the [Desktop 0.1.20](https://cdn.openorigins.com/releases/desktop-v0.1.20/SHA256SUMS) or [integration 0.1.19](https://cdn.openorigins.com/releases/v0.1.19/SHA256SUMS) checksums.
The macOS apps and disk images are signed and notarized. Open the DMG, drag Tally
to Applications, then open it. On Windows, extract the ZIP and run
`Tally/tally-desktop.exe`, keeping `tally-hook.exe` beside it. Windows binaries
are unsigned and may require administrator approval on managed devices.
Linux uses the integration installer: run `chmod +x tally-linux-x86_64`, then
`./tally-linux-x86_64`. Install the downloaded wheel with
`python -m pip install ~/Downloads/tally_langgraph-0.1.3-py3-none-any.whl`.

App and hook updates are offered in the desktop app's Settings on macOS. Windows
in-app updates are not yet available.

After connecting your agents, restart the selected client. Codex users
must install Codex CLI first, review the OpenOrigins Tally hooks in the CLI and
trust them before reopening Codex Desktop. See the public
[setup guide](https://openorigins.gitbook.io/v1/tally/setup#step-6-connect-your-client).

## Homebrew on macOS

Homebrew installs the Tally desktop app from the next desktop release. Until
then, the cask still installs the separate 0.1.21 integration installer; use the
desktop DMG above instead.

```sh
brew tap openorigins/tally https://github.com/OpenOrigins/tally-spec
brew install --cask openorigins/tally/tally
```

The cask records the release version and separate SHA-256 checksums for Apple
Silicon and Intel. Updates are published only after verifying the release
files. Run `brew update` and `brew upgrade --cask openorigins/tally/tally` to
update an installation. That upgrade replaces the integration installer with
the desktop app once the cask moves to it.

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
or keep a local delivery queue; use the desktop app for local token capture.

`settings.local.json` is an empty template. Keep API keys outside version control.

## Licenses

The specification identifies its license as CC BY 4.0. The cask and cloud-hook
code are distributed under the [Apache License 2.0](LICENSE).
