# Claude Development Template

## Identity

You are a development agent working within a generic .NET project template.

## Template Tokens

See `.claude/reference/tokens.md` for complete token definitions. Replace `{ApplicationName}`, `{Domain}`, `{Entity}` throughout the codebase.

## Core Operational Rules

1. Read session context first: `.claude/session-context.md` (never mix project contexts)
2. Load context on demand from `.claude/` based on work type only
3. Delegate to specialized agents with structured real-time progress
4. Write state to disk: `.claude/progress/`
5. Mark open questions OPEN or ASSUMED, never resolve silently
6. Before session end: Write structured handoff to `.claude/session-context.md`
7. Verify against `.claude/checklists/pre-submission.md` before completion

## Work-Type Context Mapping

Load these files based on task type:

**.NET Development:**
- `.claude/skills/dotnet-engineer/SKILL.md`
- `.claude/patterns/object-oriented-programming.md`

**CQRS Implementation:**
- `.claude/skills/dotnet-engineer/SKILL.md`
- `.claude/patterns/cqrs-patterns.md`
- `.claude/reference/critical-rules.md`
- `.claude/reference/templates/command-handler.cs.txt`
- `.claude/reference/templates/query-handler.cs.txt`
- `.claude/reference/templates/mapping-config.cs.txt`

**API Endpoints:**
- `.claude/patterns/api-patterns.md`
- `.claude/reference/templates/endpoint.cs.txt`

**Testing (Unit Tests):**
- `.claude/skills/unit-tester/SKILL.md`
- `.claude/patterns/testing-patterns.md`
- `.claude/patterns/test-driven-development.md`
- `.claude/reference/templates/test-class.cs.txt`
- `.claude/reference/templates/feature-file.feature.txt`

**Testing (UI/E2E):**
- `.claude/skills/playwright-tester/SKILL.md`
- `.claude/patterns/testing-patterns.md`

**Integration Development:**
- `.claude/skills/integration-specialist/SKILL.md`
- `.claude/patterns/service-oriented-architecture.md`

**Architecture Decisions:**
- `.claude/skills/architect/SKILL.md`
- `.claude/project/architecture.md`

**Code Review:**
- `.claude/skills/code-reviewer/SKILL.md`
- `.claude/checklists/pre-submission.md`

**Security:**
- `.claude/skills/security/SKILL.md`
- `.claude/skills/api-security/SKILL.md`
- `.claude/skills/software-security/SKILL.md`

**Performance:**
- `.claude/skills/performance-engineer/SKILL.md`

**Microservices Architecture:**
- `.claude/patterns/microservices.md`
- `.claude/skills/integration-specialist/SKILL.md`

**UI Development (Blazor):**
- `.claude/skills/blazor-specialist/SKILL.md`
- `.claude/patterns/mvvm.md`

**UI Development (MAUI):**
- `.claude/skills/maui-specialist/SKILL.md`
- `.claude/patterns/mvvm.md`

**Database:**
- `.claude/skills/database-migration/SKILL.md`

**DevOps:**
- `.claude/skills/devops-engineer/SKILL.md`

**Documentation:**
- `.claude/skills/technical-writer/SKILL.md`

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
Domain/Features/{Entity}/
  Commands/
  Queries/
  Events/
Mappers/{Entity}MappingConfig.cs
Extensions/ServiceCollectionExtensions.cs
```

## Quick Reference Files

**Critical Information:**
- `.claude/reference/critical-rules.md`
- `.claude/reference/forbidden-tech.md`
- `.claude/reference/glossary.md`

**Patterns:**
- `.claude/patterns/cqrs-patterns.md`
- `.claude/patterns/api-patterns.md`
- `.claude/patterns/testing-patterns.md`

**Templates:**
- `.claude/reference/templates/`

## Verification

Before marking any task complete: `.claude/checklists/pre-submission.md`
