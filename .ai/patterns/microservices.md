# Microservices Architecture Pattern

## Overview

Microservices architecture is an approach to developing a single application as a suite of small, independently deployable services. Each service runs in its own process, communicates via lightweight mechanisms (typically HTTP/REST or messaging), and is organized around business capabilities. This pattern enables continuous delivery, scalability, and technology diversity.

---

## Core Principles

### 1. Single Responsibility

Each microservice should have a single, well-defined responsibility aligned with a business capability.

```csharp
// ✅ CORRECT - Single responsibility per service

// {Entity}Service - Manages {entities} only
public sealed class {Entity}Service
{
    [HttpPost("/api/{entities}")]
    public async Task<IResult> Create{Entity}([FromBody] Create{Entity}Request request)
    {
        // {Entity} creation logic only
    }
}

// {ChildEntity}Service - Manages {childEntities} only
public sealed class {ChildEntity}Service
{
    [HttpPost("/api/{childEntities}")]
    public async Task<IResult> Create{ChildEntity}([FromBody] Create{ChildEntity}Request request)
    {
        // {ChildEntity} creation logic only
    }
}

// ❌ WRONG - Multiple responsibilities in one service
public sealed class MonolithicService
{
    [HttpPost("/api/{entities}")]
    public async Task<IResult> Create{Entity}() { /* ... */ }

    [HttpPost("/api/{childEntities}")]
    public async Task<IResult> Create{ChildEntity}() { /* ... */ }

    [HttpPost("/api/reports")]
    public async Task<IResult> GenerateReport() { /* ... */ }

    [HttpPost("/api/notifications")]
    public async Task<IResult> SendNotification() { /* ... */ }
}
```

### 2. Autonomy

Services should be independently deployable and scalable.

```csharp
// Each service has its own:
// - Codebase
// - Database
// - Deployment pipeline
// - Scaling configuration

// {Entity}Service - Deployed independently
// {ChildEntity}Service - Deployed independently
// NotificationService - Deployed independently
```

### 3. Decentralization

Decentralize data management and governance.

```csharp
// ✅ CORRECT - Each service owns its data

// {Entity}Service database
public sealed class {Entity}DbContext : DbContext
{
    public DbSet<{Entity}> {Entities} { get; set; }
    public DbSet<{Entity}Category> Categories { get; set; }
}

// {ChildEntity}Service database
public sealed class {ChildEntity}DbContext : DbContext
{
    public DbSet<{ChildEntity}> {ChildEntities} { get; set; }
    public DbSet<{ChildEntity}Milestone> Milestones { get; set; }
}

// ❌ WRONG - Shared database across services
public sealed class SharedDbContext : DbContext
{
    public DbSet<{Entity}> {Entities} { get; set; }
    public DbSet<{ChildEntity}> {ChildEntities} { get; set; }
    // All services accessing same database!
}
```

---

## Service Boundaries and Bounded Contexts (DDD)

### Identifying Bounded Contexts

Use Domain-Driven Design to identify service boundaries.

```
{ApplicationName}

Bounded Contexts:
├── {Domain1} Management ({Entity}Service)
│   ├── {Entities}
│   ├── Categories
│   └── {Entity} Allocations
│
├── {Domain2} Management ({ChildEntity}Service)
│   ├── {ChildEntities}
│   ├── Milestones
│   └── Progress Tracking
│
├── Reporting (ReportingService)
│   ├── Reports
│   ├── Analytics
│   └── Dashboards
│
└── Notification (NotificationService)
    ├── Email Notifications
    ├── SMS Notifications
    └── Push Notifications
```

### Context Mapping

```csharp
// File: {ApplicationName}.Services.{Entity}/Domain/{Entity}.cs

namespace {ApplicationName}.Services.{Entity}.Domain;

/// <summary>
/// {Entity} aggregate in {Entity} Management context.
/// </summary>
public sealed class {Entity}
{
    public Guid {Entity}Id { get; init; }
    public string Name { get; init; } = string.Empty;
    public decimal TotalAmount { get; init; }
    public Guid UserId { get; init; } // Reference to User context
    // {Entity}-specific properties and behavior
}

// File: {ApplicationName}.Services.{ChildEntity}/Domain/{ChildEntity}.cs

namespace {ApplicationName}.Services.{ChildEntity}.Domain;

/// <summary>
/// {ChildEntity} aggregate in {ChildEntity} Management context.
/// </summary>
public sealed class {ChildEntity}
{
    public Guid {ChildEntity}Id { get; init; }
    public string Name { get; init; } = string.Empty;
    public decimal Amount { get; init; }
    public Guid {Entity}Id { get; init; } // Reference to {Entity} context
    // {ChildEntity}-specific properties and behavior
}
```

---

## API Gateway Pattern

### Backend for Frontend (BFF)

API Gateway aggregates requests from clients and routes them to appropriate microservices.

```csharp
// File: {ApplicationName}.Gateway/Program.cs

using Yarp.ReverseProxy.Configuration;

var builder = WebApplication.CreateBuilder(args);

// Configure YARP (Yet Another Reverse Proxy)
builder.Services.AddReverseProxy()
    .LoadFromConfig(builder.Configuration.GetSection("ReverseProxy"));

// Add authentication
builder.Services.AddAuthentication("Bearer")
    .AddJwtBearer("Bearer", options =>
    {
        options.Authority = builder.Configuration["Auth:Authority"];
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateAudience = false
        };
    });

// Add authorization
builder.Services.AddAuthorization();

var app = builder.Build();

app.UseAuthentication();
app.UseAuthorization();

// YARP reverse proxy middleware
app.MapReverseProxy();

app.Run();
```

**Configuration (appsettings.json):**
```json
{
  "ReverseProxy": {
    "Routes": {
      "{entity}-route": {
        "ClusterId": "{entity}-cluster",
        "Match": {
          "Path": "/api/{entities}/{**catch-all}"
        },
        "Transforms": [
          { "PathPattern": "/api/{entities}/{**catch-all}" }
        ]
      },
      "{childEntity}-route": {
        "ClusterId": "{childEntity}-cluster",
        "Match": {
          "Path": "/api/{childEntities}/{**catch-all}"
        },
        "Transforms": [
          { "PathPattern": "/api/{childEntities}/{**catch-all}" }
        ]
      },
      "reporting-route": {
        "ClusterId": "reporting-cluster",
        "Match": {
          "Path": "/api/reports/{**catch-all}"
        }
      }
    },
    "Clusters": {
      "{entity}-cluster": {
        "Destinations": {
          "{entity}-service": {
            "Address": "http://{entity}-service:8080"
          }
        }
      },
      "{childEntity}-cluster": {
        "Destinations": {
          "{childEntity}-service": {
            "Address": "http://{childEntity}-service:8080"
          }
        }
      },
      "reporting-cluster": {
        "Destinations": {
          "reporting-service": {
            "Address": "http://reporting-service:8080"
          }
        }
      }
    }
  }
}
```

### Request Aggregation

```csharp
// File: {ApplicationName}.Gateway/Services/DashboardAggregationService.cs

namespace {ApplicationName}.Gateway.Services;

/// <summary>
/// Aggregates data from multiple microservices for dashboard.
/// </summary>
public sealed class DashboardAggregationService
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<DashboardAggregationService> _logger;

    public DashboardAggregationService(
        HttpClient httpClient,
        ILogger<DashboardAggregationService> logger)
    {
        _httpClient = httpClient;
        _logger = logger;
    }

    public async Task<DashboardResponse> GetDashboardDataAsync(
        Guid userId,
        CancellationToken cancellationToken = default)
    {
        // Call multiple services in parallel
        var {entity}Task = Get{Entities}Async(userId, cancellationToken);
        var {childEntity}Task = Get{ChildEntities}Async(userId, cancellationToken);

        await Task.WhenAll({entity}Task, {childEntity}Task);

        return new DashboardResponse
        {
            {Entities} = await {entity}Task,
            {ChildEntities} = await {childEntity}Task
        };
    }

    private async Task<List<{Entity}Summary>> Get{Entities}Async(
        Guid userId,
        CancellationToken cancellationToken)
    {
        var response = await _httpClient.GetAsync(
            $"http://{entity}-service/api/{entities}?userId={userId}",
            cancellationToken);

        response.EnsureSuccessStatusCode();

        return await response.Content.ReadFromJsonAsync<List<{Entity}Summary>>(
            cancellationToken: cancellationToken) ?? new();
    }

    private async Task<List<{ChildEntity}Summary>> Get{ChildEntities}Async(
        Guid userId,
        CancellationToken cancellationToken)
    {
        var response = await _httpClient.GetAsync(
            $"http://{childEntity}-service/api/{childEntities}?userId={userId}",
            cancellationToken);

        response.EnsureSuccessStatusCode();

        return await response.Content.ReadFromJsonAsync<List<{ChildEntity}Summary>>(
            cancellationToken: cancellationToken) ?? new();
    }
}
```

---

## Inter-Service Communication

### Synchronous Communication (REST)

```csharp
// File: {ApplicationName}.Services.{ChildEntity}/Services/{Entity}ServiceClient.cs

namespace {ApplicationName}.Services.{ChildEntity}.Services;

/// <summary>
/// Client for communicating with {Entity} Service.
/// </summary>
public sealed class {Entity}ServiceClient
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<{Entity}ServiceClient> _logger;

    public {Entity}ServiceClient(
        HttpClient httpClient,
        ILogger<{Entity}ServiceClient> logger)
    {
        _httpClient = httpClient;
        _logger = logger;
    }

    public async Task<{Entity}Dto?> Get{Entity}ByIdAsync(
        Guid {entity}Id,
        CancellationToken cancellationToken = default)
    {
        try
        {
            _logger.LogInformation("Fetching {entity} {Entity}Id from {Entity} Service", {entity}Id);

            var response = await _httpClient.GetAsync(
                $"/api/{entities}/{entity}Id",
                cancellationToken);

            if (!response.IsSuccessStatusCode)
            {
                _logger.LogWarning(
                    "Failed to fetch {entity} {Entity}Id. Status: {StatusCode}",
                    {entity}Id, response.StatusCode);
                return null;
            }

            var {entity} = await response.Content.ReadFromJsonAsync<{Entity}Dto>(
                cancellationToken: cancellationToken);

            return {entity};
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error fetching {entity} {Entity}Id", {entity}Id);
            throw;
        }
    }
}

// Registration in Program.cs
builder.Services.AddHttpClient<{Entity}ServiceClient>(client =>
{
    client.BaseAddress = new Uri(builder.Configuration["Services:{Entity}Service:Url"]!);
    client.DefaultRequestHeaders.Add("Accept", "application/json");
})
.AddStandardResilienceHandler(); // Adds retry, circuit breaker, timeout
```

### Synchronous Communication (gRPC)

```csharp
// File: {ApplicationName}.Services.{Entity}/Protos/{entity}.proto

syntax = "proto3";

option csharp_namespace = "{ApplicationName}.Services.{Entity}.Grpc";

package {entity};

service {Entity}Service {
  rpc Get{Entity} (Get{Entity}Request) returns ({Entity}Response);
  rpc Create{Entity} (Create{Entity}Request) returns (Create{Entity}Response);
  rpc Update{Entity} (Update{Entity}Request) returns (Update{Entity}Response);
}

message Get{Entity}Request {
  string {entity}_id = 1;
}

message {Entity}Response {
  string {entity}_id = 1;
  string name = 2;
  double total_amount = 3;
  string user_id = 4;
}

message Create{Entity}Request {
  string name = 1;
  double total_amount = 2;
  string user_id = 3;
}

message Create{Entity}Response {
  string {entity}_id = 1;
}

message Update{Entity}Request {
  string {entity}_id = 1;
  string name = 2;
  double total_amount = 3;
}

message Update{Entity}Response {
  bool success = 1;
}
```

**gRPC Service Implementation:**
```csharp
// File: {ApplicationName}.Services.{Entity}/GrpcServices/{Entity}GrpcService.cs

using Grpc.Core;
using {ApplicationName}.Services.{Entity}.Grpc;

namespace {ApplicationName}.Services.{Entity}.GrpcServices;

public sealed class {Entity}GrpcService : {Entity}Service.{Entity}ServiceBase
{
    private readonly IQueryHandler<Get{Entity}ByIdQuery, {Entity}Response> _queryHandler;
    private readonly ICommandHandler<Create{Entity}Command, Create{Entity}Response> _createHandler;
    private readonly ILogger<{Entity}GrpcService> _logger;

    public {Entity}GrpcService(
        IQueryHandler<Get{Entity}ByIdQuery, {Entity}Response> queryHandler,
        ICommandHandler<Create{Entity}Command, Create{Entity}Response> createHandler,
        ILogger<{Entity}GrpcService> logger)
    {
        _queryHandler = queryHandler;
        _createHandler = createHandler;
        _logger = logger;
    }

    public override async Task<{Entity}Response> Get{Entity}(
        Get{Entity}Request request,
        ServerCallContext context)
    {
        var query = new Get{Entity}ByIdQuery(Guid.Parse(request.{Entity}Id));
        var result = await _queryHandler.HandleAsync(query, context.CancellationToken);

        return new {Entity}Response
        {
            {Entity}Id = result.{Entity}Id.ToString(),
            Name = result.Name,
            TotalAmount = (double)result.Amount,
            UserId = result.UserId.ToString()
        };
    }

    public override async Task<Create{Entity}Response> Create{Entity}(
        Create{Entity}Request request,
        ServerCallContext context)
    {
        var command = new Create{Entity}Command(
            request.Name,
            (decimal)request.TotalAmount,
            DateTimeOffset.UtcNow);

        var result = await _createHandler.HandleAsync(command, context.CancellationToken);

        return new Create{Entity}Response
        {
            {Entity}Id = result.{Entity}Id.ToString()
        };
    }
}
```

**gRPC Client:**
```csharp
// File: {ApplicationName}.Services.{ChildEntity}/Services/{Entity}GrpcClient.cs

using {ApplicationName}.Services.{Entity}.Grpc;

namespace {ApplicationName}.Services.{ChildEntity}.Services;

public sealed class {Entity}GrpcClient
{
    private readonly {Entity}Service.{Entity}ServiceClient _client;
    private readonly ILogger<{Entity}GrpcClient> _logger;

    public {Entity}GrpcClient(
        {Entity}Service.{Entity}ServiceClient client,
        ILogger<{Entity}GrpcClient> logger)
    {
        _client = client;
        _logger = logger;
    }

    public async Task<{Entity}Response?> Get{Entity}Async(
        Guid {entity}Id,
        CancellationToken cancellationToken = default)
    {
        try
        {
            var request = new Get{Entity}Request { {Entity}Id = {entity}Id.ToString() };
            return await _client.Get{Entity}Async(request, cancellationToken: cancellationToken);
        }
        catch (RpcException ex)
        {
            _logger.LogError(ex, "gRPC call failed for {entity} {Entity}Id", {entity}Id);
            return null;
        }
    }
}

// Registration
builder.Services.AddGrpcClient<{Entity}Service.{Entity}ServiceClient>(options =>
{
    options.Address = new Uri(builder.Configuration["Services:{Entity}Service:GrpcUrl"]!);
});
```

### Asynchronous Communication (Message Queue)

```csharp
// File: {ApplicationName}.Services.{Entity}/Events/{Entity}CreatedEvent.cs

namespace {ApplicationName}.Services.{Entity}.Events;

/// <summary>
/// Event published when a {entity} is created.
/// </summary>
public sealed record {Entity}CreatedEvent
{
    public Guid {Entity}Id { get; init; }
    public string Name { get; init; } = string.Empty;
    public decimal TotalAmount { get; init; }
    public Guid UserId { get; init; }
    public DateTimeOffset CreatedAt { get; init; }
}
```

**Publishing Events (using MassTransit):**
```csharp
// File: {ApplicationName}.Services.{Entity}/Handlers/Create{Entity}CommandHandler.cs

using MassTransit;

public sealed class Create{Entity}CommandHandler(
    DataContext dataContext,
    IPublishEndpoint publishEndpoint,
    ILogger<Create{Entity}CommandHandler> logger
) : ICommandHandler<Create{Entity}Command, Create{Entity}Response>
{
    public async Task<Create{Entity}Response> HandleAsync(
        Create{Entity}Command command,
        CancellationToken cancellationToken = default)
    {
        // Create {entity}
        var entity = new Entities.{Domain}.{Entity}
        {
            {Entity}Id = Guid.NewGuid(),
            Name = command.Name,
            TotalAmount = command.TotalAmount,
            UserId = command.UserId
        };

        dataContext.{Entities}.Add(entity);
        var rowsAffected = await dataContext.SaveChangesAsync(cancellationToken);

        if (rowsAffected == 0)
            throw new InvalidOperationException("Failed to create {entity}");

        // Publish event
        var @event = new {Entity}CreatedEvent
        {
            {Entity}Id = entity.{Entity}Id,
            Name = entity.Name,
            TotalAmount = entity.TotalAmount,
            UserId = entity.UserId,
            CreatedAt = DateTimeOffset.UtcNow
        };

        await publishEndpoint.Publish(@event, cancellationToken);

        logger.LogInformation(
            "Published {Entity}CreatedEvent for {entity} {Entity}Id",
            entity.{Entity}Id);

        return new Create{Entity}Response(entity.{Entity}Id);
    }
}
```

**Consuming Events:**
```csharp
// File: {ApplicationName}.Services.Notification/Consumers/{Entity}CreatedEventConsumer.cs

using MassTransit;
using {ApplicationName}.Services.{Entity}.Events;

namespace {ApplicationName}.Services.Notification.Consumers;

/// <summary>
/// Consumes {Entity}CreatedEvent and sends notification.
/// </summary>
public sealed class {Entity}CreatedEventConsumer : IConsumer<{Entity}CreatedEvent>
{
    private readonly IEmailService _emailService;
    private readonly ILogger<{Entity}CreatedEventConsumer> _logger;

    public {Entity}CreatedEventConsumer(
        IEmailService emailService,
        ILogger<{Entity}CreatedEventConsumer> logger)
    {
        _emailService = emailService;
        _logger = logger;
    }

    public async Task Consume(ConsumeContext<{Entity}CreatedEvent> context)
    {
        var @event = context.Message;

        _logger.LogInformation(
            "Processing {Entity}CreatedEvent for {entity} {Entity}Id",
            @event.{Entity}Id);

        // Send notification email
        await _emailService.Send{Entity}CreatedEmailAsync(
            @event.UserId,
            @event.Name,
            @event.TotalAmount,
            context.CancellationToken);

        _logger.LogInformation(
            "Sent notification for {entity} {Entity}Id",
            @event.{Entity}Id);
    }
}

// Registration in Program.cs
builder.Services.AddMassTransit(x =>
{
    x.AddConsumer<{Entity}CreatedEventConsumer>();

    x.UsingRabbitMq((context, cfg) =>
    {
        cfg.Host(builder.Configuration["RabbitMQ:Host"], h =>
        {
            h.Username(builder.Configuration["RabbitMQ:Username"]!);
            h.Password(builder.Configuration["RabbitMQ:Password"]!);
        });

        cfg.ConfigureEndpoints(context);
    });
});
```

---

## Database Per Service Pattern

Each microservice owns its database schema and data.

```csharp
// {Entity}Service - PostgreSQL
public sealed class {Entity}DbContext : DbContext
{
    public DbSet<{Entity}> {Entities} { get; set; }
    public DbSet<{Entity}Category> Categories { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        optionsBuilder.UseNpgsql("Host={entity}-db;Database={Entity}Db;");
    }
}

// {ChildEntity}Service - PostgreSQL (separate database)
public sealed class {ChildEntity}DbContext : DbContext
{
    public DbSet<{ChildEntity}> {ChildEntities} { get; set; }
    public DbSet<Milestone> Milestones { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        optionsBuilder.UseNpgsql("Host={childEntity}-db;Database={ChildEntity}Db;");
    }
}

// NotificationService - MongoDB (different database type)
public sealed class NotificationDbContext
{
    private readonly IMongoDatabase _database;

    public NotificationDbContext(IMongoClient client)
    {
        _database = client.GetDatabase("NotificationDb");
    }

    public IMongoCollection<NotificationLog> Notifications =>
        _database.GetCollection<NotificationLog>("notifications");
}
```

---

## Saga Pattern for Distributed Transactions

### Choreography-Based Saga

Services communicate through events without a central coordinator.

```csharp
// File: {ApplicationName}.Services.Order/Events/OrderCreatedEvent.cs

public sealed record OrderCreatedEvent
{
    public Guid OrderId { get; init; }
    public Guid UserId { get; init; }
    public decimal TotalAmount { get; init; }
}

// File: {ApplicationName}.Services.Payment/Consumers/OrderCreatedEventConsumer.cs

public sealed class OrderCreatedEventConsumer : IConsumer<OrderCreatedEvent>
{
    private readonly IPublishEndpoint _publishEndpoint;

    public async Task Consume(ConsumeContext<OrderCreatedEvent> context)
    {
        var @event = context.Message;

        // Process payment
        var paymentSuccess = await ProcessPaymentAsync(@event.TotalAmount);

        if (paymentSuccess)
        {
            await _publishEndpoint.Publish(new PaymentProcessedEvent
            {
                OrderId = @event.OrderId,
                Amount = @event.TotalAmount,
                Success = true
            });
        }
        else
        {
            await _publishEndpoint.Publish(new PaymentFailedEvent
            {
                OrderId = @event.OrderId,
                Reason = "Insufficient funds"
            });
        }
    }
}

// File: {ApplicationName}.Services.Order/Consumers/PaymentFailedEventConsumer.cs

public sealed class PaymentFailedEventConsumer : IConsumer<PaymentFailedEvent>
{
    public async Task Consume(ConsumeContext<PaymentFailedEvent> context)
    {
        // Compensating transaction - cancel order
        await CancelOrderAsync(context.Message.OrderId);
    }
}
```

### Orchestration-Based Saga

A central orchestrator manages the saga workflow.

```csharp
// File: {ApplicationName}.Services.Orchestrator/Sagas/OrderSaga.cs

using MassTransit;

namespace {ApplicationName}.Services.Orchestrator.Sagas;

public sealed class OrderState : SagaStateMachineInstance
{
    public Guid CorrelationId { get; set; }
    public string CurrentState { get; set; } = string.Empty;
    public Guid OrderId { get; set; }
    public Guid UserId { get; set; }
    public decimal TotalAmount { get; set; }
}

public sealed class OrderSaga : MassTransitStateMachine<OrderState>
{
    public State OrderCreated { get; private set; } = null!;
    public State PaymentProcessed { get; private set; } = null!;
    public State InventoryReserved { get; private set; } = null!;
    public State OrderCompleted { get; private set; } = null!;
    public State OrderFailed { get; private set; } = null!;

    public Event<OrderCreatedEvent> OrderCreatedEvent { get; private set; } = null!;
    public Event<PaymentProcessedEvent> PaymentProcessedEvent { get; private set; } = null!;
    public Event<PaymentFailedEvent> PaymentFailedEvent { get; private set; } = null!;
    public Event<InventoryReservedEvent> InventoryReservedEvent { get; private set; } = null!;
    public Event<InventoryReservationFailedEvent> InventoryReservationFailedEvent { get; private set; } = null!;

    public OrderSaga()
    {
        InstanceState(x => x.CurrentState);

        Event(() => OrderCreatedEvent, x => x.CorrelateById(context => context.Message.OrderId));
        Event(() => PaymentProcessedEvent, x => x.CorrelateById(context => context.Message.OrderId));
        Event(() => PaymentFailedEvent, x => x.CorrelateById(context => context.Message.OrderId));
        Event(() => InventoryReservedEvent, x => x.CorrelateById(context => context.Message.OrderId));
        Event(() => InventoryReservationFailedEvent, x => x.CorrelateById(context => context.Message.OrderId));

        Initially(
            When(OrderCreatedEvent)
                .Then(context =>
                {
                    context.Saga.OrderId = context.Message.OrderId;
                    context.Saga.UserId = context.Message.UserId;
                    context.Saga.TotalAmount = context.Message.TotalAmount;
                })
                .TransitionTo(OrderCreated)
                .Publish(context => new ProcessPaymentCommand
                {
                    OrderId = context.Saga.OrderId,
                    Amount = context.Saga.TotalAmount
                }));

        During(OrderCreated,
            When(PaymentProcessedEvent)
                .TransitionTo(PaymentProcessed)
                .Publish(context => new ReserveInventoryCommand
                {
                    OrderId = context.Saga.OrderId
                }),
            When(PaymentFailedEvent)
                .TransitionTo(OrderFailed)
                .Publish(context => new CancelOrderCommand
                {
                    OrderId = context.Saga.OrderId,
                    Reason = context.Message.Reason
                }));

        During(PaymentProcessed,
            When(InventoryReservedEvent)
                .TransitionTo(OrderCompleted)
                .Publish(context => new CompleteOrderCommand
                {
                    OrderId = context.Saga.OrderId
                })
                .Finalize(),
            When(InventoryReservationFailedEvent)
                .TransitionTo(OrderFailed)
                .Publish(context => new RefundPaymentCommand
                {
                    OrderId = context.Saga.OrderId,
                    Amount = context.Saga.TotalAmount
                })
                .Publish(context => new CancelOrderCommand
                {
                    OrderId = context.Saga.OrderId,
                    Reason = "Inventory not available"
                }));

        SetCompletedWhenFinalized();
    }
}
```

---

## Event-Driven Architecture with Domain Events

```csharp
// File: {ApplicationName}.Common/Events/IDomainEvent.cs

namespace {ApplicationName}.Common.Events;

/// <summary>
/// Marker interface for domain events.
/// </summary>
public interface IDomainEvent
{
    Guid EventId { get; init; }
    DateTimeOffset OccurredAt { get; init; }
}

// File: {ApplicationName}.Services.{Entity}/Events/{Entity}UpdatedEvent.cs

public sealed record {Entity}UpdatedEvent : IDomainEvent
{
    public Guid EventId { get; init; } = Guid.NewGuid();
    public DateTimeOffset OccurredAt { get; init; } = DateTimeOffset.UtcNow;
    public Guid {Entity}Id { get; init; }
    public string Name { get; init; } = string.Empty;
    public decimal OldAmount { get; init; }
    public decimal NewAmount { get; init; }
    public Guid UserId { get; init; }
}

// File: {ApplicationName}.Services.Reporting/Consumers/{Entity}UpdatedEventConsumer.cs

public sealed class {Entity}UpdatedEventConsumer : IConsumer<{Entity}UpdatedEvent>
{
    private readonly ILogger<{Entity}UpdatedEventConsumer> _logger;
    private readonly ReportingDbContext _dbContext;

    public async Task Consume(ConsumeContext<{Entity}UpdatedEvent> context)
    {
        var @event = context.Message;

        _logger.LogInformation(
            "Updating reporting data for {entity} {Entity}Id",
            @event.{Entity}Id);

        // Update read model for reporting
        var reportEntry = await _dbContext.{Entity}Reports
            .FirstOrDefaultAsync(x => x.{Entity}Id == @event.{Entity}Id);

        if (reportEntry is not null)
        {
            reportEntry.Name = @event.Name;
            reportEntry.Amount = @event.NewAmount;
            reportEntry.LastUpdated = @event.OccurredAt;

            await _dbContext.SaveChangesAsync(context.CancellationToken);
        }
    }
}
```

---

## Service Discovery

### Using .NET Aspire Service Discovery

```csharp
// File: {ApplicationName}.AppHost/Program.cs (Aspire orchestration)

var builder = DistributedApplication.CreateBuilder(args);

// Define services
var {entity}Service = builder.AddProject<Projects.{Entity}Service>("{entity}-service")
    .WithHttpEndpoint(port: 8081, name: "http");

var {childEntity}Service = builder.AddProject<Projects.{ChildEntity}Service>("{childEntity}-service")
    .WithHttpEndpoint(port: 8082, name: "http");

var gateway = builder.AddProject<Projects.Gateway>("gateway")
    .WithHttpEndpoint(port: 8080, name: "http")
    .WithReference({entity}Service)
    .WithReference({childEntity}Service);

builder.Build().Run();
```

**Service Discovery in Consumer:**
```csharp
// File: {ApplicationName}.Services.{ChildEntity}/Program.cs

var builder = WebApplication.CreateBuilder(args);

// Add service discovery
builder.Services.AddServiceDiscovery();

// Add HttpClient with service discovery
builder.Services.AddHttpClient<{Entity}ServiceClient>(client =>
{
    // Service name from Aspire
    client.BaseAddress = new Uri("http://{entity}-service");
})
.AddServiceDiscovery() // Resolves service address automatically
.AddStandardResilienceHandler();

var app = builder.Build();
app.Run();
```

---

## Circuit Breaker and Resilience Patterns

```csharp
// File: {ApplicationName}.Services.{ChildEntity}/Program.cs

using Microsoft.Extensions.Http.Resilience;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddHttpClient<{Entity}ServiceClient>(client =>
{
    client.BaseAddress = new Uri(builder.Configuration["Services:{Entity}Service:Url"]!);
})
.AddStandardResilienceHandler(options =>
{
    // Retry configuration
    options.Retry.MaxRetryAttempts = 3;
    options.Retry.BackoffType = DelayBackoffType.Exponential;
    options.Retry.UseJitter = true;
    options.Retry.Delay = TimeSpan.FromSeconds(2);

    // Circuit breaker configuration
    options.CircuitBreaker.FailureRatio = 0.5;
    options.CircuitBreaker.SamplingDuration = TimeSpan.FromSeconds(30);
    options.CircuitBreaker.MinimumThroughput = 10;
    options.CircuitBreaker.BreakDuration = TimeSpan.FromSeconds(30);

    // Timeout configuration
    options.AttemptTimeout.Timeout = TimeSpan.FromSeconds(10);
    options.TotalRequestTimeout.Timeout = TimeSpan.FromSeconds(30);
});

var app = builder.Build();
app.Run();
```

---

## Distributed Tracing with OpenTelemetry

```csharp
// File: {ApplicationName}.Services.{Entity}/Program.cs

using OpenTelemetry.Resources;
using OpenTelemetry.Trace;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddOpenTelemetry()
    .ConfigureResource(resource => resource
        .AddService("{entity}-service"))
    .WithTracing(tracing => tracing
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation()
        .AddEntityFrameworkCoreInstrumentation()
        .AddSource("MassTransit")
        .AddOtlpExporter(options =>
        {
            options.Endpoint = new Uri(builder.Configuration["OpenTelemetry:Endpoint"]!);
        }));

var app = builder.Build();
app.Run();
```

**Correlation ID Propagation:**
```csharp
// File: {ApplicationName}.Common/Middleware/CorrelationIdMiddleware.cs

public sealed class CorrelationIdMiddleware
{
    private readonly RequestDelegate _next;
    private const string CorrelationIdHeader = "X-Correlation-ID";

    public CorrelationIdMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        var correlationId = context.Request.Headers[CorrelationIdHeader].FirstOrDefault()
            ?? Guid.NewGuid().ToString();

        context.Response.Headers.Add(CorrelationIdHeader, correlationId);

        using (context.RequestServices.GetRequiredService<ILogger<CorrelationIdMiddleware>>()
            .BeginScope(new Dictionary<string, object> { ["CorrelationId"] = correlationId }))
        {
            await _next(context);
        }
    }
}
```

---

## .NET Aspire for Microservices Orchestration

```csharp
// File: {ApplicationName}.AppHost/Program.cs

var builder = DistributedApplication.CreateBuilder(args);

// Add PostgreSQL for services
var postgres = builder.AddPostgres("postgres")
    .WithPgAdmin();

var {entity}Db = postgres.AddDatabase("{entity}db");
var {childEntity}Db = postgres.AddDatabase("{childEntity}db");

// Add Redis for caching
var redis = builder.AddRedis("redis");

// Add RabbitMQ for messaging
var rabbitmq = builder.AddRabbitMQ("rabbitmq")
    .WithManagementPlugin();

// Add {Entity} Service
var {entity}Service = builder.AddProject<Projects.{Entity}Service>("{entity}-service")
    .WithReference({entity}Db)
    .WithReference(redis)
    .WithReference(rabbitmq)
    .WithHttpEndpoint(port: 8081, name: "http");

// Add {ChildEntity} Service
var {childEntity}Service = builder.AddProject<Projects.{ChildEntity}Service>("{childEntity}-service")
    .WithReference({childEntity}Db)
    .WithReference(redis)
    .WithReference(rabbitmq)
    .WithHttpEndpoint(port: 8082, name: "http");

// Add Reporting Service
var reportingService = builder.AddProject<Projects.ReportingService>("reporting-service")
    .WithReference(postgres.AddDatabase("reportingdb"))
    .WithReference(redis)
    .WithReference(rabbitmq)
    .WithHttpEndpoint(port: 8083, name: "http");

// Add API Gateway
var gateway = builder.AddProject<Projects.Gateway>("gateway")
    .WithHttpEndpoint(port: 8080, name: "http")
    .WithReference({entity}Service)
    .WithReference({childEntity}Service)
    .WithReference(reportingService);

builder.Build().Run();
```

---

## Container Orchestration

### Docker Compose

```yaml
# File: docker-compose.yml

version: '3.8'

services:
  {entity}-service:
    build:
      context: ./src/{ApplicationName}.Services.{Entity}
      dockerfile: Dockerfile
    ports:
      - "8081:8080"
    environment:
      - ConnectionStrings__DefaultConnection=Host=postgres;Database={Entity}Db;Username=postgres;Password=postgres
      - RabbitMQ__Host=rabbitmq
      - Redis__ConnectionString=redis:6379
    depends_on:
      - postgres
      - rabbitmq
      - redis

  {childEntity}-service:
    build:
      context: ./src/{ApplicationName}.Services.{ChildEntity}
      dockerfile: Dockerfile
    ports:
      - "8082:8080"
    environment:
      - ConnectionStrings__DefaultConnection=Host=postgres;Database={ChildEntity}Db;Username=postgres;Password=postgres
      - RabbitMQ__Host=rabbitmq
      - Redis__ConnectionString=redis:6379
      - Services__{Entity}Service__Url=http://{entity}-service:8080
    depends_on:
      - postgres
      - rabbitmq
      - redis
      - {entity}-service

  reporting-service:
    build:
      context: ./src/{ApplicationName}.Services.Reporting
      dockerfile: Dockerfile
    ports:
      - "8083:8080"
    environment:
      - ConnectionStrings__DefaultConnection=Host=postgres;Database=ReportingDb;Username=postgres;Password=postgres
      - RabbitMQ__Host=rabbitmq
      - Redis__ConnectionString=redis:6379
    depends_on:
      - postgres
      - rabbitmq
      - redis

  gateway:
    build:
      context: ./src/{ApplicationName}.Gateway
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    environment:
      - Services__{Entity}Service__Url=http://{entity}-service:8080
      - Services__{ChildEntity}Service__Url=http://{childEntity}-service:8080
      - Services__ReportingService__Url=http://reporting-service:8080
    depends_on:
      - {entity}-service
      - {childEntity}-service
      - reporting-service

  postgres:
    image: postgres:16
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    volumes:
      - postgres-data:/var/lib/postgresql/data

  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      - RABBITMQ_DEFAULT_USER=admin
      - RABBITMQ_DEFAULT_PASS=admin

  redis:
    image: redis:7
    ports:
      - "6379:6379"

volumes:
  postgres-data:
```

### Kubernetes Deployment

```yaml
# File: k8s/{entity}-service-deployment.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: {entity}-service
  labels:
    app: {entity}-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: {entity}-service
  template:
    metadata:
      labels:
        app: {entity}-service
    spec:
      containers:
      - name: {entity}-service
        image: {registry}/{ApplicationName}/{entity}-service:latest
        ports:
        - containerPort: 8080
        env:
        - name: ConnectionStrings__DefaultConnection
          valueFrom:
            secretKeyRef:
              name: {entity}-service-secrets
              key: connection-string
        - name: RabbitMQ__Host
          value: rabbitmq-service
        - name: Redis__ConnectionString
          value: redis-service:6379
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: {entity}-service
spec:
  selector:
    app: {entity}-service
  ports:
  - protocol: TCP
    port: 8080
    targetPort: 8080
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {entity}-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {entity}-service
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

---

## Deployment Strategies

### Blue-Green Deployment

```yaml
# Blue deployment (current)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {entity}-service-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: {entity}-service
      version: blue
  template:
    metadata:
      labels:
        app: {entity}-service
        version: blue
    spec:
      containers:
      - name: {entity}-service
        image: {registry}/{ApplicationName}/{entity}-service:v1.0.0

---
# Green deployment (new version)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {entity}-service-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: {entity}-service
      version: green
  template:
    metadata:
      labels:
        app: {entity}-service
        version: green
    spec:
      containers:
      - name: {entity}-service
        image: {registry}/{ApplicationName}/{entity}-service:v2.0.0

---
# Service pointing to blue initially
apiVersion: v1
kind: Service
metadata:
  name: {entity}-service
spec:
  selector:
    app: {entity}-service
    version: blue  # Change to 'green' to switch traffic
  ports:
  - port: 8080
```

### Canary Deployment

```yaml
# Stable version (90% of traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {entity}-service-stable
spec:
  replicas: 9
  selector:
    matchLabels:
      app: {entity}-service
      version: stable
  template:
    metadata:
      labels:
        app: {entity}-service
        version: stable
    spec:
      containers:
      - name: {entity}-service
        image: {registry}/{ApplicationName}/{entity}-service:v1.0.0

---
# Canary version (10% of traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {entity}-service-canary
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {entity}-service
      version: canary
  template:
    metadata:
      labels:
        app: {entity}-service
        version: canary
    spec:
      containers:
      - name: {entity}-service
        image: {registry}/{ApplicationName}/{entity}-service:v2.0.0

---
# Service distributes traffic across both
apiVersion: v1
kind: Service
metadata:
  name: {entity}-service
spec:
  selector:
    app: {entity}-service  # Matches both stable and canary
  ports:
  - port: 8080
```

---

## Monitoring and Observability

### Health Checks

```csharp
// File: {ApplicationName}.Services.{Entity}/Program.cs

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddHealthChecks()
    .AddNpgSql(builder.Configuration.GetConnectionString("DefaultConnection")!)
    .AddRedis(builder.Configuration["Redis:ConnectionString"]!)
    .AddRabbitMQ(rabbitConnectionString: builder.Configuration["RabbitMQ:ConnectionString"]!)
    .AddCheck<{Entity}ServiceHealthCheck>("{entity}-service-health");

var app = builder.Build();

app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = _ => false // Liveness - just check if app is running
});

app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = _ => true // Readiness - check all dependencies
});

app.Run();
```

### Custom Health Check

```csharp
public sealed class {Entity}ServiceHealthCheck : IHealthCheck
{
    private readonly DataContext _dataContext;

    public {Entity}ServiceHealthCheck(DataContext dataContext)
    {
        _dataContext = dataContext;
    }

    public async Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context,
        CancellationToken cancellationToken = default)
    {
        try
        {
            // Check database connectivity
            await _dataContext.Database.CanConnectAsync(cancellationToken);

            return HealthCheckResult.Healthy("{Entity} service is healthy");
        }
        catch (Exception ex)
        {
            return HealthCheckResult.Unhealthy(
                "{Entity} service is unhealthy",
                exception: ex);
        }
    }
}
```

### Application Insights / Sentry

```csharp
// File: {ApplicationName}.Services.{Entity}/Program.cs

using I.Synergy.Framework.OpenTelemetry.Extensions;

var builder = WebApplication.CreateBuilder(args);

// Add OpenTelemetry with Application Insights
builder.Services.AddOpenTelemetryWithApplicationInsights(
    builder.Configuration["ApplicationInsights:ConnectionString"]!,
    "{entity}-service");

// Or with Sentry
builder.Services.AddSentry(options =>
{
    options.Dsn = builder.Configuration["Sentry:Dsn"];
    options.Environment = builder.Environment.EnvironmentName;
    options.TracesSampleRate = 1.0;
});

var app = builder.Build();
app.Run();
```

---

## Common Pitfalls

### ❌ WRONG - Shared Database

```csharp
// ❌ Multiple services accessing same database
public sealed class SharedDbContext : DbContext
{
    public DbSet<{Entity}> {Entities} { get; set; }
    public DbSet<{ChildEntity}> {ChildEntities} { get; set; }
}

// {Entity}Service and {ChildEntity}Service both use SharedDbContext
// This creates tight coupling and prevents independent deployment!
```

### ✅ CORRECT - Database Per Service

```csharp
// ✅ Each service has its own database
public sealed class {Entity}DbContext : DbContext
{
    public DbSet<{Entity}> {Entities} { get; set; }
}

public sealed class {ChildEntity}DbContext : DbContext
{
    public DbSet<{ChildEntity}> {ChildEntities} { get; set; }
}

public sealed class ReportingDbContext : DbContext
{
    public DbSet<Report> Reports { get; set; }
}
```

### ❌ WRONG - Synchronous Cascading Calls

```csharp
// ❌ Service A → Service B → Service C (synchronous chain)
// This creates latency and tight coupling

public async Task<OrderResponse> CreateOrderAsync(CreateOrderRequest request)
{
    // Call Service B
    var inventory = await _inventoryClient.ReserveInventoryAsync(request.Items);

    // Call Service C
    var payment = await _paymentClient.ProcessPaymentAsync(request.Amount);

    // If any service is slow or down, entire operation fails
    return new OrderResponse { /* ... */ };
}
```

### ✅ CORRECT - Event-Driven Approach

```csharp
// ✅ Service A publishes event, Services B and C react independently
public async Task<CreateOrderResponse> CreateOrderAsync(CreateOrderCommand command)
{
    // Create order
    var order = new Order
    {
        OrderId = Guid.NewGuid(),
        Items = command.Items,
        TotalAmount = command.TotalAmount
    };

    _dbContext.Orders.Add(order);
    await _dbContext.SaveChangesAsync();

    // Publish event
    await _publishEndpoint.Publish(new OrderCreatedEvent
    {
        OrderId = order.OrderId,
        Items = order.Items,
        TotalAmount = order.TotalAmount
    });

    // Return immediately - downstream services process asynchronously
    return new CreateOrderResponse(order.OrderId);
}
```

### ❌ WRONG - No Circuit Breaker

```csharp
// ❌ No resilience - if service is down, keeps trying indefinitely
public async Task<{Entity}Dto?> Get{Entity}Async(Guid {entity}Id)
{
    var response = await _httpClient.GetAsync($"/api/{entities}/{entity}Id");
    return await response.Content.ReadFromJsonAsync<{Entity}Dto>();
}
```

### ✅ CORRECT - Circuit Breaker Pattern

```csharp
// ✅ With circuit breaker and retry
builder.Services.AddHttpClient<{Entity}ServiceClient>()
    .AddStandardResilienceHandler(options =>
    {
        options.CircuitBreaker.FailureRatio = 0.5;
        options.Retry.MaxRetryAttempts = 3;
    });
```

---

## Best Practices Summary

### DO:
- ✅ Design services around business capabilities
- ✅ Use database per service pattern
- ✅ Implement circuit breaker and retry patterns
- ✅ Use asynchronous messaging for inter-service communication
- ✅ Implement distributed tracing with correlation IDs
- ✅ Use API Gateway for client-facing APIs
- ✅ Implement health checks (liveness and readiness)
- ✅ Use saga pattern for distributed transactions
- ✅ Deploy services independently
- ✅ Monitor and log extensively
- ✅ Use container orchestration (Kubernetes, .NET Aspire)
- ✅ Implement service discovery
- ✅ Version your APIs
- ✅ Use event-driven architecture where appropriate

### DON'T:
- ❌ Share databases across services
- ❌ Create synchronous cascading calls
- ❌ Skip circuit breakers and retries
- ❌ Ignore distributed tracing
- ❌ Deploy all services together (monolithic deployment)
- ❌ Use distributed transactions (2PC) - use sagas instead
- ❌ Ignore backward compatibility
- ❌ Skip health checks
- ❌ Hard-code service URLs
- ❌ Forget to handle partial failures

---

## Quality Checklist

- [ ] Services aligned with business capabilities (DDD)
- [ ] Each service has its own database
- [ ] API Gateway implemented for client access
- [ ] Inter-service communication uses HTTP/gRPC/messaging
- [ ] Circuit breaker implemented for external calls
- [ ] Retry policies configured
- [ ] Distributed tracing with correlation IDs
- [ ] Health checks (liveness and readiness) implemented
- [ ] Services independently deployable
- [ ] Saga pattern for distributed transactions
- [ ] Event-driven architecture for asynchronous operations
- [ ] Service discovery configured
- [ ] Container orchestration set up (Docker Compose/Kubernetes/Aspire)
- [ ] Monitoring and logging in place
- [ ] API versioning strategy defined
- [ ] Deployment strategy chosen (blue-green, canary, rolling)
- [ ] Authentication and authorization implemented
- [ ] Rate limiting and throttling configured
- [ ] Documentation for APIs (OpenAPI/Swagger)

---

**End of Microservices Architecture Pattern**
