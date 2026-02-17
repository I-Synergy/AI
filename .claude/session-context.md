# Session Context Template (CUSTOMIZE THIS)

**Instructions:** Copy this to `.claude/session-context.md` and customize for your project.

# {ApplicationName} Session Context

**Last Updated:** [DateTime]
**Updated By:** [User/Agent name]
**Project Version:** [Version]

---

## Project Overview

**Application Name:** [{ApplicationName}]
**Purpose:** [What this application does]
**Current Phase:** [Development / Testing / Production]
**Team Size:** [Number of developers]

---

## Architectural Patterns Established

### CQRS Pattern (Updated: YYYY-MM-DD)

- **Commands:** [How commands are structured in this project]
- **Queries:** [How queries are structured]
- **Handlers:** [Handler patterns followed]
- **Reason:** [Why this specific approach]

**Example:**
- **Commands:** Individual parameters only (NOT model objects)
- **Queries:** Named parameters for optional filters
- **Handlers:** Inject DataContext directly (no repository layer)
- **Reason:** Reduces abstraction layers, improves performance, clearer intent

### Data Access Pattern (Updated: YYYY-MM-DD)

- **Pattern:** [How data access is done]
- **Technology:** [ORM/framework used]
- **Transactions:** [How transactions are managed]
- **Reason:** [Why this pattern]

**Example:**
- **Pattern:** DataContext extension methods (AddItemAsync, RemoveItemAsync, etc.)
- **Technology:** Entity Framework Core 10 with PostgreSQL
- **Transactions:** Implicit per SaveChanges, explicit for multi-operation
- **Reason:** Simplifies data access, consistent patterns, leverages EF Core features

### Mapping Pattern (Updated: YYYY-MM-DD)

- **Technology:** [Mapping library]
- **Configuration:** [How mappings are defined]
- **Registration:** [How mappings are registered]
- **Reason:** [Why chosen]

**Example:**
- **Technology:** Mapster
- **Configuration:** Explicit configuration in `{Entity}MappingConfig.cs` files
- **Registration:** Scanned and applied in domain ServiceCollectionExtensions
- **Reason:** Better performance than AutoMapper, explicit configuration, compile-time safety

---

## User Preferences

### Development Workflow

- **Autonomy level:** [Full autonomy / Ask before major changes / etc.]
- **Progress tracking:** [Real-time updates / Status on request]
- **Testing approach:** [TDD / Tests after implementation / Mixed]
- **Documentation level:** [Comprehensive / API docs only / Minimal]

**Example:**
- **Autonomy level:** Full autonomy - agents have full repo access, execute without asking
- **Progress tracking:** Real-time updates to progress files required
- **Testing approach:** MSTest + Moq + Reqnroll, comprehensive test coverage
- **Documentation level:** XML docs on all public APIs, architecture diagrams for complex flows

### Communication Style

- **Formality:** [Direct and concise / Detailed / Encouraging]
- **Clarifications:** [Ask before starting / Proceed with assumptions / etc.]
- **Status updates:** [Automatic / On request / etc.]
- **Error reporting:** [Immediate with context / Summary at end]

**Example:**
- **Formality:** Direct and matter-of-fact, no sycophancy
- **Clarifications:** Ask before starting major work if ambiguous
- **Status updates:** Automatic real-time progress tracking
- **Error reporting:** Report all issues immediately with context

### Code Style Preferences

- **Immutability:** [Records preferred / Classes / Mixed]
- **Expression-bodied members:** [Use extensively / Sparingly]
- **Null handling:** [Nullable reference types enabled / Optional]
- **Comments:** [For complex logic only / Extensive / Minimal]

---

## Domain-Specific Knowledge

### {Domain} (Reference Implementation)

**Status:** [Complete / In Progress / Planned]
**Location:** [`src/{ApplicationName}.Domain.{Domain}/`]
**Use As Template:** [Yes / No]

**Key Learnings:**
- [Pattern or decision 1]
- [Pattern or decision 2]
- [Pattern or decision 3]

**Example:**

### Budgets (Reference Implementation)

**Status:** Complete and production-ready
**Location:** `src/BudgetTracker.Domain.Budgets/`
**Use As Template:** Yes - all future domain implementations should follow this pattern

**Key Learnings:**
- Command handlers validate at entry, use guard clauses
- Queries use named parameters for flexible filtering
- Mapping configurations are explicit and testable
- Integration tests cover all endpoints
- BDD scenarios document complex business rules

---

## Known Issues & Workarounds

### Issue 1: [Description]

- **Issue:** [What the problem is]
- **Status:** [Working / Blocked / Resolved]
- **Workaround:** [How it's currently handled]
- **Long-term solution:** [Planned fix]

**Example:**

### Issue 1: EF Core Eager Loading Performance

- **Issue:** N+1 queries when loading budget with goals and debts
- **Status:** Resolved
- **Workaround:** Added explicit `.Include(b => b.Goals).Include(b => b.Debts)` to all budget queries
- **Long-term solution:** Consider projection to DTOs with specific includes per use case

---

## Blocked Paths (Do Not Retry)

**Document approaches that were tried and don't work:**

### [Technology/Approach Name]

- **❌ WRONG:** [What doesn't work]
- **✓ CORRECT:** [What works instead]
- **Reason:** [Why the wrong approach failed]
- **Documented:** [Date]

**Example:**

### FluentValidation for Command Validation

- **❌ WRONG:** Using FluentValidation for command validation
- **✓ CORRECT:** Use Data Annotations + IValidatableObject
- **Reason:** Data Annotations integrate better with ASP.NET Core model binding, simpler approach, one less dependency
- **Documented:** 2025-02-01

---

## Reference Implementations

**Which implementations serve as templates:**

### Feature Implementation Patterns

1. **{Domain}.{Entity}** - [What pattern it demonstrates]
2. **{Domain}.{Entity}** - [What pattern it demonstrates]

**Example:**

### Feature Implementation Patterns

1. **Budgets.Budget** - Complete CRUD with all operations, full test coverage, comprehensive documentation
2. **Customers.Customer** - Demonstrates soft-delete pattern and audit logging
3. **Orders.Order** - Shows aggregate root with child entities (OrderLines)

**Pattern to Follow:**
Copy Budgets.Budget structure exactly - proven and working in production.

---

## Decisions Made

**Document significant decisions for reference:**

### Decision: [Decision Name] (Date: YYYY-MM-DD)

**Context:** [What was the situation]
**Options Considered:**
1. [Option 1] - [Pros/Cons]
2. [Option 2] - [Pros/Cons]

**Decision:** [What was chosen]
**Rationale:** [Why it was chosen]
**Impact:** [How it affects the project]

**Example:**

### Decision: Use Mapster Over AutoMapper (Date: 2025-01-15)

**Context:** Need object mapping between DTOs and entities

**Options Considered:**
1. AutoMapper - Widely used, mature, convention-based
2. Mapster - Performance-focused, explicit configuration
3. Manual mapping - Full control, most verbose

**Decision:** Use Mapster for all object mapping

**Rationale:**
- Better performance (compile-time code generation)
- Explicit configuration makes mappings testable and discoverable
- Smaller dependency footprint

**Impact:**
- All domains must use Mapster
- Mapping configurations in {Entity}MappingConfig.cs
- Team needs to learn Mapster (documentation added to wiki)

---

## Current Sprint/Iteration

**What we're working on now:**

**Sprint:** [Sprint number/name]
**Dates:** [Start - End]
**Goals:** [Sprint goals]

**Completed:**
- [x] [Completed item 1]
- [x] [Completed item 2]

**In Progress:**
- [ ] [In progress item 1]
- [ ] [In progress item 2]

**Planned:**
- [ ] [Planned item 1]
- [ ] [Planned item 2]

---

## Recent Changes

**Track recent significant changes:**

### [Date] - [Change Description]

**What Changed:** [Specific changes]
**Why:** [Reason for change]
**Impact:** [How it affects development]
**Migration Required:** [Yes/No - if yes, what]

**Example:**

### 2025-02-15 - Switched from Swashbuckle to Microsoft.AspNetCore.OpenApi

**What Changed:** Replaced Swashbuckle with Microsoft's official OpenAPI package
**Why:** Microsoft's package is now mature and officially supported
**Impact:** All existing Swagger configurations need updating, documentation approach unchanged
**Migration Required:** Yes - update all endpoint WithOpenApi() calls

---

## Integration Points

**External services and how we integrate:**

| Service | Purpose | Auth Method | Error Handling |
|---------|---------|-------------|----------------|
| [Service] | [What it does] | [How we auth] | [How we handle errors] |

**Example:**
| Service | Purpose | Auth Method | Error Handling |
|---------|---------|-------------|----------------|
| SendGrid | Email delivery | API Key | Retry 3x exponential backoff, fallback to SMTP |
| Stripe | Payment processing | OAuth2 | Circuit breaker, log failures, manual retry |

---

## Next Session Checklist

**For the next Claude session to read:**

1. **Current Focus:** [What to focus on next]
2. **Blockers:** [Any blockers to be aware of]
3. **Recent Decisions:** [Key decisions from this session]
4. **Patterns Changed:** [Any pattern changes to note]

**Example:**

1. **Current Focus:** Implement Customers domain following Budgets reference pattern
2. **Blockers:** Waiting for Customer API schema approval from Product team
3. **Recent Decisions:** Decided to use soft-delete for Customers (see Decision log above)
4. **Patterns Changed:** None - continue following established patterns

---

**Remember:** Update this file at the end of every session with new learnings, decisions, and context. This is Claude's persistent memory.
