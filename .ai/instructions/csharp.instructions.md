---
description: "C# rules for .NET source files: CQRS, EF Core, API and naming conventions"
applyTo: "**/*.cs"
---

The critical rules in `.ai/reference/critical-rules.md` apply to every C# file. AGENTS.md repeats the most important ones. Read the rule file before writing or reviewing code; do not rely on memory.

- Patterns: `.ai/patterns/cqrs-patterns.md` (commands, queries, handlers) and `.ai/patterns/api-patterns.md` (endpoints, OpenAPI, validation).
- Forbidden libraries and their replacements: `.ai/reference/forbidden-tech.md`.
- Starting points for new types: `.ai/reference/templates/` (command handler, query handler, endpoint).
- Before reporting work as done, verify against `.ai/checklists/pre-submission.md`.
