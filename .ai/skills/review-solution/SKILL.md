---
name: review-solution
description: >-
  Reviews an existing repository against this template and reports what to fix, in one pass: whether the AI setup is installed, whether the docs match the code, which Critical Coding Rules the code breaks, and how far the project structure is from the reference solution. Read-only by default; it installs the template or migrates structure only when you ask it to. Use when the user says "review this repo against the template", "audit my existing project", "can I use this template on my existing repo", "check my project against the rules", "review-solution", or wants one prioritised list of gaps for a repository that was not generated from this template.
requires:
  - verify-config
  - gap-review
  - code-reviewer
---

# Review Solution

This skill answers one question for a repository that was **not** generated from this template:
*what would I have to change to make it follow the template, and what is actually worth changing?*

It is a review, not a migration. Every step below is read-only unless it is marked **write**, and
the writes only happen after you show the user the change and they approve it.

## Why the steps are in this order

The template's own skills each assume something that an arbitrary repository may not have yet:

- `verify-config` audits `AGENTS.md` and `.ai/` against the codebase. It cannot run if `.ai/` is absent.
- `gap-review` compares a solution with an architecture document and a decision log. A repository
  that predates the template usually has neither, so only part of it applies.
- `code-reviewer` checks the Critical Coding Rules. It works on any C# code, and it is where most
  real findings come from.
- `scaffold-solution.py` renders a *new* tree and never overwrites an existing file, so it is a
  reference implementation to compare against, never a migration tool.

So the review runs in this order: inventory, install state, reference render, rule audit, structure
delta, report, then — only on request — the fixes.

## Step 1: Inventory (read-only)

Establish what you are reviewing before judging it.

```bash
git -C <repo> status --short            # uncommitted work changes what "current" means
git -C <repo> log --oneline -5
```

Record, in the report's *Scope* section:

| What | How to find it |
|---|---|
| Solution files | `*.sln`, `*.slnx` at the root or one level down |
| Projects | every `*.csproj` / `*.fsproj`, grouped by folder |
| Target frameworks | `<TargetFramework(s)>` in each project |
| Test framework | package references: `MSTest.*`, `xunit*`, `NUnit*` |
| Data access | `Microsoft.EntityFrameworkCore.*`, `Dapper`, repository interfaces |
| Template state | does `.ai/` exist; does `AGENTS.md` exist; is `.ai/session-context.md` the unfilled placeholder |
| Documents `gap-review` needs | `docs/architecture/*`, `docs/session-decisions.md`, `UBIQUITOUS_LANGUAGE.md`, `docs/bounded-contexts/*/use-cases.md` |

Do not stop to fix anything you notice here. The inventory exists so the later steps can say
*"this repository has X, so rule Y applies / does not apply"* instead of guessing.

**Scope the audit to the repository's own code.** C# that ships inside `.ai/skills/` or
`.ai/reference/templates/` is sample or template material, not the project's code; auditing it
reports findings the user cannot act on. When the repository has no solution or project file, say
that the rule audit found no application code and stop at the report — do not fall back to the
skill samples.

## Step 2: Install state (read-only)

Decide which of three situations you are in, because it changes everything downstream:

1. **No `.ai/` directory.** The template is not installed. Steps 3–5 still run (the reference
   render and the rule audit do not need `.ai/`), but `verify-config` and most skills are
   unavailable. Offer `upgrade-template` as the fix, and say plainly that it is a write.
2. **`.ai/` present but stale.** Compare the target's `.ai/reference/critical-rules.md` and
   `.ai/skills/` against the template's. A stale copy means the rule audit may quote rules the
   project has never seen.
3. **`.ai/` present and current.** Run `verify-config` as written, and fold its report into this one
   rather than repeating it.

When the template is present, also run the template's own validators against the target — they are
cheap and they find configuration drift the prose cannot. Run them from the target's root, and invoke
the shell suites with `bash` directly: `python` on a `.sh` file fails before the `||` fallback runs.

```bash
bash .ai/tests/validate-structure.sh
python .ai/tests/validate-skills.py
bash .ai/tests/validate-references.sh
python .ai/tests/validate-copilot.py
```

Report a failing validator as its own finding with the exact command and the failing line; do not
paraphrase it.

## Step 3: Reference render (read-only, outside the repository)

Render the template's solution once so the structure delta has something concrete to compare with.
Keep it **outside the repository** so it never lands in `git status`:

```bash
python .ai/scripts/scaffold-solution.py \
  --name Reference --company "Reference Corp" \
  --entity Item --entities Items --database sqlserver \
  --with apphost,web,maui,sqlite-device \
  --output <temp-dir>/reference-solution --yes
```

If the repository has no `.ai/scripts/scaffold-solution.py` (situation 1), render from a checkout of
the template instead. If the repository is not a .NET solution at all, say so and skip this step and
step 5; the rule audit in step 4 still applies wherever C# exists.

The render is a *reference*, not a target: a repository that deliberately uses a different layout
(for example one project per bounded context) is not wrong, it is different. Record which
differences are deliberate in the report's *Accepted deviations* section rather than in the gaps.

## Step 4: Rule audit (read-only)

This is the core of the review. Work rule by rule from `.ai/reference/critical-rules.md`, and for
each rule look only at the code that the rule governs. Use the table below to decide what is
checkable in this repository; a rule whose subject does not exist is *not applicable*, not *passing*.

| Rule | What to look at | Not applicable when |
|---|---|---|
| 1 Commands take individual parameters | every `record …Command(` and its constructor call sites | no commands |
| 2–4 Data access on the context | handlers: `DbSet` use, `.Update(`, `FirstOrDefaultAsync` + `Remove` | no handlers |
| 5 `CancellationToken` | every `async` method in `src/` | no async code |
| 6 Entities never returned | handler return types and response records | no handlers |
| 9 Handler suffixes | class names implementing `ICommandHandler` / `IQueryHandler` | no CQRS |
| 10 One type per file | files with more than one top-level type | never |
| 11 Enum naming | `enum` declarations | no enums |
| 12 Enum properties, not `int` | entity properties | no entities |
| 13/14 Common project, Entities ≠ Models | project references | no layered projects |
| 15 Plans in `.ai/plans/` | stray `docs/plans/` | never |
| 18 `Produces` metadata | every `MapGet`/`MapPost`/… chain | no endpoints |
| 19–21 OpenAPI, Kiota, client | API project, client project, `HttpClient` use in heads | no API |
| 22 Validation | POST/PUT routes and request models | no write routes |
| 23 Rate limiting, HTTPS | `Program.cs` of the host | no host |
| 26 No secrets | `appsettings*.json`, `.env`, connection strings, keys | never |
| 27 Interfaces in `Abstractions/` | every interface and its consumers | no interfaces |
| 28 No `Dto` suffix | type and file names | never |
| 29 Central package management | `Directory.Packages.props`, `PackageReference Version=` | no NuGet |
| 30 Heads and sharing | UI projects and their references | no UI |
| 31 Test layering | test projects, `Assert.Throws`, mocked contexts, xUnit/NUnit | no tests |

Delegate the mechanical part to the `code-reviewer` agent when it is available, and give it the rule
list above plus the inventory; it returns findings in the quality-model format. Do not ask it to
review the whole repository — ask it for the rules that apply, or it will return a style review
instead of a rule audit.

Every finding carries one severity from `.ai/reference/quality-model.md`:

- **Blocker** — correctness, security, or the build is broken.
- **Major** — a Critical Coding Rule is violated, or a defect is latent under conditions the design
  already anticipates.
- **Minor** — correct today, measurably more expensive later.

A finding without a file and line is not a finding. If you cannot point at the code, leave it out.

## Step 5: Structure delta (read-only)

Compare the repository's projects and folders with the reference render from step 3. Report only
differences that cost something — a missing `Clients` project when heads call the API with
`HttpClient`, CQRS folders scattered across projects when the template puts them in
`Domains/Features/{Entities}/`, tests that mock the context when the template uses a real provider.
A different but coherent layout is an accepted deviation, not a gap.

If the repository has the documents `gap-review` needs, run `gap-review` here and fold its
dimensions 2 (domain model) and 5 (decision traceability) into the report. If it does not, say so
once, in the report, and move on — do not invent an architecture document to review against.

## Step 6: Report (the deliverable)

Write the report to `.ai/analysis/review-<repo-name>-<date>.md` when the repository has `.ai/`;
otherwise print it and offer to save it. Use exactly this structure:

```markdown
# Solution Review — {repo} — {date}

## Scope
- Reviewed: {commit} ({branch}), {N} projects, {frameworks}
- Template state: {not installed | stale | current}
- Not applicable: {rules and steps that had no subject in this repository}

## Summary
| Severity | Findings |
|---|---|
| Blocker | {n} |
| Major | {n} |
| Minor | {n} |

## Findings
| # | Sev | Rule / area | Location | What is wrong | Minimal fix |
|---|---|---|---|---|---|
| 1 | Major | Rule 1 | `src/…/CreateOrderCommand.cs:12` | command takes the `Order` model | pass the individual fields |

## Accepted deviations
- {layout or technology choices that differ from the template on purpose, and why}

## Fix sequence
1. {the order that keeps the build green after each step}
```

Order the findings by severity, then by the cost of the fix. The *Fix sequence* is the part the user
will act on: group the fixes so that each step compiles and the tests pass before the next begins.

## Step 7: Fixes (write — only on request)

Never start these unless the user asks. Offer them as a numbered menu, and do them one at a time,
running the build and tests after each.

1. **Install or refresh the template** — `upgrade-template --dry-run` first, show the summary, then
   apply. Project-owned paths are never touched.
2. **Fix rule violations** — delegate to `developer` in batches that share a file or a rule, so one
   review covers the change.
3. **Migrate the structure** — move one feature at a time toward `Domains/Features/{Entities}/`,
   `Services`, `Service.Api`, `Clients`, using the reference render as the shape. Update the solution
   file and project references in the same change, and build after each move.
4. **Re-run this review** — the report is the acceptance test; the second run should show the
   findings you fixed gone and no new ones.

## Example

Input: *"can I use this template on my existing repo?"* for a repository with three projects, no
`.ai/`, xUnit tests, and endpoints that return entities.

Output (abridged):

```markdown
## Scope
- Reviewed: a1b2c3d (main), 3 projects, net8.0
- Template state: not installed
- Not applicable: Rules 19–21 (no API project or client), 23 (no host), 30 (no UI)

## Summary
| Severity | Findings |
|---|---|
| Blocker | 1 |
| Major | 3 |
| Minor | 0 |

## Findings
| # | Sev | Rule / area | Location | What is wrong | Minimal fix |
|---|---|---|---|---|---|
| 1 | Blocker | Rule 26 | `appsettings.json:7` | a live SQL password is committed | move it to user secrets and rotate it |
| 2 | Major | Rule 6 | `OrdersController.cs:41` | the endpoint returns the `Order` entity | map to a response record |
| 3 | Major | Rule 31 | `OrdersTests.cs:12` | xUnit and a mocked context | MSTest on the in-memory provider |
| 4 | Major | Rule 10 | `Order.cs` | entity and configuration in one file | split into `Order.cs` and `OrderConfiguration.cs` |

## Fix sequence
1. Rotate the credential and remove it from source (finding 1).
2. Split the entity from its configuration (4) — mechanical, no behaviour change.
3. Map the response (2) and add `.Produces(...)` to the routes.
4. Port the tests (3) last, so they cover the code after steps 2–3.
```

## Boundaries

- This skill reviews; it does not decide architecture. A layout that differs deliberately goes in
  *Accepted deviations*, and a change that would alter a documented decision goes to `council`.
- It never runs `scaffold-solution.py` against the repository. The render always goes to a temporary
  directory outside it.
- It reports what the template's rules say, not what the reviewer prefers. A finding the user would
  not act on is not a finding.
