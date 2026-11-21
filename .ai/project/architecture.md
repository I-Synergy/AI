# Project Architecture (CUSTOMIZE THIS)

**Instructions:** The scaffold fixes the solution shape: one flat set of projects per solution, CQRS slices inside `{ApplicationName}.Domains`, and a generated Kiota client. Sections that describe that shape are filled in. Sections marked `[CUSTOMIZE]` are project decisions that the scaffold does not make.

**Purpose:** This file defines HOW your system is structured: layers, project dependencies, data flow and the decisions behind them.

**Source of truth for the layout:** `.ai/scripts/scaffold-solution.py` and `.ai/reference/templates/solution/` (the manifest decides which project and file exists for which option).

## Architecture Style

**Primary Architecture:** Layered, with CQRS vertical slices inside one `Domains` project. A solution has one flat set of projects; there are no per-bounded-context projects.

**Why Chosen:** [CUSTOMIZE: the reasoning behind the layering for this product]

## Architectural Patterns

| Pattern | Used? | Notes |
|---------|-------|-------|
| **Clean Architecture** | Partial | Dependencies point inward to `Common`, `Entities` and `Models`. There is no separate Application project: `Services` (endpoints) and `Domains` (handlers) play that role. |
| **CQRS** | Yes | Commands change state and return a response; queries read. Handlers are `ICommandHandler` and `IQueryHandler` from `ISynergy.Framework.CQRS`. |
| **DDD** | No | Entities are POCOs with no behaviour. No aggregates or value objects are scaffolded. [CUSTOMIZE: add if the domain needs them] |
| **Vertical Slices** | Yes | `Domains/Features/{Entities}/{Commands,Queries}/{Operation}/`, one folder per operation. |
| **Event Sourcing** | No | [CUSTOMIZE] |
| **Microservices** | No | One API host (`Service.Api`). The heads are clients of that host. |

## Clean Architecture Layers

**Layer definitions and dependencies:**

```
Clients and heads     App, App.Web, App.Shared, Clients (Kiota), AppHost
        ↓ call the API over HTTP, through the generated client
API host              Service.Api  →  Services (endpoints)
        ↓
Use cases             Domains (CQRS handlers, Features/{Entities}/)
        ↓
Core model            Entities, Models, Data (IDataContext)  →  Common  →  Resources
        ↑ implemented by
Persistence           Data.SqlServer | Data.Postgres  (DataContext, migrations)
```

**Layer mapping to projects:**

- **Shared kernel:** `{ApplicationName}.Common` (constants, enumerations, converters, factories, `HttpClientSettings`) and `{ApplicationName}.Resources` (`Resources.resx`).
- **Core model:** `{ApplicationName}.Entities` (persisted POCOs and their `IEntityTypeConfiguration`), `{ApplicationName}.Models` (read models and request records), `{ApplicationName}.Data` (`Abstractions/IDataContext.cs`).
- **Persistence:** `{ApplicationName}.Data.SqlServer` or `{ApplicationName}.Data.Postgres` (the `DataContext`, the design-time factory, `Initializers/`, and `Migrations/` once the user generates them). `{ApplicationName}.Data.Sqlite` is the device store for the MAUI head (optional).
- **Use cases:** `{ApplicationName}.Domains` (commands, queries and their handlers).
- **API:** `{ApplicationName}.Services` (the `{Entities}Endpoints` library) and `{ApplicationName}.Service.Api` (the host and `Program.cs`).
- **Clients and heads:** `{ApplicationName}.Clients` (Kiota client), `{ApplicationName}.App.Shared` (shared services), `{ApplicationName}.App.Web` (Blazor), `{ApplicationName}.App` (MAUI).
- **Orchestration:** `{ApplicationName}.AppHost` (Aspire).

### Dependency matrix

Direct `ProjectReference`s of the rendered sample with SQL Server, AppHost, the web head, the device store and the MAUI head. The Postgres render has the same graph with `Data.Postgres` in place of `Data.SqlServer`.

| Project | Direct references | Notes |
|---------|-------------------|-------|
| `Resources` | none | Default namespace `{ApplicationName}.Resources`. |
| `Common` | `Resources` | Leaf of the solution. Nothing else it references is a project. |
| `Entities` | `Common` | POCOs and `IEntityTypeConfiguration`. Never references `Models`. |
| `Models` | `Common` | Never references `Entities`. Shared types go to `Common`. |
| `Data` | `Entities` | `IDataContext` exposes `DbSet<Item>`, so it sees the entities. |
| `Data.SqlServer` / `Data.Postgres` | `Data` | Provider package and the concrete `DataContext`. |
| `Data.Sqlite` | `App.Shared` | Device store implements `ISqliteLocalDataService`. |
| `Domains` | `Entities`, `Models`, `Data.{Provider}` | Handlers depend on `IDataContext` only. The provider reference lets composition and tests construct the concrete context. |
| `Services` | `Domains`, `Models` | Endpoints call handlers through `ICommandHandler` and `IQueryHandler`. No direct `Data` reference. |
| `Service.Api` | `Services` | Host. Registers `DataContext` as `IDataContext`. |
| `Clients` | `Service.Api` with `ReferenceOutputAssembly="false"` | Build order only. The API's Debug build regenerates `Api/` before this project compiles. No assembly dependency. |
| `App.Shared` | `Clients` (`PrivateAssets="compile"`), `Common`, `Models` | The Kiota types stay out of the heads' compile graph. |
| `App.Web` | `App.Shared` | Blazor head. |
| `App` | `App.Shared`, `Data.Sqlite` | MAUI head. |
| `AppHost` | `Common` (`IsAspireProjectResource="false"`), `Service.Api`, `App.Web` | The MAUI head is started with `AddMauiProject` by path, not by `ProjectReference`. |

Test projects reference the layer they test, and nothing above it:

| Test project | Direct references |
|--------------|-------------------|
| `Domains.Tests` | `Common`, `Domains`, `Entities`, `Models`, `Data.{Provider}` |
| `Service.Tests` | `Service.Api`, `Data.{Provider}` |
| `Data.{Provider}.Tests` | `Common`, `Entities`, `Data.{Provider}` |

**Rules the matrix enforces:**

1. `Entities` and `Models` never reference each other. Both reference `Common`. A type needed by both moves to `Common` (rule 9 in `AGENTS.md`).
2. Handlers depend on `IDataContext`, never on the concrete `DataContext`.
3. `Services` never references `Data`. Persistence reaches the API only through `Domains`.
4. Heads never reference `Clients`. They reach the API through `App.Shared`.
5. The graph is acyclic. `Clients` depends on `Service.Api` for build order only, so it does not close a cycle.

## Project Structure

The rendered sample (SQL Server, AppHost, web, device store, MAUI). Options remove the matching projects and folders.

```
Acme.slnx                                   # Acme.NoMaui.slnx without the MAUI head
Directory.Build.props                       # LangVersion, company, version stamp, shared NoWarn
Directory.Packages.props                    # every package version (central management)
global.json  nuget.config  aspire.config.json
.config/dotnet-tools.json                   # Kiota (rollForward false), dotnet-ef
openapi/Acme.Service.Api.json               # written by the API's Debug build
src/
├── Acme.AppHost/                           # Aspire orchestration
├── Acme.Common/                            # Constants/, Converters/, Enumerations/, Factories/, Models/
├── Acme.Resources/                         # Properties/Resources.resx
├── Acme.Entities/                          # Item.cs, ItemConfiguration.cs
├── Acme.Models/                            # Item.cs (BaseModel), CreateItemRequest.cs, UpdateItemRequest.cs
├── Acme.Data/                              # Abstractions/IDataContext.cs
├── Acme.Data.SqlServer/                    # DataContext.cs, DataContextFactory.cs, Initializers/ (Migrations/ generated by the user)
├── Acme.Data.Sqlite/                       # device store: LocalDataContext, Entities/, Services/
├── Acme.Domains/                           # Extensions/, Features/Items/{Commands,Queries}/, ResourceNotFoundException.cs
├── Acme.Services/                          # Endpoints/ItemsEndpoints.cs, Extensions/ValidationExtensions.cs
├── Acme.Service.Api/                       # Program.cs, Program.Partial.cs, Extensions/, HealthChecks/
├── Acme.Clients/                           # Api/ (Kiota output, committed)
├── Acme.App.Shared/                        # Abstractions/, Extensions/, Models/, Services/
├── Acme.App.Web/                           # Blazor: App.razor, Routes.razor, Layouts/, Pages/Items/, Components/
└── Acme.App/                               # MAUI: MauiProgram.cs, Platforms/, Views/, ViewModels/
tests/
├── Acme.Domains.Tests/                     # handlers against the in-memory provider
├── Acme.Service.Tests/                     # Service.Api through WebApplicationFactory
├── Acme.Data.SqlServer.Tests/              # model and migrations-history checks, offline
├── Acme.AcceptanceTests/                   # optional (Reqnroll)
└── Acme.UI.Tests/                          # optional (Playwright)
```

Project folder names are `{ApplicationName}.{Name}`. `Domains` is always plural, and `Service.Api` is the one singular host name.

## Interface Placement (Abstractions)

Interfaces live in an `Abstractions/` folder in the **highest project that both their consumers and their implementation already depend on**. They are not placed in the implementing project, and not automatically in `Common`.

```
// CORRECT — Domains (consumer) and Data.SqlServer (implementation) both reach Data
src/
├── Acme.Data/
│   └── Abstractions/
│       └── IDataContext.cs                   # namespace Acme.Data.Abstractions
├── Acme.Data.SqlServer/
│   └── DataContext.cs                        # implements IDataContext
└── Acme.Domains/
    └── Features/Items/Commands/CreateItem/
        └── CreateItemCommandHandler.cs       # takes IDataContext

// WRONG — the abstraction buried in the implementation project
src/Acme.Data.SqlServer/IDataContext.cs
```

The same rule places `IAcmeApiService` in `Acme.App.Shared/Abstractions/Services/`. Both heads consume it and `App.Shared` implements it, so the heads depend on the abstraction alone.

Exception: an interface used only inside a single implementation, with no consumer, stays beside that implementation and is `internal`. Full rule: `.ai/reference/critical-rules.md` rule 27.

## CQRS Implementation Pattern

**Command/Query structure (abridged from the rendered `Items` sample; the sample also logs and checks the affected row count):**

```csharp
// Commands take individual parameters, never a model object
public sealed record CreateItemCommand(
    string Name,
    string? Description) : ICommand<CreateItemResponse>;

// Queries carry the identifier they need
public sealed record GetItemByIdQuery(Guid ItemId) : IQuery<GetItemByIdResponse>;

// Handlers take IDataContext and ILogger; they map to models before returning
public sealed class CreateItemCommandHandler(
    IDataContext dataContext,
    ILogger<CreateItemCommandHandler> logger)
    : ICommandHandler<CreateItemCommand, CreateItemResponse>
{
    public async Task<CreateItemResponse> HandleAsync(
        CreateItemCommand command,
        CancellationToken cancellationToken = default)
    {
        var entity = new Entities.Item { ItemId = Guid.NewGuid(), Name = command.Name, Description = command.Description };
        dataContext.Items.Add(entity);
        await dataContext.SaveChangesAsync(cancellationToken);
        return new CreateItemResponse(entity.ItemId);
    }
}
```

**Failure signalling:**

- A command or query that targets a missing row throws `ResourceNotFoundException` (in `Domains`). The endpoint maps it to 404. It derives from `InvalidOperationException`, so `catch` blocks that expect the base type still work, and the endpoint catches it first.
- Any other `InvalidOperationException` from a handler is a refusal. The endpoint answers it as a validation problem (400).
- The `Get{Entity}ById` query returns a nullable response instead of throwing. The endpoint maps a null item to 404.

## Data Access Pattern

**NO explicit Repository interfaces.** Handlers use EF Core primitives on the named DbSet properties of `IDataContext`:

```csharp
// Create
var entity = new Entities.{Entity} { {Entity}Id = Guid.NewGuid(), /* properties */ };
dataContext.{Entities}.Add(entity);
await dataContext.SaveChangesAsync(cancellationToken);

// Read single — project straight to the model when no entity is needed outside the handler
var model = await dataContext.{Entities}
    .Where(e => e.{Entity}Id == query.{Entity}Id)
    .Select(e => new Models.{Entity}(/* map e to the model */))
    .FirstOrDefaultAsync(cancellationToken);

// Read list
var models = await dataContext.{Entities}
    .OrderBy(e => e.Name)
    .Select(e => new Models.{Entity}(/* map e to the model */))
    .ToListAsync(cancellationToken);

// Update — change tracker detects mutations on tracked entities; no Update() call
var entity = await dataContext.{Entities}.FirstOrDefaultAsync(e => e.{Entity}Id == command.{Entity}Id, cancellationToken);
entity.Name = command.Name;
await dataContext.SaveChangesAsync(cancellationToken);

// Delete
var entity = await dataContext.{Entities}.FirstOrDefaultAsync(e => e.{Entity}Id == command.{Entity}Id, cancellationToken);
dataContext.{Entities}.Remove(entity);
await dataContext.SaveChangesAsync(cancellationToken);
```

## Vertical Slice Organization

The feature folder is **plural** (`Features/{Entities}/`). Operation folders and types use the **singular** entity name:

```
src/{ApplicationName}.Domains/
  Features/{Entities}/
    Commands/
      Create{Entity}/
        Create{Entity}Command.cs
        Create{Entity}CommandHandler.cs
        Create{Entity}Response.cs
      Update{Entity}/      Update{Entity}Command.cs, Update{Entity}CommandHandler.cs, Update{Entity}Response.cs
      Delete{Entity}/      Delete{Entity}Command.cs, Delete{Entity}CommandHandler.cs, Delete{Entity}Response.cs
    Queries/
      Get{Entity}ById/     Get{Entity}ByIdQuery.cs, Get{Entity}ByIdQueryHandler.cs, Get{Entity}ByIdResponse.cs
      Get{Entities}List/   Get{Entities}ListQuery.cs, Get{Entities}ListQueryHandler.cs, Get{Entities}ListResponse.cs
  Extensions/ServiceCollectionExtensions.cs
  ResourceNotFoundException.cs
```

Namespaces follow the folders: `Acme.Domains.Features.Items.Commands.CreateItem`. The plural folder keeps the feature namespace apart from the `Item` entity (`Acme.Entities.Item`) and the `Item` model (`Acme.Models.Item`). Events are not scaffolded. [CUSTOMIZE: add `Features/{Entities}/Events/` when a feature needs them]

## Data Flow

### Request Flow

```
HTTP request
  → Service.Api (rate limiter, health, OpenAPI, versioning)
  → Services: {Entities}Endpoints (route, WithValidation<TRequest>, Results<...>)
  → Domains: ICommandHandler / IQueryHandler
  → IDataContext (DbSet<Entity>, SaveChangesAsync)
  → Data.SqlServer or Data.Postgres DataContext
  → Database
  ← Model or Response, mapped by the handler
  ← TypedResults (201, 200, 204, 400, 404)
```

### Heads Request Flow

```
Blazor page or MAUI view model
  → App.Shared I{Name}ApiService
  → {Name}ApiService maps client models to app models
  → Clients ApiClient (Kiota, typed)
  → HTTP to Service.Api
```

### Event Flow (if using domain events)

[CUSTOMIZE: not scaffolded]

**Service registration (the scaffold's pattern):**

```csharp
// Domains/Extensions/ServiceCollectionExtensions.cs
public static IServiceCollection With{ApplicationName}DomainHandlers(this IServiceCollection services)
{
    var assembly = typeof(ServiceCollectionExtensions).Assembly;
    services.AddCQRS().AddHandlers(assembly);
    return services;
}

// Service.Api/Program.cs
builder.Services
    .AddScoped<IDataContext>(services => services.GetRequiredService<DataContext>())
    .With{ApplicationName}DomainHandlers();

// Service.Api/Program.cs, after the pipeline is built
app.Map{Entities}Endpoints();
```

Each entity gets one endpoints class, `Services/Endpoints/{Entities}Endpoints.cs`, with `Map{Entities}Endpoints(this IEndpointRouteBuilder app)`. It returns the route builder so calls can be chained.

## Hosts, Clients and Orchestration

### Endpoints and the API host

- The `Services` project holds endpoint groups. The `Service.Api` host composes them. Route groups use `MapGroup("/{entities}")`, `WithTags`, an API version set, and `RequireRateLimiting(RateLimits.Api)`.
- The API is **anonymous by default**. Routes do not declare `401`. Authentication is an opt-in module. [CUSTOMIZE: the authentication model]
- Every route declares its responses with `.Produces` and `.ProducesValidationProblem()`. Rate-limited routes also declare `429`.
- Request bodies are the `Models` request records (`Create{Entity}Request`, `Update{Entity}Request`), validated by `.WithValidation<T>()` (`Services/Extensions/ValidationExtensions.cs`).
- The OpenAPI document has three transformers: the document transformer sets the server URL, the schema transformer maps .NET types to JSON schema types, and an operation transformer declares the `api-version` query parameter.

### Kiota client flow

```
Debug build of Service.Api
  1. GenerateOpenApiDocuments writes openapi/Acme.Service.Api.json
  2. Target OpenAPI (after step 1, Debug only) runs dotnet kiota generate
       → src/Acme.Clients/Api/   (namespace Acme.Clients.Api, class ApiClient)
  3. Clients builds: target IncludeGeneratedApiClient reads Api/*.cs with Directory.GetFiles
  4. App.Shared maps Acme.Clients.Api.Models.* to Acme.Models.*, and registers
     the client through Add{ApplicationName}ApiServices (named HttpClient, service discovery,
     anonymous authentication provider, scoped ApiClient)
```

- The `Api/` folder ships in the template as Kiota output for the sample entity, tokenised. A fresh render compiles in Debug and Release with no generator run.
- The generator version is pinned in `.config/dotnet-tools.json` with `rollForward: false`.
- Opt-out: `-p:AcmeGenerateApiClient=false` (the property is `{ApplicationName}GenerateApiClient`) skips regeneration. Use it in CI and in test runs that must not rewrite committed files.
- Known limitation: Kiota sorts members alphabetically, so the first Debug build can reorder generated members for an entity whose names sort differently from `Item`. The code is equivalent.

### MAUI and Blazor sharing

| Project | Role | What it holds |
|---------|------|---------------|
| `App.Shared` (RootNamespace `{ApplicationName}`) | Shared by both heads | `I{ApplicationName}ApiService` and its implementation, the client registration, settings models, `CommonServices`, `ExceptionHandlerService` |
| `App.Web` | Blazor head (plain Razor, no component library) | `App.razor`, `Routes.razor`, `Layouts/`, `Pages/{Entities}/`, `Components/`, `HealthChecks/ApiHealthCheck.cs` |
| `App` | MAUI head | `MauiProgram.cs`, `Platforms/`, `Views/`, `ViewModels/`, `Resources/` (styles), platform manifests |
| `Data.Sqlite` | Device store (optional, `sqlite-device`) | `LocalDataContext`, `Entities/Favorite`, `Services/SqliteLocalDataService` |

- Heads never reference `Clients` or call the API with a raw `HttpClient`. The exception is the web head's health probe, which uses the named client from `IHttpClientFactory` because it only checks reachability.
- The MAUI head references `Data.Sqlite`. The device store is named `Sqlite*` so it cannot collide with the shared service names.
- The MAUI target frameworks depend on the host: Android when `ANDROID_HOME` is set or on Windows, Apple targets on non-Linux hosts, and `net11.0-windows10.0.26100.0` on Windows.

### Aspire orchestration

- `AppHost` starts the database, `Service.Api` and `App.Web` with `AddDotnetProject`. The MAUI head starts with `AddMauiProject`; its Windows device is always added, and the Mac Catalyst device is added only on macOS hosts.
- SQL Server: `AddAzureSqlServer` with a container (`mssql/server`, tag `2022-latest`). Postgres: `AddAzurePostgresFlexibleServer`.
- The database password is a secret parameter (`AddParameter(..., secret: true)`). Set it with `aspire secret set Parameters:acme-database-password <value>`. It is never in source.
- Resource names are constants in `Common/Constants/AspireNames.cs`, shared by the AppHost and the services it starts.
- Launch profiles use the port tokens `{AppHostHttpsPort}` 44400, `{ApiHttpsPort}` 44401 and `{WebHttpsPort}` 44402.
- The API's default OpenAPI server URL is the service-discovery name of the API resource, so clients resolve it at runtime.

## Domain Events

**Event definitions:** [CUSTOMIZE: not scaffolded. When added, place them under `Domains/Features/{Entities}/Events/`.]

```csharp
// Domains/Features/{Entities}/Events/
public sealed record {Entity}CreatedEvent(
    Guid {Entity}Id,
    string Name,
    DateTimeOffset CreatedAt
) : IDomainEvent;
```

**Event handling approach:**
- Raise only meaningful state changes
- Dispatch via [your event infrastructure]
- Handlers must be idempotent
- Handlers must be resilient (retry transient failures)

## Integration Patterns

### External Service Integration

**Integration approach:**
- **Pattern:** [Adapter / Gateway / Direct]
- **Error Handling:** [Retry / Circuit Breaker / Fallback]. The client registration uses `Microsoft.Extensions.ServiceDiscovery` and `Microsoft.Extensions.Http`; the scaffold adds no resilience policy.
- **Authentication:** [API Key / OAuth2 / Certificate]

### Inter-Domain Communication

**How domains communicate:**
- **Same Service:** [Direct references / Domain events / Messaging]. Business domains share the `Domains` project and its `Features/` folders.
- **Different Services:** [HTTP / gRPC / Messaging]

## Persistence Strategy

**How data is persisted:**

- **Primary Store:** SQL Server 2022 (default) or PostgreSQL, selected at scaffold time. EF Core 11 with code-first migrations. The `DataContext` sets the `{applicationname}` schema and the `system` schema for the migrations history. Migrations are generated by the user with `dotnet ef migrations add Initial --project src/{ApplicationName}.Data.{Provider} --startup-project src/{ApplicationName}.Service.Api`.
- **Entity mapping:** `IEntityTypeConfiguration<T>` in its own file beside the entity, applied by `ApplyConfigurationsFromAssembly`.
- **Caching:** [CUSTOMIZE]
- **File Storage:** [Where and how files are stored] (if applicable)
- **Message Queue:** [Technology and usage] (if applicable)

**Example:**
- **Primary Store:** PostgreSQL via EF Core, code-first migrations
- **Caching:** Redis for reference data (countries, categories), 15-minute TTL
- **File Storage:** Azure Blob Storage for documents, private containers
- **Message Queue:** Azure Service Bus for cross-domain events

## Security Architecture

**Authentication & Authorization:**

- **Authentication:** Not scaffolded. The API is anonymous by default. [CUSTOMIZE: where it is implemented]
- **Authorization:** [Policy-based / Role-based / Claims-based]
- **Token handling:** [JWT validation, refresh token strategy]

**API Security:**

- **CORS:** [Configuration approach]
- **Rate Limiting:** A fixed-window policy named `RateLimits.Api` (`api`), 1000 permits per minute, no queue. Applied to every endpoint group. Registered with `AddRateLimiter` and enabled with `UseRateLimiter`.
- **HTTPS:** `UseHttpsRedirection` in every environment; `UseHsts` outside Development.
- **Response compression:** Off. Enabling it is an opt-in decision because compressed responses that combine a secret with request input are open to BREACH-style attacks.
- **Input Validation:** At the endpoint. Request models use Data Annotations on their properties, and `.WithValidation<T>()` evaluates them. Entities are not used as request bodies.

**Secrets Management:**

- **Development:** Aspire secret parameters (`aspire secret set`) and user secrets. The committed `appsettings.Development.json` holds no secrets.
- **Production:** [Azure Key Vault / AWS Secrets Manager]. Connection strings come from configuration (`ConnectionStrings:acme-db`) and are never committed.

## Scalability Strategy

**How the system scales:**

- **Horizontal Scaling:** [Stateless design / Session handling approach]. The API holds no in-process state beyond the rate limiter's fixed window.
- **Database Scaling:** [Read replicas / Sharding / Partitioning]
- **Caching Strategy:** [Distributed cache for shared data]
- **Async Processing:** [Background jobs / Message queue for long operations]

## Monitoring & Observability

**How the system is monitored:**

- **Logging:** `ILogger<T>` with structured placeholders (`{EntityId}`, `{Count}`). OpenTelemetry logging is wired by `I-Synergy.Framework.OpenTelemetry`.
- **Metrics:** ASP.NET Core, Kestrel and EF Core meters (`AddAspNetCoreInstrumentation`, `AddEntityFrameworkCoreInstrumentation`).
- **Tracing:** OpenTelemetry tracing. The exporter is OTLP in Development and the Application Insights exporter elsewhere. The connection string is never committed.
- **Health Checks:** `/health` runs only the `live` check (no I/O). `/health/ready` runs `live` and `db` (a database check with a timeout). The AppHost waits on `/health/ready`.

## Deployment Architecture

**Deployment strategy:**

- **Environment Strategy:** [Dev / Staging / Production]
- **Deployment Method:** [Blue-Green / Rolling / Canary]
- **Infrastructure:** [Cloud / On-premises / Hybrid]. The scaffold targets Aspire for local orchestration. `Service.Api` publishes as a Linux container (`linux-x64`, `linux-arm64`); the registry is set outside source control.
- **CI/CD:** [Pipeline approach and stages]. The scaffold ships no pipeline files.

## Architectural Decision Records (ADRs)

### ADR Template

```markdown
## ADR-XXX: [Decision Title]

**Status:** [Proposed / Accepted / Deprecated / Superseded]
**Date:** [YYYY-MM-DD]
**Deciders:** [Who decided]

### Context
[What is the issue that we're seeing that is motivating this decision]

### Decision
[What is the change that we're proposing/have agreed to]

### Consequences
**Positive:**
- [e.g., easier to understand, better performance]

**Negative:**
- [e.g., increased complexity, more boilerplate]

### Alternatives Considered
- [Alternative 1] - [Why rejected]
- [Alternative 2] - [Why rejected]
```

### Example ADR

```markdown
## ADR-001: [Decision Name]

**Status:** [Proposed | Accepted | Deprecated | Superseded]
**Date:** [Date]
**Deciders:** [Team]

### Context
[What is the issue that motivates this decision?]

### Decision
[What is the change being proposed or accepted?]

### Consequences
**Positive:**
- [Positive outcome]

**Negative:**
- [Negative outcome or trade-off]

### Alternatives Considered
- [Alternative 1] - [Why rejected]
```

## Reference Implementations

**Which implementations serve as patterns:**

- **Primary Reference:** `Features/{Entities}` in a rendered scaffold (the sample entity: `Item`, `Items`) - full CRUD through `Domains`, `Services` and the heads, with the test pattern for each layer
- **Alternative Patterns:** [{Domain}.{Entity}] - [What pattern it demonstrates]

**Example:**
- **Primary Reference:** `Features/Items` - Complete CRUD implementation with all operations, comprehensive testing, full documentation
- **Alternative Patterns:** [{Domain2}.{Entity}] - Demonstrates soft-delete pattern with audit fields

## Known Limitations

**Document known architectural limitations:**

1. [Limitation 1] - [Why it exists, when to address]
2. [Limitation 2] - [Impact and planned mitigation]
3. Kiota member order - the first Debug build can reorder generated members for entity names that sort differently from `Item`. Ordering only.
4. Anonymous API - no authentication, rate limiting only. Add an authentication module before exposing write routes beyond a trusted network. [CUSTOMIZE]

**Example:**
1. Single database instance - Acceptable for current scale (<100k users), plan to implement read replicas when load increases
2. Synchronous inter-domain communication - Acceptable for low latency requirements, consider event-driven architecture for high volume operations

## Future Architectural Considerations

**What might evolve:**

- [Consideration 1] - [Trigger for this change]
- [Consideration 2] - [Benefits and costs]

**Example:**
- Event sourcing for audit-heavy domains - Consider when audit requirements become more stringent
- Microservices architecture - Evaluate when team size exceeds 10 developers or domains become truly independent

---

**Remember:** This file documents your system's architecture. Update it when patterns evolve. For technology choices, see [tech-stack.md](tech-stack.md). For business domains, see [domains.md](domains.md).
