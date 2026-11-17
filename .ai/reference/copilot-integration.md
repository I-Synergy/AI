# GitHub Copilot Integration Guide

This template supports **both** Claude AI and GitHub Copilot working together in the same repository.

## Architecture

```
Template/
├── AGENTS.md                          # Orchestration instructions (source of truth)
├── .vscode/
│   ├── settings.json                  # Workspace settings for Copilot (see "VS Code workspace settings"); projects get them by merge
│   └── tasks.json                     # "Link .ai into the paths tools read" — run on demand; projects get it by merge
├── .github/
│   ├── copilot-instructions.md        # Generated: AGENTS.md + copilot-runtime.md + project block
│   ├── skills/                        # Link -> .ai/skills/ (gitignored, local)
│   ├── agents/                        # Link -> .ai/agents/ (gitignored, local)
│   └── instructions/                  # Link -> .ai/instructions/ (gitignored, local)
├── .claude/
│   ├── settings.json                  # Hooks: SessionStart, PostToolUse, Stop (shared scripts)
│   ├── skills/                        # Link -> .ai/skills/ (gitignored, local)
│   ├── agents/                        # Link -> .ai/agents/ (gitignored, local)
│   └── rules/                         # Generated copies of .ai/instructions/ (gitignored)
├── .agents/
│   └── skills/                        # Link -> .ai/skills/ (gitignored, local)
└── .ai/                               # Shared knowledge base (source of truth)
    ├── reference/                     # Standards (all systems); copilot-runtime.md feeds copilot-instructions.md
    ├── patterns/                      # Patterns (all systems)
    ├── instructions/                  # Path-scoped rules (*.instructions.md), one source for both tools
    ├── scripts/                       # sync-platforms.py, sync-instructions.py, migrate-to-ai.py
    │   └── hooks/                     # Shared hook logic (session_start.py, post_edit_sync.py, stop_build.py, py.sh)
    ├── skills/                        # Skills source — edit here (includes the former prompts)
    ├── agents/                        # Agent source — each body lists the skills it must read
    ├── tmp/                           # Scratch and hook-probe.log (gitignored)
    └── project/                       # Shared project context
```

### Adapter map

Every adapter is a folder link to `.ai/` (junction on Windows, symlink elsewhere), except
`.claude/rules/` and `.github/copilot-instructions.md`, which are generated copies. All of
them are gitignored or regenerated, so none is a second hand-maintained source.

| Adapter path | Source | Read by | Kind |
|---|---|---|---|
| `.claude/skills/` | `.ai/skills/` | Claude Code | link |
| `.claude/agents/` | `.ai/agents/` | Claude Code | link |
| `.claude/rules/*.instructions.md` | `.ai/instructions/*.instructions.md` | Claude Code (`paths:` frontmatter) | generated copy |
| `.github/skills/` | `.ai/skills/` | Copilot (VS Code, CLI, cloud agent) | link |
| `.github/agents/` | `.ai/agents/` | Copilot | link |
| `.github/instructions/` | `.ai/instructions/` | Copilot (`applyTo`) | link |
| `.github/copilot-instructions.md` | `AGENTS.md` + `.ai/reference/copilot-runtime.md` | Copilot | generated copy |
| `.agents/skills/` | `.ai/skills/` | Codex and other skills-standard agents | link |

Prompt adapters are conditional. `.claude/commands/` and `.github/prompts/` are links to
`.ai/prompts/` only while that folder holds at least one file. The template ships no prompts,
so a fresh project has neither link; a project that installed prompts from a catalog has both.
When `.ai/prompts/` is absent or empty, both are removed as legacy.

Retired: `.claude/instructions/`. Claude Code never read it. The sync removes it when it is a
link or empty. Real content found at any retired path is reported, never deleted.

**Why prompts are skills now:** the Copilot harness does not load `*.prompt.md` files. Skills
are the one format both tools load, so the former prompts live in `.ai/skills/<name>/SKILL.md`
with `disable-model-invocation: true` (invoke by name, e.g. `/ef-core`).

**Why Claude gets generated rules:** Claude Code reads path-scoped rules only from
`.claude/rules/*.md`, not from a folder link, so `sync-platforms.py` copies each
`.ai/instructions/{name}.instructions.md` there, mapping `applyTo` to `paths:`. A `**/*`
rule gets no `paths:` and always applies.

### Skills: one source, per-tool adapters

Skills have a single source of truth in `.ai/skills/`. No tool reads `.ai/skills/` directly — each one only recognises its own hardcoded location, and no setting can add `.ai/` to that list. VS Code (Copilot) scans `.agents/skills`, `.github/skills` and `.claude/skills`; Claude Code scans `.claude/skills`; OpenAI Codex scans `.agents/skills`.

The template bridges them with folder-level links (symlinks on Unix), so no content is duplicated:

| Layer | Path | Who reads it |
|-------|------|--------------|
| Source | `.ai/skills/<name>/SKILL.md` | Edit here — the only copy |
| Claude Code | `.claude/skills/` → `.ai/skills/` | Claude Code |
| GitHub Copilot | `.github/skills/` → `.ai/skills/` | Copilot in VS Code, Copilot CLI, cloud agent |
| Other agents | `.agents/skills/` → `.ai/skills/` | Codex and other skills-standard agents |

VS Code lists each source it scans, so the same skill can appear under both
`.github/skills` and `.claude/skills` in the Customizations editor. That is one file
seen through two adapter paths — each tool resolves only its own — not two copies.

### Why every tool shows `.github/` (and never `.ai/`)

The Customizations editor, the `/` menu and every tool's discovery code list the
**paths the tool reads**, not the folder you edit. Those paths are hardcoded per tool
and none of them is `.ai/` — so the adapter layer is what appears in the UI. That is
cosmetic, not a second copy: every listed path resolves to `.ai/`.

There is one exception worth knowing: **project instruction files are never listed**.

| Thing | Where it lives | Appears in the Customizations editor? |
|---|---|---|
| Skills, agents, prompts, `*.instructions.md` | `.ai/…` via adapters | Yes — under the adapter path |
| Project instructions (`AGENTS.md`, `copilot-instructions.md`) | Repository root and `.github/` | No — they are project instructions, not customization items |

`AGENTS.md` is therefore not "ignored" — it is simply not a listable item. Copilot
supports it directly (its project instruction files are `.github/copilot-instructions.md`
**or** `AGENTS.md`). This template generates `.github/copilot-instructions.md` from
`AGENTS.md` so the content reaches every Copilot surface. The copy is what Copilot must read,
and `.vscode/settings.json` sets `chat.useAgentsMdFile: false` so the Local harness does not
also load `AGENTS.md` (see the scope note below):

```
AGENTS.md  ──sync-instructions.py──▶  .github/copilot-instructions.md
(source of truth)                      (AGENTS.md verbatim + Copilot-only block)
```

`validate-copilot.py` asserts that `AGENTS.md` is embedded verbatim in the generated
file, so the two can never silently diverge. AGENTS.md wins; regenerate rather than edit
the Copilot file.

#### Can VS Code be pointed at `.ai/` directly?

Partly. VS Code can add search locations for some customization kinds, and forwards them
to Agent Host harnesses:

| Kind | Setting that adds a location | Works for |
|---|---|---|
| Instructions | `chat.instructionsFilesLocations` | VS Code sessions |
| Prompts | `chat.promptFilesLocations` | VS Code sessions. Not used here: prompts are skills |
| Agents | `chat.agentFilesLocations` | VS Code sessions. It takes a folder of custom agents, so it does not load `AGENTS.md`; do not add `"AGENTS.md": true` |
| Hooks | `chat.hookFilesLocations` | VS Code sessions. Not used here: hooks are wired in `.claude/settings.json` only |
| **Skills** | `chat.agentSkillsLocations` is deprecated and Local-harness only | **Not the Copilot harness** |

`AGENTS.md` itself is loaded by `chat.useAgentsMdFile`, not by a locations setting. Its scope is
narrow: the setting applies to **Local harness sessions only** and does not control Copilot
instruction discovery. Setting it to `false` stops the Local harness from loading the same text
twice, because `.github/copilot-instructions.md` already contains it. No setting controls the
Copilot harness, so there both files may still load.

Two consequences decide the template's design:

1. **Skills always need an adapter.** No supported setting adds `.ai/skills` for the
   Copilot harness, so `.github/skills` (or `.claude/skills`) must exist.
2. **Configured locations are editor-only.** Copilot CLI, the Copilot app, the cloud
   coding agent and Claude Code do not inherit them. Pointing settings at `.ai/` would
   make VS Code work and every other surface break — the opposite of tool-transparent.

So the template keeps the cross-tool adapter layer instead of per-editor settings. If a
project only ever uses one harness, `sync-platforms.py --tools claude` (or `copilot`)
creates just that harness's adapters.

**Sync:** Claude Code's `SessionStart` hook runs `sync-platforms.py` at session start, and its `PostToolUse` hook runs it after a write under `.ai/skills/`, `.ai/agents/` or `.ai/instructions/`. The VS Code task **Link .ai into the paths tools read** (`.vscode/tasks.json`) runs it on demand; it is not run on folder open. Copilot's runtime section tells the model to run the script when an adapter path is missing. You can also run `/sync-platforms` or `python .ai/scripts/sync-platforms.py` yourself at any time.

All adapter paths are gitignored, so a fresh clone has none of them until one of those triggers runs. `sync-platforms.py --tools claude` (or `copilot`, `agents`) limits creation to the tools a project actually uses; a real directory holding files at an adapter path is reported as `CONFLICT`, never deleted.

**Hooks are not a control.** The hook scripts in `.ai/scripts/hooks/` accept both Claude and
Copilot payload shapes and filter paths themselves. Whether the Copilot harness fires the
`.claude/settings.json` hooks is unverified; the probe in `.ai/tmp/hook-probe.log` answers it
(see the troubleshooting section). Copilot's session start and handoff behaviour is carried by
the runtime section of `.github/copilot-instructions.md`, not by the hooks.

## VS Code workspace settings

`.vscode/settings.json` is tracked and sets the workspace-level Copilot behaviour below. Workspace
settings take precedence over user settings, so a user setting does not turn these off.

| Setting | Value | Why | Harness |
|---|---|---|---|
| `chat.useAgentsMdFile` | `false` | Stops VS Code loading `AGENTS.md` a second time, because `copilot-instructions.md` embeds it | Local harness only. It does not control Copilot instruction discovery |
| `github.copilot.chat.cli.customAgents.enabled` | `true` | Enables custom agents (`.ai/agents/`) in Copilot harness sessions, so the orchestrator can delegate there | Copilot harness |
| `chat.useClaudeHooks` | `true` | Lets the Local harness run the hooks in `.claude/settings.json`. Hooks run only in a trusted workspace | Local harness |
| `chat.useAgentSkills` | `true` | Loads the skills under `.github/skills/` | Local harness (pinned) |
| `chat.includeApplyingInstructions` | `true` | Attaches path-scoped `.ai/instructions/` files by `applyTo` | Local harness (pinned) |
| `github.copilot.chat.codeGeneration.useInstructionFiles` | `true` | Uses instruction files during code generation | Local harness (pinned) |

"Pinned" means the workspace sets the value to `true` so a user setting cannot disable it. The
three pinned settings are Local-harness settings.

The Copilot harness reads `.claude/settings.json` hooks on its own (per vendor documentation). That
is not verified in this repository yet; `.ai/tmp/hook-probe.log` shows whether it runs them.

`.vscode/settings.json` also mirrors the `env` block of `.claude/settings.json` into
`terminal.integrated.env.*`, so VS Code terminals get the same environment as Claude Code.

The session-end build check is handled differently per tool. Claude Code runs it as the `Stop` hook.
Copilot has no `Stop` hook, so the runtime section tells it to run the same `dotnet build` before
its final reply when a solution exists and `src/` or `tests/` changed (`copilot-runtime.md`, section 4).

### How the settings reach a project

The template's `.vscode/settings.json` also holds settings for working on the template itself
(`python.testing.*`, `python.envFile`, `PIP_CONFIG_FILE`). Those are never shipped. A project
receives only the fragments `.ai/reference/templates/vscode/settings.json` and `tasks.json`,
merged into its own `.vscode/` files by AI Workspace Manager setup and by `upgrade-template.py`.
Both tools use the same rules, read from `.ai/reference/templates/merge-rules.json`:

- **Missing keys are added.** Objects merge key by key, so `terminal.integrated.env.windows` keeps
  a project's own variables (for example `PIP_CONFIG_FILE`) and gains the MSBuild variables.
- **Pinned keys** (`vscode.pinnedSettings`, the Copilot settings in the table above) take the
  template's value even when the project sets another. The project's comment on that line is kept,
  so the comment can describe a value that no longer applies.
- **Other conflicting values** keep the project's value and are reported as conflicts.
- **`tasks.json`** merges by `label`. A label that already exists is kept unchanged, even if its
  body differs. `version` is added only when absent.
- **Formatting and comments** are preserved; the merge edits the text and does not re-serialise it.
- **Invalid JSON** (or a duplicate key) makes the merge write nothing and report an error. VS Code
  accepts duplicate keys, so a file that works in VS Code can still be reported here.
- **Idempotent:** a second run changes nothing.

The same text-preserving merge handles `.claude/settings.json`: legacy hook commands listed in
`merge-rules.json` are removed, template hook groups are added unless their command is already
present, `permissions` lists are unioned, and other top-level keys follow the missing-key and
project-wins rules.

### What stays per-user

Some settings cannot be set from the workspace. Each developer sets them in their own VS Code or
GitHub account:

- **Sign-in and model choice.** Sign in to GitHub Copilot, or pick a model whose tool calls work in
  agent mode. Bring-your-own-key credentials are account-level.
- **Tool auto-approval.** The template deliberately does not set it.
- **Old user settings that mislead.** Remove `chat.agentFilesLocations` with an `AGENTS.md` entry,
  `chat.agentSkillsLocations` (deprecated, ignored by the Copilot harness), and any
  `chat.planAgent.defaultModel` or `inlineChat.defaultModel` that points at a model that fails tool calls.

## The orchestrator agent

`.ai/agents/orchestrator.md` is the coordinator and the entry point for GitHub Copilot. In VS Code,
select **orchestrator** in the agent dropdown. It always has the delegation tool and may run the nine
specialist agents, so you no longer need to tick **Run Subagent** for them.

- It is **not a delegation target**. Specialist agents do not delegate to it.
- Claude Code does not delegate to it. Claude's main conversation already acts as the orchestrator.
- If another agent or mode is active and no delegation tool is available, the runtime section
  (`.github/copilot-instructions.md`) tells the model to follow the fallback: read the agent's file
  and its skills and follow them directly.

## System Comparison

| Feature | Claude AI | GitHub Copilot |
|---------|-----------|----------------|
| **Primary Use** | Agentic workflows, architecture, planning | Code completion, inline suggestions |
| **Primary Config** | `AGENTS.md` (loaded by all clients) | `AGENTS.md` + `.github/copilot-instructions.md` supplement |
| **Context Management** | Session-based, progress tracking | Workspace-level, file-based |
| **Orchestration** | Multi-agent, structured tasks | Single completion context |
| **Skills** | `.claude/skills/` → `.ai/skills/` | `.github/skills/` → `.ai/skills/` |
| **Session State** | Persistent (session-context.md) | Ephemeral |

## Shared Resources

Both systems can reference:

**Standards & Rules:**
- `.ai/reference/critical-rules.md` - CQRS/DDD patterns
- `.ai/reference/forbidden-tech.md` - Technology standards
- `.ai/reference/glossary.md` - Terminology definitions
- `.ai/reference/naming-conventions.md` - Naming standards

**Patterns:**
- `.ai/patterns/cqrs-patterns.md` - CQRS implementation
- `.ai/patterns/api-patterns.md` - API endpoint patterns
- `.ai/patterns/testing-patterns.md` - Testing approaches
- `.ai/patterns/mvvm.md` - MVVM for Blazor/MAUI
- `.ai/patterns/microservices.md` - Microservices patterns
- `.ai/patterns/object-oriented-programming.md` - OOP principles
- `.ai/patterns/service-oriented-architecture.md` - SOA patterns
- `.ai/patterns/test-driven-development.md` - TDD approach

**Templates:**
- `.ai/reference/templates/*.txt` - Code templates for copy-paste

## Recommended Workflow

### Use Claude AI For:
- ✅ Multi-file feature implementations
- ✅ Architecture decisions and planning
- ✅ Complex refactoring across multiple files
- ✅ Creating test suites (unit + integration + BDD)
- ✅ Code reviews with checklist validation
- ✅ Database migrations
- ✅ Security reviews
- ✅ Performance optimization
- ✅ Documentation generation

### Use GitHub Copilot For:
- ✅ Inline code completion while typing
- ✅ Single-method implementations
- ✅ Quick boilerplate generation
- ✅ Simple test cases
- ✅ Comment-to-code generation
- ✅ Code suggestions during active development

### Use Both Together:
1. **Claude:** Plan architecture, create structure, implement core handlers
2. **Copilot:** Fill in method bodies, add validation, write simple tests
3. **Claude:** Review, verify against checklists, create integration tests
4. **Copilot:** Add XML docs, refine edge cases
5. **Claude:** Final verification and PR creation

## Configuration Updates

### When You Update Patterns

If you modify `.ai/patterns/` or `.ai/reference/`:

1. **No action needed for Claude** - Loads on-demand automatically
2. **Copilot:** Restart VS Code or reload window for changes to take effect

### When You Change Instructions, Skills or Agents

1. Edit the source under `.ai/instructions/`, `.ai/skills/` or `.ai/agents/`. Never edit an adapter path.
2. Run `python .ai/scripts/sync-platforms.py`. This regenerates `.claude/rules/` from `.ai/instructions/`, and creates or repairs the folder links.
3. Reload the VS Code window so Copilot re-reads the linked folders.

### When You Edit AGENTS.md

1. Edit `AGENTS.md` only. It is the source of truth.
2. Run `python .ai/scripts/sync-instructions.py`. This regenerates `.github/copilot-instructions.md` (the verbatim copy plus the runtime section) and keeps its project-owned block.
3. `validate-copilot.py` fails until the generated file matches `AGENTS.md`.

### When You Add New Standards

1. Add to `.ai/reference/`
2. Update `AGENTS.md` if the new standard alters task classifications or agent context, then regenerate `.github/copilot-instructions.md`
3. Reference it in the project-owned `copilot-reference` block of `.github/copilot-instructions.md` (between its markers; regeneration keeps that block), if Copilot needs a pointer that `AGENTS.md` does not carry

## Key Differences

### Claude's Advantages
- **Structured workflows** - Session management, progress tracking
- **Multi-agent orchestration** - Specialized skills for each domain
- **Long-running tasks** - Can work for hours with state preservation
- **Quality gates** - Pre-submission checklists
- **Architecture planning** - Can design before implementing

### Copilot's Advantages
- **Real-time suggestions** - As you type
- **Fast completions** - Immediate feedback
- **IDE integration** - Native VS Code experience
- **Context awareness** - Understands current file deeply
- **No setup** - Works immediately in editor

## Migration Path

If you're currently using only Copilot:

1. ✅ Keep `.github/copilot-instructions.md` (already created)
2. ✅ Copilot can now reference `.ai/reference/` and `.ai/patterns/`
3. ✅ No breaking changes to your workflow
4. ✅ Optionally add Claude for complex tasks

If you're currently using only Claude:

1. ✅ Add `.github/copilot-instructions.md` (already created)
2. ✅ Copilot can leverage your existing patterns
3. ✅ Claude workflows unchanged
4. ✅ Gain inline completion benefits

## Best Practices

### For Consistency
- ✅ Both systems reference same standards (`.ai/reference/`)
- ✅ Both systems follow same patterns (`.ai/patterns/`)
- ✅ Both systems use same token replacements
- ✅ Both systems respect forbidden technologies

### For Efficiency
- ✅ Use Claude for architecture and orchestration
- ✅ Use Copilot for rapid coding and completions
- ✅ Use Claude for final validation and PR creation
- ✅ Let both systems complement each other

### For Quality
- ✅ Claude enforces pre-submission checklist
- ✅ Copilot suggests standards-compliant code
- ✅ Both systems reference critical-rules.md
- ✅ Consistent patterns across all generated code

## Example Workflow

**Scenario:** Implement CRUD for new "Product" entity

```
1. Claude (via AGENTS.md):
   - Read session context
   - Load .ai/patterns/cqrs-patterns.md
   - Load .ai/skills/dotnet-engineer.md
   - Create Product entity structure
   - Generate command/query/handler files
   - Create endpoint scaffolding

2. Copilot (via AGENTS.md + .github/copilot-instructions.md):
   - Fill in validation logic in commands
   - Add guard clauses to handlers
   - Generate XML documentation
   - Suggest error handling patterns

3. Claude:
   - Create comprehensive test suite
   - Verify against .ai/checklists/pre-submission.md
   - Update session-context.md with learnings
   - Create PR with structured description
```

## Validation

Run the Copilot integration test to verify everything is in sync:

```bash
python3 .ai/tests/validate-copilot.py
```

This checks:
1. `.github/copilot-instructions.md` exists with no stale `.claude/` references, embeds `AGENTS.md` verbatim and embeds `.ai/reference/copilot-runtime.md`
2. `.github/skills/` exists
3. `.github/skills/` is a folder-level junction resolving to `.ai/skills/`
4. `.claude/skills/` is a folder-level junction resolving to `.ai/skills/`

`validate-adapters.py` (suite 15, 10 tests) checks the parity layout: no `${…}` prompt variables in
skills, no `.ai/prompts/` in the template, prompt adapters linked only while `.ai/prompts/` has
files, `.claude/instructions` absent, every agent body lists its skills and rules, `.claude/rules/`
matches what the generator would write, every hook command points at an existing file,
`.vscode/tasks.json` is tracked and not auto-run, `chat.useAgentsMdFile` is `false`, and the VS
Code fragments and `merge-rules.json` are valid and contained in the template's own `.vscode`
files. `test_hooks.py`, `test_jsonc_merge.py` and `test_sync_platforms.py` are pytest-only unit
suites for the hook scripts, the JSONC merge and the prompt-adapter rules.

If either check 3 or 4 fails, run `python .ai/scripts/sync-platforms.py` — a fresh
clone has no junctions because they are gitignored and cannot be tracked by git.

Run the full test suite to validate both Claude and Copilot setup:

```bash
bash .ai/tests/run-all-tests.sh
```

## Troubleshooting

### Copilot Says Skills Must Live in `.github/skills/`

That statement is correct — `.github/skills/` is Copilot's only project skill
location, and `.ai/skills/` is not a recognised location for any agent. The
template satisfies the requirement with a junction, so skills stay in `.ai/`.

Check the junction, not the content:

```bash
python .ai/scripts/sync-platforms.py --dry-run   # .github/skills -> .ai/skills should be OK
```

A missing `.github/skills/` almost always means the junction was never created on
this machine (it is gitignored), not that the skills are misplaced.

### Troubleshooting: Copilot ignores the rules or agents

Work through these in order. Steps 1 and 2 cause most failures in VS Code.

1. **Use a model that can run tool calls.**
   - Sign in to GitHub Copilot, or pick a model whose tool calls work in agent mode.
   - Observed failure: a bring-your-own-key DeepSeek model in thinking mode returns HTTP 400,
     `The reasoning_content in the thinking mode must be passed back to the API`. VS Code does
     not send that reasoning back, so each failure ends the agent turn in the middle of its tool
     loop. The steps that need several tool calls (delegating, reading the rules, writing the
     handoff) are the ones cut short. Vendor behaviour may change; re-test after model updates.
   - To confirm it, search `GitHub Copilot Chat.log` in VS Code's logs folder (on Windows,
     under `%APPDATA%\Code\logs`) for `reasoning_content`.
   - Also check `chat.planAgent.defaultModel` and `inlineChat.defaultModel`. Do not point them at a model that fails this way.

2. **Select the orchestrator agent (VS Code).**
   - Pick **orchestrator** in the agent dropdown. It has the delegation tool and runs the specialist agents.
   - Run Subagent (Agent mode → Configure Tools) is only needed when you run a different agent.
   - The runtime section names the delegation tool: `runSubagent` with the agent name in the
     Local harness, and `task` in the Copilot harness, Copilot CLI and the cloud agent. Tool
     names can change between releases; follow the names in the tool picker.
   - If no delegation tool is available, the runtime section tells the model to say so in one
     line and then read `.ai/agents/{name}.md` and its skills itself. If the reply shows neither
     a delegation nor that line, the model skipped the agent protocol.
   - The Local harness is scheduled for deprecation in February 2027 (checked 2026-11-17).
     Check the current vendor schedule before relying on it long term.

3. **Remove settings that mislead.**
   - `"chat.agentFilesLocations": {"AGENTS.md": true}` adds a folder of custom agents named
     `AGENTS.md`. It does not load the file. Remove it.
   - `chat.agentSkillsLocations` is deprecated and ignored by the Copilot harness. Remove it.
     Skills come from the `.github/skills/` link.
   - Do not set `chat.useAgentsMdFile` to `true` in this workspace. The workspace setting is
     `false` on purpose: in the Local harness, `.github/copilot-instructions.md` already embeds
     `AGENTS.md`, so enabling both loads the rules twice. The setting does not apply to the
     Copilot harness, where both files may load regardless.
   - Do not turn off the pinned settings (`chat.useAgentSkills`, `chat.includeApplyingInstructions`,
     `github.copilot.chat.codeGeneration.useInstructionFiles`). The workspace sets them to `true`;
     see "VS Code workspace settings".

4. **Check the generated files and links.**
   - `python .ai/scripts/sync-platforms.py --dry-run`: every adapter should report `OK`.
   - `.github/copilot-instructions.md` should contain the Copilot runtime section. If not, run
     `python .ai/scripts/sync-instructions.py`.
   - Path-scoped rules attach only when their `applyTo` matches the file being edited. If one
     did not load, the runtime section tells the model to read it directly; if it still is not
     read, check that `.github/instructions/` is a link to `.ai/instructions/`.

5. **Check whether the hooks fire in Copilot.** Start a new Copilot agent session, then read
   `.ai/tmp/hook-probe.log`. A line with `harness=other event=SessionStart` means a non-Claude
   harness ran the `SessionStart` hook from `.claude/settings.json`. Claude Code sessions write
   `harness=claude`. No new line means the hook did not run, or has not run yet. Either way the
   rules do not depend on the hook: the runtime section carries the session-start steps.
   The Local harness runs these hooks only when `chat.useClaudeHooks` is `true` (set in the
   workspace) and the workspace is trusted. If a Local session writes no probe line, check both.

6. **Reload the window** after changing settings, `AGENTS.md`, or anything under `.ai/instructions/`, `.ai/skills/` or `.ai/agents/`.

### Copilot Not Respecting Standards
- ✅ Work through "Troubleshooting: Copilot ignores the rules or agents" above first
- ✅ Ensure `.github/copilot-instructions.md` exists and is current: run `python .ai/scripts/sync-instructions.py` and check that the file matches `AGENTS.md`
- ✅ Reload VS Code window
- ✅ Check that file references in copilot-instructions.md are correct

### Claude Not Using Copilot Patterns
- ✅ Claude doesn't read `.github/copilot-instructions.md` (by design)
- ✅ Both systems independently reference `.ai/` resources
- ✅ No cross-contamination by design

### Conflicting Suggestions
- ✅ Both systems load the same master file: `AGENTS.md`
- ✅ Copilot's suggestions are just that - suggestions (you approve)
- ✅ Both align because they follow the same rules and reference same `.ai/reference/`

## Summary

**✅ YES** - You can use this template with Copilot!

- Both systems coexist peacefully
- Both reference the same standards and patterns
- Each system has its strengths
- No configuration conflicts
- Complementary workflows

The template is now **dual-mode**: Claude for orchestration, Copilot for completion. 🚀
