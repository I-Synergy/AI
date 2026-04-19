# Template Usage Guide

> **See [README.md](./README.md) for a comprehensive overview, features, and quick start guide.**

This guide provides detailed instructions for using and customizing this .NET project template.

## What Is This Template?

A **generic, modular .NET project template** with:
- Clean Architecture + CQRS + DDD patterns
- Comprehensive development guidelines
- Code templates for rapid development
- Specialized agent skills for Claude AI assistance
- Quality checklists and best practices
- GitHub Copilot integration via `.github/skills/`

## Quick Start

### New Project — Copy Template

```bash
# Copy the AI context directory to your project root
cp -r /path/to/Template/.ai /path/to/YourProject/.ai

# Copy Claude Code config
cp -r /path/to/Template/.claude /path/to/YourProject/.claude

# Copy CLAUDE.md to your project root
cp /path/to/Template/CLAUDE.md /path/to/YourProject/CLAUDE.md
```

### Existing Project — Use the Upgrade Script

If you already have a project based on an older version of this template:

```bash
# Interactive: review each changed file before accepting
python .ai/scripts/upgrade-template.py /path/to/YourProject

# Preview only — nothing written
python .ai/scripts/upgrade-template.py /path/to/YourProject --dry-run

# Skills only — copy new/updated skills, leave config untouched
python .ai/scripts/upgrade-template.py /path/to/YourProject --skills-only
```

The script never overwrites project-owned files (`CLAUDE.md`, `.ai/session-context.md`, `.ai/project/`, `.ai/progress/`, `.ai/plans/`, `.ai/completed/`).

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

| Token | Replace With | Example |
|-------|--------------|---------|
| `{ApplicationName}` | Your application name | `BudgetTracker` |
| `{Domain}` | Your domain names | `Budgets`, `Goals`, `Customers` |
| `{Entity}` | Your entity names | `Budget`, `Goal`, `Customer` |
| `{entity}` | Entity (lowercase) | `budget`, `goal`, `customer` |
| `{entities}` | Entity plural (lowercase) | `budgets`, `goals`, `customers` |

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
.claude/                        # Claude Code config only
├── settings.json               # Claude Code configuration (plansDirectory, hooks, permissions)
├── settings.local.json         # Local overrides (not committed)
└── skills/                     # Thin wrappers (auto-generated — do not edit)
    └── <skill>/SKILL.md        # !`cat .ai/skills/<skill>/SKILL.md`

.ai/                            # All AI context (vendor-neutral)
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
│   ├── sync-skills.py          # Sync .ai/skills/ → .claude/skills/ + .github/skills/
│   └── upgrade-template.py     # Safely upgrade existing projects
├── skills/                     # Specialized agent personas (source of truth)
│   ├── dotnet-engineer/SKILL.md
│   ├── unit-tester/SKILL.md
│   ├── refactor/SKILL.md
│   ├── design-interrogation/SKILL.md
│   ├── solution-generator/SKILL.md
│   ├── vertical-slices/SKILL.md
│   ├── gap-review/SKILL.md
│   ├── ubiquitous-language/SKILL.md
│   ├── usecase-specification/SKILL.md
│   ├── user-story/SKILL.md
│   ├── skill-creator/SKILL.md
│   └── ...                     # 27 skills total
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
└── tests/                      # 10-suite validation suite
    ├── run-all-tests.sh        # Run all suites via bash
    ├── conftest.py             # Pytest shared fixtures
    ├── test_suite.py           # Pytest wrappers (VS Code Test Explorer)
    └── validate-*.py / *.sh   # Individual validation scripts
```

## Using Code Templates

### Example: Create a New Command

1. **Copy template:** `.ai/reference/templates/command-handler.cs.txt`
2. **Replace tokens:**
   - `{ApplicationName}` → `BudgetTracker`
   - `{Domain}` → `Budgets`
   - `{Entity}` → `Budget`
3. **Save as:** `src/BudgetTracker.Domain.Budgets/Features/Budget/Commands/CreateBudgetCommand.cs`

### Token Replacement Example

**Template:**
```csharp
namespace {ApplicationName}.Domain.{Domain}.Features.{Entity}.Commands;

public sealed record Create{Entity}Command(...) : ICommand<Create{Entity}Response>;
```

**After Replacement:**
```csharp
namespace BudgetTracker.Domain.Budgets.Features.Budget.Commands;

public sealed record CreateBudgetCommand(...) : ICommand<CreateBudgetResponse>;
```

## Using Specialized Agent Skills

### Example: Implementing a New Feature

```
User: "Implement complete CRUD for Budget entity"

Claude will:
1. Load .ai/skills/dotnet-engineer/SKILL.md
2. Follow .ai/patterns/cqrs-patterns.md
3. Use templates from .ai/reference/templates/
4. Check .ai/checklists/pre-submission.md
```

### Example: Writing Tests

```
User: "Write comprehensive tests for Budget handlers"

Claude will:
1. Load .ai/skills/unit-tester/SKILL.md
2. Follow .ai/patterns/testing-patterns.md
3. Use test-class.cs.txt and feature-file.feature.txt templates
4. Create MSTest unit tests + Reqnroll BDD scenarios
```

### Example: Design Interrogation Pipeline

The design-interrogation skill orchestrates a full pipeline from raw requirements to implementation-ready blueprints:

```
/design-interrogation
  Phase -1: Document intake (upload specs, architecture docs)
  Phase  0: Strategic anchors (4 key decisions)
  Phase  1: Bounded context interrogation (parallel)

  Produces session deliverables:
  → /ubiquitous-language   capture domain vocabulary
  → /usecase-specification  use cases with Gherkin
  → /user-story             INVEST-validated stories
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

### Installing pytest on a Corporate Network

If pip is configured to use a private registry that requires authentication, use the project-scoped override:

```bash
pip install --config-file pip.ini pytest
```

The `pip.ini` at the project root routes `pip install` to public PyPI. The `.vscode/settings.json` sets `PIP_CONFIG_FILE` automatically in VS Code terminals so you don't need to specify it manually.

### VS Code Test Explorer

Once pytest is installed:
1. Open the Testing panel in VS Code
2. Click **Configure Python Tests → pytest**
3. All 10 suites appear as clickable tests
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
- **Project-Specific Patterns:** "Budget domain is our reference implementation"
- **Blocked Paths:** "Tried approach X, didn't work because Y"

## Progress Tracking

### Progress File Format

```markdown
# Implement Budget CRUD

Status: IN PROGRESS
Started: 2026-04-19

## Steps
- [x] Created CreateBudgetCommand and Handler
- [x] Created GetBudgetByIdQuery and Handler
- [ ] CreateUpdateBudgetCommand and Handler
- [ ] Create DeleteBudgetCommand and Handler
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

**Solution:** Use the project-scoped pip config: `pip install --config-file pip.ini <package>`

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
2. A PostToolUse hook auto-syncs to `.claude/skills/` and `.github/skills/`
3. If the hook isn't running: `python .ai/scripts/sync-skills.py`
4. Add to the Work-Type Context Mapping table in `CLAUDE.md`
5. Add to `README.md` skills table

### Updating an Existing Skill

Edit `.ai/skills/<skill-name>/SKILL.md` — the PostToolUse hook syncs the other tiers automatically.

### Contributing Improvements

1. Keep improvements generic — use tokens, not specific project names
2. Update relevant modular file (not CLAUDE.md unless the rule itself changes)
3. Run `bash .ai/tests/run-all-tests.sh` to validate
4. Update README.md if structural changes were made

---

**Remember:** This template is modular. Customize the `.ai/project/` files for your specific needs, and Claude will use those preferences throughout development.
