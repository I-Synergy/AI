# PowerShell Profile — Claude Code backend switcher

This profile adds two functions to your PowerShell session so you can run Claude Code against either the Anthropic API (`claude`) or the DeepSeek-compatible API (`deepseek`) from the same shell.

## What it does

- **`deepseek`** — points Claude Code at `https://api.deepseek.com/anthropic`, using the `DEEPSEEK_API_KEY` credential. Before launching, it swaps a `DEEPSEEK.md` in the current directory over `CLAUDE.md` (and restores it afterwards, including crash recovery from a stale backup).
- **`claude`** — clears the DeepSeek environment variables and runs the stock `claude` CLI.

It also loads `$HOME\.deepseek\credentials.ps1` on shell start if present.

## Dependencies (not in this repo)

- **Claude Code CLI** installed at `$env:USERPROFILE\AppData\Roaming\npm\claude.cmd`
- **`$HOME\.deepseek\credentials.ps1`** containing `$env:DEEPSEEK_API_KEY = "..."` — created per machine, never committed.
- **`DEEPSEEK.md`** in the project root — this repo ships one (see `../DEEPSEEK.md`), which is what the `deepseek` function swaps in.

## Install on a new environment

```powershell
# Copy the profile to the current user's profile path
Copy-Item powershell/Microsoft.PowerShell_profile.ps1 $PROFILE -Force

# Create the credentials file (never commit this)
New-Item -ItemType Directory -Force $HOME\.deepseek | Out-Null
Set-Content $HOME\.deepseek\credentials.ps1 '$env:DEEPSEEK_API_KEY = "YOUR_KEY_HERE"'

# Reload
. $PROFILE
```

Then run `deepseek` or `claude` in any project directory.

## Notes

- All model slots resolve to the same unified model, `deepseek-flash`. The heavy slots (`ANTHROPIC_MODEL`, `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`) append the `[1m]` suffix to request the 1M context window; `ANTHROPIC_DEFAULT_HAIKU_MODEL` uses the plain model name.
- That one model handles both vision and text tasks, so there is no separate vision tier and no per-agent `model:` frontmatter override to apply.
- `CLAUDE_CODE_SUBAGENT_MODEL = "inherit"` makes subagents inherit the main model instead of pinning them to a separate subagent model.
- `CLAUDE_CODE_EFFORT_LEVEL = "max"` requests maximum effort for heavy coding and agent tasks.
