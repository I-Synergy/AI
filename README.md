# .NET Development Template

Professional .NET development template with AI-powered agent orchestration and modular architecture.

## Overview

A **production-ready .NET project template** that provides comprehensive development patterns, specialized agent skills, and quality assurance tools for building enterprise applications with Clean Architecture, CQRS, and Domain-Driven Design.

AI context lives in `.ai/` (the single source of truth shared by Claude Code, GitHub Copilot, Pi, and Reasonix Code). Each tool reads the same files through directory junctions — no duplication, no sync lag.

## Features

### Specialized Skills

| Skill | Purpose |
|-------|---------|
| **api-endpoints** | API endpoint creation, OpenAPI, Kiota clients, security hardening |
| **dotnet-engineer** | .NET development, CQRS implementation |
| **unit-tester** | Unit testing with MSTest and Moq |
| **code-reviewer** | Code quality and architecture compliance |
| **technical-writer** | Documentation and API specs |
| **playwright-tester** | UI testing and automation |
| **blazor-specialist** | Blazor web development |
| **blazor-theme-generator** | Generate Blazor UI themes from design tokens |
| **maui-specialist** | MAUI mobile/desktop development |
| **mobile-release** | Publish MAUI apps to the App Store and Google Play |
| **winui-specialist** | WinUI 3 desktop development |
| **xaml-theme-generator** | Generate XAML theme resources from a base color palette |
| **architect** | Architecture decisions and patterns |
| **api-security** | API security and authentication |
| **security** | Application security |
| **software-security** | Security best practices |
| **performance-engineer** | Performance optimization |
| **devops-engineer** | CI/CD and deployment |
| **css-theme-generator** | Generate CSS theme variables from a base color palette |
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
| **hugo** | Hugo static site generation — blog, docs, and landing page templates |
| **upgrade-template** | Sync template improvements to existing projects without losing context |
| **verify-config** | Audit CLAUDE.md against codebase (run `/verify-config`) |
| **update-skills** | Sync `.ai/skills/` to all targets (Claude Code, GitHub Copilot, Reasonix) (run `/update-skills`) |
| **book-to-skill** | Convert a technical book (PDF/EPUB) into a structured Claude Code skill |
| **keycloak-theme-colors** | Update Keycloak login theme accent colors from a base hex color |
| **council** | High-stakes decision process — independent seat positions, chair synthesis, dissent recorded verbatim |

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
| `{Entities}` | Entity plural (PascalCase) — used for DbSet names | `Budgets`, `Goals`, `Debts` |
| `{entity}` | Entity name (lowercase) | `budget`, `goal`, `debt` |
| `{entities}` | Entity plural (lowercase) | `budgets`, `goals`, `debts` |

See `.ai/reference/tokens.md` for complete definitions.

## Quick Start

### 1. Copy the Template

```bash
# Copy AI context to your project root
cp -r ./.ai /path/to/YourProject/.ai

# Copy root config files
cp ./CLAUDE.md /path/to/YourProject/
cp ./REASONIX.md /path/to/YourProject/
cp ./AGENTS.md /path/to/YourProject/

# Copy tool configs (minimal — junctions do the rest)
cp -r ./.claude/settings.json /path/to/YourProject/.claude/
cp -r ./.pi/settings.json /path/to/YourProject/.pi/
cp -r ./.github/copilot-instructions.md /path/to/YourProject/.github/
```

### 2. Create Junctions (One Command)

All platforms read `.ai/skills/` and `.ai/agents/` through directory junctions — no file copies.

```bash
cd /path/to/YourProject
python .ai/scripts/sync-skills.py
```

This creates:

| Junction | → Source | Used By |
|----------|----------|---------|
| `.claude/skills` | `.ai/skills` | Claude Code |
| `.claude/agents` | `.ai/agents` | Claude Code |
| `.github/skills` | `.ai/skills` | GitHub Copilot |
| `.github/agents` | `.ai/agents` | GitHub Copilot |
| `.reasonix/skills` | `.ai/skills` | Reasonix Code |
| `.reasonix/agents` | `.ai/agents` | Reasonix Code |
| `.pi/skills` | `.ai/skills` | Pi |
| `.pi/agents` | `.ai/agents` | Pi |
| `.pi/chains` | `.ai/chains` | Pi |

All junction targets are in `.gitignore` — zero git bloat.

### 3. Per-Tool Setup

#### Claude Code

Claude Code auto-loads `CLAUDE.md` at the project root and discovers skills/agents from `.claude/` junctions. No additional setup needed.

```bash
claude  # start in project root
```

#### GitHub Copilot

GitHub Copilot reads `.github/copilot-instructions.md` and discovers skills from `.github/skills/` junction. Works automatically in VS Code / GitHub Codespaces.

#### Pi

Pi loads `AGENTS.md` for runtime instructions. Skills and agents are discovered from `.pi/` junctions.

```bash
pi  # start in project root
```

`.pi/settings.json` is empty — all configuration comes from `.ai/` via junctions.

#### Reasonix Code

Reasonix Code auto-loads `REASONIX.md` at the project root. Skills are loaded from `.reasonix/skills/` junction; agents from `.reasonix/agents/` (each has `runAs: subagent` for subagent discovery).

### 4. Verify

```bash
bash .ai/tests/run-all-tests.sh
```

Every suite should pass.

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
find /path/to/YourProject/.ai -type f -exec sed -i 's/{Entities}/Budgets/g' {} +
find /path/to/YourProject/.ai -type f -exec sed -i 's/{entity}/budget/g' {} +
find /path/to/YourProject/.ai -type f -exec sed -i 's/{entities}/budgets/g' {} +
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
├── AGENTS.md                        # Pi runtime instructions (auto-loaded)
├── CLAUDE.md                        # Claude Code orchestration (auto-loaded)
├── REASONIX.md                      # Reasonix Code orchestration (auto-loaded)
├── DEEPSEEK.md                      # DeepSeek backend orchestration (swapped over CLAUDE.md)
├── TEMPLATE-USAGE.md                # Detailed usage guide
├── TEMPLATE-FAQ.md                  # Frequently asked questions
├── README.md                        # This file
├── LICENSE                          # MIT license
├── pytest.ini                       # Pytest configuration (testpaths = .ai/tests)
├── pip.ini                          # Project-scoped pip config
├── .gitattributes                   # LF line endings enforced for *.sh
├── .gitignore                       # Excludes junction targets + pycache
├── .vscode/
│   └── settings.json                # Pytest discovery + PIP_CONFIG_FILE
├── .claude/
│   ├── settings.json                # Claude Code config (hooks, permissions)
│   ├── settings.local.json          # Local permission overrides
│   ├── skills/  → .ai/skills/       # Junction — do not edit
│   └── agents/  → .ai/agents/       # Junction — do not edit
├── .github/
│   ├── copilot-instructions.md      # GitHub Copilot instructions
│   ├── workflows/
│   │   ├── validate-template.yml    # Runs the validation suite in CI
│   │   └── mirror-to-azure.yml      # Mirrors GitHub → Azure DevOps (see below)
│   ├── skills/  → .ai/skills/       # Junction — do not edit
│   └── agents/  → .ai/agents/       # Junction — do not edit
├── .reasonix/
│   ├── skills/  → .ai/skills/       # Junction — do not edit
│   └── agents/  → .ai/agents/       # Junction — do not edit
├── .pi/
│   ├── settings.json                # Empty — config via junctions
│   ├── skills/  → .ai/skills/       # Junction — do not edit
│   ├── agents/  → .ai/agents/       # Junction — do not edit
│   └── chains/  → .ai/chains/       # Junction — do not edit
├── powershell/                      # Anthropic ↔ DeepSeek backend switcher
│   ├── Microsoft.PowerShell_profile.ps1
│   └── README.md                    # Setup and usage
└── .ai/                             # All AI context (vendor-neutral, shared by all assistants)
    ├── session-context.md           # Working session memory
    ├── reference/
    │   ├── critical-rules.md        # Non-negotiable patterns (read first)
    │   ├── forbidden-tech.md        # Technologies to avoid
    │   ├── tokens.md                # Token definitions
    │   ├── glossary.md              # Terminology
    │   ├── naming-conventions.md
    │   ├── copilot-integration.md
    │   ├── task-execution.md        # ReAct loop, escalation, subagent templates
    │   ├── work-type-mapping.md     # Which files to load per task type
    │   ├── operational-rules.md     # Refactoring and file-management conventions
    │   ├── session-management.md    # Session lifecycle
    │   ├── aot-and-trimming.md      # Native AOT and trimming lessons
    │   ├── readme-maintenance.md    # README update requirements
    │   ├── council.md               # Council principle — high-stakes decisions
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
    │   ├── sync-agents.py           # Agent-side entry point (delegates to sync-skills.py)
    │   ├── hygiene-lint.py          # Read-only hygiene lint — stale progress, committed secrets
    │   ├── migrate-to-ai.py         # Migrate a repo from the old .claude/ layout to .ai/
    │   └── upgrade-template.py      # Safely upgrade an existing project from this template
    ├── agents/                      # Specialized subagents (source of truth)
    ├── skills/                      # Specialized agent personas (source of truth)
    │   ├── dotnet-engineer/SKILL.md
    │   ├── unit-tester/SKILL.md
    │   ├── code-reviewer/SKILL.md
    │   ├── technical-writer/SKILL.md
    │   ├── playwright-tester/SKILL.md
    │   ├── blazor-specialist/SKILL.md
    │   ├── blazor-theme-generator/SKILL.md
    │   ├── css-theme-generator/SKILL.md
    │   ├── maui-specialist/SKILL.md
    │   ├── mobile-release/SKILL.md
    │   ├── winui-specialist/SKILL.md
    │   ├── xaml-theme-generator/SKILL.md
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
    │   ├── hugo/SKILL.md
    │   ├── upgrade-template/SKILL.md
    │   ├── verify-config/SKILL.md
    │   ├── update-skills/SKILL.md
    │   ├── api-endpoints/SKILL.md
    │   ├── book-to-skill/SKILL.md
    │   ├── keycloak-theme-colors/SKILL.md
    │   └── council/SKILL.md
    ├── chains/                      # Chain definitions (pi runner)
    │   ├── council.chain.md         # Council protocol (see .ai/reference/council.md)
    │   ├── implement-and-review.chain.md
    │   └── scout-plan-implement.chain.md
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
    └── tests/                       # Template validation suite
        ├── run-all-tests.sh         # Run every suite via bash
        ├── conftest.py              # Pytest shared fixtures
        ├── test_suite.py            # Pytest wrappers for VS Code Test Explorer
        ├── validate-structure.sh
        ├── validate-skills.py
        ├── validate-references.sh
        ├── validate-content.py
        ├── validate-tokens.sh
        ├── validate-claude-md.py
        ├── validate-settings.py
        ├── validate-copilot.py
        ├── smoke-test.py
        ├── validate-reasonix.py
        ├── validate-pi.py
        └── validate-upgrade-script.py
```

### Skills Architecture — Directory Junctions

Skills and agents live in `.ai/skills/` and `.ai/agents/` (single source of truth). All platforms read the exact same files through directory junctions — no wrappers, no copies, no sync.

```
.ai/skills/              ← Edit here (canonical source)
.ai/agents/              ← Agent definitions with runAs: subagent

.claude/skills/   → junction → .ai/skills/
.claude/agents/   → junction → .ai/agents/
.github/skills/   → junction → .ai/skills/
.github/agents/   → junction → .ai/agents/
.reasonix/skills/ → junction → .ai/skills/
.reasonix/agents/ → junction → .ai/agents/
.pi/skills/       → junction → .ai/skills/
.pi/agents/       → junction → .ai/agents/
.pi/chains/       → junction → .ai/chains/
```

Git cannot track Windows junctions (or symlinks, with the common `core.symlinks=false` default), so a fresh clone has **none** of these 9 paths until they're created locally. A `SessionStart` hook in `.claude/settings.json` runs the sync automatically the moment a Claude Code session opens in the repo, and a `PostToolUse` hook re-runs it whenever `.ai/skills/` or `.ai/agents/` files change — so Claude Code sessions self-heal with no manual step.

Other tools (GitHub Copilot, Reasonix Code, pi) don't have an equivalent session-start hook, so after cloning — or before using one of those tools for the first time — run once manually:

```bash
python .ai/scripts/sync-skills.py
```

This creates (or repairs) all 9 junctions; it's idempotent and safe to re-run at any time.

### Specialized Agents

All code and design work is delegated to specialized subagents — the main conversation handles only reasoning and user interaction.

| Agent | Role |
|-------|------|
| `architect` | Feature design, pattern selection, component boundaries, architecture analysis |
| `reviewer` | Code quality, SOLID, CQRS compliance, security review, architecture audit |
| `security` | Blast-radius and exposure analysis, threat modelling, OWASP review, dependency and secret audits |
| `tester` | MSTest/Reqnroll test design, BDD scenarios, integration test strategy |
| `designer` | Visual design — color palettes, typography, branding, design tokens |
| `developer` | .NET/C# — CQRS handlers, API endpoints, Blazor, EF Core, refactoring |
| `ui-developer` | Blazor/MAUI components, layouts, CSS/styling, UX patterns |
| `ui-tester` | Playwright E2E tests, accessibility checks, visual regression |
| `writer` | XML docs, READMEs, ADRs, technical prose |

Each agent's `model:` frontmatter in `.ai/agents/` carries the tier alias (`sonnet` or `haiku`); the concrete model behind each slot is defined by the backend profile in `powershell/Microsoft.PowerShell_profile.ps1`.

Agents are defined in `.ai/agents/` — each carries `runAs: subagent` — and every tool reads them through a folder-level junction (`.claude/agents/`, `.github/agents/`, `.reasonix/agents/`, `.pi/agents/`). Designers and UI developers self-test with Playwright before handoff.

## Testing

The template ships with a validation suite that runs the same checks under bash or pytest:

```bash
# Every suite via bash
bash .ai/tests/run-all-tests.sh

# Every suite via pytest (requires: pip install pytest)
python -m pytest .ai/tests/test_suite.py -v

# VS Code Test Explorer: install pytest, then open Testing panel
```

`run-all-tests.sh` skips `validate-upgrade-script.py`; the pytest wrapper includes it, so pytest is the fuller run.

On Windows with a corporate pip registry, use the project-scoped override:
```bash
pip install --config-file pip.ini pytest
```

The `.vscode/settings.json` sets `PIP_CONFIG_FILE` automatically in VS Code terminals.

| Script | What it checks |
|--------|----------------|
| `validate-structure.sh` | Required directories, files, skill SKILL.md presence |
| `validate-skills.py` | YAML frontmatter in every SKILL.md |
| `validate-references.sh` | File references in CLAUDE.md, README.md links, and templates |
| `validate-content.py` | Content quality in skills and patterns |
| `validate-tokens.sh` | Token consistency across templates and skills |
| `validate-claude-md.py` | All `.ai/` paths in CLAUDE.md resolve to real files |
| `validate-settings.py` | `.claude/settings.json` structure and no stale refs |
| `validate-copilot.py` | Three-tier skill sync (`.ai/` source → Claude Code + `.github/`) |
| `smoke-test.py` | Skills loadable, names/descriptions unique |
| `validate-reasonix.py` | Reasonix integration: REASONIX.md, `.reasonix/` junctions, agent skills, sync integrity |
| `validate-pi.py` | Pi integration: `.pi/` junctions (`skills`, `agents`, `chains`) and `settings.json` |
| `validate-upgrade-script.py` | Upgrade script classification and integration — pytest only |

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

### High-Stakes Decisions (Council)

```
/council                 # For decisions that are expensive to reverse — seats briefed with
                         # conflicting mandates: Design, Rules, Security, Verifiability, Feasibility
                         # Advisory verdict, chair synthesis, dissent recorded verbatim — never a vote
```

## Work-Type Context Mapping

Claude loads these files automatically based on your task type:

| Task Type | Files Loaded |
|-----------|-------------|
| .NET Development | `.ai/skills/dotnet-engineer/SKILL.md`, `.ai/patterns/object-oriented-programming.md` |
| CQRS | `.ai/skills/dotnet-engineer/SKILL.md`, `.ai/patterns/cqrs-patterns.md`, `.ai/reference/critical-rules.md`, `.ai/reference/templates/command-handler.cs.txt`, `.ai/reference/templates/query-handler.cs.txt` |
| API Endpoints | `.ai/skills/api-endpoints/SKILL.md`, `.ai/patterns/api-patterns.md`, `.ai/reference/templates/endpoint.cs.txt`, `.ai/reference/critical-rules.md` |
| OpenAPI & Kiota | `.ai/skills/api-endpoints/SKILL.md`, `.ai/patterns/api-patterns.md`, `.ai/reference/critical-rules.md` |
| Unit Tests | `.ai/skills/unit-tester/SKILL.md`, `.ai/patterns/testing-patterns.md`, `.ai/patterns/test-driven-development.md`, `.ai/reference/templates/test-class.cs.txt`, `.ai/reference/templates/feature-file.feature.txt` |
| Blazor UI | `.ai/skills/blazor-specialist/SKILL.md`, `.ai/patterns/mvvm.md` |
| MAUI | `.ai/skills/maui-specialist/SKILL.md`, `.ai/patterns/mvvm.md` |
| WinUI 3 | `.ai/skills/winui-specialist/SKILL.md`, `.ai/patterns/mvvm.md` |
| Architecture | `.ai/skills/architect/SKILL.md`, `.ai/project/architecture.md` |
| Code Review | `.ai/skills/code-reviewer/SKILL.md`, `.ai/checklists/pre-submission.md` |
| Security | `.ai/skills/security/SKILL.md`, `.ai/skills/api-security/SKILL.md`, `.ai/skills/software-security/SKILL.md` |
| Bulk Refactoring | `.ai/skills/refactor/SKILL.md` |
| Design Interrogation | `.ai/skills/design-interrogation/SKILL.md` |
| Solution Scaffolding | `.ai/skills/solution-generator/SKILL.md`, `.ai/skills/vertical-slices/SKILL.md` |
| Gap Validation | `.ai/skills/gap-review/SKILL.md` |
| Domain Modeling | `.ai/skills/ubiquitous-language/SKILL.md`, `.ai/skills/usecase-specification/SKILL.md`, `.ai/skills/user-story/SKILL.md` |
| Skill Creation | `.ai/skills/skill-creator/SKILL.md` |
| Council | `.ai/reference/council.md`, `.ai/skills/council/SKILL.md` |

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
| `DEEPSEEK.md` | DeepSeek-variant orchestration (swapped in by the PowerShell profile) |
| `powershell/` | PowerShell profile for switching between Anthropic and DeepSeek backends |
| `TEMPLATE-USAGE.md` | Detailed usage and customization guide |
| `TEMPLATE-FAQ.md` | Frequently asked questions |
| `.ai/reference/critical-rules.md` | Non-negotiable coding patterns |
| `.ai/patterns/api-patterns.md` | API endpoints, OpenAPI, Kiota, security hardening |
| `.ai/reference/forbidden-tech.md` | Banned libraries and approaches |
| `.ai/project/` | Project-specific context files |

## Repository Mirroring

This repository lives in two places: **GitHub** (`I-Synergy/AI`, source of truth) and **Azure DevOps**. A GitHub Action keeps them aligned automatically.

**Mechanism:** `.github/workflows/mirror-to-azure.yml` runs on every push to `main` and `development/main` (and on manual dispatch), force-pushing the full history to Azure DevOps via `git push --mirror`. GitHub is authoritative; any manual change made directly on Azure DevOps is overwritten on the next mirror.

**One-time setup:**

1. Create an Azure DevOps Personal Access Token with `Code (Read & Write)` scope for the target repo/org.
2. Add it as a GitHub Actions secret named `AZURE_DEVOPS_PAT` (Settings → Secrets and variables → Actions → New repository secret).

The PAT is injected via `env` and never logged; `--mirror` also propagates branch/tag deletions, so treat Azure DevOps as a read-only copy.

## [License](LICENSE)