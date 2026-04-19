# Template Frequently Asked Questions

This document captures common questions about using the .NET Development Template with Claude Code.

**Date:** 2026-02-16
**Context:** Initial template orientation and understanding

---

## Q1: How will chat commands look like?

### Answer

You can interact with the template in three ways:

#### 1. Slash Commands (Skills)

Invoke specialized skills directly:

```
/dotnet-engineer     - .NET/C# development tasks
/unit-tester         - Write MSTest unit tests
/code-reviewer       - Review code for quality and architecture
/architect           - System design and architecture decisions
/blazor-specialist   - Blazor UI development
/maui-specialist     - MAUI mobile app development
/playwright-tester   - E2E and UI testing
/database-migration  - EF Core migrations and database work
/integration-specialist - External API integrations
/performance-engineer   - Performance optimization
/security            - Security architecture and compliance
/api-security        - API security implementation
/software-security   - Application security practices
/technical-writer    - Documentation creation
```

#### 2. Natural Language Requests

Just describe what you want:

```
"Implement CQRS commands and queries for the Budget entity"
"Add API endpoints for Budget management"
"Write unit tests for CreateBudgetHandler"
"Review the current domain structure"
"Optimize database queries in the Budgets domain"
"Create E2E tests for the login flow"
```

The AI automatically:
- Recognizes the work type
- Loads relevant context files from `.ai/`
- Invokes appropriate skills
- Spawns agents if needed
- Follows all patterns and conventions

#### 3. Structured Task Requests

For complex work, provide structured details:

```
Implement Budget Domain

Requirements:
- Create entity, model, domain layer
- Implement CQRS commands (Create, Update, Delete)
- Implement queries (GetById, GetList)
- Add API endpoints
- Write unit tests

Domain: Budgets
Entity: Budget
Properties: Name, Amount, StartDate, EndDate
```

---

## Q2: Do I need to reference the CLAUDE.md file?

### Answer

**No, you do not need to reference CLAUDE.md explicitly.**

It's automatically loaded and applied to every conversation.

### What happens automatically:

- Global rules from `~/.ai/CLAUDE.md` (your personal preferences)
- Project rules from `{project}/CLAUDE.md` (template configuration)
- Both are merged and active in every request

### Just work naturally:

```
"Create a new Budget entity with CQRS handlers"
"Add API endpoints for Commodity"
"Write unit tests for CreateDebtHandler"
```

The AI will automatically follow all patterns, conventions, and rules defined in CLAUDE.md.

### Only reference CLAUDE.md if you want to:

- **Override a rule temporarily:** "ignore the no-emoji rule for this file"
- **Question a rule:** "why does CLAUDE.md forbid MediatR?"
- **Update configuration:** "add a new pattern to CLAUDE.md"

---

## Q3: Will agents be automatically created when needed?

### Answer

**Yes, agents are spawned automatically when needed.** You don't need to request them explicitly.

### When agents are spawned automatically:

- **Complex exploration** - "Find all usages of Budget entity across the codebase"
  - → Spawns `Explore` agent

- **Multi-step implementations** - "Implement complete CQRS for Budget domain"
  - → Spawns `general-purpose` agent

- **Parallel work** - "Review code AND run tests AND update docs"
  - → Spawns multiple agents in parallel

- **Large refactoring** - "Refactor all handlers in the Budgets domain"
  - → Spawns task-specific agents

- **Research tasks** - "How is authentication currently implemented?"
  - → Spawns `Explore` agent

### What you'll see:

The AI will transparently inform you when spawning agents:

```
"I'll use an Explore agent to search the codebase for Budget entity usages..."
"Spawning a general-purpose agent to implement the CQRS handlers..."
"Creating parallel agents to handle testing and documentation..."
```

### Progress tracking:

All agents automatically:
- Write progress to `.ai/progress/[task-name]-progress.md`
- Report structured results
- Move completed work to `.ai/completed/`

### You control the process:

- Request specific approaches: "Search for this manually without agents"
- Ask for parallel work: "Run tests and build in parallel"
- Request agent usage: "Use an agent to explore the authentication flow"

### Bottom line:

Focus on **what you want done**, not **how** it gets done. The AI handles orchestration.

---

## Q4: How will the agent know which skill to use?

### Answer

Three systems work together automatically:

### 1. Skills (Specialized Prompts)

**Skills are invoked when:**

**User explicitly requests:**
```
/dotnet-engineer
/unit-tester
/code-reviewer
```

**User's request matches skill description:**
```
You: "Review this code for SOLID principles"
AI: [Recognizes code review → invokes code-reviewer skill]

You: "Write unit tests for CreateBudgetHandler"
AI: [Recognizes testing → invokes unit-tester skill]

You: "Implement CQRS handlers for Budget"
AI: [Recognizes .NET development → invokes dotnet-engineer skill]
```

**Matching logic:**
- **Keywords**: "review", "test", "implement", "optimize", "secure"
- **Context**: Code review vs. development vs. testing
- **Scope**: Architecture vs. implementation vs. documentation

### 2. Agents (Autonomous Workers)

**Agents are spawned via Task tool for:**
- **Complex exploration** → `Explore` agent
- **Multi-step tasks** → `general-purpose` agent
- **Planning work** → `Plan` agent
- **Git operations** → `Bash` agent

These are different from skills—they're autonomous workers for complex tasks.

### 3. Context Files (Automatic Loading)

**Context files from `.ai/` are loaded based on Work-Type Context Mapping:**

```
Your request: "Implement CQRS for Budget"

AI automatically loads:
- .ai/skills/dotnet-engineer.md
- .ai/patterns/cqrs-patterns.md
- .ai/reference/critical-rules.md
- .ai/reference/templates/command-handler.cs.txt
```

### Complete Decision Flow Example

```
You: "Add Budget entity with CQRS handlers and unit tests"

AI process:
1. Recognize work type: CQRS Implementation + Testing

2. Load context files automatically:
   - .ai/skills/dotnet-engineer.md
   - .ai/patterns/cqrs-patterns.md
   - .ai/skills/unit-tester.md
   - .ai/patterns/testing-patterns.md

3. Decide if skills needed:
   - Implementation work → May invoke dotnet-engineer skill
   - Testing work → May invoke unit-tester skill

4. Decide if agents needed:
   - Complex task → May spawn agent for exploration
   - Or handle directly if straightforward

5. Execute work following loaded patterns

6. Write progress to .ai/progress/
```

### You don't need to worry about it

Just make natural requests, and the AI handles:
- Skill invocation
- Agent spawning
- Context loading
- Pattern following
- Progress tracking

The AI will transparently communicate what's happening:
```
"Loading CQRS patterns and dotnet-engineer context..."
"Invoking unit-tester skill for test generation..."
"Spawning Explore agent to search the codebase..."
```

---

## Q5: Can this template learn from its usage?

### Answer

**Yes, the template can learn from its usage** through contextual memory and progressive documentation.

### How the Template "Learns"

#### 1. Session Context Memory

The template maintains a learning record in `.ai/session-context.md`:

```markdown
# Session Context

## Last Updated
2026-02-16

## Project Patterns Discovered
- Budget entity uses soft delete pattern (DeletedAt timestamp)
- All monetary amounts use decimal(18,2) precision
- Date ranges validated: EndDate must be > StartDate

## Architectural Decisions
- Decision: Use Redis for caching reference data
  Rationale: Reference data rarely changes, reduces DB load
  Date: 2026-02-15

## Known Issues
- None currently

## Next Session Should Know
- Budget domain is complete reference implementation
- Follow Budget patterns for new domains
```

**Every session:**
- **Reads** session-context.md at start (learns from past)
- **Updates** session-context.md at end (teaches future sessions)

#### 2. Completed Task Archive

Finished tasks move to `.ai/completed/`:

```markdown
# Implement Budget Domain - Progress

## What Was Done
- Created Budget entity with soft delete
- Implemented CQRS commands: Create, Update, Delete
- Added validation: EndDate > StartDate

## Patterns Established
- Command parameters: individual values, not model objects
- Soft delete: use DeletedAt, not IsDeleted boolean
- Mapping: Manual (`new T(...)` or LINQ `.Select`) — no mapping library

## Issues Encountered
- Initial approach used repository pattern - refactored to DataContext extensions
- Learned: Check existing code before creating new patterns
```

#### 3. Progressive Pattern Documentation

As project-specific patterns are discovered, they're documented in `.ai/project/` and `.ai/patterns/`.

#### 4. Decision Records

Architectural decisions are tracked for future reference.

### What Gets "Learned"

| What | Where | How |
|------|-------|-----|
| **Patterns discovered** | `session-context.md` | Updated each session |
| **Architectural decisions** | `completed/` archive | Decision records |
| **Domain-specific rules** | `.ai/project/domains.md` | Progressive documentation |
| **Common issues** | `session-context.md` | Blockers and solutions |
| **Code conventions** | `session-context.md` | Project-specific styles |
| **Performance optimizations** | `completed/` tasks | What worked, what didn't |
| **Testing strategies** | `session-context.md` | Effective test patterns |

### Continuous Improvement Workflow

```
Session 1: Implement Budget Domain
├─ Discovers: Budget uses soft delete pattern
├─ Writes to: session-context.md
└─ Archives to: completed/implement-budget-domain-progress.md

Session 2: Implement Goals Domain
├─ Reads: session-context.md (learns soft delete pattern)
├─ Applies: Same soft delete approach to Goals
├─ Discovers: Goals require Budget foreign key validation
├─ Writes to: session-context.md
└─ Archives to: completed/implement-goals-domain-progress.md

Session 3: Implement Debts Domain
├─ Reads: session-context.md (learns both patterns)
├─ Applies: Soft delete + foreign key validation
├─ Discovers: Debts need additional audit fields
├─ Writes to: session-context.md
└─ Archives to: completed/implement-debts-domain-progress.md
```

Each session builds on previous learnings!

### Limitations

**The template does NOT:**
- ❌ Train the AI model itself (no fine-tuning)
- ❌ Persist memory across projects automatically
- ❌ Share learnings with other projects
- ❌ Automatically detect patterns without guidance

**The template DOES:**
- ✅ Maintain session-to-session context
- ✅ Document discovered patterns
- ✅ Archive decision history
- ✅ Build institutional knowledge over time
- ✅ Enable progressive refinement

### Making It Learn Better

**Be explicit about learnings:**
```
"Document this pattern in session-context.md for future use"
"Add this decision to the architecture decisions log"
"Extract this as a reusable pattern in .ai/patterns/"
```

**Review and consolidate regularly:**
```
"Review session context and move stable patterns to permanent docs"
"Analyze completed tasks and extract common patterns"
"Update domains.md with discovered business rules"
```

---

## Key Takeaways

1. **Interaction is flexible** - Use slash commands, natural language, or structured requests
2. **CLAUDE.md is automatic** - No need to reference it explicitly
3. **Agents are automatic** - Spawned when needed, you just focus on what to do
4. **Skills are smart** - AI recognizes work type and invokes appropriate skills
5. **Template learns** - Through session context and progressive documentation

## Quick Start Tips

1. **Start naturally**: Just describe what you want
2. **Trust the system**: It handles skill selection and agent spawning
3. **Document learnings**: Explicitly ask to document patterns and decisions
4. **Review regularly**: Consolidate session context into permanent docs
5. **Let it improve**: Each session makes the template smarter

---

**For more details, see:**
- [README.md](README.md) - Comprehensive overview
- [CLAUDE.md](CLAUDE.md) - Orchestration file (automatically loaded)
- [TEMPLATE-USAGE.md](TEMPLATE-USAGE.md) - Detailed usage guide
- [.ai/session-context.md](.ai/session-context.md) - Session memory (template)

**Last Updated:** 2026-02-16
