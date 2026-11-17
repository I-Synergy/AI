---
name: sync-platforms
description: Links the canonical .ai/ content into the paths agents actually read (.claude/, .github/, .agents/) and generates .claude/rules/ from .ai/instructions/. Run after adding, editing, or removing an item in .ai/skills/, .ai/agents/ or .ai/instructions/. Use when a tool must pick up a change made under .ai/, or when an adapter path is missing after a clone.
---

# Sync Platforms

Runs `.ai/scripts/sync-platforms.py` so every tool reads the same `.ai/` source
through folder-level links. No tool reads `.ai/` directly — each one hardcodes its own
paths — so the links are the adapter layer, and they hold no content of their own.

Adapters, by tool:

| Tool | Folder link | Source |
|---|---|---|
| Claude Code | `.claude/skills/`, `.claude/agents/` | `.ai/skills/`, `.ai/agents/` |
| GitHub Copilot | `.github/skills/`, `.github/agents/`, `.github/instructions/` | `.ai/skills/`, `.ai/agents/`, `.ai/instructions/` |
| Other skills-standard agents | `.agents/skills/` | `.ai/skills/` |

Claude Code reads path-scoped rules only from `.claude/rules/`, so for each
`.ai/instructions/{name}.instructions.md` the script writes a regular copy,
`.claude/rules/{name}.instructions.md`, mapping `applyTo` to `paths:` (`**/*` gets no `paths:`).
These copies are generated, gitignored and carry a generated-from marker. Never edit them;
edit the source in `.ai/instructions/`. Hand-written files in `.claude/rules/` are never touched.

Retired adapters (`.claude/commands/`, `.claude/instructions/`, `.github/prompts/`) are removed
when they are links or empty. Prompts are skills now (`.ai/skills/`), and `.ai/prompts/` no
longer exists in this template.

## Steps

1. **Dry run first**
   - Run `python .ai/scripts/sync-platforms.py --dry-run`
   - Report the CREATE / RECREATE lines, any SKIP for a missing source directory, and
     any CONFLICT line
   - If nothing would change, report "All tool adapters are already in sync" and stop

2. **Apply**
   - Run `python .ai/scripts/sync-platforms.py`
   - Add `--tools claude` (or `copilot`, `agents`) when the project uses only some tools
   - In VS Code, the same run is the task **Link .ai into the paths tools read** (`.vscode/tasks.json`), started from Terminal → Run Task. It does not run on folder open.
   - Report the results

3. **Verify**
   - `.claude/skills`, `.github/skills` and `.agents/skills` point at `.ai/skills`
   - `.claude/agents` and `.github/agents` point at `.ai/agents`
   - `.github/instructions` points at `.ai/instructions`
   - `.claude/rules/*.instructions.md` exists for each instruction file, with the generated-from marker
   - `.claude/commands`, `.claude/instructions` and `.github/prompts` are absent
   - no `.reasonix/` junction remains (the platform is no longer supported)
   - a CONFLICT means a real directory holds a copy: merge it into `.ai/`, delete it,
     then re-run — never delete the files without merging them

## Output Format

```
## Platform Sync Report

Dry run:
  OK       .github/skills -> .ai/skills
  CREATE   .agents/skills -> .ai/skills
  CONFLICT .claude/skills -> .ai/skills (real files, not a link)
  WOULD WRITE .claude/rules/csharp.instructions.md (from .ai/instructions/csharp.instructions.md)

Applied. Result:
  1 item(s) changed.
Merge each CONFLICT by hand: move its files into the canonical source, delete the
directory, then re-run this script.
```
