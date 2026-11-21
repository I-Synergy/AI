# Naming Conventions

## C# Code

| Element | Convention | Example |
|---------|-----------|----------|
| **Namespace** | `{ApplicationName}.{Project}` plus the folder path | `{ApplicationName}.Domains.Features.{Entities}.Commands.Create{Entity}` |
| **Command** | `{Action}{Entity}Command` | `Create{Entity}Command` |
| **Query** | `Get{Entity}{Criteria}Query` | `Get{Entity}ByIdQuery` |
| **Handler** | `{Action}{Entity}CommandHandler` / `Get{Entity}{Criteria}QueryHandler` | `Create{Entity}CommandHandler` |
| **Response** | `{Action}{Entity}Response` | `Create{Entity}Response` |
| **Model** | `{Entity}` (no suffix — never `{Entity}Dto`); request bodies `Create{Entity}Request`, `Update{Entity}Request` | `{Entity}` |
| **Interface** | `I{Type}` | `ICommandHandler<T>` |
| **Interface location** | `Abstractions/` folder in the highest shared project, namespace mirrors folder | `{ApplicationName}.Data.Abstractions.IDataContext` |
| **Classes** | PascalCase | `{Entities}Endpoints` |
| **Methods** | PascalCase + `Async` suffix | `Get{Entity}ByIdAsync` |
| **Properties** | PascalCase | `{Entity}Id`, `CreatedDate` |
| **Private fields** | `_camelCase` | `_dataContext`, `_logger` |
| **Parameters/locals** | camelCase | `{entity}Id`, `cancellationToken` |
| **Constants** | PascalCase | `Max{Entity}Amount` |
| **Enums** | PascalCase (type and values), plural unless `Status`; in `Common/Enumerations/` | `{Entity}Status.Active` |

## Project Names

One flat set of projects per solution. Folders under `src/` and `tests/` use these names. `Domains` is always plural. `Service.Api` is the one singular host name.

| Project | Holds |
|---------|-------|
| `{ApplicationName}.Common` | Constants, converters, enumerations, factories, shared models |
| `{ApplicationName}.Resources` | `Properties/Resources.resx` |
| `{ApplicationName}.Entities` | EF Core POCOs and their `IEntityTypeConfiguration` |
| `{ApplicationName}.Models` | Read models (`BaseModel`) and request records |
| `{ApplicationName}.Data` | `Abstractions/IDataContext.cs` |
| `{ApplicationName}.Data.SqlServer` or `{ApplicationName}.Data.Postgres` | `DataContext`, design-time factory, `Initializers/` |
| `{ApplicationName}.Data.Sqlite` | Device store (optional) |
| `{ApplicationName}.Domains` | Commands, queries and handlers under `Features/{Entities}/` |
| `{ApplicationName}.Services` | Endpoint groups (`Endpoints/{Entities}Endpoints.cs`) |
| `{ApplicationName}.Service.Api` | Host (`Program.cs`) |
| `{ApplicationName}.Clients` | Kiota client (`Api/`) |
| `{ApplicationName}.App.Shared`, `{ApplicationName}.App`, `{ApplicationName}.App.Web` | Shared head services, MAUI head, Blazor head |
| `{ApplicationName}.AppHost` | Aspire orchestration |
| `{ApplicationName}.Domains.Tests`, `.Service.Tests`, `.Data.{Provider}.Tests`, `.AcceptanceTests`, `.UI.Tests` | Tests, by the layer they test |

## Namespace Patterns

The namespace follows the folder, relative to the project's RootNamespace.

```csharp
{ApplicationName}.Domains.Features.{Entities}.Commands.Create{Entity}   // Domains/Features/{Entities}/Commands/Create{Entity}/
{ApplicationName}.Domains.Features.{Entities}.Queries.Get{Entity}ById  // Domains/Features/{Entities}/Queries/Get{Entity}ById/
{ApplicationName}.Services.Endpoints                                   // Services/Endpoints/{Entities}Endpoints.cs
{ApplicationName}.Entities                                             // Entities/{Entity}.cs
{ApplicationName}.Models                                               // Models/{Entity}.cs
{ApplicationName}.Data.Abstractions                                    // Data/Abstractions/IDataContext.cs
{ApplicationName}.Common.Enumerations                                  // Common/Enumerations/{Entity}Status.cs
{ApplicationName}.Abstractions.Services                                // App.Shared/Abstractions/Services/ (RootNamespace {ApplicationName})
```

The feature folder is plural, so `Acme.Domains.Features.Items.Commands.CreateItem` never collides with the `Item` entity (`Acme.Entities.Item`) or the `Item` model.

## File Naming

**One top-level type per file.** A file declares exactly one class, record, struct, interface, or enum and is named after it — never place two types in one file. Model files are named after the concept (`{Entity}.cs`), never `{Entity}Dto.cs`.

### Folders

Each operation gets its own subfolder. The feature folder is plural; the operation names use the singular entity.

```
Features/{Entities}/Commands/Create{Entity}/Create{Entity}Command.cs
Features/{Entities}/Commands/Create{Entity}/Create{Entity}CommandHandler.cs
Features/{Entities}/Queries/Get{Entities}List/Get{Entities}ListQuery.cs
```

### Commands

```
Create{Entity}Command.cs
Update{Entity}Command.cs
Delete{Entity}Command.cs

Examples:
Create{Entity}Command.cs
Update{Entity}Command.cs
Delete{Entity}Command.cs
```

### Queries

```
Get{Entity}ByIdQuery.cs
Get{Entity}ListQuery.cs
Get{Entities}By{Criteria}Query.cs

Examples:
Get{Entity}ByIdQuery.cs
Get{Entity}ListQuery.cs
Get{Entities}ByUserIdQuery.cs
```

### Handlers

```
{Action}{Entity}CommandHandler.cs
Get{Entity}{Criteria}QueryHandler.cs

Examples:
Create{Entity}CommandHandler.cs
Get{Entity}ByIdQueryHandler.cs
```

### Responses

```
Create{Entity}Response.cs
{Entity}Response.cs
{Entity}SummaryResponse.cs

Examples:
Create{Entity}Response.cs
{Entity}Response.cs
{Entity}SummaryResponse.cs
```

### Endpoints

```
{Entities}Endpoints.cs

Examples:
{Entities}Endpoints.cs
{ChildEntities}Endpoints.cs
```


## Database

- **Schema:** `{applicationname}`, set once in `DataContext.OnModelCreating` with `HasDefaultSchema`. The migrations history sits in the `system` schema.
- **Tables:** lower-case plural, set in the entity configuration with `ToTable`.
- **Columns:** the property names. No snake_case mapping is applied by default.
- **Configuration:** `IEntityTypeConfiguration<T>` in its own file beside the entity.

```csharp
// {ApplicationName}.Entities/{Entity}.cs
public class {Entity}
{
    public Guid {Entity}Id { get; set; }
    public string Name { get; set; } = string.Empty;
}

// {ApplicationName}.Entities/{Entity}Configuration.cs
builder.ToTable("{entities}");
builder.HasKey(e => e.{Entity}Id);
builder.Property(e => e.Name).IsRequired().HasMaxLength(100);
```

## API Endpoints

### Route Patterns

```
POST   /{entities}            # Create
GET    /{entities}/{id}       # Read single
GET    /{entities}            # Read list
PUT    /{entities}/{id}       # Update
DELETE /{entities}/{id}       # Delete

Examples:
POST   /{entities}
GET    /{entities}/123e4567-e89b-12d3-a456-426614174000
GET    /{entities}
PUT    /{entities}/123e4567-e89b-12d3-a456-426614174000
DELETE /{entities}/123e4567-e89b-12d3-a456-426614174000
```

### Versioning

The API is versioned with the `api-version` query string (default `1.0`). Routes carry no version segment.

```
GET /{entities}?api-version=1.0
```

## Test Naming

### MSTest

```csharp
[TestMethod]
public async Task HandleAsync_{Scenario}_{ExpectedResult}()

Examples:
[TestMethod]
public async Task HandleAsync_ValidCommand_Creates{Entity}Successfully()

[TestMethod]
public async Task HandleAsync_NullCommand_ThrowsArgumentNullException()

[TestMethod]
public async Task HandleAsync_NegativeAmount_ThrowsArgumentException()
```

### Reqnroll Features

```
{Entity}Management.feature

Examples:
{Entity}Management.feature
{ChildEntity}Management.feature
```

### Step Definitions

```
{Entity}ManagementSteps.cs

Examples:
{Entity}ManagementSteps.cs
{ChildEntity}ManagementSteps.cs
```

## Method Naming

### Command/Query Handlers

```csharp
// Always: HandleAsync
public async Task<TResponse> HandleAsync(
    TCommand command,
    CancellationToken cancellationToken = default)

// Examples
public async Task<Create{Entity}Response> HandleAsync(
    Create{Entity}Command command,
    CancellationToken cancellationToken = default)
```

### Data Access (EF Core Primitives)

```csharp
// Use named DbSet properties on IDataContext directly — no repositories, no extension methods
// Create
dataContext.{Entities}.Add(entity);
await dataContext.SaveChangesAsync(cancellationToken);

// Read single
var entity = await dataContext.{Entities}.FirstOrDefaultAsync(e => e.{Entity}Id == id, cancellationToken);

// Read list
var entities = await dataContext.{Entities}.OrderBy(e => e.Description).ToListAsync(cancellationToken);

// Update — property mutation on tracked entity, no .Update() call needed
entity.Description = command.Description;
await dataContext.SaveChangesAsync(cancellationToken);

// Delete — lookup first, null-check, then remove; validate rowsAffected
var entityToDelete = await dataContext.{Entities}.FirstOrDefaultAsync(e => e.{Entity}Id == id, cancellationToken);
if (entityToDelete is null) return NotFoundResponse();
dataContext.{Entities}.Remove(entityToDelete);
var rowsAffected = await dataContext.SaveChangesAsync(cancellationToken);
if (rowsAffected == 0) return FailureResponse();
```

## Variable Naming

### Local Variables

```csharp
// camelCase, descriptive
var {entity}Model = ...;
var created{Entity} = ...;
var userId = ...;

// NOT abbreviated
var bm = ...;  // ❌ Bad
var b = ...;   // ❌ Bad
```

### Parameters

```csharp
// camelCase, descriptive
public async Task DoSomething(
    Guid {entity}Id,
    string userName,
    CancellationToken cancellationToken)
```

### Private Fields

```csharp
// _camelCase with underscore prefix
private readonly IDataContext _dataContext;
private readonly ILogger<Create{Entity}CommandHandler> _logger;
```

## Constants and Enums

### Constants

```csharp
// PascalCase
public const int Max{Entity}NameLength = 100;
public const decimal Minimum{Entity}Amount = 0.01m;
```

### Enums

```csharp
// Type and values both PascalCase
public enum {Entity}Status
{
    Active,
    Inactive,
    Archived
}

// Usage
var status = {Entity}Status.Active;
```

## Event Naming

```csharp
{Entity}{Action}Event

Examples:
{Entity}CreatedEvent
{Entity}UpdatedEvent
{Entity}DeletedEvent
{ChildEntity}AchievedEvent
{ChildEntity}ArchivedEvent
```

## Anti-Patterns to Avoid

```csharp
// ❌ Avoid abbreviations
var bgt = ...;
var usrId = ...;

// ✅ Use full names
var {entity} = ...;
var userId = ...;

// ❌ Avoid generic names
var data = ...;
var temp = ...;
var item = ...;

// ✅ Use specific names
var {entity}Model = ...;
var created{Entity} = ...;
var active{Entity} = ...;

// ❌ Avoid Hungarian notation
string strName = ...;
int intCount = ...;

// ✅ Use clear, typed names
string name = ...;
int count = ...;
```
