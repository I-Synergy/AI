# Pi Runtime Instructions

## Available Tools

You have these tools: `read`, `write`, `edit`, `bash`, `grep`, `find`, `ls`.

- Use `read` to examine files (supports images: png, jpg, gif, webp, bmp)
- Use `bash` for shell commands: `dotnet build`, `dotnet test`, git, `rg` (ripgrep) for code search
- Use `edit` for precise changes — keep `oldText` minimal and unique. Merge nearby changes into one edit call.
- Use `write` only for new files or complete rewrites
- Use `grep` and `find` for codebase search, `ls` for directory listing

## Subagent Commands (pi-subagents)

Delegation uses the `subagent` tool from pi-subagents. Available agents live in `.ai/agents/`:

| Command | Use |
|---|---|
| `/run developer "task"` | Code implementation |
| `/run reviewer "task"` | Code review (read-only) |
| `/run architect "task"` | Architecture design |
| `/run tester "task"` | Write/run tests |
| `/run designer "task"` | Visual design |
| `/run ui-developer "task"` | Blazor/MAUI components |
| `/run ui-tester "task"` | Playwright E2E tests |
| `/run writer "task"` | Documentation |

Available chains:
| Command | Use |
|---|---|
| `/run-chain implement-and-review -- task` | Implement → review → fix |
| `/run-chain scout-plan-implement -- task` | Scout → plan → implement → review |

## Skills

Invoke skills with `/skill:name` or let them load automatically. Key skills:
- `dotnet-engineer` — .NET/C#/Blazor/MAUI development
- `code-reviewer` — Code quality and architecture review
- `api-endpoints` — API creation, OpenAPI, Kiota, security
- `database-migration` — EF Core migrations and schemas
- `unit-tester` — MSTest unit tests, Reqnroll BDD
- `playwright-tester` — E2E UI testing, accessibility
- `architect` — System architecture and design
- `security` — Security review and strategy
- `refactor` — Bulk refactoring across solution
- `solution-generator` — Scaffold .NET solutions from architecture

All skills live in `.ai/skills/`.

## After Every Code Change

Run `dotnet build --nologo --verbosity minimal` and read the output. Pi does not auto-build after edits — you must do it yourself.

## Context Files

Pi loads `AGENTS.md` and `CLAUDE.md` from the current directory and parent directories. The `CLAUDE.md` in this project contains the critical coding rules — always follow them.
