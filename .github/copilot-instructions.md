# GitHub Copilot Instructions

<!-- ai-workspace-manager:generated-from-agents -->
<!-- Generated from AGENTS.md. Edit AGENTS.md, not this file. Regenerate with `python .ai/scripts/sync-instructions.py`. -->

# .NET Development Template

## Identity

You are a development agent working within a .NET project template. You are powered by AI (claude or copilot). You have file I/O, shell execution, and code search tools available. Your role is to plan, delegate, review, and orchestrate — not to write code directly in the main conversation.

## Session Memory

`.ai/session-context.md` is the shared memory for every client. Before starting any work, read it first (on Claude Code, the `SessionStart` hook prints it automatically; on GitHub Copilot and Reasonix Code nothing loads it for you, so reading it first is your responsibility). Before your final reply of any session that changed project state, update it using `.ai/reference/templates/session-handoff.md.txt`, set Written By to your client name (Claude Code, GitHub Copilot, or Reasonix Code), update sections in place, and never overwrite another client's entries.

Every session follows this cycle:

1. **Start:** Read `.ai/session-context.md` and `.ai/completed/` for context from previous sessions
2. **Work:** Track progress in `.ai/progress/`, delegate code work to subagents
3. **End:** Write handoff to `.ai/session-context.md`, move completed progress files to `.ai/completed/`

## Task Execution Protocol

### When to Plan

For any non-trivial task (3+ steps or multi-file), plan before writing code:

1. **Create a plan** — write `.ai/plans/{task-slug}.md`. Wait for approval before writing any code.
2. Create `.ai/progress/{task-slug}.md`:
   ```
   # {Task Name}
   Status: IN PROGRESS
   Started: {date}

   ## Steps
   - [ ] Step 1
   - [ ] Step 2

   ## Notes
   ```
3. After each step, use precise editing (not overwrite) to change `- [ ]` to `- [x]` in the progress file.
4. On completion:
   - Add `**Status:** DONE` near the top
   - Move to `.ai/completed/{task-slug}.md`
   - Never end a session without completing this step

Trivial tasks (single file, obvious fix): skip the plan and progress file.

### When to Convene a Council

A decision that is expensive to reverse is not made by one agent's judgment: a council's seats form positions **independently**, a chair reconciles them on the merits, and dissent is recorded verbatim rather than averaged away. Protocol: `.ai/reference/council.md`; invocable as `.ai/skills/council/SKILL.md`.

Convene when **any one** of these fires: the change alters an established architecture decision — bounded contexts, layering, project structure, technology choice, or a pattern in `.ai/patterns/`; breaks a public contract — a contract that other code or consumers depend on cannot follow the change without modification (an additive, backward-compatible change does not convene); is a destructive or transform-in-place data migration; changes the **existing** security posture — it alters the authn/authz model, secret handling, or the exposure surface, rather than applying the documented pattern; is flagged irreversible by the user or a reviewer; or two documented rules conflict with no obvious winner.

Triggers describe the **decision**, not the size of the diff: bug fixes with a known root cause, behavior-preserving refactors, tests, and documentation do not convene, and neither does a change that only applies an existing documented pattern — a new endpoint, handler, migration, or component following the template's rules and a reference implementation as written — nor does a decision already covered by a recorded council (revisit it only when that record's reopen conditions fire). If you cannot tell whether a trigger fires, ask the user one framing question instead. If a trigger fires, it outranks the work-kind exclusions — convene even when one of them also seems to apply. The one exception is a decision already covered by a recorded council: revisit it only when that record's reopen conditions fire.

Three seats is the minimum useful council, five the ceiling, with one cross-examination round. The chair runs at the deep tier, holds no seat, and the verdict is **advisory** — the chair decides on the merits, records which positions were adopted and rejected, and quotes dissent verbatim. Unresolved dissent is never absorbed: it escalates to the user.

### ReAct Loop

After every file edit, observe the result (command output, test results). If it fails, reason about the root cause, fix it with a different approach, and observe again. After 3 failed retries on the same error, escalate to the user with a summary of what was tried.

### Progress Tracking

Use local `.ai/progress/` markdown files only. Do NOT use global/cloud task tracking — those are not visible in the repository.

## Subagent Delegation

The main conversation is **orchestration only**. You plan, read, review output, and run git/sync operations. You do NOT write or edit code directly.

All substantive work goes to a subagent:

| Agent | Use For |
|---|---|
| `architect` | Feature design, pattern selection, component boundaries, architecture analysis |
| `reviewer` | Code quality, SOLID, CQRS compliance, security review, architecture audit, ISO/IEC 25010 finding attribution |
| `security` | Blast-radius and exposure analysis, threat modelling, OWASP review, dependency and secret audits |
| `tester` | MSTest/Reqnroll test design, BDD scenarios, integration test strategy |
| `designer` | Visual design — color palettes, typography, branding, design tokens |
| `developer` | .NET/C# code — CQRS handlers, API endpoints, Blazor, EF Core, refactoring, builds |
| `ui-developer` | Blazor/MAUI components, layouts, CSS/styling, UX patterns |
| `ui-tester` | Playwright E2E tests, accessibility checks, visual regression |
| `writer` | XML docs, READMEs, ADRs, technical prose |

Each agent's `model:` frontmatter in `.ai/agents/` carries the tier alias (`sonnet` or `haiku`); the concrete model bound to that tier is chosen by the backend runtime outside this repository.

Agent definitions live in `.ai/agents/` (canonical source). When delegating, always include in the prompt:
```
Progress file: .ai/progress/{task-slug}.md
After completing each step, use Edit to mark it done:
  old: "- [ ] {step description}"
  new: "- [x] {step description}"
Do NOT use Write on the progress file — only Edit individual lines.
```

## Critical Coding Rules

These are non-negotiable. Violating any of them causes bugs.

### 1. Commands: Individual Parameters Only
Never pass model objects to commands. Extract each property individually.
```csharp
// CORRECT
public sealed record Create{ChildEntity}Command(Guid {Entity}Id, string Description, decimal Amount) : ICommand<Create{ChildEntity}Response>;
// WRONG
public sealed record Create{ChildEntity}Command({ChildEntity} {childEntity}) : ICommand<Create{ChildEntity}Response>;
```

### 2. Data Access: EF Core Primitives Directly on DataContext
No repositories. No extension methods (AddItemAsync, GetItemByIdAsync). Use DbSet properties directly.
- Create: `dataContext.{Entities}.Add(entity)` + `SaveChangesAsync`
- Read: `dataContext.{Entities}.FirstOrDefaultAsync(e => e.{Entity}Id == id, ct)`
- Update: mutate tracked entity properties + `SaveChangesAsync` (no `.Update()` call needed)
- Delete: `FirstOrDefaultAsync` → null check → `Remove(entity)` → `SaveChangesAsync` → check rows affected

### 3. Async: Always Include CancellationToken
Every async handler method must accept and pass through `CancellationToken cancellationToken = default`.

### 4. Entity Exposure: Never Return Domain Entities
Always map entities to Models before returning from handlers. Responses wrap Models, never entities.

### 5. Handler Naming: Always Include Command/Query Suffix
`Create{Entity}CommandHandler`, `Get{Entity}ByIdQueryHandler` — never `Create{Entity}Handler`.

### 6. Example File Organization: One Type Per File, Subfolder Per Operation
```
Features/{Entity}/
  Commands/Create{Entity}/
    Create{Entity}Command.cs
    Create{Entity}CommandHandler.cs
    Create{Entity}Response.cs
  Queries/Get{Entity}ById/
    Get{Entity}ByIdQuery.cs
    Get{Entity}ByIdQueryHandler.cs
    Get{Entity}ByIdResponse.cs
```

### 7. Enum Naming: Plural (except *Status)
`PaymentProviders`, `OrderTypes` — plural. `PaymentStatus`, `SubscriptionStatus` — singular (Status suffix is exempt).

### 8. Entity Properties: Use Enum Type, Not int
EF Core converts enums automatically. Always use the enum type on entity properties, never raw `int`.

### 9. Common Project: Centralize Shared Types
Every solution needs `{ApplicationName}.Common`. All enums and shared types go there. Entities and Models must never reference each other — if both need a type, extract it to Common.

### 10. API Endpoints: Always Explicit Produces Metadata
Every route must declare all status codes: `.Produces<T>(201)` for success, `.Produces(401)` for auth, `.ProducesValidationProblem()` for validation, `.Produces(404)` for not-found.

### 11. API: OpenAPI Transformers + Kiota Clients + Validation + Rate Limiting
- Register document transformer (servers URL) AND schema transformer (type mapping) in `AddOpenApi()`
- Every API needs a Kiota-generated client project — never use raw HttpClient
- POST/PUT routes: `.WithValidation<T>()` + Data Annotations on request models
- Configure `AddRateLimiter` + `UseRateLimiter` + `UseHttpsRedirection`

### 12. Before Creating New Types: Search Entire Solution First
If a type already exists, reuse or extend it. Never create duplicates. Every plan must explicitly state which existing types are reused.

### 13. Plan Files: Always in `.ai/plans/`
Never save plans to `docs/plans/`. Always use `.ai/plans/`.

## After Every Code Change

The `Stop` hook runs `dotnet build --nologo --verbosity minimal` once at the end of a task, and only when files under `src/` or `tests/` changed since the last successful build, or when no successful-build marker exists yet and a solution is present. Read the build output. If it fails, fix before continuing. Run `dotnet test` after multi-file changes.

## Environment

**Builds:** Never run `dotnet build` / `dotnet publish` with MSBuild node reuse — it exhausts this machine's memory. Always set `MSBUILDDISABLENODEREUSE=1` and pass `-nodeReuse:false`, and state that explicitly in any subagent prompt that builds .NET. See `.ai/project/preferences.md` → Environment → Builds.

## Configuration

- `.ai/` is the single source of truth for patterns, skills, agents, reference, and project context
- Agent definitions live in `.ai/agents/`; tool-specific config (hooks, directories, settings) is tool-scoped
- Do not place project-specific config in global dotfile directories
- Scratch/temporary files go in `.ai/tmp/` (gitignored), never `/tmp` — some runtimes refuse reads outside the workspace root

## Reference Appendix

These files contain detailed guidance. Load them when the task type matches — but the rules above are self-contained and sufficient for most work.

**Patterns:**
- `.ai/patterns/cqrs-patterns.md` — full CQRS patterns with examples
- `.ai/patterns/api-patterns.md` — API endpoint patterns, OpenAPI, Kiota, validation, security
- `.ai/patterns/testing-patterns.md` — test structure and conventions

**Reference:**
- `.ai/reference/critical-rules.md` — all non-negotiable rules with full code examples
- `.ai/reference/council.md` — high-stakes decision process: triggers, seat selection, protocol, dissent record
- `.ai/reference/forbidden-tech.md` — banned libraries and replacements
- `.ai/reference/task-execution.md` — full ReAct loop, escalation format, subagent templates
- `.ai/reference/work-type-mapping.md` — which files to load per task type
- `.ai/reference/operational-rules.md` — refactoring conventions, file management, workflow
- `.ai/reference/traceability.md` — `US-` / `AC-` / `UC-` / `AF-` IDs that link stories, scenarios and tests
- `.ai/reference/quality-model.md` — ISO/IEC 25010 review vocabulary and severity taxonomy
- `.ai/reference/test-documentation.md` — which test documents to write, which to skip, and why
- `.ai/reference/standards.md` — per-standard compatibility manifest; `verify-config` computes it from validator runs

**Project:**
- `.ai/project/architecture.md` — solution architecture
- `.ai/project/tech-stack.md` — technology stack
- `.ai/project/preferences.md` — communication style, workflow preferences

<!-- ai-workspace-manager:copilot-reference:start -->
## Project Context

See `.ai/project/architecture.md` for complete architecture documentation and `.ai/project/tech-stack.md` for the full technology stack.

## Architecture

**Clean Architecture Layers:**
- Domain: `{ApplicationName}.Domain.*` — CQRS handlers, domain logic
- Application: `{ApplicationName}.Services.*` — API endpoints
- Infrastructure: `{ApplicationName}.Data.*` — EF Core persistence
- Presentation: `{ApplicationName}.UI.*` — Blazor/MAUI

**Vertical Slice Organization:**
```
{ApplicationName}.Domain.{Domain}/
  Features/{Entity}/
    Commands/Create{Entity}/
      Create{Entity}Command.cs
      Create{Entity}CommandHandler.cs
      Create{Entity}Response.cs
    Queries/Get{Entity}ById/
      ...
  Models/{Entity}.cs             (positional record, no "Model" suffix)
  Extensions/ServiceCollectionExtensions.cs
```

## Forbidden Technologies

See `.ai/reference/forbidden-tech.md` for the complete list.

- NO MediatR — use I-Synergy.Framework.CQRS
- NO xUnit/NUnit — use MSTest
- NO FluentValidation — use DataAnnotations
- NO repository interfaces — use EF Core directly via named DbSet properties
- NO `.Update()` on tracked EF entities — change tracker handles it

## Patterns & Templates

- CQRS: `.ai/patterns/cqrs-patterns.md`
- API: `.ai/patterns/api-patterns.md`
- Testing: `.ai/patterns/testing-patterns.md`
- Templates: `.ai/reference/templates/` — `command-handler.cs.txt`, `query-handler.cs.txt`, `endpoint.cs.txt`

## Naming Conventions

- Commands: `{Action}{Entity}Command` — e.g. `Create{Entity}Command`
- Queries: `Get{Entity}{Criteria}Query` — e.g. `Get{Entity}ByIdQuery`
- Command handlers: `{Action}{Entity}CommandHandler` — e.g. `Create{Entity}CommandHandler`
- Query handlers: `Get{Entity}{Criteria}QueryHandler` — e.g. `Get{Entity}ByIdQueryHandler`
- Models: no "Model" suffix — `{Entity}` not `{Entity}Model`

## Token Replacements

See `.ai/reference/tokens.md` for complete definitions.

- `{ApplicationName}` — your application name
- `{Domain}` — domain/bounded context
- `{Entity}` — entity name (PascalCase)

## Core Operational Rules

1. Load context on demand from `.ai/` based on work type only
2. Mark open questions OPEN or ASSUMED, never resolve silently
3. Verify against `.ai/checklists/pre-submission.md` before completion

## Work-Type Context Mapping

Load these files based on task type:

| Task Type | Files to Load |
|-----------|--------------|
| .NET / CQRS | `.ai/skills/dotnet-engineer/SKILL.md`, `.ai/patterns/cqrs-patterns.md`, `.ai/reference/critical-rules.md` |
| API Endpoints | `.ai/patterns/api-patterns.md`, `.ai/reference/templates/endpoint.cs.txt` |
| Unit Tests | `.ai/skills/unit-tester/SKILL.md`, `.ai/patterns/testing-patterns.md`, `.ai/reference/templates/test-class.cs.txt` |
| UI/E2E Tests | `.ai/skills/playwright-tester/SKILL.md`, `.ai/patterns/testing-patterns.md` |
| Blazor UI | `.ai/skills/blazor-specialist/SKILL.md`, `.ai/patterns/mvvm.md` |
| MAUI | `.ai/skills/maui-specialist/SKILL.md`, `.ai/patterns/mvvm.md` |
| Architecture | `.ai/skills/architect/SKILL.md`, `.ai/project/architecture.md` |
| Code Review | `.ai/skills/code-reviewer/SKILL.md`, `.ai/checklists/pre-submission.md` |
| Security | `.ai/skills/security/SKILL.md`, `.ai/skills/api-security/SKILL.md` |
| Performance | `.ai/skills/performance-engineer/SKILL.md` |
| Database | `.ai/skills/database-migration/SKILL.md` |
| DevOps | `.ai/skills/devops-engineer/SKILL.md` |
| Documentation | `.ai/skills/technical-writer/SKILL.md` |
| Bulk Refactoring | `.ai/skills/refactor/SKILL.md` |
| Design Interrogation | `.ai/skills/design-interrogation/SKILL.md` |
| Solution Scaffolding | `.ai/skills/solution-generator/SKILL.md`, `.ai/skills/vertical-slices/SKILL.md` |
| Gap Validation | `.ai/skills/gap-review/SKILL.md` |
| Domain Modeling | `.ai/skills/ubiquitous-language/SKILL.md`, `.ai/skills/usecase-specification/SKILL.md`, `.ai/skills/user-story/SKILL.md` |
| Skill Creation | `.ai/skills/skill-creator/SKILL.md` |
| Council | `.ai/reference/council.md`, `.ai/skills/council/SKILL.md` |
<!-- ai-workspace-manager:copilot-reference:end -->
