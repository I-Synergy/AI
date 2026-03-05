# .NET Development Template

Professional .NET development template with AI-powered agent orchestration and modular architecture.

## Overview

A **production-ready .NET project template** that provides comprehensive development patterns, specialized agent skills, and quality assurance tools for building enterprise applications with Clean Architecture, CQRS, and Domain-Driven Design.

AI context lives in `.claude/` (auto-loaded by Claude Code).

## Features

### Specialized Skills (15)

| Skill | Purpose |
|-------|---------|
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

See `.claude/reference/tokens.md` for complete definitions.

## Quick Start

### 1. Copy Template to Your Project

```bash
# Copy AI context directory to your project root
cp -r ./.claude /path/to/YourProject/.claude

# Copy CLAUDE.md orchestration file
cp ./CLAUDE.md /path/to/YourProject/CLAUDE.md
```

### 2. Customize Project Files

Edit files in `.claude/project/`:

| File | Purpose | Key Question |
|------|---------|--------------|
| **preferences.md** | Personal workflow & style | **HOW** do you prefer to work? |
| **tech-stack.md** | Technology choices & versions | **WHAT** technologies do you use? |
| **architecture.md** | System design & patterns | **HOW** is your system structured? |
| **domains.md** | Business context & entities | **WHAT** are you building? |

### 3. Replace Tokens

```bash
find /path/to/YourProject/.claude -type f -exec sed -i 's/{ApplicationName}/BudgetTracker/g' {} +
find /path/to/YourProject/.claude -type f -exec sed -i 's/{Domain}/Budgets/g' {} +
find /path/to/YourProject/.claude -type f -exec sed -i 's/{Entity}/Budget/g' {} +
```

### 4. Initialize Session Context

Edit `.claude/session-context.md` to establish your project's initial state.

### 5. Start Developing

```
"Read .claude/session-context.md and implement CRUD for Budget entity following .claude/patterns/cqrs-patterns.md"
```

## File Structure

```
/
├── CLAUDE.md                        # AI orchestration (auto-loaded by Claude Code)
├── CLAUDE-v1.md                     # Previous version (reference)
├── TEMPLATE-USAGE.md                # Detailed usage guide
├── TEMPLATE-FAQ.md                  # Frequently asked questions
├── README.md                        # This file
└── .claude/                         # All AI context (Claude Code)
    ├── settings.json                # Claude Code configuration (plansDirectory, hooks, permissions)
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
    │       ├── mapping-config.cs.txt
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
    ├── skills/                      # Specialized agent personas
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
    │   └── verify-config/SKILL.md
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
    └── tests/                       # Template validation scripts
```

## Usage Examples

### Implementing a Feature

```
"Implement complete CRUD for Budget entity"

Claude will:
1. Read .claude/session-context.md
2. Load .claude/skills/dotnet-engineer/SKILL.md + .claude/patterns/cqrs-patterns.md
3. Use templates from .claude/reference/templates/
4. Track progress in .claude/progress/
5. Verify against .claude/checklists/pre-submission.md
6. Write handoff to .claude/session-context.md
```

### Writing Tests

```
"Write comprehensive tests for Budget handlers"

Claude will:
1. Load .claude/skills/unit-tester/SKILL.md + .claude/patterns/testing-patterns.md
2. Use test-class.cs.txt and feature-file.feature.txt templates
3. Create MSTest unit tests + Reqnroll BDD scenarios
```

### Code Review

```
"Review the Budget implementation for compliance"

Claude will:
1. Load .claude/skills/code-reviewer/SKILL.md
2. Check .claude/reference/critical-rules.md
3. Verify .claude/patterns/cqrs-patterns.md compliance
4. Run through .claude/checklists/pre-submission.md
```

## Work-Type Context Mapping

Claude loads these files automatically based on your task type:

| Task Type | Files Loaded |
|-----------|-------------|
| CQRS | `.claude/skills/dotnet-engineer/SKILL.md`, `.claude/patterns/cqrs-patterns.md`, `.claude/reference/critical-rules.md`, templates |
| API Endpoints | `.claude/patterns/api-patterns.md`, `.claude/reference/templates/endpoint.cs.txt` |
| Unit Tests | `.claude/skills/unit-tester/SKILL.md`, `.claude/patterns/testing-patterns.md`, test templates |
| Blazor UI | `.claude/skills/blazor-specialist/SKILL.md`, `.claude/patterns/mvvm.md` |
| MAUI | `.claude/skills/maui-specialist/SKILL.md`, `.claude/patterns/mvvm.md` |
| Architecture | `.claude/skills/architect/SKILL.md`, `.claude/project/architecture.md` |
| Code Review | `.claude/skills/code-reviewer/SKILL.md`, `.claude/checklists/pre-submission.md` |
| Security | `.claude/skills/security/SKILL.md`, `.claude/skills/api-security/SKILL.md` |

## Customization

### Required Before Starting

1. Edit files in `.claude/project/` with your project specifics
2. Replace all `{tokens}` with your actual values
3. Update `.claude/reference/forbidden-tech.md` for your stack
4. Initialize `.claude/session-context.md`

### Optional

1. Add domain-specific patterns to `.claude/patterns/`
2. Create custom skills in `.claude/skills/`
3. Add project-specific checklists to `.claude/checklists/`
4. Modify code templates in `.claude/reference/templates/`

## Session Management

Every session:
1. **Start** — Read `.claude/session-context.md`
2. **Review** — Check `.claude/completed/` for relevant prior work
3. **Track** — Write progress to `.claude/progress/{task-slug}.md` in real time
4. **End** — Write handoff to `.claude/session-context.md`

## Supported Technologies

### Default Stack (Fully Customizable)

- **.NET:** 10+ (C# 14)
- **ORM:** Entity Framework Core 10
- **Database:** PostgreSQL, SQL Server
- **CQRS:** I-Synergy.Framework.CQRS (NOT MediatR)
- **Mapping:** Mapster (NOT AutoMapper)
- **Testing:** MSTest + Moq + Reqnroll (NOT xUnit, NOT NUnit)
- **API:** ASP.NET Core Minimal APIs + `Microsoft.AspNetCore.OpenApi`
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
| `.claude/reference/critical-rules.md` | Non-negotiable coding patterns |
| `.claude/reference/forbidden-tech.md` | Banned libraries and approaches |
| `.claude/project/` | Project-specific context files |

## License

[Your License Here]
