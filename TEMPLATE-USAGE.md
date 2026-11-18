# Template Usage Guide

> **See [README.md](./README.md) for a comprehensive overview, features, and quick start guide.**

This guide provides detailed instructions for using and customizing this .NET project template.

## What Is This Template?

A **generic, modular .NET project template** with:
- Clean Architecture + CQRS + DDD patterns
- Comprehensive development guidelines
- Code templates for rapid development
- Specialized agent skills for Claude Code and GitHub Copilot
- Quality checklists and best practices
- All tools read `.ai/skills/` and `.ai/agents/` through per-tool adapters — zero duplication

## Quick Start

### New Project — Install a Selection (Recommended)

Do not copy the whole catalog. AI Workspace Manager installs only the skills, agents and instructions the project needs, records the selection, and reports drift against upstream:

1. Install [AI Workspace Manager](#ai-workspace-manager-extension-recommended) from the Extensions view (or `code --install-extension I-Synergy.aiworkspacemanager`).
2. Open the project folder and choose a preset or individual items.
3. Let the extension install the selection. On first activation it also writes the resolver, vocabulary, `AGENTS.md`, the tool configuration, the project folders and the platform junctions.

### New Project — Manual Fallback (Copy Everything)

Use this only when the extension cannot be used — an air-gapped machine, no VS Code, or a deliberate full-library checkout. It copies every skill, agent and instruction into the project.

```bash
# Copy the AI context directory to your project root
cp -r /path/to/Template/.ai /path/to/YourProject/.ai

# Copy root config file
cp /path/to/Template/AGENTS.md /path/to/YourProject/

# Copy tool settings (minimal — junctions handle the rest)
mkdir -p /path/to/YourProject/.claude /path/to/YourProject/.github
cp /path/to/Template/.claude/settings.json /path/to/YourProject/.claude/
cp /path/to/Template/.github/copilot-instructions.md /path/to/YourProject/.github/
```

### What Is Always Copied

The resolver selects skills, agents and instructions only. These paths sit outside the selection because `AGENTS.md`, the agents and the skills cite them by literal path, so every project must carry them:

| Path | Why it is always present |
|------|--------------------------|
| `.ai/reference/` | `critical-rules.md`, `tokens.md`, `council.md`, … are cited by path |
| `.ai/patterns/` | CQRS, API, testing, MVVM and other patterns are cited by path |
| `.ai/checklists/` | Pre-submission gate used by the agent workflow |
| `.ai/project/`, `.ai/session-context.md` | Project-owned context and session memory |
| `.ai/scripts/`, `.ai/tests/` | Adapter sync, upgrade and the validation suites |

### Create the Tool Adapters

```bash
cd /path/to/YourProject
python .ai/scripts/sync-platforms.py                 # every supported tool
python .ai/scripts/sync-platforms.py --tools claude   # only the paths you use
```

This creates six folder links so every tool reads the same `.ai/skills/`, `.ai/agents/`
and `.ai/instructions/` source — `.claude/` and `.github/` for Claude Code and Copilot, plus
`.agents/skills/` for Codex-style agents. It also generates `.claude/rules/` (copies of
`.ai/instructions/`, with `applyTo` mapped to `paths:`). Adapter paths are gitignored, so
they are local: Claude Code recreates them on session start, the **Link .ai into the paths
tools read** VS Code task (`.vscode/tasks.json`) runs this command on demand, and you can
re-run it at any time. A real directory holding files at an adapter path is reported as
`CONFLICT` and left alone, because that would be a second copy.

`.github/copilot-instructions.md` is generated from `AGENTS.md`. After editing `AGENTS.md`, regenerate it with:

```bash
python .ai/scripts/sync-instructions.py
```

### Verify Installation

```bash
bash .ai/tests/run-all-tests.sh
```

Every suite should pass.

## AI Workspace Manager Extension (Recommended)

[AI Workspace Manager](https://marketplace.visualstudio.com/items?itemName=I-Synergy.aiworkspacemanager) is the VS Code front end for the template's catalog resolver and the supported way to set up a new project. It exists because a full catalog is too large to carry into every project: a repository would otherwise ship hundreds of skills it never uses, with no clear record of what is installed or what changed upstream.

Use it to choose a preset or individual items. The extension records the selection, installs only those items, and shows drift and upstream changes against the same resolver CI uses. On first activation it also writes the resolver, vocabulary, agent configuration, supporting folders, and platform junctions.

Install it from the Extensions view (search **AI Workspace Manager for VS Code**) or:

```bash
code --install-extension I-Synergy.aiworkspacemanager
```

### What It Does

1. Reads the catalog of available skills and agents.
2. Lets you choose a preset (for example Architecture or Security) or individual items.
3. Installs the chosen items into `.ai/skills/` and `.ai/agents/`.
4. Records what was installed so the selection can be reviewed or updated later.

After the extension installs a selection, run the junction sync once so every client sees the result:

```bash
python .ai/scripts/sync-platforms.py
```

### Local State vs Template Content

The extension writes machine-local state. This template ignores those paths so they are never committed:

| Path | Purpose |
|------|---------|
| `.ai/ai.json` | Project selection |
| `.ai/ai.lock.json` | Resolved revisions and content hashes |
| `.ai/tooling.json` | Bundled tooling manifest |
| `.ai/catalog/` | Catalog categories, presets, and schemas |
| `.ai/installed/` | Install markers for agents installed as single files |
| `.ai/scripts/catalog.py` | Catalog resolver provided by the extension |
| `*.ai-installed.json` | Per-item install markers |

`.ai/skills/` and `.ai/agents/` are different: they are the committed source of truth that all clients read through junctions. Commit those, not the extension state.

### Customize Project-Specific Files

Navigate to `.ai/project/` and customize these files. **Each file has a distinct purpose with NO duplication:**

| File | Purpose | Key Question | What to Customize |
|------|---------|--------------|-------------------|
| `preferences.md` | Personal workflow | **HOW** do you work? | Communication style, problem-solving approach, autonomy level, code style preferences |
| `tech-stack.md` | Technology choices | **WHAT** do you use? | Frameworks, libraries, versions, forbidden technologies, package management |
| `architecture.md` | System design | **HOW** is it structured? | Layers, patterns, data flow, CQRS implementation, ADRs, reference implementations |
| `domains.md` | Business context | **WHAT** are you building? | Business domains, entities, rules, events, validation, ubiquitous language |
| `session-context.md` | Session memory | Track across sessions | Project decisions, learnings, blocked paths, established patterns |

### Replace Tokens Throughout

Replace these tokens with your actual values:

| Token | Meaning | Example Usage |
|-------|---------|---------------|
| `{ApplicationName}` | Your application name | `{ApplicationName}.Domain.{Domain}` |
| `{Domain}` | Your bounded context | `{ApplicationName}.Domain.{Domain}` |
| `{Entity}` | Your aggregate root (PascalCase) | `Create{Entity}Command` |
| `{Entities}` | Aggregate root plural — DbSet names | `dataContext.{Entities}` |
| `{entity}` | Aggregate root (camelCase) | `{entity}Id` |
| `{entities}` | Aggregate root plural (camelCase) | `/{entities}` |
| `{ChildEntity}` | Child entity (PascalCase) | `{Entity}With{ChildEntities}Response` |
| `{ChildEntities}` | Child entity plural (PascalCase) | `dataContext.{ChildEntities}` |
| `{childEntity}` | Child entity (camelCase) | `{childEntity}Id` |
| `{childEntities}` | Child entity plural (camelCase) | `/{childEntities}` |

### Initialize Session Context

Edit `.ai/session-context.md` to establish your project's initial context:

```markdown
# {YourApplicationName} Session Context

**Last Updated:** [Date]
**Project Start:** [Date]

## Project Overview
- **Purpose:** [What your application does]
- **Tech Stack:** [Your chosen technologies]
- **Architecture:** Clean Architecture + CQRS + DDD

## Architectural Patterns Established
[Your initial architecture decisions]
```

## Directory Structure Explained

```
AGENTS.md                        # AI orchestration instructions (Claude Code loads it; VS Code reads it via copilot-instructions.md)

.vscode/
├── settings.json                # Template's own: pytest discovery, PIP_CONFIG_FILE; projects receive the Copilot keys and terminal env by merge
└── tasks.json                   # "Link .ai into the paths tools read" (run on demand); projects receive it by merge

.claude/
├── settings.json                # Claude Code configuration (SessionStart, PostToolUse, Stop hooks; permissions)
├── skills/  → .ai/skills/       # Junction — reads source directly
├── agents/  → .ai/agents/       # Junction — reads source directly
└── rules/                       # Generated copies of .ai/instructions/ (gitignored)

.github/
├── copilot-instructions.md      # GitHub Copilot instructions — generated from AGENTS.md + copilot-runtime.md
├── skills/  → .ai/skills/       # Junction — reads source directly
├── agents/  → .ai/agents/       # Junction — reads source directly
└── instructions/  → .ai/instructions/  # Junction — reads source directly

.agents/
└── skills/  → .ai/skills/       # Junction — read by Codex and other skills-standard agents

.ai/                            # All AI context (vendor-neutral, canonical source)
├── session-context.md          # Working session memory
├── reference/                  # Quick reference guides
│   ├── tokens.md               # Template tokens definition
│   ├── glossary.md             # Terminology
│   ├── critical-rules.md       # Non-negotiable patterns
│   ├── forbidden-tech.md       # Technologies to avoid
│   ├── naming-conventions.md   # Naming standards
│   └── templates/              # Code templates (.cs.txt, .feature.txt)
├── patterns/                   # Implementation patterns
│   ├── cqrs-patterns.md        # Complete CQRS guide
│   ├── api-patterns.md         # API endpoint patterns
│   ├── testing-patterns.md     # Testing patterns
│   └── ...                     # 8 patterns total
├── scripts/                    # Automation scripts
│   ├── sync-platforms.py       # Link .ai/ into the paths each tool reads (--tools to limit)
│   └── upgrade-template.py     # Safely upgrade existing projects
├── skills/                     # Specialized agent personas (source of truth)
├── agents/                     # Specialized subagents (runAs: subagent) and the orchestrator (Copilot entry point)
├── checklists/
│   └── pre-submission.md       # Comprehensive quality checklist
├── project/                    # CUSTOMIZE THESE FOR YOUR PROJECT
│   ├── preferences.md          # HOW you work (personal workflow/style)
│   ├── tech-stack.md           # WHAT you use (technologies/versions)
│   ├── architecture.md         # HOW it's structured (system design)
│   └── domains.md              # WHAT you're building (business context)
├── plans/                      # Plan files (written by Claude Code, local only)
├── progress/                   # Active task progress files
├── completed/                  # Completed task archives
└── tests/                      # Template validation suite
    ├── run-all-tests.sh        # Run all suites via bash
    ├── conftest.py             # Pytest shared fixtures
    ├── test_suite.py           # Pytest wrappers (VS Code Test Explorer)
    └── validate-*.py / *.sh   # Individual validation scripts
```

## Using Code Templates

### Example: Create a New Command

1. **Copy template:** `.ai/reference/templates/command-handler.cs.txt`
2. **Replace tokens:**
   - `{ApplicationName}` → your application name
   - `{Domain}` → your bounded context
   - `{Entity}` → your aggregate root
3. **Save as:** `src/{ApplicationName}.Domain.{Domain}/Features/{Entity}/Commands/Create{Entity}Command.cs`

### Token Replacement Example

**Template:**
```csharp
namespace {ApplicationName}.Domain.{Domain}.Features.{Entity}.Commands;

public sealed record Create{Entity}Command(...) : ICommand<Create{Entity}Response>;
```

**After Replacement:** every token is substituted with your own names, following the same
`{ApplicationName}.Domain.{Domain}` / `Create{Entity}Command` shape.

## Using Specialized Agent Skills

### Example: Implementing a New Feature

```
User: "Implement complete CRUD for {Entity} entity"

Claude will:
1. Load .ai/skills/dotnet-engineer/SKILL.md
2. Follow .ai/patterns/cqrs-patterns.md
3. Use templates from .ai/reference/templates/
4. Check .ai/checklists/pre-submission.md
```

### Example: Writing Tests

```
User: "Write comprehensive tests for {Entity} handlers"

Claude will:
1. Load .ai/skills/unit-tester/SKILL.md
2. Follow .ai/patterns/testing-patterns.md
3. Use test-class.cs.txt and feature-file.feature.txt templates
4. Create MSTest unit tests + Reqnroll BDD scenarios
```

### Example: Product Discovery & Design Interrogation Pipeline

Start with product discovery to interview stakeholders and build a product brief, then design-interrogation consumes that output to interrogate technical dimensions:

```
/product-discovery
  18 phases (0-17): intake/governance, problem, audience, users, value, scope, market, journeys, UX, UI, platforms, mocks/prototype, data/integrations, compliance, operations, launch, risks, completeness check
  Produces: product brief, audience profile, UX/UI design briefs, wireframes, mockups, clickable prototype
  
  → Interview transcribed into docs/product/{product-brief, audience-profile, ux-brief, ui-design-brief, platform-deliverables}.md
  → Wireframes, mockups, clickable prototype in docs/product/prototype/

/design-interrogation
  Consumes product-discovery output (no re-asking what's already decided)
  Phase -1: Document intake (reads docs/product/*)
  Phase  0: Strategic anchors (5 key decisions)
  Phase  1: Bounded context interrogation (parallel)
  Dimensions 1-8: Domain (plus migration immediately after for migrations), quality attributes
  Dimensions 9-15: Client surfaces, identity/access, data, delivery, observability, testing, AI/ML

  Produces session deliverables:
  → /ubiquitous-language   capture domain vocabulary
  → /usecase-specification  use cases with Gherkin
  → /user-story             INVEST-validated stories
  → Product Specification   consolidated what-we-build + technical requirements
  → /solution-generator     .NET solution scaffold
  → /vertical-slices        blueprint JSON per slice
  → /gap-review             validate against design
```

## Validating the Template

Run the validation suite to confirm everything is in order:

```bash
# Via bash (always available)
bash .ai/tests/run-all-tests.sh

# Via pytest (requires pip install pytest)
python -m pytest .ai/tests/test_suite.py -v
```

`run-all-tests.sh` skips `validate-upgrade-script.py`; the pytest wrapper includes it, so pytest is the fuller run.

### Installing pytest on a Corporate Network

If pip is configured to use a private registry that requires authentication, use the project-scoped override:

```bash
PIP_CONFIG_FILE=pip.ini pip install -r requirements-dev.txt
```

The `pip.ini` at the project root routes `pip install` to public PyPI. The `.vscode/settings.json` sets `PIP_CONFIG_FILE` automatically in VS Code terminals so you don't need to specify it manually.

### VS Code Test Explorer

Once pytest is installed:
1. Open the Testing panel in VS Code
2. Click **Configure Python Tests → pytest**
3. Every suite appears as a clickable test
4. Failed tests show the full script output inline

## Customizing for Your Stack

### Clear Separation of Concerns

- **preferences.md** = Personal workflow (communication, autonomy, code style)
- **tech-stack.md** = Technology choices (frameworks, versions, forbidden tech)
- **architecture.md** = System structure (layers, patterns, data flow)
- **domains.md** = Business context (entities, rules, events)

**No duplication means:**
- Update tech choices ONLY in `tech-stack.md`
- Update architectural patterns ONLY in `architecture.md`
- Update workflow preferences ONLY in `preferences.md`
- Update business logic ONLY in `domains.md`

### Example: Using Different Technologies

**If you use MediatR instead of another CQRS framework:**

1. **Update tech-stack.md:**
   ```markdown
   | **CQRS** | MediatR | 13.x | Industry standard, team familiarity |
   ```

2. **Update architecture.md** with MediatR-specific CQRS examples

3. **Update patterns (if needed):**
   Edit `.ai/patterns/cqrs-patterns.md` with MediatR-specific patterns

## Session Context Workflow

### Every Claude Session Should:

1. **Start:** Read `.ai/session-context.md`
2. **Work:** Follow established patterns
3. **End:** Update `.ai/session-context.md` with learnings using `.ai/reference/templates/session-handoff.md.txt`

### What to Document in Session Context

- **Architectural Decisions:** "We chose to use MediatR because..."
- **User Preferences:** "User prefers verbose logging in development"
- **Project-Specific Patterns:** "{Domain} domain is our reference implementation"
- **Blocked Paths:** "Tried approach X, didn't work because Y"

## Progress Tracking

### Progress File Format

```markdown
# Implement {Entity} CRUD

Status: IN PROGRESS
Started: 2026-04-19

## Steps
- [x] Created Create{Entity}Command and Handler
- [x] Created Get{Entity}ByIdQuery and Handler
- [ ] CreateUpdate{Entity}Command and Handler
- [ ] Create Delete{Entity}Command and Handler
- [ ] Create endpoints
- [ ] Write tests

## Notes
```

Files are created in `.ai/progress/`, updated with each step, and moved to `.ai/completed/` when done.

## Quality Assurance

### Before Completing Any Task

Run through `.ai/checklists/pre-submission.md`:

1. **Architecture verified**
2. **Code quality checked**
3. **CQRS patterns followed**
4. **Security validated**
5. **Tests written and passing**
6. **Documentation complete**

## Common Workflows

### Adding a New Domain

1. Create projects:
   ```
   {ApplicationName}.Entities.{NewDomain}/
   {ApplicationName}.Models.{NewDomain}/
   {ApplicationName}.Domain.{NewDomain}/
   {ApplicationName}.Services.{NewDomain}/
   ```
2. Copy templates from `.ai/reference/templates/`
3. Replace tokens with your domain/entity names
4. Follow patterns from `.ai/patterns/cqrs-patterns.md`
5. Check `.ai/checklists/pre-submission.md`

### Bulk Refactoring

```
/refactor

Steps:
1. Read reference material
2. Grep ALL files for the pattern (including string literals and log messages)
3. Apply replacements
4. Verify zero remaining instances
5. Fix any resulting build errors
6. Delete obsolete files
7. dotnet build
```

### Upgrading an Existing Project

```bash
python .ai/scripts/upgrade-template.py /path/to/YourProject

# Review each diff interactively:
# [a]ccept  [s]kip  [q]uit

# Or run non-interactively in CI:
python .ai/scripts/upgrade-template.py /path/to/YourProject --non-interactive
```

The same script installs the template into a project that has none of it — any
template-owned path the target lacks is reported as `ADDED` and copied.

#### What the script installs

Template-owned paths are copied when missing and diffed when they differ:

| Path | Notes |
|---|---|
| `.ai/**` | All skills, agents, patterns, reference, scripts, checklists, tests |
| `AGENTS.md` | Diffed, never silently replaced |
| `requirements-dev.txt` | Pinned PyYAML + pytest |
| `requirements-dev.lock` | Hash-pinned dependency lock installed by CI |
| `.sonarcloud.properties` | SonarCloud analysis scope + UTF-8 encoding |
| `pytest.ini` | `testpaths = .ai/tests` |
| `pip.ini` | Project-scoped PyPI index |
| `.gitignore` | Junction, `__pycache__` and `.ai/tmp/` ignores |
| `.github/workflows/validate-template.yml` | CI validation job |
| `.github/workflows/ci.yml` | Release versioning, tagging and publishing on merge to `main` |

Three files are merged, not copied or diffed. The template's shipped configuration is added to
your copy and your values are kept:

| Project file | What is merged | Result |
|---|---|---|
| `.vscode/settings.json` | The fragment `.ai/reference/templates/vscode/settings.json`: `chat.useAgentsMdFile: false` for the Local harness, `customAgents.enabled`, `chat.useClaudeHooks`, pinned skill and instruction loading, `chat.defaultConfiguration` with manual tool approval for new sessions, and the `terminal.integrated.env.*` build variables | Missing keys added; pinned Copilot keys set to the template value (your comment on that line is kept); other conflicts keep your value and are reported |
| `.vscode/tasks.json` | The fragment `.ai/reference/templates/vscode/tasks.json`: the **Link .ai into the paths tools read** task (run on demand, no folder-open run) | Tasks merged by `label`; a task with an existing label is kept unchanged |
| `.claude/settings.json` | The template's `.claude/settings.json` | Legacy hook commands listed in `merge-rules.json` removed; template hooks and `permissions` lists added (union); other keys added when missing; your values win on conflicts |

Pinned keys and the other merge rules are in `.ai/reference/templates/merge-rules.json`. Comments
and formatting are preserved. Invalid JSON in your file means nothing is written for it and the
error is reported. The template's own `.vscode/settings.json` also holds template-only settings
(`python.testing.*`, `PIP_CONFIG_FILE`) that are never shipped. See `.ai/reference/copilot-integration.md`,
section "How the settings reach a project".

#### What it never touches

`PROJECT_OWNED` paths are skipped with no read and no diff — `.ai/session-context.md`,
`.ai/project/`, `.ai/progress/`, `.ai/completed/`, `.ai/plans/`, `.ai/analysis/`,
`COMPLIANCE.md`, `.github/copilot-instructions.md` and `.claude/settings.local.json`.
The upgrade then regenerates `.github/copilot-instructions.md` from the project's `AGENTS.md`
(its project-owned `copilot-reference` block survives the regeneration), so the file is
rebuilt rather than copied or diffed.

`.github/workflows/ci.yml` is template-owned, so an upgrade copies it when missing and
diffs it when it differs. `CHANGELOG.md` is a normal project file: the release workflow
does not update it, and the upgrade does not copy or diff it.

`.gitignore` is a normal file, not a junction target, so if your project already has
one the upgrade shows a diff — accept it only after checking your own ignore rules are
still present. The entries the template needs are:

```gitignore
.claude/skills/
.claude/agents/
.claude/rules/*.instructions.md
.github/skills/
.github/agents/
.github/instructions/
.agents/skills/
.ai/tmp/
__pycache__/
.pytest_cache/
```

#### After any install or upgrade

```bash
pip install -r requirements-dev.txt
python .ai/scripts/sync-platforms.py      # recreate the six folder adapters and .claude/rules/
python -m pytest .ai/tests/test_suite.py -q
```

## Troubleshooting

### "Claude doesn't remember previous decisions"

**Solution:** Update `.ai/session-context.md` with decisions and preferences.

### "Generated code doesn't follow my patterns"

**Solution:** Document your patterns in `.ai/project/preferences.md` or `architecture.md` and reference them.

### "Progress files in wrong location"

**Solution:** Ensure agents create files in `.ai/progress/`, not `~/.claude/todos/` (use local markdown files, not the built-in task tools).

### "Forbidden technology used"

**Solution:** Update `.ai/reference/forbidden-tech.md` with your actual forbidden technologies.

### "Tests failing after upgrade"

**Solution:** Run `python .ai/tests/validate-skills.py` to check YAML frontmatter, then `bash .ai/tests/run-all-tests.sh` for the full suite.

### "pip install failing on corporate network"

**Solution:** Use the project-scoped pip config: `PIP_CONFIG_FILE=pip.ini pip install <package>`

## Best Practices

1. **Keep session-context.md updated** — It's Claude's memory across sessions
2. **Customize project/ files first** — Before starting development
3. **Respect file separation** — Don't duplicate info across preferences/tech-stack/architecture/domains
4. **Use cross-references** — Each file links to related files where appropriate
5. **Reference patterns explicitly** — Tell Claude which pattern file to follow
6. **Use checklists before completion** — Ensure quality
7. **Upgrade regularly** — Run the upgrade script when the template improves

## Template Maintenance

### Adding a New Skill

1. Create `.ai/skills/<skill-name>/SKILL.md` with correct YAML frontmatter
2. Skills are immediately available to all tools through the adapters — no copy step
3. A PostToolUse hook repairs the adapters when `.ai/skills/` files change
4. Add to the Work-Type Context Mapping table in `AGENTS.md`
5. Add to `README.md` skills table

### Updating an Existing Skill

Edit `.ai/skills/<skill-name>/SKILL.md` — every tool sees the change through its adapter path.

### After Cloning

```bash
python .ai/scripts/sync-platforms.py
```

This creates the six folder adapters and generates `.claude/rules/`. On Windows this requires no
special permissions (directory junctions are user-level). On macOS/Linux, standard symlinks are used.
Opening the repo in VS Code does not create them: the **Link .ai into the paths tools read** task
in `.vscode/tasks.json` does, when you run it (Terminal → Run Task). Claude Code creates them at
session start.

#### Upgrading from an older template

Earlier releases shipped `.ai/prompts/`. Prompts are skills now, so the upgrade does not delete
`.ai/prompts/` in your project. It prints a notice instead. Move any custom prompts into
`.ai/skills/<name>/SKILL.md` (with `disable-model-invocation: true` to keep them explicit-only),
then remove the folder. Prompt adapters follow `.ai/prompts/`: `.claude/commands/` and
`.github/prompts/` are linked to it only while it holds files, and `sync-platforms.py` removes
them when it is absent or empty. The retired `.claude/instructions/` is removed the same way when
it is a link or empty. Real content found at any of these paths is reported and left in place.

### Contributing Improvements

1. Keep improvements generic — use tokens, not specific project names
2. Update relevant modular file (not AGENTS.md unless the rule itself changes)
3. Run `bash .ai/tests/run-all-tests.sh` to validate
4. Update README.md if structural changes were made

---

**Remember:** This template is modular. Customize the `.ai/project/` files for your specific needs, and Claude will use those preferences throughout development.
