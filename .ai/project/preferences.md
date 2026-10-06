# Project Development Preferences (CUSTOMIZE THIS)

**Instructions:** Copy this template and customize for your specific project preferences.

**Purpose:** This file defines HOW you prefer to work - your personal workflow, communication style, and development approach.

## Environment

### Builds — memory constraint (IMPORTANT)

**Never run `dotnet build` / `dotnet publish` with MSBuild node reuse enabled.** This machine runs out of physical memory whenever it is left on.

MSBuild's default node reuse keeps a pool of worker processes alive after a build completes (one per core) so the next build starts faster. A single solution publish left **18 MSBuild processes plus a `VBCSCompiler` alive — roughly 3.8 GB resident** — and successive builds multiply that.

- **All three knobs are already set** in `.claude/settings.json` → `env`, so builds run through Claude Code get them automatically — including subagents and hooks:

  | Setting | Kills | Typical footprint |
  |---|---|---|
  | `MSBUILDDISABLENODEREUSE=1` | MSBuild worker nodes | ~18 processes, ~3.5 GB |
  | `DOTNET_CLI_USE_MSBUILD_SERVER=0` | MSBuild server | — |
  | `UseSharedCompilation=false` | `VBCSCompiler` (Roslyn compiler server) | ~430 MB |

  `UseSharedCompilation` works via `env` because MSBuild surfaces environment variables as properties.

- **Verified:** after `dotnet build` on the full solution, process count for `MSBuild` + `VBCSCompiler` + `dotnet` is **0**. Expect the build itself to be slower (~40 s vs ~19 s for an incremental solution build) — that is the cost of not reusing anything.
- When invoking `dotnet` outside the harness (or if the `env` block is ever removed), pass the flags explicitly:
  ```bash
  MSBUILDDISABLENODEREUSE=1 dotnet build <proj> -nodeReuse:false -p:UseSharedCompilation=false
  ```
- Run `dotnet build-server shutdown` after heavy builds. **Caveat:** that shuts down the MSBuild *server* and the compiler server, but it does **not** kill node-reuse *worker* processes — those need `Stop-Process`, or the ~15-minute idle timeout. Killing them is safe once CPU time is flat across two samples, which proves they are idle rather than mid-build.
- **This applies to delegated subagents too.** Any subagent prompt that triggers a .NET build must state this requirement explicitly — several agents each running `dotnet build` is what multiplies the node pools.

## Working Relationship

### Communication Style
- **Formality level:** [Direct and concise / Detailed explanations / etc.]
- **Sycophancy:** [No sycophancy / Be encouraging / etc.]
- **Challenge my thinking:** [Yes / No / Only when critical]
- **Timeline estimates:** [Never include / Always include / Include when asked]
- **Git co-authorship:** [Don't add Claude / Add Claude / etc.]

### Problem-Solving Approach
- **Shortcuts vs. Correct fixes:** [Always correct fix / Quick fixes acceptable for prototypes / etc.]
- **Bug fixing:** [Fix immediately / Create ticket / Ask first]
- **Technical debt:** [Never acceptable / Acceptable with documentation / etc.]
- **Assumption handling:** [Always verify / Ask when uncertain / Proceed with reasonable assumptions]
- **"Good enough" threshold:** [Production-ready only / Prototype-acceptable / etc.]
- **Decision-making:** [User decides all tradeoffs / Agent autonomy for technical details / etc.]

## Development Workflow

### Autonomy Level
- **Agent access:** [Full repository access / Read-only / Specific directories only]
- **Execution model:** [Execute without asking / Ask before major changes / Ask for everything]
- **Progress tracking:** [Real-time automatic updates / Status on request / etc.]

### Documentation Preferences
- **XML docs:** [All public APIs / Public interfaces only / Optional]
- **Code comments:** [For complex logic only / Extensively / Minimal]
- **Architecture docs:** [Mermaid diagrams required / Text only / Optional]
- **README updates:** [With every feature / Major changes only / Manual]

## Code Style

### Language Features
- **Immutability:** [Records preferred / Classes with init / Mixed]
- **Null handling:** [Nullable reference types enabled / Optional / Disabled]
- **Expression-bodied members:** [Use extensively / Use sparingly / Avoid]
- **Pattern matching:** [Use modern C# features / Conservative approach]

### Organization
- **File organization:** [One class per file / Multiple if related / No preference]
- **Namespace structure:** [Match folder structure / Flat / Custom]
- **Using statements:** [Implicit global usings / Explicit / Minimal]

## Review & Quality Gates

### Pre-Submission Requirements
- **Code review:** [Automated checklist / Manual review / Both]
- **Build status:** [0 errors, 0 warnings / 0 errors only / Build succeeds]
- **Test results:** [All pass / Critical pass / Optional]
- **Documentation:** [Complete / API docs only / Optional]

### Quality Metrics
- **Code coverage:** [80%+ / 70%+ / 60%+]
- **Cyclomatic complexity:** [< 10 / < 15 / No limit]
- **Method length:** [< 50 lines / < 100 lines / No limit]

## Session Context Integration

**How this integrates with session-context.md:**

When starting a new session, Claude should:
1. Read this preferences file
2. Apply these preferences to all work
3. Document preference-based decisions in session-context.md
4. Never re-ask questions answered here

---

**Remember:** This file defines your personal working style. For technology choices, see [tech-stack.md](tech-stack.md). For system design, see [architecture.md](architecture.md).
