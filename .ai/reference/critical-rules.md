# Critical Rules (Read First)

These are non-negotiable patterns that cause bugs if violated.

## 1. Commands: Individual Parameters Only

**NEVER pass model objects to commands.**

```csharp
// CORRECT - Individual parameters
public sealed record Create{ChildEntity}Command(
    Guid {Entity}Id,
    string Description,
    decimal Amount
) : ICommand<Create{ChildEntity}Response>;

// WRONG - Passing model object
public sealed record Create{ChildEntity}Command(
    {ChildEntity} {childEntity}
) : ICommand<Create{ChildEntity}Response>;
```

### Endpoint Construction

```csharp
// CORRECT - Extract properties from model
app.MapPost("/{childEntities}", async ({ChildEntity} model, ICommandHandler handler) =>
{
    var command = new Create{ChildEntity}Command(model.{Entity}Id, model.Description, model.Amount);
    return await handler.HandleAsync(command);
});

// WRONG - Passing model directly
var command = new Create{ChildEntity}Command(model);
```

## 2. Delete Operations: Use FirstOrDefaultAsync + Remove + SaveChangesAsync

```csharp
// CORRECT
var entity = await dataContext.{ChildEntities}.FirstOrDefaultAsync(e => e.{ChildEntity}Id == command.{ChildEntity}Id, cancellationToken);

if (entity is null)
    throw new InvalidOperationException($"{ChildEntity} {command.{ChildEntity}Id} not found");

dataContext.{ChildEntities}.Remove(entity);
var rowsAffected = await dataContext.SaveChangesAsync(cancellationToken);

if (rowsAffected == 0)
    throw new InvalidOperationException($"Failed to delete {ChildEntity} {command.{ChildEntity}Id}");

// WRONG - These extension methods are NOT used
await dataContext.DeleteItemByIdAsync<{ChildEntity}, Guid>(id, cancellationToken);
await dataContext.RemoveItemAsync<{ChildEntity}, Guid>(id, cancellationToken);
```

## 3. Query Parameters: Use Named Parameters

For optional filters, always use named parameters to avoid ambiguity.

```csharp
// CORRECT - Named parameters prevent ambiguity
var query = new GetDepositsTotalAmountQuery({ChildEntity}Id: id);
var query = new GetDepositsTotalAmountQuery({Entity}Id: id);

// WRONG - Positional parameters are ambiguous
var query = new GetDepositsTotalAmountQuery(id, true);
```

## 4. Data Access: Use EF Core Primitives on DataContext

**NO explicit Repository interfaces. NO extension methods like AddItemAsync/GetItemByIdAsync.** Use EF Core directly. Handlers depend on `IDataContext` (`{ApplicationName}.Data/Abstractions/`), which exposes the same named DbSet properties.

```csharp
// CORRECT — Use named DbSet properties from DataContext for all operations
// Create
var entity = new Entities.{Entity} { {Entity}Id = Guid.NewGuid(), ... };
dataContext.{Entities}.Add(entity);
await dataContext.SaveChangesAsync(cancellationToken);

// Read single
var entity = await dataContext.{Entities}.FirstOrDefaultAsync(e => e.{Entity}Id == id, cancellationToken);
var model = /* map entity to {Entity} model */;

// Read list
var models = await dataContext.{Entities}
    .OrderBy(b => b.Description)
    .Select(b => /* map b to {Entity} model */)
    .ToListAsync(cancellationToken);

// Update — no .Update() call needed; change tracker detects property mutations on tracked entities
var entity = await dataContext.{Entities}.FirstOrDefaultAsync(e => e.{Entity}Id == command.{Entity}Id, cancellationToken);
entity.Description = command.Description;
await dataContext.SaveChangesAsync(cancellationToken);

// Delete
var entity = await dataContext.{Entities}.FirstOrDefaultAsync(e => e.{Entity}Id == command.{Entity}Id, cancellationToken);
dataContext.{Entities}.Remove(entity);
await dataContext.SaveChangesAsync(cancellationToken);

// WRONG - We don't use repositories
await _repository.Add(model);

// WRONG - We don't use these extension methods
await dataContext.AddItemAsync<{Entity}, {Entity}Model>(model, ct);
await dataContext.GetItemByIdAsync<{Entity}, {Entity}Model, Guid>(id, ct);
```

## 5. Async: Always Include CancellationToken

```csharp
// CORRECT
public async Task<Get{Entity}ByIdResponse> HandleAsync(
    Get{Entity}ByIdQuery query,
    CancellationToken cancellationToken = default)
{
    var entity = await dataContext.{Entities}.FirstOrDefaultAsync(e => e.{Entity}Id == query.{Entity}Id, cancellationToken);
    var {entity} = /* map entity to {Entity} model */;
    return new Get{Entity}ByIdResponse({entity});
}

// WRONG - Blocking on async
public Get{Entity}ByIdResponse Handle(Get{Entity}ByIdQuery query)
{
    var entity = dataContext.{Entities}.FirstOrDefaultAsync(
        e => e.{Entity}Id == query.{Entity}Id,
        CancellationToken.None).Result; // DEADLOCK RISK!
}

// WRONG - No CancellationToken
public async Task<Get{Entity}ByIdResponse> HandleAsync(Get{Entity}ByIdQuery query)
{
    // Missing cancellation support
}
```

## 6. Entity Exposure: NEVER Expose Domain Entities

Always convert to Models before returning from handlers. Responses wrap Models.

```csharp
// CORRECT - Response wraps Model
public async Task<Get{Entity}ByIdResponse> HandleAsync(...)
{
    var entity = await dataContext.{Entities}.FirstOrDefaultAsync(e => e.{Entity}Id == query.{Entity}Id, ct);
    var {entity} = /* map entity to {Entity} model */;
    return new Get{Entity}ByIdResponse({entity});
}

// WRONG - Return domain entity directly
public async Task<Entities.{Entity}> HandleAsync(...)
{
    return await dataContext.{Entities}.FirstOrDefaultAsync(e => e.{Entity}Id == id, ct);
}
```

## 7. Progress Files: Current Solution Only

Progress files MUST be in the current solution's `.ai/` folder.

```
CORRECT:   .ai/progress/task-progress.md
WRONG:     ~/.ai/progress/task-progress.md
WRONG:     /other/solution/.ai/progress/task-progress.md
```

## 8. Session Context: Read First, Update Last

Every session MUST:
1. Read `.ai/session-context.md` FIRST
2. Build on established patterns
3. Update session-context.md with learnings before ending

## 9. Handler Naming: Always Include Command/Query Suffix

```csharp
// CORRECT
public sealed class Create{Entity}CommandHandler : ICommandHandler<...>
public sealed class Get{Entity}ByIdQueryHandler : IQueryHandler<...>

// WRONG - Missing suffix
public sealed class Create{Entity}Handler : ICommandHandler<...>
public sealed class Get{Entity}ByIdHandler : IQueryHandler<...>
```

## 10. File Organization: One Type Per File, Subfolder Per Operation

**Every top-level type gets its own file.** A file contains exactly one class, record, struct, interface, or enum — never two, however small or closely related they are. A private nested type is part of its parent type, not a second top-level type.

```
// CORRECT - Plural feature folder, singular entity in operation names, one subfolder per operation
{ApplicationName}.Domains/Features/{Entities}/
  Commands/Create{Entity}/
    Create{Entity}Command.cs
    Create{Entity}CommandHandler.cs
    Create{Entity}Response.cs
  Commands/Update{Entity}/
    Update{Entity}Command.cs
    Update{Entity}CommandHandler.cs
    Update{Entity}Response.cs
  Queries/Get{Entity}ById/
    Get{Entity}ByIdQuery.cs
    Get{Entity}ByIdQueryHandler.cs
    Get{Entity}ByIdResponse.cs

// WRONG - Singular feature folder, flat operation folders, or combined files
{ApplicationName}.Domains/Features/{Entity}/Commands/
  Create{Entity}Command.cs      (command + response combined)
  Create{Entity}Handler.cs      (also: no operation subfolder, and no Command suffix)

// WRONG - two top-level types in one file, anywhere in the solution
Create{Entity}Response.cs
  public sealed record Create{Entity}Response(Guid {Entity}Id);
  public sealed record Update{Entity}Response(bool Success);   // belongs in its own file
```

The feature folder is plural (`Features/{Entities}/`) and the namespace follows it (`Acme.Domains.Features.Items.Commands.CreateItem`), which keeps the feature apart from the `Item` entity type. The entity mapping `IEntityTypeConfiguration<T>` is a separate file beside the entity (`Item.cs` and `ItemConfiguration.cs` in `{ApplicationName}.Entities`), not a nested type.

## 11. Enum Naming: Always Plural (except *Status)

All enum type names must be plural. Only enums with a `Status` suffix are exempt.

```csharp
// CORRECT — plural names
public enum PaymentProviders { Stripe, PayNl, Mollie }
public enum SubscriptionHistoryEvents { Created, Activated, Cancelled }
public enum SecurityEventTypes { AuthenticationSuccess, AuthenticationFailed }
public enum AlertSeverities { Low, Medium, High }
public enum OrderTypes { Buy, Sell }

// CORRECT — Status suffix is exempt (kept singular)
public enum PaymentStatus { Pending, Succeeded, Failed }
public enum SubscriptionStatus { Active, Paused, Cancelled }
public enum EmailOutboxStatus { Pending, Processing, Sent, Failed }

// WRONG — singular non-Status enum names
public enum PaymentProvider { Stripe, PayNl, Mollie }
public enum SecurityEventType { AuthenticationSuccess, AuthenticationFailed }
public enum AlertSeverity { Low, Medium, High }
public enum OrderType { Buy, Sell }
```

## 12. Entity Properties: Use Enum Type, Not int

EF Core automatically converts enum types to/from int in the database. Always use the enum type on entity properties — never raw `int`.

```csharp
// CORRECT — EF Core converts enum to int automatically
public PaymentStatus Status { get; set; }
public PaymentProviders Provider { get; set; }
public SubscriptionStatus SubscriptionStatus { get; set; }
public InvoiceStates StatusId { get; set; }

// WRONG — Never store enum values as raw int on entities
public int Status { get; set; }
public int Provider { get; set; }
public int SubscriptionStatus { get; set; }
public int StatusId { get; set; }
```

## 13. Common Project: Centralize Shared Types

Every solution MUST include `{ApplicationName}.Common` and `{ApplicationName}.Resources`. `Common` references `Resources`. Every other project references `Common`, directly or transitively. Shared types, especially enumerations, MUST live in `Common`, never in a domain or data project where they create cross-dependencies.

`Common` folders: `Constants/` (`AspireNames`, `ConnectionStrings`, `DatabaseConstants`, `RateLimits`), `Converters/`, `Enumerations/`, `Factories/`, `Models/` (`HttpClientSettings`). Resource strings live in `{ApplicationName}.Resources` (`Properties/Resources.resx`, default namespace `{ApplicationName}.Resources`).

```
// CORRECT — Enum defined once in Common, consumed everywhere
// {ApplicationName}.Common/Enumerations/PaymentStatus.cs
public enum PaymentStatus { Pending = 0, Succeeded = 1, Failed = 2 }

// {ApplicationName}.Entities, {ApplicationName}.Models: reference Common
// {ApplicationName}.Data: references Entities (transitively Common)
// {ApplicationName}.Domains: references Entities, Models, Data.{Provider}
// {ApplicationName}.Services: references Domains, Models

// WRONG — Enum defined in the Entities project, forcing Models or the heads to reference Entities to use it
// {ApplicationName}.Entities/Enumerations/{Entity}Status.cs

// WRONG — Duplicate enum definitions across projects
// {ApplicationName}.Entities: {Entity}Status
// {ApplicationName}.Models: {Entity}Status  (duplicate)
```

Other types that belong in Common: shared constants, common interfaces (e.g., `IEntity`, `IAuditable`), reusable value objects, and extension methods used across multiple projects.

## 14. Entities and Models: Never Reference Each Other

An entity MUST never reference a model, and a model MUST never reference an entity. If both projects need the same type, that type belongs in `{ApplicationName}.Common`.

```
// CORRECT — Shared type extracted to Common
// {ApplicationName}.Common/Enumerations/PaymentStatus.cs
public enum PaymentStatus { Pending = 0, Succeeded = 1, Failed = 2 }

// {ApplicationName}.Entities/Payment.cs
public class Payment { public PaymentStatus Status { get; set; } }

// {ApplicationName}.Models/Payment.cs
public sealed record Payment { public PaymentStatus Status { get; init; } }   // named after the concept (rule 28)

// WRONG — Entities project references Models for a shared enum
// {ApplicationName}.Entities has a project reference to {ApplicationName}.Models

// WRONG — Models project references Entities for a shared enum
// {ApplicationName}.Models has a project reference to {ApplicationName}.Entities
```

A cross-reference between Entities and Models is the canary: it signals a type that should have been extracted to Common.

## 15. Plan Files: Always in `.ai/plans/`

Plans and design docs MUST be saved in the project-local `.ai/plans/` folder. The `writing-plans` and `brainstorming` skills default to `docs/plans/` — always override that to `.ai/plans/`.

```
CORRECT:   .ai/plans/2026-02-28-feature-name.md
WRONG:     docs/plans/2026-02-28-feature-name.md
WRONG:     ~/.ai/plans/2026-02-28-feature-name.md
```

This is configured via `plansDirectory` in `.claude/settings.json` and must not be bypassed by skill defaults.

## 16. New Types: Search Entire Solution First

**Before creating any entity, model, class, or property — search the entire solution first.** If it already exists, reuse or extend it. Never create overlapping or redundant types.

```
// CORRECT — search first, reuse what exists
// "Customer" already has Person, Address, PhoneNumber → reference those

// WRONG — duplicating existing domain types
public class Client { string Name; string Phone; string Street; }
```

This check is mandatory at **planning time**. Every plan must explicitly state which existing entities are reused before proposing new ones.

## 17. Code Writing: Always Delegate to Specialized Subagents

All code writing, editing, and modification MUST be delegated to a specialized subagent. The main conversation handles reasoning, analysis, planning, and user interaction only.

| Task | Subagent |
|------|----------|
| Planning, architecture, design decisions | `architect` subagent (Sonnet) or main conversation (Pro) |
| Code exploration and search | `Explore` subagent |
| .NET implementation (CQRS, API, Blazor, data access, builds) | `developer` subagent |
| Unit/integration tests (MSTest, Moq, Reqnroll) | `tester` subagent |
| E2E/UI tests (Playwright, accessibility) | `ui-tester` subagent |
| Visual design (color, typography, branding, tokens) | `designer` subagent |
| UI components, layouts, styling | `ui-developer` subagent |
| Code review (SOLID, CQRS, security, architecture) | `reviewer` subagent |
| Documentation (XML docs, API docs, READMEs, ADRs) | `writer` subagent |

All agents are defined in `.ai/agents/` and hard-linked to `.claude/agents/` for discovery.

## 18. Endpoint Produces Metadata: Always Explicit

Every API endpoint route MUST explicitly declare every status code it can return, via `.Produces<T>()`, `.Produces(statusCode)` or `.ProducesValidationProblem()`. Never rely on inference: OpenAPI and the generated client need the metadata.

The scaffold's API is anonymous by default. An anonymous route declares no `401`. A route that requires authentication declares `.Produces(StatusCodes.Status401Unauthorized)`. Every route in the rate-limited group also declares `429`.

```csharp
// CORRECT — the rendered Items endpoints (anonymous, rate limited)
group.MapPost("", AddItemAsync)
    .Accepts<Models.CreateItemRequest>("application/json")
    .WithValidation<Models.CreateItemRequest>()
    .Produces(StatusCodes.Status429TooManyRequests)     // rate limited
    .Produces<Guid>(StatusCodes.Status201Created)       // success
    .ProducesValidationProblem();                       // validation

group.MapGet("{id:guid}", GetItemByIdAsync)
    .Produces(StatusCodes.Status429TooManyRequests)
    .Produces<Models.Item>(StatusCodes.Status200OK)     // success
    .Produces(StatusCodes.Status404NotFound);           // not found

group.MapDelete("{id:guid}", DeleteItemAsync)
    .Produces(StatusCodes.Status429TooManyRequests)
    .Produces(StatusCodes.Status204NoContent)           // success
    .Produces(StatusCodes.Status404NotFound)            // not found
    .ProducesValidationProblem();                       // refusal

// WRONG — only error codes declared, success type omitted
group.MapPost("", AddItemAsync)
    .Accepts<Models.CreateItemRequest>("application/json")
    .ProducesValidationProblem();

// WRONG — no produces metadata at all
group.MapGet("{id:guid}", GetItemByIdAsync);
```

## 19. API Projects: OpenAPI Document Generation in .csproj

Every API project `.csproj` MUST write the OpenAPI document on Debug builds, so the Kiota client (rule 21) can be regenerated from it. The scaffold's `Service.Api` is the reference: the document is generated in Debug only, and Release builds are not affected by it.

```xml
<!-- CORRECT — Service.Api: the document is generated on Debug builds only -->
<Project Sdk="Microsoft.NET.Sdk.Web">

  <PropertyGroup>
    <OpenApiGenerateDocuments>false</OpenApiGenerateDocuments>
    <OpenApiGenerateDocumentsOnBuild>false</OpenApiGenerateDocumentsOnBuild>
  </PropertyGroup>

  <PropertyGroup Condition="'$(Configuration)' == 'Debug'">
    <OpenApiDocumentsDirectory>../../openapi</OpenApiDocumentsDirectory>
    <OpenApiGenerateDocuments>true</OpenApiGenerateDocuments>
    <OpenApiGenerateDocumentsOnBuild>true</OpenApiGenerateDocumentsOnBuild>
    <OpenApiGenerationEnvironment>Development</OpenApiGenerationEnvironment>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.Extensions.ApiDescription.Server" Condition="'$(Configuration)' == 'Debug'">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
    </PackageReference>
  </ItemGroup>
</Project>

<!-- WRONG — Missing OpenAPI generation configuration and package reference -->
<Project Sdk="Microsoft.NET.Sdk.Web">
  <!-- No OpenApiGenerateDocumentsOnBuild, no OpenApiDocumentsDirectory, -->
  <!-- no Microsoft.Extensions.ApiDescription.Server reference -->
</Project>
```

`OpenApiDocumentsDirectory` is relative to the project file: `../../openapi` puts the document in the solution-level `openapi/` folder. The package reference uses `PrivateAssets="all"` so it does not leak to downstream consumers.

## 20. OpenAPI: Document Transformer (Servers) + Schema Transformer (Types)

Every API project MUST register both a document transformer and a schema transformer in `AddOpenApi()`.

Both transformers MUST be registered in a single `AddOpenApi` call:

```csharp
// CORRECT — Both transformers in one AddOpenApi call
builder.Services.AddOpenApi(options =>
{
    // Document transformer: sets servers URL for Kiota clients
    options.AddDocumentTransformer((document, context, ct) =>
    {
        document.Servers = [new OpenApiServer { Url = "https://api" }];
        return Task.CompletedTask;
    });

    // Schema transformer: maps .NET types to JSON schema types
    options.AddSchemaTransformer((schema, context, ct) =>
    {
        var propertyType = context.JsonPropertyInfo?.PropertyType;
        if (propertyType == null)
            return Task.CompletedTask;

        var actualType = Nullable.GetUnderlyingType(propertyType) ?? propertyType;

        if (actualType == typeof(DateTimeOffset) || actualType == typeof(DateTime))
        {
            schema.Type = JsonSchemaType.String; schema.Format = "date-time";
        }
        else if (actualType == typeof(DateOnly))
        {
            schema.Type = JsonSchemaType.String; schema.Format = "date";
        }
        else if (actualType == typeof(TimeOnly))
        {
            schema.Type = JsonSchemaType.String; schema.Format = "time";
        }
        else if (actualType == typeof(TimeSpan))
        {
            schema.Type = JsonSchemaType.String; schema.Format = "duration";
        }
        else if (actualType == typeof(decimal) || actualType == typeof(double))
        {
            schema.Type = JsonSchemaType.Number; schema.Format = "double";
        }
        else if (actualType == typeof(float))
        {
            schema.Type = JsonSchemaType.Number; schema.Format = "float";
        }
        else if (actualType == typeof(int))
        {
            schema.Type = JsonSchemaType.Integer; schema.Format = "int32";
        }
        else if (actualType == typeof(long))
        {
            schema.Type = JsonSchemaType.Integer; schema.Format = "int64";
        }
        else if (actualType == typeof(Guid))
        {
            schema.Type = JsonSchemaType.String; schema.Format = "uuid";
        }
        else if (actualType == typeof(string))
        {
            schema.Type = JsonSchemaType.String;
        }
        else if (actualType == typeof(bool))
        {
            schema.Type = JsonSchemaType.Boolean;
        }
        else if (actualType.IsEnum)
        {
            schema.Type = JsonSchemaType.String;
            schema.Enum = Enum.GetNames(actualType)
                .Select(name => System.Text.Json.Nodes.JsonValue.Create(name)!)
                .Cast<System.Text.Json.Nodes.JsonNode>()
                .ToList();
        }

        return Task.CompletedTask;
    });
});

// WRONG — No transformers; Kiota client has no base URL and all types are UntypedNode
builder.Services.AddOpenApi();
```

## 21. API Clients: Kiota-Generated, Never Raw HttpClient

Every API has a Kiota-generated client project named `{ApplicationName}.Clients` (no `.Api` or app suffix). Heads never call the API with a raw `HttpClient`. They use the typed client through the shared service in `{ApplicationName}.App.Shared`.

```csharp
// CORRECT — the generated ApiClient is injected into the App.Shared service, which maps the client models
public sealed class {ApplicationName}ApiService(ApiClient client) : I{ApplicationName}ApiService
{
    public async Task<IReadOnlyList<Item>> GetItemsAsync(CancellationToken cancellationToken = default)
    {
        var items = await client.Items.GetAsync(cancellationToken: cancellationToken);
        return items?.Select(Map).ToList() ?? [];
    }
}

// WRONG — raw HttpClient with magic strings and hand-written deserialisation
public sealed class ItemsService(HttpClient httpClient)
{
    public async Task<List<Item>?> GetItemsAsync()
    {
        var json = await httpClient.GetStringAsync("/items");
        return JsonSerializer.Deserialize<List<Item>>(json);
    }
}
```

The client project:
- References `Microsoft.Kiota.Bundle` and `Microsoft.Extensions.Http`.
- References `{ApplicationName}.Service.Api` with `ReferenceOutputAssembly="false"`. The reference orders the builds and adds no assembly dependency.
- Sets `EnableDefaultCompileItems` to `false`. The compile list is built by the target `IncludeGeneratedApiClient`, which reads `Api/` with `Directory.GetFiles` before compilation. A wildcard item can hold a stale listing after regeneration.
- Contains `Api/` as the generated source: `ApiClient.cs`, `Items/`, `Models/`. It is committed and never edited by hand. A regeneration overwrites it (`--clean-output`).
- Has no DI extension class. Registration lives in `{ApplicationName}.App.Shared/Extensions/HostApplicationBuilderExtensions.cs` as `Add{ApplicationName}ApiServices`: named `HttpClient`, service discovery, the anonymous authentication provider and the scoped `ApiClient`.

Regeneration:
- A Debug build of `{ApplicationName}.Service.Api` writes `openapi/{ApplicationName}.Service.Api.json` (rule 19). The target `OpenAPI` then runs `dotnet kiota generate` into `src/{ApplicationName}.Clients/Api`.
- The Kiota version is pinned in `.config/dotnet-tools.json` with `rollForward: false`.
- Opt-out: `-p:{ApplicationName}GenerateApiClient=false` skips regeneration. Use it in CI and in test runs that must not rewrite committed files. The API reads the property, so pass it on the top-level command line.
- `kiota-lock.json` is written by the generator and is not shipped in the template. Once generated, it is committed with `Api/`.

Documented exception: the web head's health probe (`App.Web/HealthChecks/ApiHealthCheck.cs`) uses the named client from `IHttpClientFactory`, because it only checks reachability.

## 22. Input Validation: Data Annotations on Properties + Validation Filter

Every POST/PUT route that accepts a body MUST include `.WithValidation<T>()` and `.ProducesValidationProblem()`. Request models are the `Models` request records (`Create{Entity}Request`, `Update{Entity}Request`), never entities. Their Data Annotations sit on properties, because a validator reads properties, not constructor parameters.

```csharp
// CORRECT — annotated, non-positional request record; the filter evaluates the annotations
public sealed record CreateItemRequest
{
    [Required, MaxLength(100)]
    public string Name { get; init; } = string.Empty;

    [MaxLength(500)]
    public string? Description { get; init; }
}

group.MapPost("", AddItemAsync)
    .Accepts<Models.CreateItemRequest>("application/json")
    .WithValidation<Models.CreateItemRequest>()
    .ProducesValidationProblem();

// WRONG — positional record: attributes on constructor parameters are not checked
public sealed record CreateItemRequest([Required, MaxLength(100)] string Name);

// WRONG — no validation filter; the declared ProducesValidationProblem never runs
group.MapPost("", AddItemAsync)
    .Accepts<Models.CreateItemRequest>("application/json")
    .ProducesValidationProblem();
```

A missing or malformed body is answered 400 before the filter runs. Errors are grouped by member, so two errors on one member are reported together.

## 23. Rate Limiting and HTTPS Enforcement

Every API project MUST configure rate limiting and HTTPS redirection.

```csharp
// CORRECT — Rate limiter and HTTPS configured
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddRateLimiter(options =>
{
    options.AddFixedWindowLimiter("api", config =>
    {
        config.PermitLimit = 1000;
        config.Window = TimeSpan.FromMinutes(1);
        config.QueueProcessingOrder = QueueProcessingOrder.OldestFirst;
        config.QueueLimit = 0;
    });
});

var app = builder.Build();

app.UseHttpsRedirection();
app.UseRateLimiter();

app.Run();

// WRONG — No rate limiting, no HTTPS redirection
var app = builder.Build();
app.Run();
```

## 24. Enums: Explicit Values When Persisted or Serialized

Any enum that is persisted to a database or serialized (JSON, protobuf, OpenAPI) MUST declare explicit `= 0, = 1, …` values, with a comment stating the values are persisted and must never be renumbered.

```csharp
// CORRECT — explicit values; stable across inserts
public enum PaymentStatus
{
    Pending = 0,   // values are persisted, never renumber
    Succeeded = 1,
    Failed = 2,
}

// WRONG — implicit declaration order; inserting a member relabels every row
public enum PaymentStatus
{
    Pending,       // 0
    Succeeded,     // 1
    Failed,        // 2
    // Inserting "Refunded" above Failed turns Failed into 3 —
    // every stored row flips its meaning
}
```

Inserting a member in declaration order relabels every persisted row / flips every stored setting.

## 25. Bound Breaking Package Ranges

Pin known-incompatible transitive packages with an upper bound so the mismatch fails at restore instead of compile:

```xml
<!-- Directory.Packages.props — upper-bound the known-incompatible package -->
<PackageVersion Include="Microsoft.OpenApi" Version="[2.11.0,3.0.0)" />
```

Without the bound, a newer transitive version is resolved and the build fails deep inside a consuming project with a version-mismatch error — hours of debugging instead of a restore-time failure.

## 26. No Secrets in the Repo or Runbooks

Never commit `.p8` private keys, keystore material, or service-account JSON. Reference pipeline secret variable names and put a placeholder in the doc:

```yaml
# CORRECT — secrets referenced by name
env:
  GOOGLE_PLAY_SA_JSON: $(GOOGLE_PLAY_SA_JSON)
  APP_STORE_P8: $(APP_STORE_API_KEY_P8)

# WRONG — never commit the actual key material
env:
  GOOGLE_PLAY_SA_JSON: '{ "type": "service_account", ... }'   # LEAK
```

## 27. Interfaces: `Abstractions/` Folder, Highest Shared Project

**Every interface lives in an `Abstractions/` folder, in the highest project that its consumers and its implementation already depend on.**

```csharp
// CORRECT — Domains (consumer) and Data.SqlServer (implementation) both reach Data, so IDataContext lives there
// {ApplicationName}.Data/Abstractions/IDataContext.cs
namespace {ApplicationName}.Data.Abstractions;

public interface IDataContext
{
    DbSet<Item> Items { get; }
    Task<int> SaveChangesAsync(CancellationToken cancellationToken = default);
}

// {ApplicationName}.Data.SqlServer/DataContext.cs implements IDataContext
// {ApplicationName}.Domains handlers take IDataContext and never the concrete DataContext

// WRONG — abstraction buried in the implementing project, forcing every consumer
// to reference the implementation just to see the contract
// {ApplicationName}.Data.SqlServer/IDataContext.cs
```

Placement rules:

1. **The abstraction belongs to the consumer side.** The implementing project depends on the interface, never the other way round.
2. **Choose the highest project that both sides already reference**, directly or transitively. `IDataContext` sits in `Data`, not `Data.SqlServer`, because `Domains` and `Data.SqlServer` both reach `Data`.
3. **Do not create a project or add a reference just to host one interface.** If no shared project exists, place it in the highest consumer project and invert the reference instead.
4. **`{ApplicationName}.Common` is not the automatic answer.** Only genuinely solution-wide contracts (`IEntity`, `IAuditable`) belong there. See rule 13.
5. **Folder and namespace mirror each other**, relative to the project's RootNamespace: `Abstractions/`, optional grouping subfolder (`Abstractions/Services/`), namespace `{ApplicationName}.Data.Abstractions` in `Data`, and `{ApplicationName}.Abstractions.Services` in `App.Shared` (RootNamespace `{ApplicationName}`).

**Exception — implementation-only seams.** If an interface is used only inside a single implementation and never by a consumer, keep it beside that implementation instead of in an `Abstractions/` folder, and make it `internal` when the implementation and its callers are internal. A public interface reachable by external code never qualifies for this exception.

## 28. Models: Never Use a `Dto` Suffix

Models *are* DTOs — the suffix adds no information to the type name, the file name, or any reference to it. Name the model after the concept it carries.

```csharp
// CORRECT — type and file named after the concept
// Models/{Entity}.cs
public sealed record {Entity}(Guid {Entity}Id, string Description, decimal Amount);

// WRONG — redundant suffix on type and file
// Models/{Entity}Dto.cs
public sealed record {Entity}Dto(Guid {Entity}Id, string Description, decimal Amount);

// WRONG — the same redundancy under other spellings
public sealed record {Entity}DTO(...);
public sealed record {Entity}DtoModel(...);
```

`Response` and `Request` already state their role and are never `...Dto` either. The rule applies to every model type: entity projections, read models, view models, and API models.

## 29. Package Versions: Central Management and NuGet Audit

Every package version lives in `Directory.Packages.props` (`ManagePackageVersionsCentrally` is `true`). Project files reference packages without a `Version`. No project file, `Version` override or second props file sets a version.

NuGet audit is a build gate: `NuGetAuditMode` is `all`, `NuGetAuditLevel` is `low`, and `NU1900` to `NU1905` are `WarningsAsErrors`. An audit that did not run cannot pass silently.

```xml
<!-- CORRECT — the version is owned by Directory.Packages.props -->
<PackageVersion Include="Microsoft.EntityFrameworkCore.Sqlite" Version="11.0.0" />

<!-- Project file: no version -->
<PackageReference Include="Microsoft.EntityFrameworkCore.Sqlite" />

<!-- WRONG — version in a project file -->
<PackageReference Include="Microsoft.EntityFrameworkCore.Sqlite" Version="11.0.0" />
```

Pre-release pins are listed in `.ai/project/tech-stack.md` with their reason. `global.json` allows pre-release SDKs for them. Remove each pin when a stable release exists.

## 30. MAUI and Blazor Heads: Names and Sharing

The UI projects use three names, and each sets `RootNamespace` to `{ApplicationName}`:

- `{ApplicationName}.App`: the MAUI head.
- `{ApplicationName}.App.Shared`: the API service interface and implementation, the client registration (`Add{ApplicationName}ApiServices`) and the settings models, shared by both heads.
- `{ApplicationName}.App.Web`: the Blazor head (plain Razor, no component library).

Heads reference `App.Shared` and never reference `Clients` or use Kiota types. Shared behaviour goes into `App.Shared`. Head-specific UI stays in the head. The device store `{ApplicationName}.Data.Sqlite` is referenced by the MAUI head only, and its types are named `Sqlite*`. No licence key, store identifier or signing identity appears in source (rule 26).

## 31. Tests: Layering and Real-Provider Tests

Test projects follow the layer they test: `{ApplicationName}.Domains.Tests`, `{ApplicationName}.Service.Tests`, `{ApplicationName}.Data.{Provider}.Tests`, and optionally `{ApplicationName}.AcceptanceTests` and `{ApplicationName}.UI.Tests`. Test code uses MSTest only.

- Handler tests run the real `DataContext` on the EF Core in-memory provider, through a per-test helper such as `TestDatabase`. They pass `NullLogger<T>.Instance` as the logger. They do not mock `DataContext`.
- Provider behaviour (indexes, foreign keys, model configuration, the migrations history table) is tested in `Data.{Provider}.Tests`, against the provider itself.
- Expected exceptions use `Assert.ThrowsExactly<T>` or `await Assert.ThrowsExactlyAsync<T>(...)`. `[ExpectedException]` is not used.
- Moq is not referenced by the test projects. Add it only for a narrow external seam that a handler must not call.

```csharp
// CORRECT — the real provider, a NullLogger, and an exact exception type
using var db = new TestDatabase();
var handler = new DeleteItemCommandHandler(db.Context, NullLogger<DeleteItemCommandHandler>.Instance);
await Assert.ThrowsExactlyAsync<ResourceNotFoundException>(() => handler.HandleAsync(command));

// WRONG — mocked DataContext
var dataContext = new Mock<DataContext>();

// WRONG — expected-exception attribute
[ExpectedException(typeof(ResourceNotFoundException))]
```

`Service.Tests` boots the real `Service.Api` through `WebApplicationFactory<Program>` and replaces the provider `DataContext` with the in-memory one.

## Quick Violation Checklist

Before submitting code, verify you haven't violated these:

- [ ] Commands use individual parameters (not model objects)
- [ ] Delete operations use `FirstOrDefaultAsync` + `Remove` + `SaveChangesAsync`
- [ ] Queries use named parameters for optional filters
- [ ] Data access uses named DbSet properties on DataContext with `FirstOrDefaultAsync` for single lookups (no `.Set<T>()`, no `FindAsync`, no extension methods, no repositories)
- [ ] Create handlers construct entities directly with `new Entity { ... }`
- [ ] All async methods include CancellationToken
- [ ] Domain entities never exposed directly (responses wrap Models)
- [ ] Handlers named with `CommandHandler` / `QueryHandler` suffix
- [ ] Each type in its own file, each operation in its own subfolder
- [ ] No file declares more than one top-level type
- [ ] Model names never carry a `Dto` suffix
- [ ] Progress files in current solution's `.ai/` folder
- [ ] Plan files saved to `.ai/plans/` (not `docs/plans/`)
- [ ] Session context read first and updated last
- [ ] Solution includes `{ApplicationName}.Common` and `{ApplicationName}.Resources` projects with all enumerations centralized
- [ ] Entities and models never reference each other (cross-reference = belongs in Common)
- [ ] Interfaces live in an `Abstractions/` folder in the highest project both consumers and implementation already reference (implementation-only seams excepted)
- [ ] Enum names are plural (except *Status suffix enums)
- [ ] EF Core entity properties use enum types, not raw int
- [ ] Code and design work delegated to specialized subagents (`architect`, `developer`, `designer`, `ui-developer`, `tester`, `ui-tester`, `reviewer`, `writer`) — not done in main conversation
- [ ] All endpoint routes declare both success and error `.Produces()` metadata
- [ ] Every API project `.csproj` writes the OpenAPI document on Debug builds (`OpenApiGenerateDocumentsOnBuild`, `OpenApiDocumentsDirectory`, and `Microsoft.Extensions.ApiDescription.Server` on Debug)
- [ ] Every API project registers a document transformer (servers URL) and schema transformer (type mapping) in `AddOpenApi()`
- [ ] Every API has a Kiota-generated client project — never use raw `HttpClient` to call an internal API
- [ ] Kiota version pinned in `dotnet-tools.json` with `rollForward: false`
- [ ] API project `.csproj` includes `OpenAPI` MSBuild target that runs `dotnet kiota generate` after every build
- [ ] Client project uses `Microsoft.Kiota.Bundle` and `Microsoft.Extensions.Http`
- [ ] Generated client source (`Api/`, `Models/`, `ApiClient.cs`, `kiota-lock.json`) is committed
- [ ] POST/PUT routes use `.WithValidation<T>()` with Data Annotations on request models
- [ ] Rate limiting configured (`AddRateLimiter` + `UseRateLimiter`) and `UseHttpsRedirection` called
- [ ] Persisted/serialized enums declare explicit `= 0, = 1, …` values with a "never renumber" comment
- [ ] Known-incompatible transitive packages are upper-bounded in `Directory.Packages.props`
- [ ] Package versions only in `Directory.Packages.props`; NuGet audit errors (NU1900-NU1905) kept on
- [ ] Kiota `Api/` never edited by hand; the regeneration opt-out is used in CI and test runs
- [ ] UI projects named `{ApplicationName}.App`, `{ApplicationName}.App.Shared`, `{ApplicationName}.App.Web`; heads do not reference `Clients`
- [ ] Tests follow the layer they test, use the real provider with `NullLogger`, and use `Assert.ThrowsExactly`; no mocked `DataContext`, no `[ExpectedException]`
- [ ] No `.p8` keys, keystores, or service-account JSON in the repo or runbooks (reference secret variable names)
