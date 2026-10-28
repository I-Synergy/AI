# Service-Oriented Architecture (SOA) Pattern

## Overview

Service-Oriented Architecture is an architectural pattern where functionality is organized as a collection of interoperable services. Each service is a discrete unit of functionality that can be accessed remotely and independently updated.

---

## Core SOA Principles

### 1. Standardized Service Contract

**Definition:** Services adhere to a communications agreement defined by one or more service descriptions.

```csharp
// ✅ CORRECT - Well-defined service contract
namespace {ApplicationName}.Contracts.{Entities};

/// <summary>
/// Service contract for {entity} management operations.
/// </summary>
public interface I{Entity}Service
{
    /// <summary>
    /// Creates a new {entity}.
    /// </summary>
    /// <param name="request">{Entity} creation request.</param>
    /// <param name="ct">Cancellation token.</param>
    /// <returns>Created {entity} response with ID.</returns>
    Task<Create{Entity}Response> Create{Entity}Async(
        Create{Entity}Request request,
        CancellationToken ct = default);

    /// <summary>
    /// Retrieves a {entity} by its identifier.
    /// </summary>
    /// <param name="{entity}Id">The {entity} identifier.</param>
    /// <param name="ct">Cancellation token.</param>
    /// <returns>{Entity} details or null if not found.</returns>
    Task<{Entity}Dto?> Get{Entity}Async(
        Guid {entity}Id,
        CancellationToken ct = default);

    /// <summary>
    /// Updates an existing {entity}.
    /// </summary>
    /// <param name="{entity}Id">The {entity} identifier.</param>
    /// <param name="request">Update request.</param>
    /// <param name="ct">Cancellation token.</param>
    /// <returns>Success indicator.</returns>
    Task<bool> Update{Entity}Async(
        Guid {entity}Id,
        Update{Entity}Request request,
        CancellationToken ct = default);

    /// <summary>
    /// Deletes a {entity}.
    /// </summary>
    /// <param name="{entity}Id">The {entity} identifier.</param>
    /// <param name="ct">Cancellation token.</param>
    /// <returns>Success indicator.</returns>
    Task<bool> Delete{Entity}Async(
        Guid {entity}Id,
        CancellationToken ct = default);
}

// ❌ WRONG - Poorly defined contract
public interface I{Entity}Service
{
    Task<object> DoSomething(Dictionary<string, object> data); // Unclear!
    Task Process(string xml); // String-based, not typed
    {Entity} Get{Entity}(int id); // Synchronous, uses int instead of Guid
}
```

### 2. Service Loose Coupling

**Definition:** Services minimize dependencies on each other.

```csharp
// ✅ CORRECT - Loosely coupled services
namespace {ApplicationName}.Services.{Entities};

public sealed class {Entity}Service : I{Entity}Service
{
    private readonly ICommandHandler<Create{Entity}Command, Create{Entity}Response> _createHandler;
    private readonly IQueryHandler<Get{Entity}ByIdQuery, {Entity}Response> _getHandler;
    private readonly IMapper _mapper;
    private readonly IEventPublisher _eventPublisher; // Only depends on abstraction

    public {Entity}Service(
        ICommandHandler<Create{Entity}Command, Create{Entity}Response> createHandler,
        IQueryHandler<Get{Entity}ByIdQuery, {Entity}Response> getHandler,
        IMapper mapper,
        IEventPublisher eventPublisher)
    {
        _createHandler = createHandler;
        _getHandler = getHandler;
        _mapper = mapper;
        _eventPublisher = eventPublisher;
    }

    public async Task<Create{Entity}Response> Create{Entity}Async(
        Create{Entity}Request request,
        CancellationToken ct = default)
    {
        var command = _mapper.Map<Create{Entity}Command>(request);
        var response = await _createHandler.HandleAsync(command, ct);

        // Publish event for interested services (loose coupling)
        await _eventPublisher.PublishAsync(
            new {Entity}CreatedEvent(response.{Entity}Id, request.Name, request.Amount),
            ct);

        return response;
    }
}

// ❌ WRONG - Tightly coupled service
public sealed class {Entity}Service
{
    private readonly Sql{Entity}Repository _repository; // Tight coupling to specific implementation
    private readonly SmtpEmailSender _emailSender; // Direct dependency
    private readonly {ChildEntity}Service _{childEntity}Service; // Direct service-to-service dependency

    public async Task Create{Entity}Async(Create{Entity}Request request)
    {
        var {entity} = await _repository.SaveAsync(request);

        // Tight coupling - directly calling another service
        await _{childEntity}Service.CreateDefault{ChildEntities}Async({entity}.{Entity}Id);

        // Tight coupling - directly sending email
        await _emailSender.SendAsync("{Entity} created");
    }
}
```

### 3. Service Abstraction

**Definition:** Services hide implementation logic from consumers.

```csharp
// ✅ CORRECT - Well-abstracted service
namespace {ApplicationName}.Services.{Entities};

public sealed class {Entity}CalculationService : I{Entity}CalculationService
{
    private readonly IQueryHandler<Get{Entity}ByIdQuery, {Entity}Response> _getHandler;
    private readonly IQueryHandler<Get{ChildEntities}By{Entity}Query, List<{ChildEntity}Response>> _get{ChildEntities}Handler;
    private readonly ILogger<{Entity}CalculationService> _logger;

    public {Entity}CalculationService(
        IQueryHandler<Get{Entity}ByIdQuery, {Entity}Response> getHandler,
        IQueryHandler<Get{ChildEntities}By{Entity}Query, List<{ChildEntity}Response>> get{ChildEntities}Handler,
        ILogger<{Entity}CalculationService> logger)
    {
        _getHandler = getHandler;
        _get{ChildEntities}Handler = get{ChildEntities}Handler;
        _logger = logger;
    }

    /// <summary>
    /// Calculates remaining {entity} amount.
    /// Consumer doesn't need to know about {childEntities}, allocations, etc.
    /// </summary>
    public async Task<decimal> CalculateRemainingAsync(
        Guid {entity}Id,
        CancellationToken ct = default)
    {
        _logger.LogDebug("Calculating remaining for {entity} {Entity}Id", {entity}Id);

        // Internal complexity hidden from consumer
        var {entity} = await _getHandler.HandleAsync(
            new Get{Entity}ByIdQuery({entity}Id),
            ct);

        var {childEntities} = await _get{ChildEntities}Handler.HandleAsync(
            new Get{ChildEntities}By{Entity}Query({entity}Id),
            ct);

        var allocated = {childEntities}.Sum(g => g.Amount);
        var remaining = {entity}.Amount - allocated;

        _logger.LogDebug(
            "{Entity}Id has {Remaining} remaining",
            {entity}Id, remaining);

        return remaining;
    }
}

// ❌ WRONG - Leaky abstraction exposing internals
public interface I{Entity}CalculationService
{
    Task<decimal> CalculateRemainingAsync(Guid {entity}Id);

    // Exposes internal implementation details
    Task<Dictionary<string, decimal>> GetInternalCalculationCache();
    Task<List<string>> GetDatabaseQueryLog();
    Task SetCachingStrategy(CachingStrategyEnum strategy);
}
```

### 4. Service Reusability

**Definition:** Logic is divided into services with the intention of promoting reuse.

```csharp
// ✅ CORRECT - Reusable service design
namespace {ApplicationName}.Services.Common;

/// <summary>
/// Reusable validation service for multiple domains.
/// </summary>
public interface IValidationService<T>
{
    Task<ValidationResult> ValidateAsync(T item, CancellationToken ct = default);
}

public sealed class {Entity}ValidationService : IValidationService<{Entity}>
{
    private readonly IQueryHandler<Get{Entity}ByIdQuery, {Entity}Response> _getHandler;

    public {Entity}ValidationService(
        IQueryHandler<Get{Entity}ByIdQuery, {Entity}Response> getHandler)
    {
        _getHandler = getHandler;
    }

    public async Task<ValidationResult> ValidateAsync(
        {Entity} {entity},
        CancellationToken ct = default)
    {
        var errors = new List<string>();

        if ({entity}.Amount <= 0)
            errors.Add("Amount must be positive");

        if (string.IsNullOrWhiteSpace({entity}.Name))
            errors.Add("Name is required");

        // Reusable duplicate check
        if (await IsDuplicateAsync({entity}.Name, ct))
            errors.Add("{Entity} name already exists");

        return errors.Count == 0
            ? ValidationResult.Success()
            : ValidationResult.Fail(errors);
    }

    private async Task<bool> IsDuplicateAsync(string name, CancellationToken ct)
    {
        // Reusable duplicate checking logic
        await Task.CompletedTask;
        return false;
    }
}

// Reuse same pattern for other entities
public sealed class {ChildEntity}ValidationService : IValidationService<{ChildEntity}>
{
    public async Task<ValidationResult> ValidateAsync({ChildEntity} {childEntity}, CancellationToken ct = default)
    {
        // Same validation pattern, different rules
        var errors = new List<string>();

        if ({childEntity}.Amount <= 0)
            errors.Add("Target amount must be positive");

        return errors.Count == 0
            ? ValidationResult.Success()
            : ValidationResult.Fail(errors);
    }
}
```

### 5. Service Autonomy

**Definition:** Services have control over the logic they encapsulate.

```csharp
// ✅ CORRECT - Autonomous service with own data store
namespace {ApplicationName}.Services.{Entities};

public sealed class {Entity}Service : I{Entity}Service
{
    private readonly DataContext _dataContext; // Own database context
    private readonly IEventPublisher _eventPublisher;

    public {Entity}Service(DataContext dataContext, IEventPublisher eventPublisher)
    {
        _dataContext = dataContext;
        _eventPublisher = eventPublisher;
    }

    public async Task<Create{Entity}Response> Create{Entity}Async(
        Create{Entity}Request request,
        CancellationToken ct = default)
    {
        // Full autonomy over {entity} creation logic
        var {entity} = new {Entity}
        {
            {Entity}Id = Guid.NewGuid(),
            Name = request.Name,
            Amount = request.Amount,
            CreatedDate = DateTimeOffset.UtcNow
        };

        // Own transaction boundary
        using var transaction = await _dataContext.Database.BeginTransactionAsync(ct);

        try
        {
            _dataContext.{Entities}.Add({entity});
            await _dataContext.SaveChangesAsync(ct);

            await transaction.CommitAsync(ct);

            // Notify other services via events (maintains autonomy)
            await _eventPublisher.PublishAsync(
                new {Entity}CreatedEvent({entity}.{Entity}Id, {entity}.Name, {entity}.Amount),
                ct);

            return new Create{Entity}Response({entity}.{Entity}Id);
        }
        catch
        {
            await transaction.RollbackAsync(ct);
            throw;
        }
    }
}

// ❌ WRONG - Lacks autonomy, depends on external coordination
public sealed class {Entity}Service
{
    private readonly ISharedTransactionManager _transactionManager; // External coordination
    private readonly ISharedDataStore _sharedData; // Shared data store

    public async Task Create{Entity}Async(Create{Entity}Request request)
    {
        // Waiting for external transaction manager
        await _transactionManager.BeginTransactionAsync();

        // Sharing data store with other services
        await _sharedData.SaveAsync(request);

        // Manually coordinating with other services
        await _transactionManager.NotifyServicesAsync("{entity}.created");

        await _transactionManager.CommitAsync();
    }
}
```

### 6. Service Statelessness

**Definition:** Services minimize retained state.

```csharp
// ✅ CORRECT - Stateless service
namespace {ApplicationName}.Services.{Entities};

public sealed class {Entity}Service : I{Entity}Service
{
    private readonly ICommandHandler<Create{Entity}Command, Create{Entity}Response> _createHandler;
    private readonly ILogger<{Entity}Service> _logger;

    public {Entity}Service(
        ICommandHandler<Create{Entity}Command, Create{Entity}Response> createHandler,
        ILogger<{Entity}Service> logger)
    {
        _createHandler = createHandler;
        _logger = logger;
    }

    // Stateless - all state passed via parameters
    public async Task<Create{Entity}Response> Create{Entity}Async(
        Create{Entity}Request request,
        CancellationToken ct = default)
    {
        _logger.LogInformation("Creating {entity} {Name}", request.Name);

        var command = new Create{Entity}Command(
            request.Name,
            request.Amount,
            request.StartDate);

        return await _createHandler.HandleAsync(command, ct);
    }

    // Stateless - retrieves fresh data each call
    public async Task<{Entity}Dto?> Get{Entity}Async(
        Guid {entity}Id,
        CancellationToken ct = default)
    {
        _logger.LogDebug("Retrieving {entity} {Entity}Id", {entity}Id);

        var query = new Get{Entity}ByIdQuery({entity}Id);
        var response = await _getHandler.HandleAsync(query, ct);

        return response.{Entity} is null ? null : new {Entity}Dto(response.{Entity}.{Entity}Id, response.{Entity}.Name, response.{Entity}.Amount);
    }
}

// ❌ WRONG - Stateful service (anti-pattern in SOA)
public sealed class {Entity}Service
{
    private {Entity}? _current{Entity}; // Instance state!
    private readonly List<{Entity}> _cached{Entities} = new(); // Mutable state!

    public async Task<Create{Entity}Response> Create{Entity}Async(Create{Entity}Request request)
    {
        var {entity} = Create{Entity}(request);

        _current{Entity} = {entity}; // Storing state!
        _cached{Entities}.Add({entity}); // Mutating state!

        return new Create{Entity}Response({entity}.{Entity}Id);
    }

    public {Entity}? GetCurrent{Entity}() => _current{Entity}; // Returning instance state!
}
```

### 7. Service Discoverability

**Definition:** Services are designed to be externally discoverable.

```csharp
// ✅ CORRECT - Discoverable service with metadata
namespace {ApplicationName}.Services.{Entities};

[ServiceContract(
    Name = "{Entity}Service",
    Version = "1.0",
    Description = "Provides {entity} management operations")]
public sealed class {Entity}Service : I{Entity}Service
{
    // Service metadata for discovery
    public ServiceMetadata GetMetadata()
    {
        return new ServiceMetadata
        {
            Name = "{Entity}Service",
            Version = "1.0",
            Description = "{Entity} management operations",
            Endpoints = new List<EndpointMetadata>
            {
                new("Create{Entity}", "POST", "/api/{entities}", "Creates a new {entity}"),
                new("Get{Entity}", "GET", "/api/{entities}/{id}", "Retrieves a {entity}"),
                new("Update{Entity}", "PUT", "/api/{entities}/{id}", "Updates a {entity}"),
                new("Delete{Entity}", "DELETE", "/api/{entities}/{id}", "Deletes a {entity}")
            },
            Capabilities = new List<string>
            {
                "Create", "Read", "Update", "Delete", "Calculate"
            }
        };
    }
}

// Service registration for discovery
public static class ServiceCollectionExtensions
{
    public static IServiceCollection Add{Entity}Service(this IServiceCollection services)
    {
        services.AddScoped<I{Entity}Service, {Entity}Service>();

        // Register for service discovery
        services.AddSingleton<IServiceRegistry>(sp =>
        {
            var registry = sp.GetRequiredService<IServiceRegistry>();
            var {entity}Service = sp.GetRequiredService<I{Entity}Service>();

            if ({entity}Service is {Entity}Service service)
            {
                registry.Register(service.GetMetadata());
            }

            return registry;
        });

        return services;
    }
}

public record ServiceMetadata
{
    public string Name { get; init; } = string.Empty;
    public string Version { get; init; } = string.Empty;
    public string Description { get; init; } = string.Empty;
    public List<EndpointMetadata> Endpoints { get; init; } = new();
    public List<string> Capabilities { get; init; } = new();
}

public record EndpointMetadata(
    string Name,
    string Method,
    string Path,
    string Description);
```

---

## Service Communication Patterns

### Message-Based Communication

```csharp
// ✅ CORRECT - Message-based communication
namespace {ApplicationName}.Services.Messaging;

// Message contract
public sealed record {Entity}CreatedMessage
{
    public Guid {Entity}Id { get; init; }
    public string Name { get; init; } = string.Empty;
    public decimal Amount { get; init; }
    public DateTimeOffset CreatedDate { get; init; }
    public string CreatedBy { get; init; } = string.Empty;
}

// Publisher service
public sealed class {Entity}EventPublisher : I{Entity}EventPublisher
{
    private readonly IMessageBus _messageBus;
    private readonly ILogger<{Entity}EventPublisher> _logger;

    public {Entity}EventPublisher(
        IMessageBus messageBus,
        ILogger<{Entity}EventPublisher> logger)
    {
        _messageBus = messageBus;
        _logger = logger;
    }

    public async Task Publish{Entity}CreatedAsync(
        {Entity} {entity},
        CancellationToken ct = default)
    {
        var message = new {Entity}CreatedMessage
        {
            {Entity}Id = {entity}.{Entity}Id,
            Name = {entity}.Name,
            Amount = {entity}.Amount,
            CreatedDate = {entity}.CreatedDate,
            CreatedBy = {entity}.CreatedBy
        };

        _logger.LogInformation(
            "Publishing {Entity}Created message for {Entity}Id",
            {entity}.{Entity}Id);

        await _messageBus.PublishAsync("{entity}.created", message, ct);
    }
}

// Subscriber service
public sealed class NotificationService : IMessageHandler<{Entity}CreatedMessage>
{
    private readonly IEmailService _emailService;
    private readonly ILogger<NotificationService> _logger;

    public NotificationService(
        IEmailService emailService,
        ILogger<NotificationService> logger)
    {
        _emailService = emailService;
        _logger = logger;
    }

    public async Task HandleAsync(
        {Entity}CreatedMessage message,
        CancellationToken ct = default)
    {
        _logger.LogInformation(
            "Handling {Entity}Created message for {Entity}Id",
            message.{Entity}Id);

        await _emailService.SendAsync(
            message.CreatedBy,
            "{Entity} Created",
            $"Your {entity} '{message.Name}' with amount {message.Amount:C} has been created.",
            ct);
    }
}
```

### Request-Reply Pattern

```csharp
// ✅ CORRECT - Request-reply pattern
namespace {ApplicationName}.Services.{Entities};

// Request
public sealed record Calculate{Entity}SummaryRequest
{
    public Guid {Entity}Id { get; init; }
    public bool Include{ChildEntities} { get; init; }
    public bool Include{ChildEntities} { get; init; }
}

// Reply
public sealed record Calculate{Entity}SummaryReply
{
    public Guid {Entity}Id { get; init; }
    public string Name { get; init; } = string.Empty;
    public decimal TotalAmount { get; init; }
    public decimal AllocatedAmount { get; init; }
    public decimal RemainingAmount { get; init; }
    public List<{ChildEntity}Summary> {ChildEntities} { get; init; } = new();
}

// Service implementing request-reply
public sealed class {Entity}QueryService : I{Entity}QueryService
{
    private readonly IQueryHandler<Get{Entity}ByIdQuery, {Entity}Response> _get{Entity}Handler;
    private readonly IQueryHandler<Get{ChildEntities}By{Entity}Query, List<{ChildEntity}Response>> _get{ChildEntities}Handler;

    public {Entity}QueryService(
        IQueryHandler<Get{Entity}ByIdQuery, {Entity}Response> get{Entity}Handler,
        IQueryHandler<Get{ChildEntities}By{Entity}Query, List<{ChildEntity}Response>> get{ChildEntities}Handler)
    {
        _get{Entity}Handler = get{Entity}Handler;
        _get{ChildEntities}Handler = get{ChildEntities}Handler;
    }

    public async Task<Calculate{Entity}SummaryReply> CalculateSummaryAsync(
        Calculate{Entity}SummaryRequest request,
        CancellationToken ct = default)
    {
        var {entity} = await _get{Entity}Handler.HandleAsync(
            new Get{Entity}ByIdQuery(request.{Entity}Id),
            ct);

        var {childEntities} = request.Include{ChildEntities}
            ? await _get{ChildEntities}Handler.HandleAsync(
                new Get{ChildEntities}By{Entity}Query(request.{Entity}Id),
                ct)
            : new List<{ChildEntity}Response>();

        var allocated = {childEntities}.Sum(c => c.Amount);

        return new Calculate{Entity}SummaryReply
        {
            {Entity}Id = {entity}.{Entity}Id,
            Name = {entity}.Name,
            TotalAmount = {entity}.Amount,
            AllocatedAmount = allocated,
            RemainingAmount = {entity}.Amount - allocated,
            {ChildEntities} = {childEntities}
                .Select(c => new {ChildEntity}Summary(c.{ChildEntity}Id, c.Name, c.Amount))
                .ToList()
        };
    }
}
```

---

## Service Orchestration vs Choreography

### Orchestration (Centralized Coordination)

```csharp
// ✅ CORRECT - Service orchestration
namespace {ApplicationName}.Services.Orchestration;

/// <summary>
/// Orchestrator for {entity} creation workflow.
/// Centralized coordination of multiple services.
/// </summary>
public sealed class {Entity}CreationOrchestrator : I{Entity}CreationOrchestrator
{
    private readonly I{Entity}Service _{entity}Service;
    private readonly I{ChildEntity}Service _{childEntity}Service;
    private readonly INotificationService _notificationService;
    private readonly IAuditService _auditService;
    private readonly ILogger<{Entity}CreationOrchestrator> _logger;

    public {Entity}CreationOrchestrator(
        I{Entity}Service {entity}Service,
        I{ChildEntity}Service {childEntity}Service,
        INotificationService notificationService,
        IAuditService auditService,
        ILogger<{Entity}CreationOrchestrator> logger)
    {
        _{entity}Service = {entity}Service;
        _{childEntity}Service = {childEntity}Service;
        _notificationService = notificationService;
        _auditService = auditService;
        _logger = logger;
    }

    public async Task<{Entity}CreationResult> Create{Entity}With{ChildEntities}Async(
        Create{Entity}With{ChildEntities}Request request,
        CancellationToken ct = default)
    {
        _logger.LogInformation(
            "Starting orchestrated {entity} creation for {Entity}Name",
            request.{Entity}Name);

        try
        {
            // Step 1: Create {entity}
            var {entity}Request = new Create{Entity}Request
            {
                Name = request.{Entity}Name,
                Amount = request.Amount,
                StartDate = request.StartDate
            };

            var {entity}Response = await _{entity}Service.Create{Entity}Async({entity}Request, ct);

            // Step 2: Create {childEntities} (sequential orchestration)
            var {childEntity}Ids = new List<Guid>();
            foreach (var {childEntity}Request in request.{ChildEntities})
            {
                var {childEntity}Response = await _{childEntity}Service.Create{ChildEntity}Async(
                    new Create{ChildEntity}Request
                    {
                        {Entity}Id = {entity}Response.{Entity}Id,
                        Name = {childEntity}Request.Name,
                        Amount = {childEntity}Request.Amount
                    },
                    ct);

                {childEntity}Ids.Add({childEntity}Response.{ChildEntity}Id);
            }

            // Step 3: Send notification
            await _notificationService.Send{Entity}CreatedNotificationAsync(
                {entity}Response.{Entity}Id,
                request.CreatedBy,
                ct);

            // Step 4: Audit
            await _auditService.Log{Entity}CreationAsync(
                {entity}Response.{Entity}Id,
                request.CreatedBy,
                ct);

            _logger.LogInformation(
                "Completed orchestrated {entity} creation for {Entity}Id",
                {entity}Response.{Entity}Id);

            return new {Entity}CreationResult
            {
                {Entity}Id = {entity}Response.{Entity}Id,
                {ChildEntity}Ids = {childEntity}Ids,
                Success = true
            };
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Failed orchestrated {entity} creation for {Entity}Name",
                request.{Entity}Name);

            throw;
        }
    }
}
```

### Choreography (Decentralized Coordination)

```csharp
// ✅ CORRECT - Service choreography
namespace {ApplicationName}.Services.Events;

// {Entity} service publishes event (doesn't know about consumers)
public sealed class {Entity}Service : I{Entity}Service
{
    private readonly IEventPublisher _eventPublisher;
    private readonly DataContext _dataContext;

    public async Task<Create{Entity}Response> Create{Entity}Async(
        Create{Entity}Request request,
        CancellationToken ct = default)
    {
        var {entity} = new {Entity}
        {
            {Entity}Id = Guid.NewGuid(),
            Name = request.Name,
            Amount = request.Amount
        };

        _dataContext.{Entities}.Add({entity});
        await _dataContext.SaveChangesAsync(ct);

        // Publish event - no knowledge of consumers
        await _eventPublisher.PublishAsync(
            new {Entity}CreatedEvent
            {
                {Entity}Id = {entity}.{Entity}Id,
                Name = {entity}.Name,
                Amount = {entity}.Amount,
                CreatedBy = request.CreatedBy
            },
            ct);

        return new Create{Entity}Response({entity}.{Entity}Id);
    }
}

// {ChildEntity} service reacts to event
public sealed class {ChildEntity}EventHandler : IEventHandler<{Entity}CreatedEvent>
{
    private readonly I{ChildEntity}Service _{childEntity}Service;

    public async Task HandleAsync({Entity}CreatedEvent domainEvent, CancellationToken ct)
    {
        // React to {entity} creation by creating default {childEntities}
        await _{childEntity}Service.CreateDefault{ChildEntities}Async(domainEvent.{Entity}Id, ct);
    }
}

// Notification service reacts to event
public sealed class NotificationEventHandler : IEventHandler<{Entity}CreatedEvent>
{
    private readonly INotificationService _notificationService;

    public async Task HandleAsync({Entity}CreatedEvent domainEvent, CancellationToken ct)
    {
        // React to {entity} creation by sending notification
        await _notificationService.Send{Entity}CreatedNotificationAsync(
            domainEvent.{Entity}Id,
            domainEvent.CreatedBy,
            ct);
    }
}

// Audit service reacts to event
public sealed class AuditEventHandler : IEventHandler<{Entity}CreatedEvent>
{
    private readonly IAuditService _auditService;

    public async Task HandleAsync({Entity}CreatedEvent domainEvent, CancellationToken ct)
    {
        // React to {entity} creation by logging audit entry
        await _auditService.Log{Entity}CreationAsync(
            domainEvent.{Entity}Id,
            domainEvent.CreatedBy,
            ct);
    }
}
```

---

## Service Versioning

### URL Versioning

```csharp
// ✅ CORRECT - URL versioning
namespace {ApplicationName}.Services.{Entities}.V1;

public static class {Entity}EndpointsV1
{
    public static void Map{Entity}EndpointsV1(
        this IEndpointRouteBuilder app,
        ApiVersionSet versionSet)
    {
        var group = app.MapGroup("/v1/{entities}")
            .WithApiVersionSet(versionSet)
            .HasApiVersion(1.0)
            .WithTags("{Entities} V1");

        group.MapPost("/", Create{Entity}V1);
        group.MapGet("/{id:guid}", Get{Entity}V1);
    }

    private static async Task<IResult> Create{Entity}V1(
        Create{Entity}RequestV1 request,
        I{Entity}Service {entity}Service,
        CancellationToken ct)
    {
        var response = await {entity}Service.Create{Entity}Async(request, ct);
        return Results.Created($"/v1/{entities}/{response.{Entity}Id}", response);
    }

    private static async Task<IResult> Get{Entity}V1(
        Guid id,
        I{Entity}Service {entity}Service,
        CancellationToken ct)
    {
        var {entity} = await {entity}Service.Get{Entity}Async(id, ct);
        return {entity} is not null ? Results.Ok({entity}) : Results.NotFound();
    }
}

namespace {ApplicationName}.Services.{Entities}.V2;

public static class {Entity}EndpointsV2
{
    public static void Map{Entity}EndpointsV2(
        this IEndpointRouteBuilder app,
        ApiVersionSet versionSet)
    {
        var group = app.MapGroup("/v2/{entities}")
            .WithApiVersionSet(versionSet)
            .HasApiVersion(2.0)
            .WithTags("{Entities} V2");

        group.MapPost("/", Create{Entity}V2); // Enhanced version
        group.MapGet("/{id:guid}", Get{Entity}V2); // Enhanced version
    }

    private static async Task<IResult> Create{Entity}V2(
        Create{Entity}RequestV2 request, // New request model
        I{Entity}ServiceV2 {entity}Service, // V2 service
        CancellationToken ct)
    {
        var response = await {entity}Service.Create{Entity}Async(request, ct);
        return Results.Created($"/v2/{entities}/{response.{Entity}Id}", response);
    }
}
```

### Header Versioning

```csharp
// ✅ CORRECT - Header versioning
public sealed class ApiVersionMiddleware
{
    private readonly RequestDelegate _next;

    public ApiVersionMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        // Read version from header
        if (context.Request.Headers.TryGetValue("api-version", out var version))
        {
            context.Items["ApiVersion"] = version.ToString();
        }
        else
        {
            context.Items["ApiVersion"] = "1.0"; // Default version
        }

        await _next(context);
    }
}

// Service implementation with version awareness
public sealed class {Entity}Service : I{Entity}Service
{
    private readonly IHttpContextAccessor _httpContextAccessor;

    public async Task<Create{Entity}Response> Create{Entity}Async(
        Create{Entity}Request request,
        CancellationToken ct = default)
    {
        var apiVersion = _httpContextAccessor.HttpContext?.Items["ApiVersion"]?.ToString();

        return apiVersion switch
        {
            "2.0" => await Create{Entity}V2Async(request, ct),
            _ => await Create{Entity}V1Async(request, ct)
        };
    }
}
```

---

## Idempotency

```csharp
// ✅ CORRECT - Idempotent service operations
namespace {ApplicationName}.Services.{Entities};

public sealed class {Entity}Service : I{Entity}Service
{
    private readonly DataContext _dataContext;
    private readonly IDistributedCache _cache;
    private readonly ILogger<{Entity}Service> _logger;

    public async Task<Create{Entity}Response> Create{Entity}Async(
        Create{Entity}Request request,
        CancellationToken ct = default)
    {
        // Use idempotency key to prevent duplicate creation
        var idempotencyKey = request.IdempotencyKey ??
            throw new ArgumentException("Idempotency key required");

        // Check if already processed
        var cached = await _cache.GetStringAsync($"idempotency:{idempotencyKey}", ct);
        if (cached is not null)
        {
            _logger.LogInformation(
                "Request already processed, returning cached response for key {IdempotencyKey}",
                idempotencyKey);

            return JsonSerializer.Deserialize<Create{Entity}Response>(cached)!;
        }

        // Process request
        var {entity} = new {Entity}
        {
            {Entity}Id = Guid.NewGuid(),
            Name = request.Name,
            Amount = request.Amount
        };

        _dataContext.{Entities}.Add({entity});
        await _dataContext.SaveChangesAsync(ct);

        var response = new Create{Entity}Response({entity}.{Entity}Id);

        // Cache response for idempotency
        await _cache.SetStringAsync(
            $"idempotency:{idempotencyKey}",
            JsonSerializer.Serialize(response),
            new DistributedCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = TimeSpan.FromHours(24)
            },
            ct);

        return response;
    }
}

public sealed record Create{Entity}Request
{
    public string IdempotencyKey { get; init; } = string.Empty;
    public string Name { get; init; } = string.Empty;
    public decimal Amount { get; init; }
}
```

---

## Transaction Management

### Distributed Transactions (Saga Pattern)

```csharp
// ✅ CORRECT - Saga pattern for distributed transactions
namespace {ApplicationName}.Services.Sagas;

public sealed class {Entity}CreationSaga : ISaga
{
    private readonly I{Entity}Service _{entity}Service;
    private readonly I{ChildEntity}Service _{childEntity}Service;
    private readonly INotificationService _notificationService;
    private readonly ILogger<{Entity}CreationSaga> _logger;

    public async Task<SagaResult> ExecuteAsync(
        {Entity}CreationSagaData data,
        CancellationToken ct = default)
    {
        Guid? {entity}Id = null;
        var {childEntity}Ids = new List<Guid>();

        try
        {
            // Step 1: Create {entity}
            var {entity}Response = await _{entity}Service.Create{Entity}Async(
                new Create{Entity}Request
                {
                    Name = data.{Entity}Name,
                    Amount = data.Amount
                },
                ct);

            {entity}Id = {entity}Response.{Entity}Id;

            // Step 2: Create {childEntities}
            foreach (var {childEntity}Data in data.{ChildEntities})
            {
                var {childEntity}Response = await _{childEntity}Service.Create{ChildEntity}Async(
                    new Create{ChildEntity}Request
                    {
                        {Entity}Id = {entity}Id.Value,
                        Name = {childEntity}Data.Name,
                        Amount = {childEntity}Data.Amount
                    },
                    ct);

                {childEntity}Ids.Add({childEntity}Response.{ChildEntity}Id);
            }

            // Step 3: Send notification
            await _notificationService.Send{Entity}CreatedNotificationAsync(
                {entity}Id.Value,
                data.CreatedBy,
                ct);

            return SagaResult.Success({entity}Id.Value, {childEntity}Ids);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Saga failed, initiating compensation");

            // Compensating transactions (rollback)
            await CompensateAsync({entity}Id, {childEntity}Ids, ct);

            return SagaResult.Failed(ex.Message);
        }
    }

    private async Task CompensateAsync(
        Guid? {entity}Id,
        List<Guid> {childEntity}Ids,
        CancellationToken ct)
    {
        // Reverse operations in opposite order

        // Remove {childEntities}
        foreach (var {childEntity}Id in {childEntity}Ids)
        {
            try
            {
                await _{childEntity}Service.Delete{ChildEntity}Async({childEntity}Id, ct);
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, "Failed to compensate {childEntity} {ChildEntity}Id", {childEntity}Id);
            }
        }

        // Remove {entity}
        if ({entity}Id.HasValue)
        {
            try
            {
                await _{entity}Service.Delete{Entity}Async({entity}Id.Value, ct);
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, "Failed to compensate {entity} {Entity}Id", {entity}Id);
            }
        }
    }
}
```

---

## SOA vs Microservices

| Aspect | SOA | Microservices |
|--------|-----|---------------|
| **Scope** | Enterprise-wide | Bounded context/domain |
| **Communication** | ESB, SOAP, sometimes REST | REST, gRPC, message queues |
| **Data** | Shared database common | Database per service |
| **Governance** | Centralized | Decentralized |
| **Size** | Larger services | Smaller, focused services |
| **Deployment** | Monolithic deployment common | Independent deployment |
| **Technology** | Standardized stack | Polyglot (multiple technologies) |

---

## Common Pitfalls

### Pitfall 1: Chatty Service Communication

```csharp
// ❌ WRONG - Multiple service calls for related data
public async Task<{Entity}Summary> Get{Entity}SummaryAsync(Guid {entity}Id)
{
    var {entity} = await _{entity}Service.Get{Entity}Async({entity}Id);
    var {childEntities} = await _{childEntity}Service.Get{ChildEntities}By{Entity}IdAsync({entity}Id); // Separate call
    var {childEntities} = await _{childEntity}Service.Get{ChildEntities}By{Entity}IdAsync({entity}Id); // Separate call

    // Multiple network roundtrips!
    return new {Entity}Summary({entity}, {childEntities}, {childEntities});
}

// ✅ CORRECT - Single call with composite data
public async Task<{Entity}Summary> Get{Entity}SummaryAsync(Guid {entity}Id)
{
    // Single service call returns all related data
    return await _{entity}QueryService.Get{Entity}SummaryAsync({entity}Id);
}
```

### Pitfall 2: Tight Service Coupling

```csharp
// ❌ WRONG - Direct service-to-service calls
public async Task Create{Entity}Async(Create{Entity}Request request)
{
    var {entity} = await Save{Entity}Async(request);

    // Direct coupling to other services
    await _{childEntity}Service.CreateDefault{ChildEntities}Async({entity}.{Entity}Id);
    await _notificationService.NotifyAsync({entity});
}

// ✅ CORRECT - Event-based decoupling
public async Task Create{Entity}Async(Create{Entity}Request request)
{
    var {entity} = await Save{Entity}Async(request);

    // Publish event - services react independently
    await _eventPublisher.PublishAsync(new {Entity}CreatedEvent({entity}));
}
```

---

## Summary Checklist

- [ ] **Service contracts** - Clear, well-documented interfaces
- [ ] **Loose coupling** - Minimal dependencies between services
- [ ] **Abstraction** - Implementation details hidden
- [ ] **Reusability** - Services designed for multiple consumers
- [ ] **Autonomy** - Services control their own logic and data
- [ ] **Statelessness** - Minimal retained state between calls
- [ ] **Discoverability** - Services externally discoverable
- [ ] **Message-based** - Asynchronous communication where appropriate
- [ ] **Versioning** - Clear versioning strategy
- [ ] **Idempotency** - Operations safely repeatable
- [ ] **Transaction management** - Saga pattern for distributed transactions
- [ ] **Error handling** - Proper fault tolerance and resilience

---

## Related Patterns

- [Object-Oriented Programming](./object-oriented-programming.md) - OOP principles
- [Microservices](./microservices.md) - Microservices architecture
- [Test-Driven Development](./test-driven-development.md) - TDD methodology
