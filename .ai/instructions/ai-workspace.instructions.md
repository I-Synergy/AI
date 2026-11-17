---
description: "Session workspace files: progress tracking, plans, completed work and session handoff"
applyTo: ".ai/progress/**,.ai/plans/**,.ai/completed/**,.ai/session-context.md"
---

These files record the state of the work. Follow the cycle in AGENTS.md: read first, track progress, hand off at the end.

- Plans live in `.ai/plans/{task-slug}.md`. Never save plans to `docs/plans/`.
- Progress files live in `.ai/progress/{task-slug}.md`. Use the format in AGENTS.md (Status, Started, Steps, Notes).
- Change a progress step only with Edit, one line at a time (`- [ ]` to `- [x]`). Never rewrite the whole file with Write.
- When a task is done, set `**Status:** DONE` and move the file to `.ai/completed/`.
- Handoffs use `.ai/reference/templates/session-handoff.md.txt`. Update sections in place and never overwrite another client's entries.
