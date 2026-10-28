# Naming Conventions

## C# Code

| Element | Convention | Example |
|---------|-----------|----------|
| **Namespace** | `{ApplicationName}.{Layer}.{Domain}` | `{ApplicationName}.Domain.{Domain}` |
| **Command** | `{Action}{Entity}Command` | `Create{Entity}Command` |
| **Query** | `Get{Entity}{Criteria}Query` | `Get{Entity}ByIdQuery` |
| **Handler** | `{Action}{Entity}CommandHandler` / `Get{Entity}{Criteria}QueryHandler` | `Create{Entity}CommandHandler` |
| **Response** | `{Action}{Entity}Response` | `Create{Entity}Response` |
| **DTO / Model** | `{Entity}` (no suffix) | `{Entity}` |
| **Interface** | `I{Type}` | `ICommandHandler<T>` |
| **Classes** | PascalCase | `{Entity}Endpoints` |
| **Methods** | PascalCase + `Async` suffix | `Get{Entity}ByIdAsync` |
| **Properties** | PascalCase | `{Entity}Id`, `CreatedDate` |
| **Private fields** | `_camelCase` | `_dataContext`, `_logger` |
| **Parameters/locals** | camelCase | `{entity}Id`, `cancellationToken` |
| **Constants** | PascalCase | `Max{Entity}Amount` |
| **Enums** | PascalCase (type and values) | `{Entity}Status.Active` |

## Namespace Patterns

```csharp
// Domain layer
{ApplicationName}.Domain.{Domain}
{ApplicationName}.Domain.{Domain}.Features.{Entity}.Commands
{ApplicationName}.Domain.{Domain}.Features.{Entity}.Queries
{ApplicationName}.Domain.{Domain}.Features.{Entity}.Events

// Application layer
{ApplicationName}.Services.{Domain}
{ApplicationName}.Services.{Domain}.Endpoints

// Infrastructure layer
{ApplicationName}.Entities.{Domain}
{ApplicationName}.Models.{Domain}
{ApplicationName}.Data

// Examples
{ApplicationName}.Domain.{Domain}
{ApplicationName}.Domain.{Domain}.Features.{Entity}.Commands
{ApplicationName}.Services.{Domain}.Endpoints
{ApplicationName}.Entities.{Domain}
```

## File Naming

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
{Entity}Endpoints.cs

Examples:
{Entity}Endpoints.cs
{ChildEntity}Endpoints.cs
```


## Database (PostgreSQL)

- **Tables:** snake_case (managed by EF Core conventions)
- **Columns:** snake_case (managed by EF Core conventions)

EF Core automatically handles C# PascalCase to database snake_case conversion.

```csharp
// C# Entity
public class {Entity}
{
    public Guid {Entity}Id { get; set; }
    public string Name { get; set; }
    public decimal TotalAmount { get; set; }
}

// Database table (automatic)
Table: {entities}
Columns: {entity}_id, name, total_amount
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

```
/v1/{entities}
/v2/{entities}

Examples:
/v1/{entities}
/v2/{entities}
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
// Use named DbSet properties on DataContext directly — no repositories, no extension methods
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
private readonly DataContext _dataContext;
private readonly ILogger<Create{Entity}CommandHandler> _logger;
private readonly IMapper _mapper;
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
