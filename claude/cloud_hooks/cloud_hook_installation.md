# Claude Code cloud hooks for Tally

This package is a **separate installation option** for single-repository Claude Code cloud sessions outside Claude Projects. It sends Claude Code activity directly to OpenOrigins without installing the Tally desktop app in the cloud environment. For sessions running on your own computer, including Remote Control, use the [normal Tally installer](https://dashboard.openorigins.com/) unless you specifically need direct HTTP delivery.

Claude Code does not load repository hooks in a Claude Project cloud thread or an Anthropic-hosted cloud session with multiple repositories. This package cannot log those sessions through repository settings; see [Claude's cloud hook limitations](https://code.claude.com/docs/en/cloud-environments#limitations-in-cloud-sessions).

## Files in the release archive

| File | Use |
| --- | --- |
| `settings.json` | Claude Code hooks. Commit this file to the repository used by cloud sessions. |
| `tally_session_start.py` | Sends `SessionStart`, which Claude Code does not support as an HTTP hook. Commit this file alongside `settings.json`. |
| `settings.local.json` | Empty local API-key template. Do **not** commit a populated copy or copy it into a cloud session. |
| `cloud_hook_installation.md` | This guide. |

## Set up a cloud session

1. In the OpenOrigins dashboard, generate a dedicated **Agent API key** for this integration. Keep it out of Git.
2. In the repository that Claude Code will clone, copy `settings.json` and `tally_session_start.py` into its `.claude/` directory. If `.claude/settings.json` already exists, add each Tally hook group under its matching event instead of replacing your other settings or handlers. Keep the `SessionStart` command path pointing to `.claude/tally_session_start.py`.
3. Commit and push those two files to the branch you will use for the cloud session. The empty `settings.local.json` template is only for local use; do not add it to the cloud repository.
4. In [Claude Code cloud environments](https://code.claude.com/docs/en/cloud-environments), set `OO_API_KEY` to your Agent API key. Allow outbound HTTPS to `api.prod.openorigins.com` in that environment's network settings. Environment variables can be read by anyone who can use that environment, so use a dedicated key and limit access to the environment.
5. Start a **new** cloud session for that repository and branch, selecting the environment you configured. In Claude Code, `/hooks` should show the `SessionStart` command and the other HTTP events. Send a simple prompt, then check the session in the OpenOrigins Tally dashboard.

The cloud environment includes Python 3 for the start hook. The other events use Claude Code's built-in HTTP hook handler. If your cloud environment cannot reach the OpenOrigins API, the requests will fail; enabling the hooks alone does not grant network access. For a nonproduction endpoint, change every `url` in `settings.json` and set `TALLY_HOOK_URL` in the cloud environment to the same endpoint for `SessionStart`.

## Optional local trial

For a local Claude Code project, copy the same `settings.json` and `tally_session_start.py` into `.claude/`. Copy the empty `settings.local.json` template into `.claude/settings.local.json`, put your Agent API key in its `OO_API_KEY` value, and add `.claude/settings.local.json` to the project's `.gitignore`. Check with `git check-ignore -v .claude/settings.local.json` before working in that repository. Restart Claude Code after changing settings.

The local HTTP trial requires Python 3 and a connection to the OpenOrigins API. Do not enable these hooks alongside Tally's native Claude Code hooks in the same project: each event would be sent twice.

## What this option reports

The hooks send Claude Code's standard event payloads for session start and end, prompts, tool activity, permissions, notifications, subagents, compaction, and response completion. Payloads can include prompt text and tool inputs or outputs, so choose the repository and cloud environment accordingly.

This direct HTTP option currently **does not report input, output, cache, or thinking token counts**. It also does not run Tally's local task-assist helper or keep a local delivery journal. A failed HTTP request can therefore lose that event; Claude Code continues after nonblocking hook failures. Use the native Tally installer for local sessions when token counts and queued delivery are needed.

## Troubleshooting and removal

- If `/hooks` does not list the handlers, check the repository branch, JSON syntax (`python3 -m json.tool .claude/settings.json`), and the exact path to `tally_session_start.py`.
- If events do not reach Tally, check that `OO_API_KEY` is set in the selected cloud environment and that its network policy permits `api.prod.openorigins.com`. Run Claude Code with debug logging to see hook errors; never paste the key into logs or support messages.
- To remove the integration, remove these Tally hook entries from `.claude/settings.json`, remove `.claude/tally_session_start.py`, and start a new cloud session. Revoke the dedicated Agent API key if it will no longer be used.
