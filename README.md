# Tally specification and installation

Public specification, Homebrew cask and standalone Claude Code cloud hooks for
[OpenOrigins Tally](https://openorigins.com/tally).

- [Agent log specification](Tally-SPEC.md) — version 0.2, draft for public comment.
- [Cloud hook setup](claude/cloud_hooks/cloud_hook_installation.md) — the separate
  HTTP-hook option for supported Claude Code cloud sessions.
- [OpenOrigins dashboard](https://dashboard.openorigins.com/) — create an account,
  generate an Agent API key and download the native installer for your platform.

## Homebrew on macOS

```sh
brew tap openorigins/tally https://github.com/OpenOrigins/tally-spec
brew install --cask openorigins/tally/tally
```

The cask records the release version and separate SHA-256 checksums for Apple
Silicon and Intel installers. Updates are published only after verifying the
release files. Run `brew update` and `brew upgrade --cask openorigins/tally/tally`
to update an installation.

## Claude Code cloud hooks

The files under `claude/cloud_hooks/` are a separate integration for
single-repository cloud sessions outside Claude Projects. Follow their setup
guide before enabling them. The direct HTTP option does not report token counts
or keep a local delivery queue; use the native installer for local token capture.

`settings.local.json` is an empty template. Keep API keys outside version control.

## Licenses

The specification identifies its license as CC BY 4.0. The cask and cloud-hook
code are distributed under the [Apache License 2.0](LICENSE).
