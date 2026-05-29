# .NET Development Template

Professional .NET development template with AI-powered agent orchestration and modular architecture.

## Overview

A **production-ready .NET project template** that provides comprehensive development patterns, specialized agent skills, and quality assurance tools for building enterprise applications with Clean Architecture, CQRS, and Domain-Driven Design.

AI context lives in `.ai/` (the single source of truth shared by Claude Code, GitHub Copilot, and Reasonix Code). Claude Code config stays in `.claude/settings.json`. Reasonix Code reads `REASONIX.md` at root.

## Features

### Specialized Skills (30)

| Skill | Purpose |
|-------|---------|
| **api-endpoints** | API endpoint creation, OpenAPI, Kiota clients, security hardening |
| **dotnet-engineer** | .NET development, CQRS implementation |
| **unit-tester** | Unit testing with MSTest and Moq |
| **code-reviewer** | Code quality and architecture compliance |
| **technical-writer** | Documentation and API specs |
| **playwright-tester** | UI testing and automation |
| **blazor-specialist** | Blazor web development |
| **maui-specialist** | MAUI mobile/desktop development |
| **architect** | Architecture decisions and patterns |
| **api-security** | API security and authentication |
| **security** | Application security |
| **software-security** | Security best practices |
| **performance-engineer** | Performance optimization |
| **devops-engineer** | CI/CD and deployment |
| **database-migration** | Database migrations and schema |
| **integration-specialist** | Third-party integrations |
| **refactor** | Bulk find-and-replace and pattern migrations across the solution |
| **design-interrogation** | Structured design interviews — stress-test plans, resolve decision trees |
| **skill-creator** | Create, test, and improve Claude skills iteratively |
| **ubiquitous-language** | Capture and maintain domain vocabulary glossary |
| **usecase-specification** | Draft and finalize use case specs with Gherkin |
| **user-story** | Draft and finalize INVEST-validated user stories with Gherkin |
| **solution-generator** | Scaffold a .NET solution from an architecture document |
| **vertical-slices** | Translate use cases/stories to vertical slice blueprint JSON |
| **gap-review** | Validate generated solution against original design decisions |
| **upgrade-template** | Sync template improvements to existing projects without losing context |
| **verify-config** | Audit CLAUDE.md against codebase (run `/verify-config`) |
| **update-skills** | Sync `.ai/skills/` to all targets (Claude Code, GitHub Copilot, Reasonix) (run `/update-skills`) |
| **book-to-skill** | Convert a technical book (PDF/EPUB) into a structured Claude Code skill |
| **keycloak-theme-colors** | Update Keycloak login theme accent colors from a base hex color |

### Pattern Guides (8)

| Pattern | Description |
|---------|-------------|
| **cqrs-patterns** | Complete Command/Query separation guide |
| **api-patterns** | RESTful API and Minimal API patterns |
| **testing-patterns** | Unit, integration, and BDD testing |
| **mvvm** | Model-View-ViewModel for UI |
| **microservices** | Microservices architecture patterns |
| **service-oriented-architecture** | SOA patterns and practices |
| **object-oriented-programming** | OOP principles and patterns |
| **test-driven-development** | TDD workflow and best practices |

### Template Tokens

| Token | Replace With | Example |
|-------|--------------|---------|
| `{ApplicationName}` | Your application name | `BudgetTracker` |
| `{Domain}` | Domain/bounded context | `Budgets`, `Goals`, `Debts` |
| `{Entity}` | Entity name (PascalCase) | `Budget`, `Goal`, `Debt` |
| `{entity}` | Entity name (lowercase) | `budget`, `goal`, `debt` |
| `{entities}` | Entity plural (lowercase) | `budgets`, `goals`, `debts` |

See `.ai/reference/tokens.md` for complete definitions.

## Quick Start

### New Project — Copy Template

```bash
# Copy AI context directory to your project root
cp -r ./.ai /path/to/YourProject/.ai

# Copy Claude Code config
cp -r ./.claude /path/to/YourProject/

# Copy Reasonix Code config
cp -r ./.reasonix /path/to/YourProject/

# Copy orchestration files
cp ./CLAUDE.md /path/to/YourProject/CLAUDE.md
cp ./REASONIX.md /path/to/YourProject/REASONIX.md
```

### Existing Project — Upgrade with Script

```bash
# Interactive upgrade — review each changed file before accepting
python .ai/scripts/upgrade-template.py /path/to/YourProject

# Preview only — no files written
python .ai/scripts/upgrade-template.py /path/to/YourProject --dry-run

# Skills only — copy new/updated skills without touching config
python .ai/scripts/upgrade-template.py /path/to/YourProject --skills-only
```

The script classifies every file as **template-owned** (safe to update, including `CLAUDE.md`) or **project-owned** (never overwritten — `.ai/project/`, `.ai/session-context.md`, `.ai/progress/`, `.ai/plans/`, `.ai/completed/`).

### Customize Project Files

Edit files in `.ai/project/` to customize for your project:

| File | Purpose | Key Question |
|------|---------|--------------|
| **preferences.md** | Personal workflow & style | **HOW** do you prefer to work? |
| **tech-stack.md** | Technology choices & versions | **WHAT** technologies do you use? |
| **architecture.md** | System design & patterns | **HOW** is your system structured? |
| **domains.md** | Business context & entities | **WHAT** are you building? |

### Replace Tokens

```bash
find /path/to/YourProject/.ai -type f -exec sed -i 's/{ApplicationName}/BudgetTracker/g' {} +
find /path/to/YourProject/.ai -type f -exec sed -i 's/{Domain}/Budgets/g' {} +
find /path/to/YourProject/.ai -type f -exec sed -i 's/{Entity}/Budget/g' {} +
```

### Initialize Session Context

Edit `.ai/session-context.md` to establish your project's initial state.

### Start Developing

```
/api-endpoints "Create CRUD endpoints for Budget entity"
```

## File Structure

```
/
├── CLAUDE.md                        # AI orchestration (auto-loaded by Claude Code)
├── REASONIX.md                      # AI orchestration (auto-loaded by Reasonix Code)
├── CLAUDE-v1.md                     # Previous version (reference)
├── TEMPLATE-USAGE.md                # Detailed usage guide
├── TEMPLATE-FAQ.md                  # Frequently asked questions
├── README.md                        # This file
├── pytest.ini                       # Pytest configuration (testpaths = .ai/tests)
├── pip.ini                          # Project-scoped pip config (overrides corporate registry)
├── .gitattributes                   # LF line endings enforced for *.sh
├── .gitignore                       # Excludes __pycache__, .pytest_cache
├── .vscode/
│   └── settings.json                # Pytest discovery + PIP_CONFIG_FILE terminal env
├── .claude/settings.json            # Claude Code configuration (hooks, permissions, additionalDirectories)
├── .claude/settings.local.json      # Local overrides (not committed)
│                                    # Note: skills/ wrappers are auto-generated — do not edit
├── .reasonix/                       # Reasonix Code skills (auto-synced from .ai/ — do not edit directly)
│   └── skills/                      # Thin wrappers referencing .ai/skills/ + subagent skills from .ai/agents/
├── REASONIX.md                      # Reasonix Code orchestration
└── .ai/                             # All AI context (vendor-neutral, shared by all assistants)
    ├── session-context.md           # Working session memory
    ├── reference/
    │   ├── critical-rules.md        # Non-negotiable patterns (read first)
    │   ├── forbidden-tech.md        # Technologies to avoid
    │   ├── tokens.md                # Token definitions
    │   ├── glossary.md              # Terminology
    │   ├── naming-conventions.md
    │   ├── copilot-integration.md
    │   └── templates/               # Code templates (.cs.txt, .feature.txt)
    │       ├── command-handler.cs.txt
    │       ├── query-handler.cs.txt
    │       ├── endpoint.cs.txt
    │       ├── test-class.cs.txt
    │       ├── feature-file.feature.txt
    │       └── session-handoff.md.txt
    ├── patterns/                    # Implementation guides
    │   ├── cqrs-patterns.md
    │   ├── api-patterns.md
    │   ├── testing-patterns.md
    │   ├── mvvm.md
    │   ├── microservices.md
    │   ├── service-oriented-architecture.md
    │   ├── object-oriented-programming.md
    │   └── test-driven-development.md
    ├── scripts/                     # Automation scripts
    │   ├── sync-skills.py           # Sync .ai/skills/ to Claude Code, GitHub Copilot, and Reasonix targets
    │   └── upgrade-template.py      # Safely upgrade an existing project from this template
    ├── agents/                      # Specialized subagents (source of truth)
    ├── skills/                      # Specialized agent personas (source of truth)
    │   ├── dotnet-engineer/SKILL.md
    │   ├── unit-tester/SKILL.md
    │   ├── code-reviewer/SKILL.md
    │   ├── technical-writer/SKILL.md
    │   ├── playwright-tester/SKILL.md
    │   ├── blazor-specialist/SKILL.md
    │   ├── maui-specialist/SKILL.md
    │   ├── architect/SKILL.md
    │   ├── api-security/SKILL.md
    │   ├── security/SKILL.md
    │   ├── software-security/SKILL.md
    │   ├── performance-engineer/SKILL.md
    │   ├── devops-engineer/SKILL.md
    │   ├── database-migration/SKILL.md
    │   ├── integration-specialist/SKILL.md
    │   ├── refactor/SKILL.md
    │   ├── design-interrogation/SKILL.md
    │   ├── skill-creator/SKILL.md
    │   ├── ubiquitous-language/SKILL.md
    │   ├── usecase-specification/SKILL.md
    │   ├── user-story/SKILL.md
    │   ├── solution-generator/SKILL.md
    │   ├── vertical-slices/SKILL.md
    │   ├── gap-review/SKILL.md
    │   ├── upgrade-template/SKILL.md
    │   ├── verify-config/SKILL.md
    │   ├── update-skills/SKILL.md
    │   ├── api-endpoints/SKILL.md
    │   ├── book-to-skill/SKILL.md
    │   └── keycloak-theme-colors/SKILL.md
    ├── checklists/
    │   └── pre-submission.md        # Quality gate — run before completing any task
    ├── project/                     # CUSTOMIZE THESE FOR YOUR PROJECT
    │   ├── preferences.md           # HOW you work (workflow, style, autonomy)
    │   ├── tech-stack.md            # WHAT you use (tech choices, versions)
    │   ├── architecture.md          # HOW it's structured (layers, patterns, flow)
    │   ├── domains.md               # WHAT you're building (business, entities)
    │   └── README.md
    ├── plans/                       # Plan files (written by Claude Code)
    ├── progress/                    # Active task tracking
    ├── completed/                   # Archived completed tasks
    ├── analysis/                    # Analysis files
    └── tests/                       # Template validation suite (11 suites)
        ├── run-all-tests.sh         # Run all 11 suites (bash)
        ├── conftest.py              # Pytest shared fixtures
        ├── test_suite.py            # Pytest wrappers for VS Code Test Explorer (11 tests)
        ├── validate-structure.sh
        ├── validate-skills.py
        ├── validate-references.sh
        ├── validate-content.py
        ├── validate-tokens.sh
        ├── validate-claude-md.py
        ├── validate-settings.py
        ├── validate-copilot.py
        ├── validate-reasonix.py
        ├── validate-upgrade-script.py
        └── smoke-test.py
```

### Skills Architecture (Four-Tier)

Skills live in `.ai/skills/` (single source of truth) and are synced to three targets:

| Target | Format | Purpose |
|--------|--------|---------|
| `.ai/skills/<name>/SKILL.md` | Full content | Source of truth — edit here |
| `.claude/skills/` (auto-managed) | Thin wrappers `!`cat .ai/...`` | Claude Code dynamic injection |
| `.github/skills/` (auto-managed) | Full content copies | GitHub Copilot reads directly |
| `.reasonix/skills/` (auto-managed) | Thin wrappers → `.ai/skills/` | Reasonix `run_skill` |

Agent definitions from `.ai/agents/` are also synced to `.reasonix/skills/` as `runAs: subagent` skills.

Run `/update-skills` (or `python .ai/scripts/sync-skills.py`) after adding or editing a skill. A PostToolUse hook auto-syncs on every `.ai/skills/` write.

### Specialized Agents (8)

All code and design work is delegated to specialized subagents — the main conversation handles only reasoning and user interaction.

| Agent | Model | Role |
|-------|-------|------|
| `architect` | **deepseek-v4-pro** | Feature design, pattern selection, component boundaries, architecture analysis |
| `reviewer` | **deepseek-v4-pro** | Code quality, SOLID, CQRS compliance, security review, architecture audit |
| `tester` | **deepseek-v4-pro** | MSTest/Reqnroll test design, BDD scenarios, integration test strategy |
| `designer` | **deepseek-v4-pro** | Visual design — color palettes, typography, branding, design tokens |
| `developer` | **deepseek-v4-flash** | .NET/C# — CQRS handlers, API endpoints, Blazor, EF Core, refactoring |
| `ui-developer` | **deepseek-v4-flash** | Blazor/MAUI components, layouts, CSS/styling, UX patterns |
| `ui-tester` | **deepseek-v4-flash** | Playwright E2E tests, accessibility checks, visual regression |
| `writer` | **deepseek-v4-flash** | XML docs, READMEs, ADRs, technical prose |

**Model mapping:** `deepseek-v4-pro` ↔ Claude `sonnet` tier · `deepseek-v4-flash` ↔ Claude `haiku` tier

Agents are defined in `.ai/agents/` and discovered via `.claude/agents/` wrappers or `.reasonix/skills/` subagent skills. Designers and UI developers self-test with Playwright before handoff.

## Testing

The template ships with an 11-suite validation suite. Run via bash or pytest:

```bash
# All suites via bash
bash .ai/tests/run-all-tests.sh

# All suites via pytest (requires: pip install pytest)
python -m pytest .ai/tests/test_suite.py -v

# VS Code Test Explorer: install pytest, then open Testing panel
```

On Windows with a corporate pip registry, use the project-scoped override:
```bash
pip install --config-file pip.ini pytest
```

The `.vscode/settings.json` sets `PIP_CONFIG_FILE` automatically in VS Code terminals.

| Suite | Script | What it checks |
|-------|--------|----------------|
| 1 | `validate-structure.sh` | Required directories, files, skill SKILL.md presence |
| 2 | `validate-skills.py` | YAML frontmatter in every SKILL.md |
| 3 | `validate-references.sh` | File references in CLAUDE.md and templates |
| 4 | `validate-content.py` | Content quality in skills and patterns |
| 5 | `validate-tokens.sh` | Token consistency across templates and skills |
| 6 | `validate-claude-md.py` | All `.ai/` paths in CLAUDE.md resolve to real files |
| 7 | `validate-settings.py` | `.claude/settings.json` structure and no stale refs |
| 8 | `validate-copilot.py` | Three-tier skill sync (`.ai/` source → Claude Code + `.github/`) |
| 9 | `smoke-test.py` | Skills loadable, names/descriptions unique |
| 10 | `validate-upgrade-script.py` | Upgrade script classification and integration |
| 11 | `validate-reasonix.py` | Reasonix integration: REASONIX.md, `.reasonix/skills/` wrappers, agent skills, sync integrity |

## Usage Examples

### Implementing a Feature

```
"Implement complete CRUD for Budget entity"

Claude will:
1. Read .ai/session-context.md
2. Load .ai/skills/dotnet-engineer/SKILL.md + .ai/patterns/cqrs-patterns.md
3. Use templates from .ai/reference/templates/
4. Track progress in .ai/progress/
5. Verify against .ai/checklists/pre-submission.md
6. Write handoff to .ai/session-context.md
```

### Writing Tests

```
"Write comprehensive tests for Budget handlers"

Claude will:
1. Load .ai/skills/unit-tester/SKILL.md + .ai/patterns/testing-patterns.md
2. Use test-class.cs.txt and feature-file.feature.txt templates
3. Create MSTest unit tests + Reqnroll BDD scenarios
```

### Design Interrogation Pipeline

```
/design-interrogation    # Phase -1 to Phase 1: intake → strategic anchors → BC interrogation
                         # Produces: ubiquitous language, use cases, user stories, solution scaffold
/solution-generator      # Scaffold .NET solution from architecture document
/vertical-slices         # Generate blueprint JSON per vertical slice
/gap-review              # Validate generated solution against design decisions
```

### Upgrading an Existing Project

```
/upgrade-template        # Interactive: review each changed file before accepting
                         # CLAUDE.md is updated (diffed), project-owned files are never touched
```

## Work-Type Context Mapping

Claude loads these files automatically based on your task type:

| Task Type | Files Loaded |
|-----------|-------------|
| .NET Development | `.ai/skills/dotnet-engineer/SKILL.md`, `.ai/patterns/object-oriented-programming.md` |
| CQRS | `.ai/skills/dotnet-engineer/SKILL.md`, `.ai/patterns/cqrs-patterns.md`, `.ai/reference/critical-rules.md`, templates |
| API Endpoints | `.ai/skills/api-endpoints/SKILL.md`, `.ai/patterns/api-patterns.md`, `.ai/reference/templates/endpoint.cs.txt`, `.ai/reference/critical-rules.md` |
| OpenAPI & Kiota | `.ai/skills/api-endpoints/SKILL.md`, `.ai/patterns/api-patterns.md`, `.ai/reference/critical-rules.md` |
| Unit Tests | `.ai/skills/unit-tester/SKILL.md`, `.ai/patterns/testing-patterns.md`, test templates |
| Blazor UI | `.ai/skills/blazor-specialist/SKILL.md`, `.ai/patterns/mvvm.md` |
| MAUI | `.ai/skills/maui-specialist/SKILL.md`, `.ai/patterns/mvvm.md` |
| Architecture | `.ai/skills/architect/SKILL.md`, `.ai/project/architecture.md` |
| Code Review | `.ai/skills/code-reviewer/SKILL.md`, `.ai/checklists/pre-submission.md` |
| Security | `.ai/skills/security/SKILL.md`, `.ai/skills/api-security/SKILL.md` |
| Bulk Refactoring | `.ai/skills/refactor/SKILL.md` |
| Design Interrogation | `.ai/skills/design-interrogation/SKILL.md` |
| Solution Scaffolding | `.ai/skills/solution-generator/SKILL.md`, `.ai/skills/vertical-slices/SKILL.md` |
| Gap Validation | `.ai/skills/gap-review/SKILL.md` |
| Domain Modeling | `.ai/skills/ubiquitous-language/SKILL.md`, `.ai/skills/usecase-specification/SKILL.md`, `.ai/skills/user-story/SKILL.md` |
| Skill Creation | `.ai/skills/skill-creator/SKILL.md` |

## Customization

### Required Before Starting

1. Edit files in `.ai/project/` with your project specifics
2. Replace all `{tokens}` with your actual values
3. Update `.ai/reference/forbidden-tech.md` for your stack
4. Initialize `.ai/session-context.md`

### Optional

1. Add domain-specific patterns to `.ai/patterns/`
2. Create custom skills in `.ai/skills/`
3. Add project-specific checklists to `.ai/checklists/`
4. Modify code templates in `.ai/reference/templates/`

## Session Management

Every session (Claude Code, GitHub Copilot, and Reasonix Code):
1. **Start** — Read `.ai/session-context.md`
2. **Review** — Check `.ai/completed/` for relevant prior work
3. **Track** — Write progress to `.ai/progress/{task-slug}.md` in real time (MANDATORY — `todo_write` is ephemeral and does NOT replace `.ai/progress/` files)
4. **End** — Write handoff to `.ai/session-context.md` using `.ai/reference/templates/session-handoff.md.txt`

## Supported Technologies

### Default Stack (Fully Customizable)

- **.NET:** 10+ (C# 14)
- **ORM:** Entity Framework Core 10
- **Database:** PostgreSQL, SQL Server
- **CQRS:** I-Synergy.Framework.CQRS (NOT MediatR)
- **Mapping:** Manual (`new T(...)` / LINQ `.Select`) — no mapping library
- **Testing:** MSTest + Moq + Reqnroll (NOT xUnit, NOT NUnit)
- **API:** ASP.NET Core Minimal APIs + `Microsoft.AspNetCore.OpenApi` + Kiota client generation
- **UI:** Blazor, MAUI
- **Validation:** Data Annotations (NOT FluentValidation)

### Architectural Patterns

- **Clean Architecture** — Layered separation of concerns
- **CQRS** — Command/Query Responsibility Segregation
- **Domain-Driven Design** — Aggregates, entities, value objects
- **Vertical Slice Architecture** — Feature folders per entity

## Documentation

| File | Purpose |
|------|---------|
| `README.md` | This file — overview and quick reference |
| `CLAUDE.md` | AI orchestration (auto-loaded by Claude Code) |
| `TEMPLATE-USAGE.md` | Detailed usage and customization guide |
| `TEMPLATE-FAQ.md` | Frequently asked questions |
| `.ai/reference/critical-rules.md` | Non-negotiable coding patterns |
| `.ai/patterns/api-patterns.md` | API endpoints, OpenAPI, Kiota, security hardening |
| `.ai/reference/forbidden-tech.md` | Banned libraries and approaches |
| `.ai/project/` | Project-specific context files |

## [License](LICENSE)