# Business Domains (CUSTOMIZE THIS)

**Instructions:** Document your project's business domains and entities.

**Purpose:** This file defines WHAT you're building - business contexts, entities, rules, and domain relationships.

## Domain Overview

**Total Domains:** [Number]

**Organization Strategy:** [How domains are organized - by business capability / by team / by module]

## Domain List

| Domain | Purpose | Status | Team/Owner |
|--------|---------|--------|------------|
| [{Domain1}] | [Business purpose] | [Active / Planned / Deprecated] | [Team/Person] |
| [{Domain2}] | [Business purpose] | [Active / Planned / Deprecated] | [Team/Person] |

**Example:**
| Domain | Purpose | Status | Team/Owner |
|--------|---------|--------|------------|
| {Domain1} | [Primary business capability] | Active | Team A |
| {Domain2} | [Supporting business capability] | Active | Team B |
| {Domain3} | [Reporting capability] | Planned | Team C |

---

## Domain Details

### {Domain1} Domain

**Purpose:** [What this domain does in business terms]

**Bounded Context:** [What this domain is responsible for - its boundaries]

**Entities:**

| Entity | Description | Aggregate Root? | Key Properties |
|--------|-------------|-----------------|----------------|
| [{Entity1}] | [What it represents] | [Yes / No] | [Key properties] |
| [{Entity2}] | [What it represents] | [Yes / No] | [Key properties] |

**Example:**
| Entity | Description | Aggregate Root? | Key Properties |
|--------|-------------|-----------------|----------------|
| {Entity} | Primary aggregate root | Yes | Name, Amount, StartDate, EndDate |
| {ChildEntity} | Child entity owned by {Entity} | No | Name, Amount, CreatedDate |

**Domain Events:**

- [{Entity}Created] - [When fired and why it matters]
- [{Entity}Updated] - [When fired and why it matters]
- [{Entity}Deleted] - [When fired and why it matters]

**Example:**
- [{Entity}Created] - When a new {entity} is successfully created; triggers notification to user
- [{ChildEntity}Updated] - When a child {childEntity} changes; triggers aggregate recalculation
- [{Entity}Deleted] - When an {entity} is removed; triggers cleanup of related records

**Business Rules:**

1. [Rule 1] - [Description and rationale]
2. [Rule 2] - [Description and rationale]
3. [Rule 3] - [Description and rationale]

**Example:**
1. {Entity}.Amount must be positive - Cannot create negative {entities}
2. The sum of child {childEntities} cannot exceed the parent {entity} amount - Prevents over-allocation
3. {ChildEntity}.CreatedDate cannot be in the future - Ensures valid chronological data
4. {Entity} periods cannot overlap for the same owner - Prevents ambiguous period assignment

**Validation Rules:**

| Field | Validation | Error Message |
|-------|-----------|---------------|
| [Field] | [Rule] | [Message] |

**Example:**
| Field | Validation | Error Message |
|-------|-----------|---------------|
| {Entity}.Name | Required, Max 100 chars | "{Entity} name is required and must be less than 100 characters" |
| {Entity}.Amount | > 0, < 1,000,000 | "{Entity} amount must be between 0 and 1,000,000" |
| {ChildEntity}.Amount | > 0 | "{ChildEntity} amount must be positive" |

**Domain-Specific Patterns:**

- [Pattern 1] - [Why used in this domain]
- [Pattern 2] - [Why used in this domain]

**Example:**
- **Soft Delete** - {Entity} entities use soft delete (IsDeleted flag) to maintain historical data for reporting
- **Cascade Archiving** - Deleting an {entity} marks its child {childEntities} as archived, not deleted
- **Temporal Data** - {Entity} has StartDate/EndDate for period-based queries and overlapping validation

**Project Structure:**

```
{ApplicationName}.Contracts.{Domain}/       # Service contracts, interfaces
{ApplicationName}.Entities.{Domain}/        # EF Core entity classes
{ApplicationName}.Models.{Domain}/          # DTOs, view models
{ApplicationName}.Domain.{Domain}/          # CQRS handlers, domain logic
{ApplicationName}.Services.{Domain}/        # API endpoints
{ApplicationName}.ViewModels.{Domain}/      # MVVM ViewModels (if applicable)
```

**Dependencies:**

- **Depends On:** [Other domains this one depends on]
- **Depended On By:** [Other domains that depend on this one]

**Example:**
- **Depends On:** None (core domain)
- **Depended On By:** {Domain2} (reads {entity} data), {Domain3} (aggregates {entity} metrics)

---

### {Domain2} Domain

[Repeat the same structure for each domain]

---

## Cross-Domain Relationships

**Document how domains interact:**

```
[Visual representation of domain dependencies]

Example:
{Domain1} ----reads----→ {Domain2} (get related details)
{Domain1} ----creates---→ {Domain3} (raise a domain event)
{Domain3} ----reads----→ All Domains (aggregate reporting data)
```

**Relationship Details:**

| Source Domain | Relationship | Target Domain | Method | Notes |
|--------------|--------------|---------------|--------|-------|
| [Domain1] | [reads/writes/creates] | [Domain2] | [How communicated] | [Why needed] |

**Example:**
| Source Domain | Relationship | Target Domain | Method | Notes |
|--------------|--------------|---------------|--------|-------|
| {Domain1} | reads | {Domain2} | Direct reference | Get related details |
| {Domain1} | creates | {Domain3} | Domain event | Create a record when the aggregate completes |
| {Domain3} | reads | All | Read-only queries | Aggregate data for reporting |

## Shared Concepts

**Concepts used across multiple domains:**

| Concept | Domains | Approach | Location |
|---------|---------|----------|----------|
| [Concept] | [Domain1, Domain2] | [Shared / Duplicated / Referenced] | [Where defined] |

**Example:**
| Concept | Domains | Approach | Location |
|---------|---------|----------|----------|
| {ValueObject} | {Domain1}, {Domain2} | Shared value object | Common.ValueObjects |
| Money | {Domain1}, {Domain2} | Shared value object with currency | Common.ValueObjects |
| AuditFields | All domains | Base entity | Common.Entities.BaseEntity |

## Domain Maturity

**Implementation maturity per domain:**

| Domain | Maturity | Coverage | Technical Debt | Notes |
|--------|----------|----------|----------------|-------|
| [{Domain}] | [Initial / Growing / Mature] | [% complete] | [Low / Medium / High] | [Notes] |

**Maturity Levels:**
- **Initial:** Basic CRUD, minimal testing, incomplete features
- **Growing:** Most features implemented, good test coverage, some edge cases missing
- **Mature:** Complete implementation, comprehensive testing, production-ready, well-documented

**Example:**
| Domain | Maturity | Coverage | Technical Debt | Notes |
|--------|----------|----------|----------------|-------|
| {Domain1} | Mature | 100% | Low | Complete CRUD, full testing, comprehensive documentation |
| {Domain2} | Growing | 60% | Medium | Missing bulk operations, needs performance optimization |
| {Domain3} | Initial | 20% | Low | Basic create/read only, needs update/delete and validation |

## Reference Implementation

**Which domain serves as the template:**

**Primary Reference:** [{Domain}] - [Why it's the reference]

**What to copy from the reference:**
- [Aspect 1] - [What to learn from it]
- [Aspect 2] - [What to learn from it]
- [Aspect 3] - [What to learn from it]

**Example:**

**Primary Reference:** [{Entities}] - Complete implementation with all CRUD operations, comprehensive testing, full documentation

**What to copy from the reference:**
- CQRS handler structure and naming conventions
- API endpoint organization
- Unit test structure with BDD scenarios
- XML documentation style

## Domain Evolution History

**Track how domains have evolved over time:**

### {Domain} Evolution

**Version 1.0 (Date):**
- [Feature 1]
- [Feature 2]

**Version 2.0 (Date):**
- [Feature added]
- [Refactoring done]
- [Breaking change]

**Example:**

### {Entities} Evolution

**Version 1.0 (2025-01-01):**
- Basic {entity} CRUD operations
- Simple {childEntity} tracking
- Basic validation

**Version 2.0 (2025-02-01):**
- Added {childEntity} management
- Implemented recurring transactions
- Added {entity} templates
- Enhanced validation with business rules

**Version 2.1 (2025-02-15):**
- Performance optimization for large {entity} lists
- Added {entity} category filtering
- Implemented soft delete for historical data

## Future Domains

**Planned domains not yet implemented:**

| Future Domain | Purpose | Priority | Dependencies | Estimated Effort |
|---------------|---------|----------|--------------|------------------|
| [Domain] | [Purpose] | [High / Medium / Low] | [Required domains] | [Small / Medium / Large] |

**Example:**
| Future Domain | Purpose | Priority | Dependencies | Estimated Effort |
|---------------|---------|----------|--------------|------------------|
| {Domain2} | Reporting and insights | Medium | {Entities} | Medium |
| Notifications | User notifications | Low | All domains | Small |
| {Domain3} | Automated business workflows | High | {Entities} | Large |

## Domain Ubiquitous Language

**Key terms used in each domain:**

### {Domain} Terms

| Term | Definition | Usage |
|------|------------|-------|
| [Term] | [Business definition] | [How used in code] |

**Example:**

### {Domain} Terms

| Term | Definition | Usage |
|------|------------|-------|
| {Entity} | Primary aggregate root record | {Entity} entity, {Entity}Model DTO |
| {ChildEntity} | A child record owned by an {entity} | {ChildEntity} entity, child of {Entity} |
| Allocation | Assignment of {entity} amount to categories | Property on {Entity} entity |
| Rollover | Carrying unused {entity} to next period | Feature flag on {Entity} |

---

**Remember:** Keep this file updated as domains evolve. Reference it in session-context.md when working on specific domains. For architectural patterns, see [architecture.md](architecture.md). For technology choices, see [tech-stack.md](tech-stack.md).
