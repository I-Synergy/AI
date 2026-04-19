# Template Frequently Asked Questions

This document captures common questions about using the .NET Development Template with Claude Code.

**Last Updated:** 2026-04-19

---

## Q1: How will chat commands look like?

### Answer

You can interact with the template in three ways:

#### 1. Slash Commands (Skills)

Invoke specialized skills directly:

```
/dotnet-engineer          - .NET/C# development tasks
/unit-tester              - Write MSTest unit tests
/code-reviewer            - Review code for quality and architecture
/architect                - System design and architecture decisions
/blazor-specialist        - Blazor UI development
/maui-specialist          - MAUI mobile app development
/playwright-tester        - E2E and UI testing
/database-migration       - EF Core migrations and database work
/integration-specialist   - External API integrations
/performance-engineer     - Performance optimization
/security                 - Security architecture and compliance
/api-security             - API security implementation
/software-security        - Application security practices
/technical-writer         - Documentation creation
/refactor                 - Bulk find-and-replace migrations across solution
/design-interrogation     - Structured design interviews and stress-testing
/skill-creator            - Create and improve Claude skills
/ubiquitous-language      - Capture domain vocabulary glossary
/usecase-specification    - Draft use case specs with Gherkin
/user-story               - Draft INVEST-validated user stories
/solution-generator       - Scaffold .NET solution from architecture doc
/vertical-slices          - Generate vertical slice blueprint JSON
/gap-review               - Validate solution against design decisions
/upgrade-template         - Upgrade existing project from template
/verify-config            - Audit CLAUDE.md against actual codebase
/update-skills            - Sync .claude/skills/ and .github/skills/
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
"Stress-test my API design"
"Extract a ubiquitous language glossary from this spec"
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

- Global rules from `~/.claude/CLAUDE.md` (your personal preferences)
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
- Write progress to `.ai/progress/{task-slug}.md`
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

You: "Grill me on my API design"
AI: [Recognizes stress-test request → invokes design-interrogation skill]
```

**Matching logic:**
- **Keywords**: "review", "test", "implement", "optimize", "secure", "grill me", "stress-test"
- **Context**: Code review vs. development vs. testing vs. architecture
- **Scope**: Implementation vs. documentation vs. design

### 2. Agents (Autonomous Workers)

**Agents are spawned via Task tool for:**
- **Complex exploration** → `Explore` agent
- **Multi-step tasks** → `general-purpose` agent
- **Planning work** → `Plan` agent
- **Git operations** → `Bash` agent

These are different from skills — they're autonomous workers for complex tasks.

### 3. Context Files (Automatic Loading)

**Context files from `.ai/` are loaded based on Work-Type Context Mapping:**

```
Your request: "Implement CQRS for Budget"

AI automatically loads:
- .ai/skills/dotnet-engineer/SKILL.md
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
   - .ai/skills/dotnet-engineer/SKILL.md
   - .ai/patterns/cqrs-patterns.md
   - .ai/skills/unit-tester/SKILL.md
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
2026-04-19

## Project Patterns Discovered
- Budget entity uses soft delete pattern (DeletedAt timestamp)
- All monetary amounts use decimal(18,2) precision
- Date ranges validated: EndDate must be > StartDate

## Architectural Decisions
- Decision: Use Redis for caching reference data
  Rationale: Reference data rarely changes, reduces DB load
  Date: 2026-04-19
```

**Every session:**
- **Reads** session-context.md at start (learns from past)
- **Updates** session-context.md at end (teaches future sessions)

#### 2. Completed Task Archive

Finished tasks move to `.ai/completed/` and serve as historical reference.

#### 3. Progressive Pattern Documentation

As project-specific patterns are discovered, they're documented in `.ai/project/` and `.ai/patterns/`.

### What Gets "Learned"

| What | Where | How |
|------|-------|-----|
| **Patterns discovered** | `session-context.md` | Updated each session |
| **Architectural decisions** | `completed/` archive | Decision records |
| **Domain-specific rules** | `.ai/project/domains.md` | Progressive documentation |
| **Common issues** | `session-context.md` | Blockers and solutions |
| **Code conventions** | `session-context.md` | Project-specific styles |

### Limitations

**The template does NOT:**
- ❌ Train the AI model itself (no fine-tuning)
- ❌ Persist memory across projects automatically
- ❌ Automatically detect patterns without guidance

**The template DOES:**
- ✅ Maintain session-to-session context
- ✅ Document discovered patterns
- ✅ Archive decision history
- ✅ Build institutional knowledge over time

---

## Q6: How do I upgrade an existing project when the template improves?

### Answer

Use the included upgrade script — it safely copies template-owned files while never touching your project-owned files.

```bash
# Interactive mode — review each changed file
python .ai/scripts/upgrade-template.py /path/to/YourProject

# Preview mode — see what would change, nothing written
python .ai/scripts/upgrade-template.py /path/to/YourProject --dry-run

# Skills only — copy new/updated skills without touching anything else
python .ai/scripts/upgrade-template.py /path/to/YourProject --skills-only

# Non-interactive — accept all changes (use in CI)
python .ai/scripts/upgrade-template.py /path/to/YourProject --non-interactive
```

### What gets updated vs. preserved

| Category | Examples | Behavior |
|----------|---------|---------|
| **Template-owned** | `.ai/skills/`, `.ai/patterns/`, `.ai/reference/templates/`, `.ai/tests/` | Safely updated |
| **Project-owned** | `CLAUDE.md`, `.ai/session-context.md`, `.ai/project/`, `.ai/progress/` | Never touched |

Or invoke as a slash command:
```
/upgrade-template
```

---

## Q7: How do I run the validation tests?

### Answer

The template includes a 10-suite validation suite that can be run via bash or pytest (VS Code Test Explorer).

#### Bash (works everywhere)

```bash
bash .ai/tests/run-all-tests.sh
```

#### Pytest (VS Code Test Explorer integration)

```bash
# Install pytest (use project-scoped pip config if on corporate network)
pip install --config-file pip.ini pytest

# Run all suites
python -m pytest .ai/tests/test_suite.py -v

# Run a single suite
python -m pytest .ai/tests/test_suite.py::test_yaml_frontmatter -v
```

Once pytest is installed, VS Code's Test Explorer panel shows all 10 suites as clickable tests with inline failure output.

#### What each suite checks

| # | Suite | Checks |
|---|-------|--------|
| 1 | Directory Structure | Required dirs, SKILL.md presence, templates |
| 2 | YAML Frontmatter | name, description, allowed-tools in every SKILL.md |
| 3 | File References | All paths referenced in CLAUDE.md and templates exist |
| 4 | Content Quality | Skills and patterns have sufficient content |
| 5 | Token Consistency | `{Entity}`, `{Domain}` etc. defined and used consistently |
| 6 | CLAUDE.md References | No broken `.ai/` paths in CLAUDE.md |
| 7 | Settings & Structure | `.claude/settings.json` structure, no stale paths |
| 8 | Copilot Integration | Three-tier skill sync is correct and in sync |
| 9 | Smoke Tests | All skills loadable, names and descriptions unique |
| 10 | Upgrade Script | Script classification logic and integration tests |

---

## Key Takeaways

1. **Interaction is flexible** - Use slash commands, natural language, or structured requests
2. **CLAUDE.md is automatic** - No need to reference it explicitly
3. **Agents are automatic** - Spawned when needed, you just focus on what to do
4. **Skills are smart** - AI recognizes work type and invokes appropriate skills
5. **Template learns** - Through session context and progressive documentation
6. **Safe to upgrade** - The upgrade script preserves all project-owned files

## Quick Start Tips

1. **Start naturally**: Just describe what you want
2. **Trust the system**: It handles skill selection and agent spawning
3. **Document learnings**: Explicitly ask to document patterns and decisions
4. **Review regularly**: Consolidate session context into permanent docs
5. **Upgrade regularly**: Run the upgrade script when the template improves

---

**For more details, see:**
- [README.md](README.md) - Comprehensive overview
- [CLAUDE.md](CLAUDE.md) - Orchestration file (automatically loaded)
- [TEMPLATE-USAGE.md](TEMPLATE-USAGE.md) - Detailed usage guide
- [.ai/session-context.md](.ai/session-context.md) - Session memory (template)
