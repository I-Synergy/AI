# Claude Development Orchestration

**This is the main orchestration file. All detailed patterns and references are in modular `.claude/` files.**

## Quick Start

1. **Read Session Context First:** `.claude/session-context.md`
2. **Check Critical Rules:** `.claude/reference/critical-rules.md`
3. **Review Tokens:** `.claude/reference/tokens.md`
4. **Follow Patterns:** `.claude/patterns/`

## Template Structure

This is a **generic .NET project template**. Replace all tokens before use:

| Token | Example |
|-------|---------|
| `{ApplicationName}` | `BudgetTracker` |
| `{Domain}` | `Budgets`, `Goals` |
| `{Entity}` | `Budget`, `Goal` |

See `.claude/reference/tokens.md` for complete list.

## Core Principles

1. **No Shortcuts** - The correct fix is always better than the quick fix
2. **Fix Bugs Now** - Don't defer, don't say "out of scope"
3. **Agent Delegation** - ALL work delegated to agents with full access
4. **Real-Time Progress** - Every agent reports progress automatically
5. **Session Context** - Read first, update last

## Agent Workflow (MANDATORY)

**ALL work must be delegated to agents with full repository access and real-time progress reporting.**

### Critical Requirements

1. **Full Delegation**
   - Every task delegated to an agent
   - Agent has **full access and all permissions**
   - Applies to **EVERY agent** - first, sequential, parallel, sub-agents, ALL

2. **Real-Time Progress**
   - Each agent reports progress **in real-time**
   - Progress updates are **automatic**
   - Updates continuous throughout task lifecycle

3. **Universal Requirements**
   - **EVERY agent** must:
     - Have full repository access
     - Report progress in real-time
     - Create/update progress files in `.claude/progress/`
     - Follow all workflow requirements

4. **Progress Files**
   - **Location:** `.claude/progress/[task].md`
   - **Created:** Immediately when task starts
   - **Updated:** In real-time as work progresses
   - **Completed:** Moved to `.claude/completed/`

5. **Session Context**
   - **READ FIRST:** `.claude/session-context.md`
   - **UPDATE LAST:** Document learnings before ending

### Workflow Pattern

```
New Session
  ↓
Read .claude/session-context.md
  ↓
Read .claude/completed/* (understand previous work)
  ↓
Task Assignment
  ↓
Agent(s): Create progress → Report real-time → Complete
  ↓
Verify → Move to completed → Update session-context.md
```

## Reference Files (Read These First)

Located in `.claude/reference/`:

| File | Purpose |
|------|---------|
| `tokens.md` | Template token definitions |
| `glossary.md` | Terminology and concepts |
| `critical-rules.md` | **Non-negotiable patterns** |
| `forbidden-tech.md` | Technologies to avoid |
| `naming-conventions.md` | Naming standards |

## Pattern Files (Implementation Guides)

Located in `.claude/patterns/`:

| File | Contains |
|------|----------|
| `api-patterns.md` | Minimal API endpoints |
| `cqrs-patterns.md` | Complete CQRS implementation |
| `microservices.md` | Microservices architecture, service boundaries, inter-service communication |
| `mvvm.md` | Model-View-ViewModel pattern for MAUI/Blazor |
| `object-oriented-programming.md` | SOLID principles, OOP best practices |
| `service-oriented-architecture.md` | SOA patterns and implementation |
| `test-driven-development.md` | TDD methodology, Red-Green-Refactor cycle |
| `testing-patterns.md` | MSTest + Moq + Reqnroll |

## Skill Files (Specialized Agents)

Located in `.claude/skills/`:

| Skill | Specialty |
|-------|-----------|
| `api-security.md` | API security, authentication, authorization, OWASP API Top 10 |
| `architect.md` | Solution architecture & design decisions |
| `blazor-specialist.md` | Blazor UI development |
| `code-reviewer.md` | Quality assurance specialist |
| `database-migration.md` | EF Core migrations & database management |
| `devops-engineer.md` | CI/CD pipelines & containerization |
| `dotnet-engineer.md` | .NET/C#/Blazor/MAUI development |
| `integration-specialist.md` | External API integration & webhooks |
| `maui-specialist.md` | MAUI mobile app development |
| `performance-engineer.md` | Performance optimization & profiling |
| `playwright-tester.md` | UI testing |
| `security.md` | Security architect & coordinator, compliance, risk management |
| `software-security.md` | Application security, secure coding, OWASP Top 10 |
| `technical-writer.md` | Documentation |
| `unit-tester.md` | MSTest + Moq + Reqnroll testing |

## Code Templates (Copy & Customize)

Located in `.claude/reference/templates/`:

- `command-handler.cs.txt` - Command + Handler
- `query-handler.cs.txt` - Query + Handler
- `endpoint.cs.txt` - Minimal API endpoint
- `mapping-config.cs.txt` - Mapster configuration
- `test-class.cs.txt` - MSTest unit test
- `feature-file.feature.txt` - Reqnroll BDD scenario

## Checklists (Quality Gates)

Located in `.claude/checklists/`:

- `pre-submission.md` - **Comprehensive quality checklist**

## Project-Specific Files (Customize These)

Located in `.claude/project/` - **These are templates. Copy and customize for your project:**

| File | Customize With |
|------|----------------|
| `preferences.md` | Your project's coding preferences |
| `tech-stack.md` | Your actual technology choices |
| `architecture.md` | Your architecture decisions |
| `domains.md` | Your business domains |
| `session-context.md` | Your project session memory |

## Critical Rules (MUST FOLLOW)

1. **Commands:** Individual parameters only (NOT model objects)
2. **Delete Operations:** Use `RemoveItemAsync<TEntity, TKey>()`
3. **Query Parameters:** Use named parameters for optional filters
4. **Data Access:** Use DataContext extensions (NO repositories)
5. **Mapping:** Mapster only (configure in `{Entity}MappingConfig.cs`)
6. **Async:** Always include `CancellationToken`, never `.Wait()` or `.Result`
7. **Entity Exposure:** NEVER expose domain entities (always DTOs)
8. **Progress Files:** MUST be in current solution's `.claude/` folder
9. **Session Context:** Read first, update last
10. **Guard Clauses:** All public methods

See `.claude/reference/critical-rules.md` for details.

## Forbidden Technologies

**DO NOT USE:**
- MediatR → Use your CQRS framework
- AutoMapper → Use Mapster
- xUnit/NUnit → Use MSTest
- SpecFlow → Use Reqnroll
- Swashbuckle → Use Microsoft.AspNetCore.OpenApi
- FluentValidation → Use Data Annotations
- Standalone Polly → Use Microsoft.Extensions.Resilience

See `.claude/reference/forbidden-tech.md` for complete list and alternatives.

## Quick Command Reference

### Create New Feature

1. Read reference: `.claude/patterns/cqrs-patterns.md`
2. Copy templates from `.claude/reference/templates/`
3. Replace tokens: `{ApplicationName}`, `{Domain}`, `{Entity}`
4. Create: Commands, Queries, Handlers, Endpoints
5. Add: Mapping configuration
6. Write: Tests
7. Check: `.claude/checklists/pre-submission.md`

### Invoke Specialized Agent

```
Use .claude/skills/{skill-name}.md as context for specialized work:
- dotnet-engineer.md - For CQRS implementation
- unit-tester.md - For testing
- code-reviewer.md - For review
- technical-writer.md - For documentation
- playwright-tester.md - For UI testing
```

## Architecture Overview

### Clean Architecture Layers

| Layer | Project Pattern | Responsibilities |
|-------|----------------|------------------|
| **Domain** | `{ApplicationName}.Domain.*` | Entities, CQRS, domain logic (NO external dependencies) |
| **Application** | `{ApplicationName}.Services.*` | API endpoints, orchestration, validation |
| **Infrastructure** | `{ApplicationName}.Data.*` | Persistence, external integrations |
| **Presentation** | `{ApplicationName}.UI.*` | Blazor/MAUI apps, ViewModels |

### Project Structure Per Domain

```
{ApplicationName}.Contracts.{Domain}/      Interfaces and service contracts (Optional)
{ApplicationName}.Entities.{Domain}/       EF Core entity classes (Required)
{ApplicationName}.Models.{Domain}/         DTOs and view models (Required)
{ApplicationName}.Domain.{Domain}/         CQRS Commands/Queries/Handlers (Required)
{ApplicationName}.Services.{Domain}/       API Endpoints (Required)
{ApplicationName}.ViewModels.{Domain}/     MVVM ViewModels (Optional - UI only)
```

**Minimum required:** Entities, Models, Domain, Services (4 projects)

### Vertical Slice Organization

```
Domain/
  Features/
    {Entity}/
      Commands/
        Create{Entity}Command.cs
        Create{Entity}Handler.cs
      Queries/
        Get{Entity}ByIdQuery.cs
        Get{Entity}ByIdHandler.cs
      Events/
        {Entity}CreatedEvent.cs
  Mappers/
    {Entity}MappingConfig.cs
  Extensions/
    ServiceCollectionExtensions.cs
```

## CQRS Quick Reference

### Command Pattern

```csharp
// Individual parameters (NOT model objects)
public sealed record CreateBudgetCommand(
    string Name,
    decimal Amount,
    DateTimeOffset StartDate
) : ICommand<CreateBudgetResponse>;

public sealed record CreateBudgetResponse(Guid BudgetId);
```

### Query Pattern

```csharp
// Named parameters for optional filters
public sealed record GetBudgetByIdQuery(Guid BudgetId) : IQuery<BudgetResponse>;

public sealed record GetBudgetListQuery(
    int PageNumber = 1,
    int PageSize = 20,
    string? SearchTerm = null
) : IQuery<List<BudgetResponse>>;
```

### Handler Pattern

```csharp
public sealed class CreateBudgetHandler(
    DataContext dataContext,
    ILogger<CreateBudgetHandler> logger
) : ICommandHandler<CreateBudgetCommand, CreateBudgetResponse>
{
    public async Task<CreateBudgetResponse> HandleAsync(
        CreateBudgetCommand command,
        CancellationToken cancellationToken = default)
    {
        // Guard clauses
        ArgumentNullException.ThrowIfNull(command);

        // Logging
        logger.LogInformation("Creating {EntityType}", nameof(Budget));

        // Map and persist
        var entity = command.Adapt<Budget>();
        var model = entity.Adapt<BudgetModel>();
        await dataContext.AddItemAsync<Budget, BudgetModel>(model, cancellationToken);

        // Return DTO
        return new CreateBudgetResponse(entity.BudgetId);
    }
}
```

## Data Access Quick Reference

```csharp
// Create
await dataContext.AddItemAsync<TEntity, TModel>(model, ct);

// Read
await dataContext.GetItemByIdAsync<TEntity, TModel, TKey>(id, ct);

// Update
await dataContext.UpdateItemAsync<TEntity, TModel>(model, ct);

// Delete - CRITICAL: Use RemoveItemAsync
await dataContext.RemoveItemAsync<TEntity, TKey>(id, ct);

// List/Query - LINQ directly on DbSet
var items = await dataContext.Set<TEntity>()
    .Where(x => x.IsActive)
    .ToListAsync(ct);
```

## Testing Quick Reference

```csharp
// MSTest pattern
[TestClass]
public class CreateBudgetHandlerTests
{
    [TestInitialize]
    public void Setup() { }

    [TestMethod]
    public async Task HandleAsync_ValidCommand_CreatesBudgetSuccessfully()
    {
        // Arrange
        // Act
        // Assert
    }
}
```

## Common Pitfalls

See `.claude/reference/critical-rules.md` for detailed examples.

**Quick checklist:**
- ❌ Commands with model objects → ✅ Individual parameters
- ❌ `DeleteItemByIdAsync` → ✅ `RemoveItemAsync`
- ❌ Positional optional parameters → ✅ Named parameters
- ❌ Repository interfaces → ✅ DataContext extensions
- ❌ AutoMapper → ✅ Mapster
- ❌ `.Wait()` or `.Result` → ✅ `async/await` with `CancellationToken`

## Session Context Management

### Every Session MUST:

1. **Read First:** `.claude/session-context.md`
2. **Build On:** Use established patterns and preferences
3. **Update Last:** Document learnings before ending

### What to Preserve:

- Architectural decisions
- User preferences
- Project-specific context
- Historical decisions
- Blocked paths (what doesn't work)

## File Organization

```

├── .claude/
│   ├── reference/
│   │   ├── tokens.md
│   │   ├── glossary.md
│   │   ├── critical-rules.md
│   │   ├── forbidden-tech.md
│   │   ├── naming-conventions.md
│   │   └── templates/
│   │       ├── command-handler.cs.txt
│   │       ├── query-handler.cs.txt
│   │       ├── endpoint.cs.txt
│   │       ├── mapping-config.cs.txt
│   │       ├── test-class.cs.txt
│   │       └── feature-file.feature.txt
│   ├── patterns/
│   │   ├── cqrs-patterns.md
│   │   ├── api-patterns.md
│   │   └── testing-patterns.md
│   ├── skills/
│   │   ├── dotnet-engineer.md
│   │   ├── unit-tester.md
│   │   ├── code-reviewer.md
│   │   ├── technical-writer.md
│   │   └── playwright-tester.md
│   ├── checklists/
│   │   └── pre-submission.md
│   ├── project/
│   │   ├── preferences.md (customize)
│   │   ├── tech-stack.md (customize)
│   │   ├── architecture.md (customize)
│   │   ├── domains.md (customize)
│   │   └── session-context.md (customize)
│   ├── progress/
│   │   └── [active-task].md
│   ├── completed/
│   │   └── [completed-task].md
│   └── session-context.md (working file)
├── src/
│   └── (your application code)
├── tests/
│   └── (your tests)
├── CLAUDE.md (this file)
├── TEMPLATE-USAGE.md (how to use this template)
└── README.md (your project README)
```

## Next Steps

1. **Read:** `TEMPLATE-USAGE.md` for how to customize this template
2. **Customize:** Files in `.claude/project/` for your specific project
3. **Replace:** All `{tokens}` with your actual values
4. **Start:** Building with agents following patterns in `.claude/patterns/`

---

**Remember:** This file is orchestration only. All detailed patterns, examples, and templates are in modular `.claude/` files.
