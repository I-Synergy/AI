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
- 57% token optimization based on Claude Context OS v2 research

## Quick Start

### 1. Copy Template to Your Project

```bash
# Copy the entire .claude directory to your project root
cp -r /path/to/Template/.claude /path/to/YourProject/.claude

# Copy CLAUDE.md to your project root
cp /path/to/Template/CLAUDE.md /path/to/YourProject/CLAUDE.md
```

### 2. Customize Project-Specific Files

Navigate to `.claude/project/` and customize these files. **Each file has a distinct purpose with NO duplication:**

| File | Purpose | Key Question | What to Customize |
|------|---------|--------------|-------------------|
| `preferences.md` | Personal workflow | **HOW** do you work? | Communication style, problem-solving approach, autonomy level, code style preferences |
| `tech-stack.md` | Technology choices | **WHAT** do you use? | Frameworks, libraries, versions, forbidden technologies, package management |
| `architecture.md` | System design | **HOW** is it structured? | Layers, patterns, data flow, CQRS implementation, ADRs, reference implementations |
| `domains.md` | Business context | **WHAT** are you building? | Business domains, entities, rules, events, validation, ubiquitous language |
| `session-context.md` | Session memory | Track across sessions | Project decisions, learnings, blocked paths, established patterns |

**Benefits of this separation:**
- No duplicate information across files
- Clear separation of concerns
- Easy to find relevant information
- Each file references others where appropriate

### 3. Replace Tokens Throughout

Replace these tokens with your actual values:

| Token | Replace With | Example |
|-------|--------------|---------|
| `{ApplicationName}` | Your application name | `BudgetTracker` |
| `{Domain}` | Your domain names | `Budgets`, `Goals`, `Customers` |
| `{Entity}` | Your entity names | `Budget`, `Goal`, `Customer` |
| `{entity}` | Entity (lowercase) | `budget`, `goal`, `customer` |
| `{entities}` | Entity plural (lowercase) | `budgets`, `goals`, `customers` |

### 4. Initialize Session Context

Edit `.claude/session-context.md` to establish your project's initial context:

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

## User Preferences
[Your preferences from .claude/project/preferences.md]
```

## Directory Structure Explained

```
.claude/
├── reference/              # Quick reference guides
│   ├── tokens.md          # Template tokens definition
│   ├── glossary.md        # Terminology
│   ├── critical-rules.md  # Non-negotiable patterns
│   ├── forbidden-tech.md  # Technologies to avoid
│   ├── naming-conventions.md  # Naming standards
│   └── templates/         # Code templates (.cs.txt, .feature.txt)
├── patterns/              # Implementation patterns
│   ├── cqrs-patterns.md   # Complete CQRS guide
│   ├── api-patterns.md    # API endpoint patterns
│   └── testing-patterns.md  # Testing patterns
├── skills/                # Specialized agent personas
│   ├── dotnet-engineer.md     # .NET development
│   ├── unit-tester.md         # Testing specialist
│   ├── code-reviewer.md       # QA specialist
│   ├── technical-writer.md    # Documentation
│   └── playwright-tester.md   # UI testing
├── checklists/            # Quality gate checklists
│   └── pre-submission.md  # Comprehensive quality checklist
├── project/               # **CUSTOMIZE THESE (NO DUPLICATION)**
│   ├── preferences.md     # HOW you work (personal workflow/style)
│   ├── tech-stack.md      # WHAT you use (technologies/versions)
│   ├── architecture.md    # HOW it's structured (system design)
│   ├── domains.md         # WHAT you're building (business context)
│   └── session-context.md # Session memory (decisions/learnings)
├── progress/              # Active task progress files
├── completed/             # Completed task archives
└── session-context.md     # Working session memory file
```

## Using Code Templates

### Example: Create a New Command

1. **Copy template:** `.claude/reference/templates/command-handler.cs.txt`
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

When working with Claude AI, reference the appropriate skill file:

### Example: Implementing a New Feature

```
User: "Implement complete CRUD for Budget entity"

Claude should:
1. Reference: .claude/skills/dotnet-engineer.md
2. Follow: .claude/patterns/cqrs-patterns.md
3. Use templates: .claude/reference/templates/
4. Check: .claude/checklists/pre-submission.md
```

### Example: Writing Tests

```
User: "Write comprehensive tests for Budget handlers"

Claude should:
1. Reference: .claude/skills/unit-tester.md
2. Follow: .claude/patterns/testing-patterns.md
3. Use templates: .claude/reference/templates/test-class.cs.txt
4. Create: Reqnroll scenarios using feature-file.feature.txt
```

## Customizing for Your Stack

### Clear Separation of Concerns

The template now uses **non-overlapping configuration files**:

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
   Update forbidden technologies table - remove MediatR if present

2. **Update architecture.md:**
   Update CQRS Implementation Pattern section with MediatR examples
   ```csharp
   public sealed record CreateBudgetCommand(...) : IRequest<CreateBudgetResponse>;

   public sealed class CreateBudgetHandler
       : IRequestHandler<CreateBudgetCommand, CreateBudgetResponse>
   ```

3. **Update patterns (if needed):**
   Edit `.claude/patterns/cqrs-patterns.md` with MediatR-specific patterns

**Don't duplicate:** Technology choice stays in tech-stack.md, pattern examples stay in architecture.md

## Session Context Workflow

### Every Claude Session Should:

1. **Start:** Read `.claude/session-context.md`
2. **Work:** Follow established patterns
3. **End:** Update `.claude/session-context.md` with learnings

### What to Document in Session Context

- **Architectural Decisions:** "We chose to use MediatR because..."
- **User Preferences:** "User prefers verbose logging in development"
- **Project-Specific Patterns:** "Budget domain is our reference implementation"
- **Blocked Paths:** "Tried approach X, didn't work because Y"

## Progress Tracking

### Agent Creates Progress File

When Claude AI creates an agent to work on a task:

1. **Immediately creates:** `.claude/progress/implement-budget-crud.md`
2. **Updates in real-time** as work progresses
3. **On completion:** Moves to `.claude/completed/implement-budget-crud.md`

### Progress File Format

```markdown
# Implement Budget CRUD Progress

## Status: In Progress
## Started: 2025-02-16 10:00
## Last Updated: 2025-02-16 10:30

## Completed Steps
- [x] Created CreateBudgetCommand and Handler
- [x] Created GetBudgetByIdQuery and Handler

## Current Step
- [ ] Creating UpdateBudgetCommand and Handler

## Pending Steps
- [ ] Create DeleteBudgetCommand and Handler
- [ ] Create endpoints
- [ ] Write tests

## Files Created/Modified
- `src/BudgetTracker.Domain.Budgets/Features/Budget/Commands/CreateBudgetCommand.cs`
- `src/BudgetTracker.Domain.Budgets/Features/Budget/Commands/CreateBudgetHandler.cs`
```

## Quality Assurance

### Before Completing Any Task

Run through `.claude/checklists/pre-submission.md`:

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

2. Copy templates from `.claude/reference/templates/`
3. Replace tokens with your domain/entity names
4. Follow patterns from `.claude/patterns/cqrs-patterns.md`
5. Check `.claude/checklists/pre-submission.md`

### Adding a New Feature

1. Reference: `.claude/skills/dotnet-engineer.md`
2. Use templates: `.claude/reference/templates/`
3. Follow: `.claude/patterns/cqrs-patterns.md`
4. Test using: `.claude/patterns/testing-patterns.md`
5. Verify: `.claude/checklists/pre-submission.md`

## Troubleshooting

### "Claude doesn't remember previous decisions"

**Solution:** Update `.claude/session-context.md` with decisions and preferences.

### "Generated code doesn't follow my patterns"

**Solution:** Document your patterns in `.claude/project/preferences.md` and reference them.

### "Progress files in wrong location"

**Solution:** Ensure agents create files in `.claude/progress/`, not `~/.claude/`

### "Forbidden technology used"

**Solution:** Update `.claude/reference/forbidden-tech.md` with your actual forbidden technologies.

## Best Practices

1. **Keep session-context.md updated** - It's Claude's memory across sessions
2. **Customize project/ files first** - Before starting development
3. **Respect file separation** - Don't duplicate info across preferences/tech-stack/architecture/domains
4. **Use cross-references** - Each file links to related files at the bottom
5. **Reference patterns explicitly** - Tell Claude which pattern file to follow
6. **Use checklists before completion** - Ensure quality
7. **Document blockers immediately** - In progress files
8. **Archive completed work** - Move to .claude/completed/

### File Separation Guide

**Where to document what:**
- Communication style → `preferences.md`
- Framework version → `tech-stack.md`
- CQRS pattern structure → `architecture.md`
- Business rules → `domains.md`
- Project decisions → `session-context.md`

**Don't put:**
- Technology choices in preferences.md
- Architectural patterns in tech-stack.md
- Business rules in architecture.md
- Workflow preferences in domains.md

## Template Maintenance

### Updating the Template

1. Update modular files in `.claude/` subdirectories
2. Keep `CLAUDE.md` as orchestration only (don't bloat it)
3. Keep templates generic (use tokens, not specific names)
4. Test token replacement with real project

### Contributing Improvements

If you improve this template:
1. Keep improvements generic
2. Use tokens instead of specific project names
3. Update relevant modular file (not CLAUDE.md)
4. Test with a fresh project

## Getting Help

### If Claude Doesn't Follow Patterns

```
Remind Claude to:
1. Read .claude/session-context.md FIRST
2. Reference .claude/reference/critical-rules.md
3. Follow .claude/patterns/{relevant-pattern}.md
4. Check .claude/checklists/pre-submission.md before completing
```

### If Generated Code Has Issues

```
Ask Claude to:
1. Review .claude/skills/code-reviewer.md
2. Run through .claude/checklists/pre-submission.md
3. Compare against .claude/patterns/{relevant-pattern}.md
4. Fix issues and document learnings in session-context.md
```

## Example: Complete New Project Setup

```bash
# 1. Copy template
cp -r /Template/.claude /MyProject/.claude
cp /Template/CLAUDE.md /MyProject/CLAUDE.md

# 2. Customize project files
cd /MyProject/.claude/project
# Edit: preferences.md, tech-stack.md, architecture.md, domains.md

# 3. Initialize session context
cd /MyProject/.claude
cp project/session-context.md session-context.md
# Edit session-context.md with project specifics

# 4. Ready to develop!
# Tell Claude: "Read .claude/session-context.md and implement CRUD for Customer entity"
```

---

**Remember:** This template is modular. Customize the `.claude/project/` files for your specific needs, and Claude will use those preferences throughout development.
