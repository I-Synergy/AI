# Plan: Merge VS Code workspace settings instead of copying them

Status: DONE (2026-11-17), see .ai/completed/vscode-settings-merge.md
Created: 2026-11-17
Repos: template `D:\Projects\Github\AI` and extension `D:\Projects\Github\AIWorkspaceManager`

## Findings

- **Extension:** `WorkspaceSetupService.InstallAgentConfig` (`src/AiWorkspaceManager.Core.Workspace/Setup/WorkspaceSetupService.cs`) never writes `.vscode/`. So the template's Copilot workspace settings never reach projects installed by the extension. It copies `.claude/settings.json` only when missing, so existing projects never receive hook updates.
- **Template:** `upgrade-template.py` lists `.vscode/settings.json` and `.vscode/tasks.json` as TEMPLATE_OWNED. Accepting the diff overwrites the project's whole file.
- **Template's own settings file:** `.vscode/settings.json` mixes settings for working on the template itself (`python.testing.*` on `.ai/tests`, `PIP_CONFIG_FILE` → `pip.ini`) with the settings meant for projects. The file can't be shipped as is.
- **Extension `GitignoreEntries`:** it lacks `.claude/rules/*.instructions.md`. (Ignoring `.github/hooks/` is correct: the extension links catalog hook items there per file; see the follow-up.)
- **Uncommitted work:** the extension repo has uncommitted changes, including in `MaintenanceService.cs` and `WorkspaceOperations.cs`. The work must build on them, not revert them.

## Approach

### Template (source of truth stays in `.ai/`)

1. Add the shipped fragments:
   - `.ai/reference/templates/vscode/settings.json`: the Copilot settings and the `terminal.integrated.env.*` build variables
   - `.ai/reference/templates/vscode/tasks.json`: the sync task

   The template's own `.vscode/settings.json` keeps its dev settings plus the fragment's keys. A validator asserts that the template's own files contain the fragment.
2. `upgrade-template.py`: drop `.vscode/*` from TEMPLATE_OWNED. Merge the fragments into the target's `.vscode/settings.json` and `tasks.json` using the merge rules below. Comments and formatting in the target are preserved.
3. Validators, tests and docs.

### Extension (.NET core, the code that runs for every project)

4. Add `JsoncMerger` in `AiWorkspaceManager.Core.Workspace`. It merges by editing the text and never re-serialises, so comments, trailing commas, ordering and formatting in the user's file survive. It finds object and array spans with `Utf8JsonReader` (`JsonCommentHandling.Skip`, trailing commas allowed) and inserts only the missing members.
5. `InstallAgentConfig` merges the template's `.ai/reference/templates/vscode/*.json` into `.vscode/settings.json` and `tasks.json`, and creates a file only if it is absent. If the template has no fragment (an older ref), it skips the step and never falls back to copying the template's own `.vscode` files. The result is reported in the summary: added keys, kept conflicts, created/merged/unchanged.
6. Unit tests in `tests/AiWorkspaceManager.Core.Workspace.Tests`.
7. README and CHANGELOG.

## Merge rules (both tools)

- **Missing file:** create it from the fragment.
- **Missing key:** add it.
- **Both values are objects:** merge recursively (e.g. `terminal.integrated.env.windows` keeps `PIP_CONFIG_FILE` and gains the MSBuild keys).
- **Same key, different scalar or array value:** **the project wins**. The value is kept and reported as a conflict, never overwritten.
- **`tasks.json`:** tasks merge by `label`. A missing label is appended; an existing label is kept unchanged. `version` is added only if absent.
- **Invalid JSON in the target:** write nothing and report the error.
- **Idempotent:** a second run changes nothing.

## Decisions (user, 2026-11-17)

1. **Conflicts:** the template wins for the **pinned** Copilot keys; the project wins for everything else (kept and reported).
2. **Scope:** also merge `.claude/settings.json` in the extension, and fix the extension's gitignore list.

## Shared merge data (source of truth in `.ai/`, read by both tools)

`.ai/reference/templates/merge-rules.json`:

```json
{
  "version": 1,
  "vscode": {
    "pinnedSettings": [
      "chat.useAgentsMdFile",
      "github.copilot.chat.cli.customAgents.enabled",
      "chat.useClaudeHooks",
      "chat.useAgentSkills",
      "chat.includeApplyingInstructions",
      "github.copilot.chat.codeGeneration.useInstructionFiles"
    ]
  },
  "claude": {
    "legacyHookCommands": ["<the four exact legacy strings now hardcoded in upgrade-template.py LEGACY_HOOK_COMMANDS>"]
  }
}
```

A pinned key is a top-level settings key: its value is replaced with the template's value and reported as "pinned".

## `.claude/settings.json` merge rules

- **Missing file:** copy it.
- **`hooks`:** for each event, remove hook entries whose `command` is in `legacyHookCommands`. Add each template hook group whose commands are not already present (compare by command string). Keep every other project hook.
- **`env`:** add missing keys; the project wins on conflicts.
- **`permissions.allow`, `permissions.deny`, `permissions.additionalDirectories`:** union, keeping the project's order and appending what is missing.
- **Other top-level keys** (e.g. `plansDirectory`): add if missing; the project wins.
- **Preserved:** formatting and comments, using the same text-surgery merger.

## Extension gitignore fix

- `GitignoreEntries`: add `.claude/rules/*.instructions.md`. Keep `.github/hooks/` (superseded: catalog hook links live there; see the follow-up).
- Existing lines in projects are never removed.

## Verification

- Template: full suite and pytest.
- Extension: `dotnet build` / `dotnet test` with `MSBUILDDISABLENODEREUSE=1` and `-nodeReuse:false`, plus its JS tests.
- Manual: run setup against a scratch project with a commented `.vscode/settings.json` and an existing task.

## Follow-up: align the extension's adapters and UI (user request, 2026-11-17)

The extension's `PlatformMirrorService` (`src/AiWorkspaceManager.Core.Workspace/Platforms/PlatformMirrorService.cs`, which has uncommitted user work) still uses the old adapter layout:
- It links `.ai/instructions` → `.claude/instructions`, a folder Claude never reads.
- It links `.ai/prompts` → `.claude/commands` and `.github/prompts`.
- It links catalog hook items per file into `.github/hooks/`.

The template's `sync-platforms.py` now removes the first two links as legacy. The two tools would undo each other on every run.

### Alignment, applying the copilot-parity council decision

- **Instructions:**
  - The extension stops linking `.claude/instructions` and removes it as a legacy link.
  - It generates `.claude/rules/{name}.instructions.md` copy-only, byte-identical to `sync-platforms.py` `render_rule` (same marker comment, `applyTo` → `paths:`, omitted for `**`/`**/*`).
  - It refuses to overwrite files without the marker and removes stale generated files only.
- **Prompts:**
  - Catalog prompt items, from third-party sources such as awesome-copilot, can still be installed into `.ai/prompts/`.
  - Both tools link `.claude/commands` and `.github/prompts` **only while `.ai/prompts/` exists and holds files**, and remove the links otherwise.
  - The template's own prompts are skills now, so a fresh template project has no `.ai/prompts`.
  - `sync-platforms.py` and `validate-adapters.py` TEST 3 change accordingly.
- **Hooks:**
  - User-installed catalog hook items keep their per-file `.github/hooks/` links. These are opt-in installs, not template hooks, so the C3 decision is unaffected.
  - `.github/hooks/` stays gitignored.

### UI (webview)

- **`settings-view.ts` client descriptions** say what each client actually gets:
  - Claude: `.claude/skills`, `agents`, generated `rules`, and the `settings.json` hooks.
  - Copilot: `.github/skills`, `agents`, `instructions`, `copilot-instructions.md` and the `.vscode` workspace settings.
  - Prompts are mentioned only as "if installed".
- **Kind filters and badges:** the Prompts kind shows a hint that the Copilot harness does not load prompt files; skills are the portable format.
- **Setup and maintenance results:** show the merge outcome per file — `.vscode/settings.json`, `.vscode/tasks.json`, `.claude/settings.json` — as created / merged (added, pinned) / unchanged / conflicts kept / error.
- **Mirror report:** shows the generated rules and the retired links.
