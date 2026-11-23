---
name: solution-generator
description: Generates a complete .NET solution scaffold with the template generator (python .ai/scripts/scaffold-solution.py), then adds the feature slices of each bounded context from the architecture document. Use after design-interrogation to turn the architecture document, ubiquitous language, and use cases into a working solution. Trigger whenever the user says "generate the solution", "scaffold the project", "create the solution structure", or wants to turn an architecture document into code.
requires:
  - database-migration
  - gap-review
---

# Solution Generator

Creates a runnable solution from the templates in `.ai/reference/templates/solution/`, then adds the domain slices. The generator owns the shared shape (projects, configuration, client, hosts, tests). This skill owns the part that differs per product: the `Features/{Entities}/` slices and the entities, models, and endpoints behind them.

## Step 1: Run the generator

```
python .ai/scripts/scaffold-solution.py
```

With no flags it prompts for every value. For a scripted run, pass the values as flags and add `--yes` so it never prompts:

```
python .ai/scripts/scaffold-solution.py --name Acme --company "Acme Corp" \
  --application-id com.example.acme --entity Item --entities Items \
  --database sqlserver --with apphost,web,maui,sqlite-device --output ./Acme --yes
```

| Flag | Meaning |
|---|---|
| `--name` | Application name, PascalCase, a valid C# identifier segment. Required with `--yes`. |
| `--company` | Company written to `Directory.Build.props`. Required with `--yes`. |
| `--application-id` | Lower-case reverse DNS identifier of the MAUI head (Android package, Apple bundle, Windows identity). Default `com.example.<name>`. |
| `--entity` / `--entities` | First sample entity, singular and plural, PascalCase. Default `Item` / plural of the entity. |
| `--database` | `sqlserver` (default) or `postgres`. Selects `{Name}.Data.SqlServer` or `{Name}.Data.Postgres`. |
| `--with a,b,c` | Optional heads and stores. Skips the flag prompts. Values: `apphost`, `maui`, `web`, `sqlite-device`. |
| `--output` | Output directory, default `./<name>`. |
| `--yes` | Do not prompt; use defaults for values not given. |
| `--dry-run` | Report what would be created, write nothing. |
| `--force-token KEY=VALUE` | Override `Version`, `Year`, `AppHostHttpsPort`, or `ApiHttpsPort` for reproducible renders. |
| `--check-templates` | Verify the template set against its manifest and token table. Run this after editing any template. |

Existing files are never overwritten. Use an empty output directory.

`worker`, `tests-acceptance`, and `tests-ui` are offered by the script, but their templates do not exist yet. Choosing one prints `templates not available yet` and the flag is treated as not set. Do not promise those projects to the user.

Next steps the script prints (the repository's build rules apply to any build you run from it, see `.ai/project/preferences.md`):

```
dotnet tool restore
dotnet restore
dotnet build -nodeReuse:false
dotnet test
dotnet ef migrations add Initial --project src/{Name}.Data.SqlServer --startup-project src/{Name}.Service.Api
```

## Step 2: What the generator produces

Projects are flat under `src/` and `tests/`. Each name is `{Name}.{Layer}`:

| Project | Role |
|---|---|
| `{Name}.Common` | Shared constants, enumerations (`{Entity}Status` and any other shared enum), `HttpClientSettings`, `AspireNames` |
| `{Name}.Resources` | Localised strings (`.resx` and the generated `Properties.Resources`) |
| `{Name}.Entities` | EF Core entities and their `IEntityTypeConfiguration<T>` classes, one file each |
| `{Name}.Models` | Read models and `Create{Entity}Request` / `Update{Entity}Request` bodies |
| `{Name}.Data` | `IDataContext` abstraction shared by the handlers |
| `{Name}.Data.SqlServer` or `{Name}.Data.Postgres` | Provider `DataContext`, design-time `DataContextFactory`, `DatabaseInitializer` |
| `{Name}.Domains` | `Features/{Entities}/{Commands,Queries}/{Operation}/` slices, `ResourceNotFoundException`, `With{Name}DomainHandlers` registration |
| `{Name}.Services` | The endpoints library: `Endpoints/{Entities}Endpoints.cs` and validation extensions |
| `{Name}.Service.Api` | The API host (`Program.cs`), health checks, database check, `Program.Partial.cs` |
| `{Name}.Clients` | Kiota client in `Api/`, regenerated from the API's OpenAPI document on a Debug build |
| `{Name}.AppHost` | Aspire host (`apphost`) |
| `{Name}.App.Shared` | Shared layer for the heads: `I{Name}ApiService` abstraction, `HostApplicationBuilderExtensions`, settings models (`maui`, `web`, or `sqlite-device`) |
| `{Name}.App` | MAUI head (`maui`) |
| `{Name}.App.Web` | Blazor web head, plain Razor (`web`) |
| `{Name}.Data.Sqlite` | Device-local SQLite store (`sqlite-device`) |
| `{Name}.Domains.Tests`, `{Name}.Service.Tests`, `{Name}.Data.{Provider}.Tests` | Test projects by layer, on a real EF Core provider |

The sample `Item` slice that the generator writes (read it, do not invent a second shape):

- `Domains/Features/Items/Commands/CreateItem/` holds `CreateItemCommand`, `CreateItemCommandHandler`, `CreateItemResponse`. Update and Delete follow the same shape.
- `Domains/Features/Items/Queries/GetItemById/` and `GetItemsList/` hold the query, handler, and response.
- `Services/Endpoints/ItemsEndpoints.cs` maps the group. It catches `ResourceNotFoundException` as 404 and any other `InvalidOperationException` as a validation problem.

## Step 3: Add the bounded context's slices

The generator writes one sample entity. Replace it with the bounded context from the architecture document. Work through the use cases in `docs/bounded-contexts/{Domain}/use-cases.md`, one slice per use case main flow:

1. **Entities.** One class per aggregate root in `{Name}.Entities/{Entity}.cs`, with a matching `{Entity}Configuration.cs` in the same project. Use enum types for status properties, not `int`.
2. **Enums.** Put every enum in `{Name}.Common/Enumerations/`, plural name unless it ends in `Status`. Pin the values (`= 0, = 1`) when they are persisted.
3. **Models.** Read model in `{Name}.Models/{Entity}.cs`. Request bodies carry Data Annotations (`Create{Entity}Request`, `Update{Entity}Request`). No `Dto` suffix.
4. **Slices.** For each use case, create `Features/{Entities}/Commands/{Operation}{Entity}/` or `Queries/{Operation}{Entities}/` with its command or query, handler, and response, one type per file. Command parameters are individual values, never a model object.
5. **Data set.** Add the `DbSet` property to `DataContext` in the provider project, and apply the configuration with `ApplyConfigurationsFromAssembly` (already in the generated context).
6. **Endpoints.** Add the operation to `{Name}.Services/Endpoints/{Entities}Endpoints.cs`. Declare every status code with `.Produces` and `.ProducesValidationProblem()`. Add `.WithValidation<T>()` to POST and PUT routes.
7. **Migration.** Generate the first migration once the entities settle (see `database-migration`).
8. **Tests.** One test class per handler under `tests/{Name}.Domains.Tests/Handlers/{Entities}/`, and one endpoint test class under `tests/{Name}.Service.Tests/`.

The handler, endpoint, and entity conventions are in `.ai/patterns/cqrs-patterns.md`, `.ai/patterns/api-patterns.md`, and `.ai/patterns/testing-patterns.md`. Do not restate them here.

## Step 4: Traceability in test stubs

Generate every test stub with the identifiers the slice carries, so the traceability validator stays green:

- A `// Traces: US-{Domain}-{NNN} / AC-{Domain}-{NNN}.{n}, AC-{Domain}-{NNN}.{m}` line directly below the file's header comment.
- Exactly one `[TestCategory("AC-{Domain}-{NNN}.{n}")]` on each test method that is evidence for a criterion, with `[TestMethod]` written first.
- At least one test method per acceptance criterion the slice's `source` references. Read `source.acceptance_criteria`, or the criteria of `source.user_stories` when that key is omitted.
- Use the shape in `.ai/reference/templates/test-class.cs.txt`. The identifier rules are in `.ai/reference/traceability.md`.
- A slice whose `source` is absent or unlabelled is in legacy mode. Generate the stub without an identifier rather than inventing one.

## Step 5: Verify

- Run `python .ai/scripts/scaffold-solution.py --check-templates` if you changed a template.
- Build and run the tests in the generated solution (`dotnet build -nodeReuse:false`, `dotnet test`).
- Run `gap-review` to check the generated solution against the architecture document and the session decisions.
