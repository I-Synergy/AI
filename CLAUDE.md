# Claude Development Template

## Identity

You are a development agent working within a generic .NET project template.

## Template Tokens

See `.claude/reference/tokens.md` for complete token definitions. Replace `{ApplicationName}`, `{Domain}`, `{Entity}` throughout the codebase.

## Environment

> **Fill in for your project.** Describe OS, shell, and environment-specific constraints. Examples:
> - Windows: Use PowerShell-compatible commands (no bash-specific syntax), Windows temp paths
> - Include any long path or build constraints relevant to your platform

When searching for code references, frameworks, or dependencies, search the ENTIRE solution directory tree including sibling projects and external folders — not just the current project directory. Ask the user for the correct path if unsure.

## Configuration

- Use local `.claude/` folder (project-level) for project-specific settings like progress and plan files.
- Do NOT place project-specific config in the global `~/.claude/` directory unless explicitly instructed.
- When modifying CLAUDE.md or any configuration files, always read the existing file first and preserve existing conventions before making changes.

## Core Operational Rules

1. Read session context first: `.claude/session-context.md` (never mix project contexts)
2. Load context on demand from `.claude/` based on work type only
3. Mark open questions OPEN or ASSUMED, never resolve silently
4. Before session end: Write structured handoff to `.claude/session-context.md`
5. Verify against `.claude/checklists/pre-submission.md` before completion

## Task Execution Protocol

**On every non-trivial task (3+ steps or multi-file):**

1. **Enter plan mode first** — call `EnterPlanMode`, present the plan, wait for approval before writing any code
2. **Create a progress file** — immediately write `.claude/progress/{task-slug}.md` using this structure:
   ```
   # {Task Name}
   Status: IN PROGRESS
   Started: {date}

   ## Steps
   - [ ] Step 1
   - [ ] Step 2

   ## Notes
   ```
3. **Update progress file** after completing each step — use Edit to change `- [ ]` to `- [x]`, never overwrite the whole file
4. **On completion (mandatory, not optional):**
   - Edit the progress file: add `**Status:** DONE` near the top
   - Move the file: `mv .claude/progress/{task-slug}.md .claude/completed/`
   - If a copy already exists in `.claude/completed/`, delete the one in `progress/` instead
   - **Do not end the session without completing this step**

> **Why this matters:** Files left in `.claude/progress/` are treated as in-progress work in future sessions, causing confusion about what is still pending.

**Trivial tasks** (single file, obvious fix): skip plan mode and progress file.

### Progress Tracking: Local Files Only

**Do NOT use the built-in `TaskCreate`/`TaskUpdate`/`TaskList` tools** — they store data globally in `~/.claude/todos/` and are not visible in the repository. Instead, always use local `.claude/progress/` markdown files for tracking task progress. Plans are already configured to write locally via `plansDirectory` in `.claude/settings.json`.

### Subagent Template

**Valid `subagent_type` values** (skill names like `dotnet-engineer` are NOT valid agent types):

| Use case | `subagent_type` |
|-|-|
| Code implementation, CQRS, tests | `general-purpose` |
| File/codebase exploration | `Explore` |
| Implementation planning | `Plan` |
| Shell commands, git, build | `Bash` |

When delegating to a subagent via the Task tool, always include in the task prompt:

```
Progress file: .claude/progress/{task-slug}.md
After completing each step, use the Edit tool to mark it done:
  old: "- [ ] {step description}"
  new: "- [x] {step description}"
Do NOT use Write on the progress file — only Edit individual lines.
```

Subagents do not inherit this CLAUDE.md. All progress instructions must be explicit in the task prompt.

## Critical Coding Rules

These cause bugs if violated. Full examples in `.claude/reference/critical-rules.md`.

| Rule | Correct | Wrong |
|-|-|-|
| Commands | Individual parameters | Passing model objects |
| Delete | `FirstOrDefaultAsync` + `Remove` + `SaveChangesAsync` | Extension methods like `RemoveItemAsync` |
| Query filters | Named parameters | Positional parameters |
| Data access | EF Core primitives (`FirstOrDefaultAsync`, `Add`, `Remove`, `SaveChangesAsync`); no `.Update()` on tracked entities | Extension methods, repositories, or `.Update()` on tracked entities |
| Mapping | Mapster `entity.Adapt<T>()` or `ProjectToType<T>()` | AutoMapper or manual mapping |
| Async | Always include `CancellationToken` | Omit or use `.Result` |
| Return types | Responses wrap Models | Never return domain entities |
| Handler naming | `Create{Entity}CommandHandler` / `Get{Entity}ByIdQueryHandler` | Missing `CommandHandler`/`QueryHandler` suffix |
| File organization | One type per file, subfolder per operation | Combined files or flat folders |
| Entity construction | Direct `new Entity { ... }` in handlers | `command.Adapt<Entity>()` via Mapster |
| Enum naming | Plural names (`PaymentProviders`, not `PaymentProvider`) | Singular names for non-`*Status` enums |
| Entity enum types | `public PaymentProviders Provider { get; set; }` | `public int Provider { get; set; }` on EF entities |

**Data access (EF Core primitives):**
```csharp
// Create — named DbSet Add; always check rowsAffected > 0 and throw on failure
var entity = new Entities.{Domain}.{Entity} { {Entity}Id = Guid.NewGuid(), ... };
dataContext.{Entities}.Add(entity);
var rowsAffected = await dataContext.SaveChangesAsync(cancellationToken);
if (rowsAffected == 0) throw new InvalidOperationException("Failed to create {entity}");

// Read single — named DbSet FirstOrDefaultAsync
var entity = await dataContext.{Entities}.FirstOrDefaultAsync(e => e.{Entity}Id == id, cancellationToken);
var model = entity?.Adapt<{Entity}>();

// Read list — named DbSet required for LINQ (ordering, filtering, ProjectToType)
var models = await dataContext.{Entities}
    .OrderBy(e => e.Description)
    .ProjectToType<{Entity}>()
    .ToListAsync(cancellationToken);

// Update — FirstOrDefaultAsync + property mutation (no .Update() call needed — change tracker handles it)
var entity = await dataContext.{Entities}.FirstOrDefaultAsync(e => e.{Entity}Id == command.{Entity}Id, cancellationToken);
entity.Property = command.Property;
var rowsAffected = await dataContext.SaveChangesAsync(cancellationToken);
if (rowsAffected == 0) throw new InvalidOperationException("{Entity} not found or no changes made");

// Delete — named DbSet FirstOrDefaultAsync + named DbSet Remove; check rowsAffected > 0
var entity = await dataContext.{Entities}.FirstOrDefaultAsync(e => e.{Entity}Id == command.{Entity}Id, cancellationToken);
dataContext.{Entities}.Remove(entity);
var rowsAffected = await dataContext.SaveChangesAsync(cancellationToken);
if (rowsAffected == 0) throw new InvalidOperationException($"Failed to delete {entity.{Entity}Id}");
```

**Model conventions:**
- Models are positional records in `{Domain}/Models/` (inside domain project)
- No "Model" suffix: `Budget`, not `BudgetModel`
- Responses wrap models: `Get{Entity}ByIdResponse({Entity}? {Entity})`
- Mapper config: single `Configuration : IRegister` class per domain (not per entity), auto-discovered via assembly scanning
- Cross-domain entity mappings are allowed inside a domain's `Configuration.cs` when a feature references entities from another domain (e.g., Budgets mapping `Entities.Settings.ExpenseType`)

**Mapster registration (in `Extensions/ServiceCollectionExtensions.cs`):**
```csharp
var assembly = typeof(ServiceCollectionExtensions).Assembly;
// Scan picks up all IRegister implementations (Configuration class) in the assembly
var mappingConfigs = TypeAdapterConfig.GlobalSettings.Scan(assembly);
TypeAdapterConfig.GlobalSettings.Apply(mappingConfigs);
services.AddCQRS().AddHandlers(assembly);
```

## Work-Type Context Mapping

Load these files based on task type:

| Task Type | Files to Load |
|-|-|
| .NET Development | `.claude/skills/dotnet-engineer/SKILL.md`, `.claude/patterns/object-oriented-programming.md` |
| CQRS | `.claude/skills/dotnet-engineer/SKILL.md`, `.claude/patterns/cqrs-patterns.md`, `.claude/reference/critical-rules.md`, `.claude/reference/templates/command-handler.cs.txt`, `.claude/reference/templates/query-handler.cs.txt`, `.claude/reference/templates/mapping-config.cs.txt` |
| API Endpoints | `.claude/patterns/api-patterns.md`, `.claude/reference/templates/endpoint.cs.txt` |
| Unit Tests | `.claude/skills/unit-tester/SKILL.md`, `.claude/patterns/testing-patterns.md`, `.claude/patterns/test-driven-development.md`, `.claude/reference/templates/test-class.cs.txt`, `.claude/reference/templates/feature-file.feature.txt` |
| UI/E2E Tests | `.claude/skills/playwright-tester/SKILL.md`, `.claude/patterns/testing-patterns.md` |
| Integration | `.claude/skills/integration-specialist/SKILL.md`, `.claude/patterns/service-oriented-architecture.md` |
| Architecture | `.claude/skills/architect/SKILL.md`, `.claude/project/architecture.md` |
| Code Review | `.claude/skills/code-reviewer/SKILL.md`, `.claude/checklists/pre-submission.md` |
| Security | `.claude/skills/security/SKILL.md`, `.claude/skills/api-security/SKILL.md`, `.claude/skills/software-security/SKILL.md` |
| Performance | `.claude/skills/performance-engineer/SKILL.md` |
| Microservices | `.claude/patterns/microservices.md`, `.claude/skills/integration-specialist/SKILL.md` |
| Blazor UI | `.claude/skills/blazor-specialist/SKILL.md`, `.claude/patterns/mvvm.md` |
| MAUI | `.claude/skills/maui-specialist/SKILL.md`, `.claude/patterns/mvvm.md` |
| Database | `.claude/skills/database-migration/SKILL.md` |
| DevOps | `.claude/skills/devops-engineer/SKILL.md` |
| Documentation | `.claude/skills/technical-writer/SKILL.md` |

## Task Definition Template

Use this structure for all tasks:

```markdown
# Task: [Task Name]

## Context Files Required
- [List files from Work-Type Context Mapping]

## Action
[What to do - specific, measurable]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Verify
Run pre-submission checklist: `.claude/checklists/pre-submission.md`

## Done
- Progress file moved to `.claude/completed/`
- Session context updated with learnings
- All acceptance criteria met
```

## Session Management

**Every session:**
1. Read `.claude/session-context.md`
2. Read `.claude/completed/` (relevant tasks)
3. Work with real-time progress reporting
4. Write structured handoff before ending

**Agent delegation:**
- All agents have full repository access
- All agents report progress in real-time to `.claude/progress/`
- All agents use structured output (not free-form prose)

## Session Switching

Start new session when:
- Context exceeds 32K tokens
- Switching projects or domains
- Changing work types
- Session reached completion

Before ending: Use `.claude/reference/templates/session-handoff.md.txt` template. Write to `.claude/session-context.md`.

## Reference Architecture

**Clean Architecture Layers:**
- Domain: `{ApplicationName}.Domain.*`
- Application: `{ApplicationName}.Services.*`
- Infrastructure: `{ApplicationName}.Data.*`
- Presentation: `{ApplicationName}.UI.*`

**Minimum Projects Per Domain:** Entities, Models, Domain, Services

**Vertical Slice Organization:**
```
{ApplicationName}.Domain.{Domain}/
  Features/{Entity}/
    Commands/Create{Entity}/
      Create{Entity}Command.cs
      Create{Entity}CommandHandler.cs
      Create{Entity}Response.cs
    Commands/Update{Entity}/
      ...
    Commands/Delete{Entity}/
      ...
    Queries/Get{Entity}ById/
      ...
    Queries/Get{Entities}List/
      ...
    Events/
  Models/{Entity}.cs             (positional record, no "Model" suffix)
  Mappers/Configuration.cs       (single Mapster IRegister per domain)
  Extensions/ServiceCollectionExtensions.cs
```

## Key Reference Files

**Critical Information:**
- `.claude/reference/critical-rules.md` — non-negotiable patterns with full examples
- `.claude/reference/forbidden-tech.md` — banned libraries/approaches
- `.claude/reference/tokens.md` — template token definitions
- `.claude/reference/glossary.md`

**Project Context:**
- `.claude/project/architecture.md` — complete architecture documentation
- `.claude/project/domains.md` — business domain catalog
- `.claude/project/tech-stack.md` — full technology stack

**Patterns:**
- `.claude/patterns/cqrs-patterns.md`
- `.claude/patterns/api-patterns.md`
- `.claude/patterns/testing-patterns.md`

**Templates:**
- `.claude/reference/templates/` — code generation templates
- `.claude/reference/templates/session-handoff.md.txt` — session handoff template

**Checklists:**
- `.claude/checklists/pre-submission.md` — run before marking any task complete

## Refactoring Conventions

- When performing bulk refactoring across multiple files, always check ALL instances of the pattern — including string literals in exception messages, logger calls, and similar constructs — not just the primary target. After making bulk changes, do a final grep to verify zero remaining instances.
- When doing large multi-file migrations or refactoring, always include file deletion of old/moved files as part of the plan. Do not skip cleanup steps expecting manual approval — include them but confirm with the user before executing.
- When a file migration or move is performed, ALWAYS delete the original source files AND remove any associated config/mapping files (e.g., MappingConfig, registration entries) from the old location. Do not wait for manual approval on file deletion during migrations.
- Before starting work, verify the scope by searching the ENTIRE solution/repo for the target pattern — not just the current project or domain. If referencing external projects or frameworks, ask the user for the correct path rather than assuming.
- Before applying bulk replacements, analyze ALL instances first. Categorize by whether the replacement is safe, unsafe, or needs modification. Present categories with examples and wait for user confirmation before editing any files.
- For large refactors (15+ files), process in batches scoped to one domain at a time and run the build between batches to catch regressions early.

## File Management

- Never autonomously delete documentation files, progress tracking files, or session context files unless the user explicitly asks for deletion. Always ask before removing any non-code artifacts.
- Check the environment section for platform-specific shell syntax constraints before running commands.

## Workflow Preferences

- When asked to 'build' or 'check the build', ONLY run the build command and report results. Do not autonomously investigate or fix errors unless explicitly asked to do so.
- A **PostToolUse hook** can be configured in `.claude/settings.json` that automatically runs `dotnet build` after every file edit. This surfaces build errors immediately after changes without needing a manual build step.

## Documentation Maintenance

- When making architectural changes (new CQRS patterns, data access conventions, mapping approaches, project structure changes), update CLAUDE.md and the relevant `.claude/` reference files to reflect the new patterns in the same session.
- After completing a feature or refactor that introduces new conventions, verify that CLAUDE.md, `.claude/reference/critical-rules.md`, and `.claude/patterns/cqrs-patterns.md` still accurately describe the codebase. Flag any drift to the user.
- Run `/verify-config` periodically to audit CLAUDE.md against the actual codebase.

## Verification

Before marking any task complete: `.claude/checklists/pre-submission.md`
