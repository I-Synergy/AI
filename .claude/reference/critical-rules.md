# Critical Rules (Read First)

These are non-negotiable patterns that cause bugs if violated.

## 1. Commands: Individual Parameters Only

**NEVER pass model objects to commands.**

```csharp
✅ CORRECT - Individual parameters
public sealed record CreateDebtCommand(
    Guid BudgetId,
    string Description,
    decimal Amount
) : ICommand<CreateDebtResponse>;

❌ WRONG - Passing model object
public sealed record CreateDebtCommand(
    DebtModel Debt
) : ICommand<CreateDebtResponse>;
```

### Endpoint Construction

```csharp
✅ CORRECT - Extract properties from model
app.MapPost("/debts", async (DebtModel model, ICommandHandler handler) =>
{
    var command = new CreateDebtCommand(model.BudgetId, model.Description, model.Amount);
    return await handler.HandleAsync(command);
});

❌ WRONG - Passing model directly
var command = new CreateDebtCommand(model);
```

## 2. Delete Operations: Use RemoveItemAsync

```csharp
✅ CORRECT
await dataContext.RemoveItemAsync<Debt, Guid>(id, cancellationToken);

❌ WRONG - This method doesn't exist
await dataContext.DeleteItemByIdAsync<Debt, Guid>(id, cancellationToken);
```

## 3. Query Parameters: Use Named Parameters

For optional filters, always use named parameters to avoid ambiguity.

```csharp
✅ CORRECT - Named parameters prevent ambiguity
var query = new GetDepositsTotalAmountQuery(GoalId: id);
var query = new GetDepositsTotalAmountQuery(BudgetId: id);

❌ WRONG - Positional parameters are ambiguous
var query = new GetDepositsTotalAmountQuery(id, true);
```

## 4. Data Access: Use DataContext Extension Methods

**NO explicit Repository interfaces.** Use EF Core extension methods directly.

```csharp
✅ CORRECT
await dataContext.AddItemAsync<Budget, BudgetModel>(model, ct);
await dataContext.GetItemByIdAsync<Budget, BudgetModel, Guid>(id, ct);
await dataContext.UpdateItemAsync<Budget, BudgetModel>(model, ct);
await dataContext.RemoveItemAsync<Budget, Guid>(id, ct);

❌ WRONG - We don't use repositories
await _repository.Add(model);
await _budgetRepository.GetByIdAsync(id);
```

## 5. Mapping: Mapster Only

Always configure mappings in `{Entity}MappingConfig.cs`.

```csharp
✅ CORRECT - Mapster with configuration
var model = entity.Adapt<BudgetModel>();

❌ WRONG - AutoMapper
var model = _mapper.Map<BudgetModel>(entity);

❌ WRONG - Manual mapping
var model = new BudgetModel {
    BudgetId = entity.BudgetId,
    Name = entity.Name,
    // ... manual property assignment
};
```

## 6. Async: Always Include CancellationToken

```csharp
✅ CORRECT
public async Task<BudgetResponse> HandleAsync(
    GetBudgetByIdQuery query,
    CancellationToken cancellationToken = default)
{
    var budget = await dataContext.GetItemByIdAsync<Budget, BudgetModel, Guid>(
        query.BudgetId,
        cancellationToken);
    return budget.Adapt<BudgetResponse>();
}

❌ WRONG - Blocking on async
public BudgetResponse Handle(GetBudgetByIdQuery query)
{
    var budget = dataContext.GetItemByIdAsync<Budget, BudgetModel, Guid>(
        query.BudgetId,
        CancellationToken.None).Result; // DEADLOCK RISK!
    return budget.Adapt<BudgetResponse>();
}

❌ WRONG - No CancellationToken
public async Task<BudgetResponse> HandleAsync(GetBudgetByIdQuery query)
{
    // Missing cancellation support
}
```

## 7. Entity Exposure: NEVER Expose Domain Entities

Always map to DTOs/Models before returning from handlers or APIs.

```csharp
✅ CORRECT - Return DTO
public async Task<BudgetResponse> HandleAsync(...)
{
    var model = await dataContext.GetItemByIdAsync<Budget, BudgetModel, Guid>(...);
    return model.Adapt<BudgetResponse>(); // DTO
}

❌ WRONG - Return domain entity
public async Task<Budget> HandleAsync(...)
{
    var entity = await dataContext.Set<Budget>().FindAsync(id);
    return entity; // Exposes domain entity
}
```

## 8. Progress Files: Current Solution Only

Progress files MUST be in the current solution's `.claude/` folder.

```bash
✅ CORRECT
.claude/progress/task-progress.md

❌ WRONG - User profile directory
~/.claude/progress/task-progress.md

❌ WRONG - Different solution
/other/solution/.claude/progress/task-progress.md
```

## 9. Session Context: Read First, Update Last

Every session MUST:

```bash
✅ CORRECT
1. Read .claude/session-context.md FIRST
2. Build on established patterns
3. Update session-context.md with learnings before ending

❌ WRONG
1. Ignore session context
2. Re-ask questions already documented
3. Contradict established patterns
```

## 10. Guard Clauses: All Public Methods

```csharp
✅ CORRECT
public async Task<CreateBudgetResponse> HandleAsync(
    CreateBudgetCommand command,
    CancellationToken cancellationToken = default)
{
    ArgumentNullException.ThrowIfNull(command);
    ArgumentException.ThrowIfNullOrWhiteSpace(command.Name, nameof(command.Name));

    if (command.Amount <= 0)
        throw new ArgumentException("Amount must be positive", nameof(command.Amount));

    // Main logic
}

❌ WRONG - No validation
public async Task<CreateBudgetResponse> HandleAsync(
    CreateBudgetCommand command,
    CancellationToken cancellationToken = default)
{
    // Directly use command without validation - CRASH RISK
    var entity = command.Adapt<Budget>();
}
```

## Quick Violation Checklist

Before submitting code, verify you haven't violated these:

- [ ] Commands use individual parameters (not model objects)
- [ ] Delete operations use `RemoveItemAsync<TEntity, TKey>()`
- [ ] Queries use named parameters for optional filters
- [ ] Data access uses DataContext extensions (no repositories)
- [ ] Mapping uses Mapster (not AutoMapper or manual)
- [ ] All async methods include CancellationToken
- [ ] Domain entities never exposed directly (always DTOs)
- [ ] Progress files in current solution's `.claude/` folder
- [ ] Session context read first and updated last
- [ ] Guard clauses on all public methods
