# Plan: Copilot parity with Claude Code

Status: DONE (2026-11-17), see .ai/completed/copilot-parity.md
Created: 2026-11-17

## Goal

GitHub Copilot should find and use the same `.ai/` content as Claude Code, with `.ai/` staying the only source. That covers rules/instructions, checklists, patterns, progress tracking, session handoff, prompts, agents and skills. It should work in VS Code (Local and Copilot harness), Copilot CLI and the cloud agent.

## Root cause analysis (why Copilot ignores the rules and agents today)

### 1. Runtime: the model loop breaks (user environment, not the repo)

The VS Code logs (`%APPDATA%/Code/logs/2026111{6,7}*/.../GitHub Copilot Chat.log`) show:

- Copilot is **not signed in** ("no Copilot token source", "user is not signed in"). Every agent request goes to a BYOK model, `deepseek-flash`: 1,488 of 1,597 requests. Requests reach that model through the Local harness model wrapper (`copilotLanguageModelWrapper`).
- **36 requests failed with HTTP 400**: "The `reasoning_content` in the thinking mode must be passed back to the API". DeepSeek's thinking mode requires the reasoning from earlier turns to be sent back, and VS Code doesn't do that. Each failure ends the agent turn in the middle of its tool loop. Delegating to an agent, reading the critical rules and writing the handoff all need several tool calls, so these are the steps most likely to be cut off.
- Even when nothing fails, a small "Flash" model has to follow roughly 40 KB of orchestration instructions with no hooks enforcing anything. Claude Code runs a frontier model and has the Agent tool and hooks.

The repo can't fix this part. It is the main reason behind the symptom.

### 2. Template: the instructions only tell Claude Code how to do things

| Area | Claude Code today | Copilot today |
|---|---|---|
| Delegation | AGENTS.md says "delegate"; the Agent tool is always available | No tool is named. Delegation in Copilot needs `runSubagent` (Local) or `task` (Copilot harness), and Run Subagent must be enabled in the tool picker |
| Agent skills | `skills:` frontmatter loads the skill into the agent automatically | `skills:` is Claude-only and ignored. A Copilot agent gets only its one-paragraph body, so it starts without the rules |
| Copilot-only block | n/a | Its "Load these files … per task type" tells the main agent to do the work itself, which contradicts "orchestration only" |
| Session context | `SessionStart` hook prints `.ai/session-context.md` | No hook loads it; the model has to remember to read it |
| Link sync | `SessionStart`/`PostToolUse` hooks | `.vscode/tasks.json` (untracked, so missing on clone); the auto-run task also needs `task.allowAutomaticTasks` |
| Prompts | `.claude/commands`, but names show as `/ef-core.prompt` | Copilot harness **does not load `*.prompt.md`** (skills only) |
| `*.instructions.md` | `.claude/instructions` isn't a path Claude Code reads (it reads `.claude/rules`) | Loaded, but there's only one file (SonarQube), so no `.cs` rule auto-attaches |
| Rules | Loaded once from AGENTS.md | Loaded **twice**: AGENTS.md plus `copilot-instructions.md`, which embeds it word for word |

### 3. User settings mistakes (`%APPDATA%/Code/User/settings.json`)

- `"chat.agentFilesLocations": {"AGENTS.md": true}` adds a *custom-agent folder* named `AGENTS.md`. It does not load AGENTS.md (that is done by `chat.useAgentsMdFile`).
- `chat.agentSkillsLocations` is deprecated and ignored by the Copilot harness.
- `chat.planAgent.defaultModel` / `inlineChat.defaultModel` point at the failing DeepSeek model.

## Changes

### Phase A: user environment (you do this; I'll give the exact steps)

1. Sign in to GitHub Copilot, or use a model whose tool calling works in VS Code: a non-thinking DeepSeek variant, or Claude/GPT through BYOK.
2. Remove `chat.agentFilesLocations: {"AGENTS.md": true}` and `chat.agentSkillsLocations`.
3. In Agent mode → Configure Tools, enable **Run Subagent** (Local harness).

### Phase B: template (delegated to subagents after approval)

Reused, not duplicated: `sync-platforms.py`, `sync-instructions.py`, `validate-copilot.py`, the existing `.ai/agents/*.md`, `.ai/instructions/`, `.claude/settings.json`, `.vscode/tasks.json`.

1. **Copilot block rewrite** (`sync-instructions.py` reference block). Replace the conflicting "load these files" table with a Copilot runtime section:
   - Start by reading `.ai/session-context.md` and `.ai/progress/`, because no hook does it for Copilot.
   - Delegate using the agent's name. Spell out how: `runSubagent` with `agentName` (Local harness) or `task` (Copilot harness). If neither tool is available, say so and follow the agent's skill files directly.
   - End with the handoff, the README check and moving the progress file.
2. **Stop the double load.** Add `"chat.useAgentsMdFile": false` to the tracked `.vscode/settings.json`, so VS Code reads the content once (`copilot-instructions.md` is the full superset). CLI and cloud agent behavior is unchanged.
3. **Agents work without Claude-only frontmatter.** `sync-platforms.py` checks, and the agent bodies say, "Before starting, read: `.ai/skills/<skill>/SKILL.md` …, `.ai/reference/critical-rules.md`". This mirrors the `skills:` list, which Claude keeps using. Add `disable-model-invocation: false` explicitly. Leave `model:` alone, because Copilot ignores tier aliases it doesn't know.
4. **Rules attach automatically, in both tools.** Add a small set of scoped instruction files to `.ai/instructions/`:
   - `csharp-rules.instructions.md` (`applyTo: "**/*.cs"`): the 15 critical rules in short form, plus links to patterns and checklists
   - `tests.instructions.md` (`tests/**`)
   - `ai-workspace.instructions.md` (`.ai/**`): progress-file and handoff conventions

   `sync-platforms.py` generates `.claude/rules/*.md` from these files (`applyTo` → `paths:`), gitignored, replacing the dead `.claude/instructions` link. VS Code reads them directly through `.github/instructions`.
5. **Prompts → skills.** The Copilot harness ignores prompt files, so convert the 20 `.ai/prompts/*.prompt.md` files into `.ai/skills/<name>/SKILL.md` with `disable-model-invocation: true`. Both tools then reach them through the existing skills adapters. Retire the `.claude/commands` and `.github/prompts` links, and `upgrade-template.py` maps old prompt paths.
6. **Shared hooks.** Move the inline Python of the SessionStart hook into `.ai/scripts/hooks/session-start.py`. Wire it to Claude (`.claude/settings.json`) and to Copilot (`.github/hooks/ai-workspace.json`, camelCase `sessionStart` / `postToolUse`). The Copilot harness also reads `.claude/settings.json`, so before adding a second file, test whether that one file is enough. Use `python3` with `python` as a fallback so macOS and Linux work.
7. **Commit `.vscode/tasks.json`.** Document that `task.allowAutomaticTasks` has to be allowed once.
8. **Validators.** Extend `validate-copilot.py` with these checks:
   - every agent body lists its skills
   - the Copilot block contains the delegation and session protocol
   - `.github/hooks` JSON is valid
   - `.claude/rules` is generated
   - no `*.prompt.md` is left
   - `tasks.json` is tracked
9. **Docs.** Update `README.md`, `.ai/reference/copilot-integration.md`, `TEMPLATE-FAQ.md` and `TEMPLATE-USAGE.md`, and correct the wrong statement on README line 301.
10. **Verify.** Run `run-all-tests.sh`, the pytest suite and `validate-upgrade-script.py`. Then do a manual check in VS Code with a working model: ask for a .NET change, and confirm that (a) `developer` is delegated to, (b) a critical rule is applied, and (c) session context and a progress file are used.

## User decisions (2026-11-17)

- Convene a council on the adapter-structure change.
- Disable AGENTS.md loading in VS Code through the workspace setting `chat.useAgentsMdFile: false`.
- `.github/copilot-instructions.md` remains a generated copy of AGENTS.md. AGENTS.md is the truth.

## Council framing: adapter-layer-for-copilot-parity

**Trigger:** the change alters an established architecture decision: the template's project structure, i.e. which `.ai/` folders are exposed through which adapter paths.

**Decision question:** How should the template expose `.ai/prompts`, `.ai/instructions` and its lifecycle hooks, so that both Claude Code and GitHub Copilot load and act on them, while `.ai/` remains the single source of truth?

**Constraints:**
1. `.ai/` is the only hand-edited source. Adapter paths are gitignored links or generated output, never a second hand-maintained copy.
2. AGENTS.md is the truth. `.github/copilot-instructions.md` stays a generated copy of it, and VS Code's AGENTS.md loading is disabled by `chat.useAgentsMdFile: false`.
3. It must work in Claude Code and in Copilot: VS Code Local harness, VS Code Copilot harness, Copilot CLI and the Copilot cloud agent.
4. Downstream projects upgrade through `upgrade-template.py` without losing project-owned files.
5. The existing validation suite keeps passing, and new behavior is covered by a validator.
6. Windows, macOS and Linux.

**Established facts** (vendor docs and local logs, verified 2026-11-17):
- The Copilot harness does not load `*.prompt.md`; it uses skills (`.github/skills`, `.agents/skills`). The Local harness still loads prompt files and is deprecated as of February 2027.
- Claude Code reads `.claude/commands/*.md` as slash commands, `.claude/skills`, and `.claude/rules/*.md` (with `paths:` frontmatter). It does not read `.claude/instructions/`.
- Copilot reads `*.instructions.md` (with `applyTo:`) from `.github/instructions`.
- Copilot harness repository hooks are read from `.github/hooks/*.json`, `.github/copilot/settings.json` and `.claude/settings.json`. Event names and payloads differ from Claude's, and the `if:` field is Claude-only.
- Today `.ai/prompts` holds 20 Copilot-format prompt files (`mode:`, `tools:` frontmatter), and `.ai/instructions` holds one file (`applyTo: "**/*"`).

**Known options** (per sub-decision, unordered):
- **(a) Prompts:** A1 keep `.ai/prompts` and the `.claude/commands` and `.github/prompts` links as they are · A2 convert the prompts into `.ai/skills/<name>/SKILL.md` and retire the prompt adapters · A3 keep `.ai/prompts` as the source and generate skill wrappers from it
- **(b) Instructions:** B1 keep the `.claude/instructions` link · B2 generate `.claude/rules/*.md` from `.ai/instructions/*.instructions.md` (`applyTo` → `paths`) · B3 drop the Claude instructions adapter and rely on AGENTS.md text
- **(c) Hooks:** C1 Claude-only hooks, with Copilot relying on written instructions · C2 shared scripts in `.ai/scripts/hooks/`, wired into both `.claude/settings.json` and `.github/hooks/` · C3 shared scripts wired only in `.claude/settings.json`, which the Copilot harness also reads

**Deadline:** none

# Council Record: adapter-layer-for-copilot-parity

**Status:** DECIDED. User confirmed C3 on 2026-11-17.
**Date:** 2026-11-17
**Trigger:** the change alters an established architecture decision: project structure and the adapter layout.
**Decision question:** How should the template expose `.ai/prompts`, `.ai/instructions` and its lifecycle hooks, so that both Claude Code and GitHub Copilot load and act on them, while `.ai/` remains the single source of truth?

**Seats:**
- Design → `architect`
- Security → `security`
- Verifiability → `tester`
- Feasibility → `developer`

Rules seat omitted: the critical rules govern .NET code, which this change doesn't touch. Template conventions are covered by the Design seat.

## Positions

Final positions, after the single cross-examination round.

| Seat | (a) Prompts | (b) Instructions | (c) Hooks | Confidence |
|---|---|---|---|---|
| Design | A2 | B4 now, guarded by a validator, escalating to B2 | C2, read-only hooks only; Stop stays Claude-only | Medium-high / medium / medium |
| Security | A2 | B3 default; B4 acceptable while all files are `**/*`; generation preferred over a link | C3, until a documented Copilot trust gate for `.github/hooks` exists | Medium / medium-high / medium |
| Verifiability | A2, plus a validator rejecting `${...}` in skills | B2; B4 acceptable with a validator | C2, limited to the logic scripts | Medium-high / medium / medium |
| Feasibility | A2 | B2; B3 rejected | Changed from C2 to C3 | High / high / medium |

## Decision

**(a) A2.** Convert the 20 `.ai/prompts/*.prompt.md` into `.ai/skills/<name>/SKILL.md`:
- Use `disable-model-invocation: true` for prompts that should only run when called explicitly.
- Rewrite `${selection}`, `${file}`, `${input:…}` and `${workspaceFolder}` as prose. Seven files are affected.
- Drop prompt-specific `mode:`, `tools:` and `model:`.
- Retire the `.claude/commands` and `.github/prompts` adapters and remove `.ai/prompts`.
- Add a validator that rejects `${` tokens in `SKILL.md`.

**(b) B2.** Generate `.claude/rules/<name>.md` from `.ai/instructions/<name>.instructions.md`, mapping `applyTo` → `paths:` and omitting `paths:` for `**/*`:
- The generator is copy-only: it writes regular files and never follows or creates links.
- The output is gitignored and regenerated by `sync-platforms.py`.
- A drift validator compares the output with its source.
- `.github/instructions` stays a plain link.
- Drop the `.claude/instructions` link.
- Add `rules` to the `.claude/` allow-list in `validate-settings.py`.

**(c) C3.** Move all hook logic into shared scripts under `.ai/scripts/hooks/`, wired **only** in `.claude/settings.json`, with no `.github/hooks`:
- The scripts accept both Claude and Copilot payload shapes and filter by path themselves, because `if:` is Claude-only.
- The build script exits immediately unless it runs under Claude Code (`CLAUDE_PROJECT_DIR` set).
- Hooks call a portable Python launcher (`python3`, falling back to `python`).
- Hooks are an enhancement, not a control. Copilot's session start and handoff behavior is guaranteed by the Copilot section of `copilot-instructions.md`.
- A probe step (a log-writing hook run in the VS Code Copilot harness) records whether Copilot fires `.claude/settings.json` hooks.

**Required follow-through** (facts the seats raised, accepted by the chair):
- `upgrade-template.py` TEMPLATE_OWNED gains `.ai/instructions` and the new skills.
- Upgrade runs `sync-instructions.py` so the downstream `copilot-instructions.md` is regenerated from AGENTS.md, keeping its marked Copilot block.
- `sync-platforms.py` `_rmdir` logs failures instead of `ignore_errors=True`.
- The `.vscode/tasks.json` task becomes run-on-demand, with no `folderOpen` auto-run. Copilot instructions tell the model to run `sync-platforms.py` when an adapter path is missing.

## Rationale

- **Adopted:**
  - (a) is unanimous: skills are the only format both tools load (Design, Verifiability). Feasibility supplied the rewrite inventory, and Security the explicit-only guard.
  - (b) B2: Feasibility and Verifiability argued that path scoping must survive. This plan adds path-scoped instruction files (C#, tests, `.ai/` workspace), which is the condition every seat named for B2.
  - (c) C3: Security and Feasibility argued that `.github/hooks` adds a new auto-run file in the Copilot cloud agent and CLI with no confirmed trust gate. Under C3, Copilot still gets the hooks if its documented reading of `.claude/settings.json` holds, with no new exposure file. If it doesn't hold, the instructions in `copilot-instructions.md` still carry the behavior.
- **Rejected:**
  - B3 (Security's default) and B4 (Design): both are valid only while every instruction file is `**/*`, and this plan adds scoped files.
  - C2 (Design, Verifiability): it adds an auto-run surface whose trust model no seat could confirm. Its benefit depends on the same unverified Copilot hook behavior C3 relies on, so the probe decides before any extra exposure is added.
  - Security's junction-deletion finding: withdrawn by Security after the chair checked the code.

## Recorded dissent (verbatim)

> **Design:** "(c) I hold C2, but I concede B's security point. Wiring `.github/hooks` widens the auto-exec surface into the cloud agent and CLI without a confirmed trust gate. I narrow C2 so that only idempotent, read-only hooks go in `.github/hooks`."

> **Verifiability:** "On (c) I keep C2, but with a narrower claim. Seat B's C3 argument is about security exposure, not verifiability. It does not make C3 more observable. It does matter, though, because it makes Copilot-side hook wiring something I cannot show to be safe."

> **Security** (on (b), partially overruled): "On (b), I move to B3 as the default, agreeing with the other seats' condition on the single `**/*` file."

## Reopen conditions

- The probe shows the Copilot harness does **not** fire `.claude/settings.json` `SessionStart` with parseable stdin, **and** Copilot documents a trust gate for `.github/hooks/*.json` → reconvene on C2 (read-only hooks only).
- The VS Code Local harness's Feb 2027 removal is cancelled, and a prompt's behavior can't be expressed as a skill → reconsider A1/A3 for that prompt.
- Claude Code stops honoring `paths:` in `.claude/rules`, or Copilot changes `applyTo` semantics → revisit B2.
- A `copilot-setup-steps.yml` is proposed to give the cloud agent adapters → that is a new exposure surface and needs its own security review.

## Escalation

The council split 2–2 on (c). The chair decided C3 on the merits, and the user is asked to confirm, or to choose C2 limited to read-only hooks.

## Out of scope

Getting a Flash-class model to follow orchestration reliably. Phase A fixes the runtime; the template can only make the instructions explicit and the rules attach automatically.
