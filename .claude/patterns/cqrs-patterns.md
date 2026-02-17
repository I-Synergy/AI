# CQRS Implementation Patterns

Complete patterns for implementing Command Query Responsibility Segregation.

## Core Concepts

### CQRS Separation

- **Commands** - Change system state (Create, Update, Delete)
- **Queries** - Read data without side effects (Get, List, Search)
- **Handlers** - Execute commands/queries
- **Responses** - Return data from handlers

### Key Principles

1. Commands use **individual primitive parameters** (NOT model objects, NOT entities)
2. Queries use **named parameters** for optional filters
3. Handlers inject **DataContext directly** (NO repository layer)
4. **Never expose** domain entities in public APIs — not as parameters, not as return values
5. One handler per command/query (Single Responsibility)
6. **Data access** uses `<TEntity, TModel>` pattern for reads (`GetItemByIdAsync<TEntity, TModel, TId>`)
7. **Mapping flow**: Command → Entity (write) | Entity → Model → Response DTO (read)
8. Entities are used **internally** for domain logic and persistence — never passed across layer boundaries

---

## Command Patterns

### Create Command

```csharp
// File: {ApplicationName}.Domain.{Domain}/Features/{Entity}/Commands/Create{Entity}Command.cs

namespace {ApplicationName}.Domain.{Domain}.Features.{Entity}.Commands;

using System.ComponentModel.DataAnnotations;

/// <summary>
/// Command to create a new {entity}.
/// </summary>
public sealed record Create{Entity}Command(
    [Required]
    [StringLength(100, MinimumLength = 3)]
    string Property1,

    [Range(0.01, double.MaxValue)]
    decimal Property2,

    DateTimeOffset Property3
) : ICommand<Create{Entity}Response>, IValidatableObject
{
    /// <summary>
    /// Validates the command.
    /// </summary>
    public IEnumerable<ValidationResult> Validate(ValidationContext validationContext)
    {
        if (Property3 > DateTimeOffset.UtcNow.AddYears(1))
        {
            yield return new ValidationResult(
                "Property3 cannot be more than 1 year in the future",
                new[] { nameof(Property3) });
        }
    }
}

/// <summary>
/// Response containing the created {entity} identifier.
/// </summary>
public sealed record Create{Entity}Response(Guid {Entity}Id);
```

### Update Command

```csharp
// File: {ApplicationName}.Domain.{Domain}/Features/{Entity}/Commands/Update{Entity}Command.cs

namespace {ApplicationName}.Domain.{Domain}.Features.{Entity}.Commands;

using System.ComponentModel.DataAnnotations;

/// <summary>
/// Command to update an existing {entity}.
/// </summary>
public sealed record Update{Entity}Command(
    [Required]
    Guid {Entity}Id,

    [Required]
    [StringLength(100, MinimumLength = 3)]
    string Property1,

    [Range(0.01, double.MaxValue)]
    decimal Property2
) : ICommand<Update{Entity}Response>;

/// <summary>
/// Response for the update operation.
/// </summary>
public sealed record Update{Entity}Response(
    bool Success,
    DateTimeOffset UpdatedAt
);
```

### Delete Command

```csharp
// File: {ApplicationName}.Domain.{Domain}/Features/{Entity}/Commands/Delete{Entity}Command.cs

namespace {ApplicationName}.Domain.{Domain}.Features.{Entity}.Commands;

using System.ComponentModel.DataAnnotations;

/// <summary>
/// Command to delete an existing {entity}.
/// </summary>
public sealed record Delete{Entity}Command(
    [Required]
    Guid {Entity}Id
) : ICommand<Delete{Entity}Response>;

/// <summary>
/// Response for the delete operation.
/// </summary>
public sealed record Delete{Entity}Response(bool Success);
```

---

## Query Patterns

### Get By ID Query

```csharp
// File: {ApplicationName}.Domain.{Domain}/Features/{Entity}/Queries/Get{Entity}ByIdQuery.cs

namespace {ApplicationName}.Domain.{Domain}.Features.{Entity}.Queries;

using System.ComponentModel.DataAnnotations;

/// <summary>
/// Query to retrieve a {entity} by its identifier.
/// </summary>
public sealed record Get{Entity}ByIdQuery(
    [Required]
    Guid {Entity}Id
) : IQuery<{Entity}Response>;

/// <summary>
/// Response containing {entity} details.
/// </summary>
public sealed record {Entity}Response(
    Guid {Entity}Id,
    string Property1,
    decimal Property2,
    DateTimeOffset Property3,
    DateTimeOffset CreatedDate,
    DateTimeOffset? ChangedDate
);
```

### Get List Query

```csharp
// File: {ApplicationName}.Domain.{Domain}/Features/{Entity}/Queries/Get{Entity}ListQuery.cs

namespace {ApplicationName}.Domain.{Domain}.Features.{Entity}.Queries;

/// <summary>
/// Query to retrieve a paginated list of {entities}.
/// </summary>
public sealed record Get{Entity}ListQuery(
    int PageNumber = 1,
    int PageSize = 20,
    string? SearchTerm = null
) : IQuery<List<{Entity}SummaryResponse>>;

/// <summary>
/// Summary response for list operations.
/// </summary>
public sealed record {Entity}SummaryResponse(
    Guid {Entity}Id,
    string Property1,
    decimal Property2
);
```

### Query with Optional Filters

```csharp
/// <summary>
/// Query to get total amount with optional filters.
/// </summary>
public sealed record Get{Entity}TotalAmountQuery(
    Guid? Filter1Id = null,
    Guid? Filter2Id = null,
    DateTimeOffset? StartDate = null,
    DateTimeOffset? EndDate = null
) : IQuery<decimal>;

// Usage with named parameters
var query = new Get{Entity}TotalAmountQuery(Filter1Id: id);
var query = new Get{Entity}TotalAmountQuery(Filter2Id: id);
var query = new Get{Entity}TotalAmountQuery(StartDate: start, EndDate: end);
```

---

## Handler Patterns

### Create Handler

```csharp
// File: {ApplicationName}.Domain.{Domain}/Features/{Entity}/Commands/Create{Entity}Handler.cs

namespace {ApplicationName}.Domain.{Domain}.Features.{Entity}.Commands;

using Mapster;
using Microsoft.Extensions.Logging;

/// <summary>
/// Handles the creation of a new {entity}.
/// </summary>
public sealed class Create{Entity}Handler(
    DataContext dataContext,
    ILogger<Create{Entity}Handler> logger
) : ICommandHandler<Create{Entity}Command, Create{Entity}Response>
{
    /// <summary>
    /// Handles the <see cref="Create{Entity}Command"/> asynchronously.
    /// </summary>
    public async Task<Create{Entity}Response> HandleAsync(
        Create{Entity}Command command,
        CancellationToken cancellationToken = default)
    {
        // Guard clauses
        ArgumentNullException.ThrowIfNull(command);
        ArgumentException.ThrowIfNullOrWhiteSpace(command.Property1, nameof(command.Property1));

        if (command.Property2 <= 0)
            throw new ArgumentException("Property2 must be positive", nameof(command.Property2));

        logger.LogInformation(
            "Creating {EntityType} with Property1: {Property1}",
            nameof({Entity}), command.Property1);

        // Create entity directly from command properties
        var entity = new Entities.{Domain}.{Entity}
        {
            {Entity}Id = Guid.NewGuid(),
            Property1 = command.Property1,
            Property2 = command.Property2,
            Property3 = command.Property3
        };

        dataContext.Add(entity);
        var rowsAffected = await dataContext.SaveChangesAsync(cancellationToken);

        if (rowsAffected == 0)
            throw new InvalidOperationException($"Failed to create {nameof({Entity})}");

        logger.LogInformation(
            "Created {EntityType} with ID: {EntityId}",
            nameof({Entity}), entity.{Entity}Id);

        return new Create{Entity}Response(entity.{Entity}Id);
    }
}
```

### Update Handler

```csharp
// File: {ApplicationName}.Domain.{Domain}/Features/{Entity}/Commands/Update{Entity}Handler.cs

namespace {ApplicationName}.Domain.{Domain}.Features.{Entity}.Commands;

using Mapster;
using Microsoft.Extensions.Logging;

/// <summary>
/// Handles updating an existing {entity}.
/// </summary>
public sealed class Update{Entity}Handler(
    DataContext dataContext,
    ILogger<Update{Entity}Handler> logger
) : ICommandHandler<Update{Entity}Command, Update{Entity}Response>
{
    /// <summary>
    /// Handles the <see cref="Update{Entity}Command"/> asynchronously.
    /// </summary>
    public async Task<Update{Entity}Response> HandleAsync(
        Update{Entity}Command command,
        CancellationToken cancellationToken = default)
    {
        ArgumentNullException.ThrowIfNull(command);

        logger.LogInformation(
            "Updating {EntityType} with ID: {EntityId}",
            nameof({Entity}), command.{Entity}Id);

        // Retrieve existing entity to ensure it exists
        var existing = await dataContext.GetItemByIdAsync<{Entity}, {Entity}Model, Guid>(
            command.{Entity}Id,
            cancellationToken);

        // Map command to entity, preserving ID
        var entity = command.Adapt<{Entity}>();
        entity.{Entity}Id = command.{Entity}Id;
        entity.ChangedDate = DateTimeOffset.UtcNow;

        // Update
        var model = entity.Adapt<{Entity}Model>();
        await dataContext.UpdateItemAsync<{Entity}, {Entity}Model>(
            model,
            cancellationToken);

        logger.LogInformation(
            "Updated {EntityType} with ID: {EntityId}",
            nameof({Entity}), command.{Entity}Id);

        return new Update{Entity}Response(true, DateTimeOffset.UtcNow);
    }
}
```

### Delete Handler

```csharp
// File: {ApplicationName}.Domain.{Domain}/Features/{Entity}/Commands/Delete{Entity}Handler.cs

namespace {ApplicationName}.Domain.{Domain}.Features.{Entity}.Commands;

using Microsoft.Extensions.Logging;

/// <summary>
/// Handles deleting an existing {entity}.
/// </summary>
public sealed class Delete{Entity}Handler(
    DataContext dataContext,
    ILogger<Delete{Entity}Handler> logger
) : ICommandHandler<Delete{Entity}Command, Delete{Entity}Response>
{
    /// <summary>
    /// Handles the <see cref="Delete{Entity}Command"/> asynchronously.
    /// </summary>
    public async Task<Delete{Entity}Response> HandleAsync(
        Delete{Entity}Command command,
        CancellationToken cancellationToken = default)
    {
        ArgumentNullException.ThrowIfNull(command);

        logger.LogInformation(
            "Deleting {EntityType} with ID: {EntityId}",
            nameof({Entity}), command.{Entity}Id);

        // CRITICAL: Use RemoveItemAsync, NOT DeleteItemByIdAsync
        await dataContext.RemoveItemAsync<{Entity}, Guid>(
            command.{Entity}Id,
            cancellationToken);

        logger.LogInformation(
            "Deleted {EntityType} with ID: {EntityId}",
            nameof({Entity}), command.{Entity}Id);

        return new Delete{Entity}Response(true);
    }
}
```

### Get By ID Handler

```csharp
// File: {ApplicationName}.Domain.{Domain}/Features/{Entity}/Queries/Get{Entity}ByIdHandler.cs

namespace {ApplicationName}.Domain.{Domain}.Features.{Entity}.Queries;

using Mapster;
using Microsoft.Extensions.Logging;

/// <summary>
/// Handles retrieving a {entity} by its identifier.
/// </summary>
public sealed class Get{Entity}ByIdHandler(
    DataContext dataContext,
    ILogger<Get{Entity}ByIdHandler> logger
) : IQueryHandler<Get{Entity}ByIdQuery, {Entity}Response>
{
    /// <summary>
    /// Handles the <see cref="Get{Entity}ByIdQuery"/> asynchronously.
    /// </summary>
    public async Task<{Entity}Response> HandleAsync(
        Get{Entity}ByIdQuery query,
        CancellationToken cancellationToken = default)
    {
        ArgumentNullException.ThrowIfNull(query);

        logger.LogDebug(
            "Retrieving {EntityType} with ID: {EntityId}",
            nameof({Entity}), query.{Entity}Id);

        var model = await dataContext.GetItemByIdAsync<{Entity}, {Entity}Model, Guid>(
            query.{Entity}Id,
            cancellationToken);

        logger.LogDebug(
            "Retrieved {EntityType} with ID: {EntityId}",
            nameof({Entity}), query.{Entity}Id);

        return model.Adapt<{Entity}Response>();
    }
}
```

### Get List Handler

```csharp
// File: {ApplicationName}.Domain.{Domain}/Features/{Entity}/Queries/Get{Entity}ListHandler.cs

namespace {ApplicationName}.Domain.{Domain}.Features.{Entity}.Queries;

using Mapster;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;

/// <summary>
/// Handles retrieving a paginated list of {entities}.
/// </summary>
public sealed class Get{Entity}ListHandler(
    DataContext dataContext,
    ILogger<Get{Entity}ListHandler> logger
) : IQueryHandler<Get{Entity}ListQuery, List<{Entity}SummaryResponse>>
{
    /// <summary>
    /// Handles the <see cref="Get{Entity}ListQuery"/> asynchronously.
    /// </summary>
    public async Task<List<{Entity}SummaryResponse>> HandleAsync(
        Get{Entity}ListQuery query,
        CancellationToken cancellationToken = default)
    {
        ArgumentNullException.ThrowIfNull(query);

        logger.LogDebug(
            "Retrieving {EntityType} list - Page: {PageNumber}, Size: {PageSize}",
            nameof({Entity}), query.PageNumber, query.PageSize);

        var queryable = dataContext.Set<{Entity}>().AsQueryable();

        // Apply search filter if provided
        if (!string.IsNullOrWhiteSpace(query.SearchTerm))
        {
            queryable = queryable.Where(e =>
                e.Property1.Contains(query.SearchTerm));
        }

        // Apply pagination
        var entities = await queryable
            .OrderByDescending(e => e.CreatedDate)
            .Skip((query.PageNumber - 1) * query.PageSize)
            .Take(query.PageSize)
            .ToListAsync(cancellationToken);

        logger.LogDebug(
            "Retrieved {Count} {EntityType} records",
            entities.Count, nameof({Entity}));

        return entities.Adapt<List<{Entity}SummaryResponse>>();
    }
}
```

---

## Data Access Patterns

### Available Extension Methods

```csharp
// Create — write entity directly, never via Model
dataContext.Add(entity);
var rowsAffected = await dataContext.SaveChangesAsync(cancellationToken);

// Read — uses <TEntity, TModel> pattern; Mapster maps Entity → Model
var model = await dataContext.GetItemByIdAsync<TEntity, TModel, TKey>(id, cancellationToken);

// Update
await dataContext.UpdateItemAsync<TEntity, TModel>(model, cancellationToken);

// Delete - CRITICAL: Use RemoveItemAsync, not DeleteItemByIdAsync
await dataContext.RemoveItemAsync<TEntity, TKey>(id, cancellationToken);

// List/Query - Use LINQ directly on DbSet
var entities = await dataContext.Set<TEntity>()
    .Where(x => x.IsActive)
    .ToListAsync(cancellationToken);
```

### Complex Query Example

```csharp
public async Task<List<{Entity}SummaryResponse>> HandleAsync(
    Get{Entity}sByFilterQuery query,
    CancellationToken cancellationToken = default)
{
    var queryable = dataContext.Set<{Entity}>()
        .Include(e => e.RelatedEntities) // Prevent N+1
        .AsQueryable();

    // Apply filters
    if (query.Filter1Id.HasValue)
        queryable = queryable.Where(e => e.Filter1Id == query.Filter1Id.Value);

    if (query.StartDate.HasValue)
        queryable = queryable.Where(e => e.CreatedDate >= query.StartDate.Value);

    if (!string.IsNullOrWhiteSpace(query.SearchTerm))
        queryable = queryable.Where(e => e.Name.Contains(query.SearchTerm));

    // Execute and map
    var entities = await queryable
        .OrderBy(e => e.Name)
        .ToListAsync(cancellationToken);

    return entities.Adapt<List<{Entity}SummaryResponse>>();
}
```

---

## Response Patterns

### When to Use Each Response Type

| Scenario | Response Type | Example |
|----------|---------------|---------|
| **Create operation** | Return ID only | `CreateBudgetResponse(Guid BudgetId)` |
| **Update operation** | Return success + metadata | `UpdateBudgetResponse(bool Success, DateTimeOffset UpdatedAt)` |
| **Delete operation** | Return success only | `DeleteBudgetResponse(bool Success)` |
| **Get by ID** | Return full object | `BudgetResponse` with all properties |
| **List query** | Return collection of summaries | `List<BudgetSummaryResponse>` |
| **Aggregate query** | Return calculated value | `decimal` (total amount) |

### Response Examples

```csharp
// Minimal - Just ID for Create
public sealed record CreateBudgetResponse(Guid BudgetId);

// Moderate - Success + metadata for Update
public sealed record UpdateBudgetResponse(
    bool Success,
    Guid BudgetId,
    DateTimeOffset UpdatedAt
);

// Full - Complete object for Get
public sealed record BudgetResponse(
    Guid BudgetId,
    string Name,
    decimal Amount,
    DateTimeOffset StartDate,
    DateTimeOffset CreatedDate,
    int GoalsCount,
    decimal TotalAllocated
);

// Summary - Lightweight for Lists
public sealed record BudgetSummaryResponse(
    Guid BudgetId,
    string Name,
    decimal Amount
);

// Aggregate - Single value for calculations
// Return type: decimal, int, bool, etc. (no wrapper record needed)
```

---

## Validation Patterns

### Data Annotations

```csharp
public sealed record Create{Entity}Command(
    [Required]
    [StringLength(100, MinimumLength = 3)]
    string Property1,

    [Range(0.01, double.MaxValue)]
    decimal Property2,

    [EmailAddress]
    string? Email,

    [Url]
    string? Website
) : ICommand<Create{Entity}Response>;
```

### Custom Validation (IValidatableObject)

```csharp
public sealed record Create{Entity}Command(
    [Required] string Property1,
    [Range(0.01, double.MaxValue)] decimal Property2,
    DateTimeOffset Property3
) : ICommand<Create{Entity}Response>, IValidatableObject
{
    public IEnumerable<ValidationResult> Validate(ValidationContext validationContext)
    {
        if (Property3 <= DateTimeOffset.UtcNow)
        {
            yield return new ValidationResult(
                "Property3 must be in the future",
                new[] { nameof(Property3) });
        }

        if (Property2 > 1_000_000m)
        {
            yield return new ValidationResult(
                "Property2 exceeds maximum allowed value",
                new[] { nameof(Property2) });
        }
    }
}
```

### Handler Guard Clauses

```csharp
public async Task<Create{Entity}Response> HandleAsync(
    Create{Entity}Command command,
    CancellationToken cancellationToken = default)
{
    // Guard clauses at method start
    ArgumentNullException.ThrowIfNull(command);
    ArgumentException.ThrowIfNullOrWhiteSpace(command.Property1, nameof(command.Property1));

    if (command.Property2 <= 0)
        throw new ArgumentException("Property2 must be positive", nameof(command.Property2));

    // Main logic follows
}
```

---

## Service Registration

```csharp
// File: {ApplicationName}.Domain.{Domain}/Extensions/ServiceCollectionExtensions.cs

namespace {ApplicationName}.Domain.{Domain}.Extensions;

using Mapster;
using Microsoft.Extensions.DependencyInjection;

/// <summary>
/// Service collection extensions for {Domain} domain.
/// </summary>
public static class ServiceCollectionExtensions
{
    /// <summary>
    /// Registers {Domain} domain handlers and mappers.
    /// </summary>
    public static IServiceCollection With{Domain}DomainHandlers(
        this IServiceCollection services)
    {
        var assembly = typeof(ServiceCollectionExtensions).Assembly;

        // Register Mapster configurations
        var mappingConfigs = TypeAdapterConfig.GlobalSettings.Scan(assembly);
        TypeAdapterConfig.GlobalSettings.Apply(mappingConfigs);

        // Register CQRS handlers
        services.AddCQRS().AddHandlers(assembly);

        return services;
    }
}
```

---

## Common Pitfalls

### ❌ Wrong: Passing Model Objects

```csharp
// WRONG
public sealed record CreateDebtCommand(DebtModel Debt) : ICommand<CreateDebtResponse>;

// CORRECT
public sealed record CreateDebtCommand(
    Guid BudgetId,
    string Description,
    decimal Amount
) : ICommand<CreateDebtResponse>;
```

### ❌ Wrong: Using Wrong Delete Method

```csharp
// WRONG - This method doesn't exist
await dataContext.DeleteItemByIdAsync<Debt, Guid>(id, ct);

// CORRECT
await dataContext.RemoveItemAsync<Debt, Guid>(id, ct);
```

### ❌ Wrong: Positional Optional Parameters

```csharp
// WRONG - Ambiguous
var query = new GetTotalQuery(id, true);

// CORRECT - Named parameters
var query = new GetTotalQuery(BudgetId: id);
var query = new GetTotalQuery(GoalId: id);
```

### ❌ Wrong: Exposing Domain Entities

```csharp
// WRONG - Returns domain entity
public async Task<Budget> HandleAsync(...)
{
    return entity;
}

// CORRECT - Returns DTO
public async Task<BudgetResponse> HandleAsync(...)
{
    return model.Adapt<BudgetResponse>();
}
```
