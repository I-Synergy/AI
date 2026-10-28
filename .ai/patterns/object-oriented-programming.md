# Object-Oriented Programming (OOP) Pattern

## Overview

Object-Oriented Programming is a programming paradigm based on the concept of "objects" which contain data (fields/properties) and code (methods). This pattern emphasizes encapsulation, inheritance, polymorphism, and abstraction to create maintainable, reusable, and scalable software.

---

## SOLID Principles

### Single Responsibility Principle (SRP)

**Definition:** A class should have only one reason to change - it should have only one job or responsibility.

```csharp
// ✅ CORRECT - Single responsibility
public sealed class {Entity}Repository
{
    private readonly DataContext _dataContext;

    public {Entity}Repository(DataContext dataContext)
    {
        _dataContext = dataContext;
    }

    public async Task<{Entity}> GetByIdAsync(Guid id, CancellationToken ct)
    {
        return await _dataContext.{Entities}.FirstOrDefaultAsync(e => e.{Entity}Id == id, ct);
    }
}

public sealed class {Entity}Validator
{
    public ValidationResult Validate({Entity} {entity})
    {
        // Only validation logic
        if ({entity}.Amount <= 0)
            return ValidationResult.Fail("Amount must be positive");

        return ValidationResult.Success();
    }
}

// ❌ WRONG - Multiple responsibilities
public sealed class {Entity}Manager
{
    // Data access
    public async Task<{Entity}> GetByIdAsync(Guid id) { /* ... */ }

    // Validation
    public bool IsValid({Entity} {entity}) { /* ... */ }

    // Email sending
    public async Task SendNotificationAsync({Entity} {entity}) { /* ... */ }

    // Logging
    public void LogActivity(string message) { /* ... */ }
}
```

### Open/Closed Principle (OCP)

**Definition:** Software entities should be open for extension but closed for modification.

```csharp
// ✅ CORRECT - Open for extension via abstraction
public interface IPaymentProcessor
{
    Task<PaymentResult> ProcessAsync(decimal amount, CancellationToken ct);
}

public sealed class CreditCardPaymentProcessor : IPaymentProcessor
{
    public async Task<PaymentResult> ProcessAsync(decimal amount, CancellationToken ct)
    {
        // Credit card specific logic
        return new PaymentResult(true);
    }
}

public sealed class PayPalPaymentProcessor : IPaymentProcessor
{
    public async Task<PaymentResult> ProcessAsync(decimal amount, CancellationToken ct)
    {
        // PayPal specific logic
        return new PaymentResult(true);
    }
}

public sealed class PaymentService
{
    private readonly IPaymentProcessor _processor;

    public PaymentService(IPaymentProcessor processor)
    {
        _processor = processor;
    }

    public async Task ProcessPaymentAsync(decimal amount, CancellationToken ct)
    {
        await _processor.ProcessAsync(amount, ct);
    }
}

// ❌ WRONG - Modification required for new payment types
public sealed class PaymentService
{
    public async Task ProcessPaymentAsync(string type, decimal amount)
    {
        if (type == "CreditCard")
        {
            // Credit card logic
        }
        else if (type == "PayPal")
        {
            // PayPal logic
        }
        // Adding Bitcoin requires modifying this class!
    }
}
```

### Liskov Substitution Principle (LSP)

**Definition:** Objects of a superclass should be replaceable with objects of a subclass without breaking the application.

```csharp
// ✅ CORRECT - Derived types maintain base contract
public abstract class Document
{
    public string Title { get; init; } = string.Empty;

    public virtual async Task<byte[]> GenerateAsync(CancellationToken ct)
    {
        // Base implementation
        return Array.Empty<byte>();
    }
}

public sealed class PdfDocument : Document
{
    public override async Task<byte[]> GenerateAsync(CancellationToken ct)
    {
        // PDF-specific generation that honors the contract
        var pdfBytes = await GeneratePdfBytesAsync(ct);
        return pdfBytes; // Returns byte[] as expected
    }

    private async Task<byte[]> GeneratePdfBytesAsync(CancellationToken ct)
    {
        await Task.CompletedTask;
        return new byte[] { /* PDF data */ };
    }
}

public sealed class WordDocument : Document
{
    public override async Task<byte[]> GenerateAsync(CancellationToken ct)
    {
        // Word-specific generation that honors the contract
        var wordBytes = await GenerateWordBytesAsync(ct);
        return wordBytes;
    }

    private async Task<byte[]> GenerateWordBytesAsync(CancellationToken ct)
    {
        await Task.CompletedTask;
        return new byte[] { /* Word data */ };
    }
}

// ❌ WRONG - Violates LSP by changing behavior
public sealed class ReadOnlyDocument : Document
{
    public override async Task<byte[]> GenerateAsync(CancellationToken ct)
    {
        // Violates contract by throwing exception
        throw new NotSupportedException("Cannot generate read-only documents");
    }
}
```

### Interface Segregation Principle (ISP)

**Definition:** Clients should not be forced to depend on interfaces they don't use.

```csharp
// ✅ CORRECT - Segregated interfaces
public interface IReadable<T>
{
    Task<T> GetByIdAsync(Guid id, CancellationToken ct);
    Task<List<T>> GetAllAsync(CancellationToken ct);
}

public interface IWritable<T>
{
    Task<Guid> CreateAsync(T item, CancellationToken ct);
    Task UpdateAsync(T item, CancellationToken ct);
}

public interface IDeletable
{
    Task DeleteAsync(Guid id, CancellationToken ct);
}

// Read-only repository only implements what it needs
public sealed class ReadOnly{Entity}Repository : IReadable<{Entity}>
{
    private readonly DataContext _dataContext;

    public ReadOnly{Entity}Repository(DataContext dataContext)
    {
        _dataContext = dataContext;
    }

    public async Task<{Entity}> GetByIdAsync(Guid id, CancellationToken ct)
    {
        return await _dataContext.{Entities}.FirstOrDefaultAsync(e => e.{Entity}Id == id, ct);
    }

    public async Task<List<{Entity}>> GetAllAsync(CancellationToken ct)
    {
        return await _dataContext.Set<{Entity}>().ToListAsync(ct);
    }
}

// Full repository implements all interfaces
public sealed class {Entity}Repository : IReadable<{Entity}>, IWritable<{Entity}>, IDeletable
{
    private readonly DataContext _dataContext;

    public {Entity}Repository(DataContext dataContext)
    {
        _dataContext = dataContext;
    }

    public async Task<{Entity}> GetByIdAsync(Guid id, CancellationToken ct)
    {
        return await _dataContext.{Entities}.FirstOrDefaultAsync(e => e.{Entity}Id == id, ct);
    }

    public async Task<List<{Entity}>> GetAllAsync(CancellationToken ct)
    {
        return await _dataContext.Set<{Entity}>().ToListAsync(ct);
    }

    public async Task<Guid> CreateAsync({Entity} item, CancellationToken ct)
    {
        _dataContext.{Entities}.Add(item);
        await _dataContext.SaveChangesAsync(ct);
        return item.{Entity}Id;
    }

    public async Task UpdateAsync({Entity} item, CancellationToken ct)
    {
        var entity = await _dataContext.{Entities}.FirstOrDefaultAsync(b => b.{Entity}Id == item.{Entity}Id, ct);
        if (entity is null) throw new InvalidOperationException($"{Entity} {item.{Entity}Id} not found");
        entity.Name = item.Name;
        entity.Amount = item.Amount;
        await _dataContext.SaveChangesAsync(ct);
    }

    public async Task DeleteAsync(Guid id, CancellationToken ct)
    {
        var entity = await _dataContext.{Entities}.FirstOrDefaultAsync(e => e.{Entity}Id == id, ct);
        if (entity is null) throw new InvalidOperationException($"{Entity} {id} not found");
        _dataContext.{Entities}.Remove(entity);
        await _dataContext.SaveChangesAsync(ct);
    }
}

// ❌ WRONG - Fat interface forces unnecessary implementation
public interface IRepository<T>
{
    Task<T> GetByIdAsync(Guid id, CancellationToken ct);
    Task<List<T>> GetAllAsync(CancellationToken ct);
    Task<Guid> CreateAsync(T item, CancellationToken ct);
    Task UpdateAsync(T item, CancellationToken ct);
    Task DeleteAsync(Guid id, CancellationToken ct);
    Task BulkInsertAsync(List<T> items, CancellationToken ct);
    Task<int> CountAsync(CancellationToken ct);
    Task<bool> ExistsAsync(Guid id, CancellationToken ct);
}

// Read-only repository forced to implement write operations
public sealed class ReadOnlyRepository : IRepository<{Entity}>
{
    public async Task<Guid> CreateAsync({Entity} item, CancellationToken ct)
    {
        throw new NotSupportedException(); // Forced to implement!
    }

    public async Task UpdateAsync({Entity} item, CancellationToken ct)
    {
        throw new NotSupportedException(); // Forced to implement!
    }
}
```

### Dependency Inversion Principle (DIP)

**Definition:** High-level modules should not depend on low-level modules. Both should depend on abstractions.

```csharp
// ✅ CORRECT - Depend on abstractions
public interface IEmailService
{
    Task SendAsync(string to, string subject, string body, CancellationToken ct);
}

public sealed class SmtpEmailService : IEmailService
{
    private readonly IConfiguration _configuration;

    public SmtpEmailService(IConfiguration configuration)
    {
        _configuration = configuration;
    }

    public async Task SendAsync(string to, string subject, string body, CancellationToken ct)
    {
        // SMTP implementation
        await Task.CompletedTask;
    }
}

public sealed class {Entity}CreatedHandler : IEventHandler<{Entity}CreatedEvent>
{
    private readonly IEmailService _emailService; // Depends on abstraction

    public {Entity}CreatedHandler(IEmailService emailService)
    {
        _emailService = emailService;
    }

    public async Task HandleAsync({Entity}CreatedEvent domainEvent, CancellationToken ct)
    {
        await _emailService.SendAsync(
            "user@example.com",
            "{Entity} Created",
            $"{Entity} {domainEvent.Name} was created",
            ct);
    }
}

// ❌ WRONG - Depends on concrete implementation
public sealed class {Entity}CreatedHandler
{
    private readonly SmtpEmailService _emailService; // Concrete dependency!

    public {Entity}CreatedHandler()
    {
        _emailService = new SmtpEmailService(); // Creates dependency directly
    }

    public async Task HandleAsync({Entity}CreatedEvent domainEvent)
    {
        await _emailService.SendAsync(
            "user@example.com",
            "{Entity} Created",
            $"{Entity} {domainEvent.Name} was created");
    }
}
```

---

## Core OOP Concepts

### Encapsulation

**Definition:** Bundling data and methods that operate on that data within a single unit (class), and restricting access to internal state.

```csharp
// ✅ CORRECT - Properly encapsulated
public sealed class {Entity}
{
    private decimal _amount;
    private readonly List<{ChildEntity}> _{childEntities} = new();

    public Guid {Entity}Id { get; init; }
    public string Name { get; init; } = string.Empty;

    public decimal Amount
    {
        get => _amount;
        init
        {
            if (value <= 0)
                throw new ArgumentException("Amount must be positive", nameof(Amount));
            _amount = value;
        }
    }

    public IReadOnlyCollection<{ChildEntity}> {ChildEntities} => _{childEntities}.AsReadOnly();

    public void Add{ChildEntity}({ChildEntity} {childEntity})
    {
        ArgumentNullException.ThrowIfNull({childEntity});

        if (_{childEntities}.Any(g => g.{ChildEntity}Id == {childEntity}.{ChildEntity}Id))
            throw new InvalidOperationException("{ChildEntity} already exists");

        _{childEntities}.Add({childEntity});
    }

    public void Remove{ChildEntity}(Guid {childEntity}Id)
    {
        var {childEntity} = _{childEntities}.FirstOrDefault(g => g.{ChildEntity}Id == {childEntity}Id);
        if ({childEntity} is null)
            throw new InvalidOperationException("{ChildEntity} not found");

        _{childEntities}.Remove({childEntity});
    }
}

// ❌ WRONG - Poor encapsulation
public sealed class {Entity}
{
    public Guid {Entity}Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public decimal Amount { get; set; } // No validation!
    public List<{ChildEntity}> {ChildEntities} { get; set; } = new(); // Direct access to mutable collection!
}
```

### Inheritance

**Definition:** Mechanism where a new class derives properties and behavior from an existing class.

```csharp
// ✅ CORRECT - Inheritance with proper abstraction
public abstract class Entity
{
    public Guid Id { get; init; }
    public DateTimeOffset CreatedDate { get; init; }
    public DateTimeOffset? ChangedDate { get; set; }

    protected Entity()
    {
        Id = Guid.NewGuid();
        CreatedDate = DateTimeOffset.UtcNow;
    }
}

public abstract class AuditableEntity : Entity
{
    public string CreatedBy { get; init; } = string.Empty;
    public string? ChangedBy { get; set; }
}

public sealed class {Entity} : AuditableEntity
{
    public string Name { get; init; } = string.Empty;
    public decimal Amount { get; init; }

    // Inherits: Id, CreatedDate, ChangedDate, CreatedBy, ChangedBy
}

// ✅ CORRECT - Composition over inheritance (often preferred)
public sealed class {Entity}
{
    public Guid {Entity}Id { get; init; }
    public string Name { get; init; } = string.Empty;
    public decimal Amount { get; init; }
    public AuditInfo AuditInfo { get; init; } = new(); // Composition
}

public sealed class AuditInfo
{
    public DateTimeOffset CreatedDate { get; init; }
    public string CreatedBy { get; init; } = string.Empty;
    public DateTimeOffset? ChangedDate { get; set; }
    public string? ChangedBy { get; set; }
}

// ❌ WRONG - Deep inheritance hierarchy (fragile)
public class BaseEntity { }
public class AuditableEntity : BaseEntity { }
public class VersionedEntity : AuditableEntity { }
public class SoftDeletableEntity : VersionedEntity { }
public class {Entity} : SoftDeletableEntity { } // Too many levels!
```

### Polymorphism

**Definition:** Ability of objects to take on multiple forms, allowing methods to be used interchangeably.

```csharp
// ✅ CORRECT - Polymorphism via interfaces
public interface IDocumentGenerator
{
    Task<byte[]> GenerateAsync({Entity} {entity}, CancellationToken ct);
}

public sealed class PdfDocumentGenerator : IDocumentGenerator
{
    public async Task<byte[]> GenerateAsync({Entity} {entity}, CancellationToken ct)
    {
        // PDF-specific generation
        await Task.CompletedTask;
        return new byte[] { /* PDF data */ };
    }
}

public sealed class ExcelDocumentGenerator : IDocumentGenerator
{
    public async Task<byte[]> GenerateAsync({Entity} {entity}, CancellationToken ct)
    {
        // Excel-specific generation
        await Task.CompletedTask;
        return new byte[] { /* Excel data */ };
    }
}

public sealed class DocumentService
{
    public async Task<byte[]> GenerateDocumentAsync(
        {Entity} {entity},
        IDocumentGenerator generator,
        CancellationToken ct)
    {
        // Polymorphic call - works with any IDocumentGenerator
        return await generator.GenerateAsync({entity}, ct);
    }
}

// ✅ CORRECT - Polymorphism via abstract base class
public abstract class NotificationSender
{
    public abstract Task SendAsync(string message, CancellationToken ct);

    // Template method pattern
    public async Task SendWithRetryAsync(string message, CancellationToken ct)
    {
        for (int i = 0; i < 3; i++)
        {
            try
            {
                await SendAsync(message, ct);
                return;
            }
            catch when (i < 2)
            {
                await Task.Delay(1000 * (i + 1), ct);
            }
        }
    }
}

public sealed class EmailNotificationSender : NotificationSender
{
    public override async Task SendAsync(string message, CancellationToken ct)
    {
        // Email-specific implementation
        await Task.CompletedTask;
    }
}

public sealed class SmsNotificationSender : NotificationSender
{
    public override async Task SendAsync(string message, CancellationToken ct)
    {
        // SMS-specific implementation
        await Task.CompletedTask;
    }
}
```

### Abstraction

**Definition:** Hiding complex implementation details and exposing only necessary features.

```csharp
// ✅ CORRECT - Clean abstraction
public interface I{Entity}Calculator
{
    decimal CalculateRemaining({Entity} {entity});
    decimal CalculateAllocated({Entity} {entity});
    bool IsOver{Entity}({Entity} {entity});
}

public sealed class {Entity}Calculator : I{Entity}Calculator
{
    public decimal CalculateRemaining({Entity} {entity})
    {
        ArgumentNullException.ThrowIfNull({entity});

        var allocated = CalculateAllocated({entity});
        return {entity}.Amount - allocated;
    }

    public decimal CalculateAllocated({Entity} {entity})
    {
        ArgumentNullException.ThrowIfNull({entity});

        return {entity}.{ChildEntities}.Sum(g => g.Amount);
    }

    public bool IsOver{Entity}({Entity} {entity})
    {
        ArgumentNullException.ThrowIfNull({entity});

        return CalculateRemaining({entity}) < 0;
    }
}

// Consumer doesn't need to know implementation details
public sealed class {Entity}Service
{
    private readonly I{Entity}Calculator _calculator;

    public {Entity}Service(I{Entity}Calculator calculator)
    {
        _calculator = calculator;
    }

    public async Task<{Entity}Summary> GetSummaryAsync({Entity} {entity}, CancellationToken ct)
    {
        return new {Entity}Summary(
            {entity}.{Entity}Id,
            {entity}.Name,
            _calculator.CalculateRemaining({entity}),
            _calculator.IsOver{Entity}({entity}));
    }
}

// ❌ WRONG - Leaky abstraction
public interface I{Entity}Calculator
{
    // Exposes internal implementation details
    Dictionary<string, decimal> GetInternalCalculationCache();
    void SetCacheExpiration(TimeSpan expiration);
    List<string> GetDebugLogs();
}
```

---

## Design Patterns (Gang of Four)

### Creational Patterns

#### Factory Pattern

**Purpose:** Create objects without specifying exact class.

```csharp
// ✅ CORRECT - Factory pattern
public interface IPaymentProcessorFactory
{
    IPaymentProcessor Create(PaymentMethod method);
}

public sealed class PaymentProcessorFactory : IPaymentProcessorFactory
{
    private readonly IServiceProvider _serviceProvider;

    public PaymentProcessorFactory(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }

    public IPaymentProcessor Create(PaymentMethod method)
    {
        return method switch
        {
            PaymentMethod.CreditCard => _serviceProvider.GetRequiredService<CreditCardPaymentProcessor>(),
            PaymentMethod.PayPal => _serviceProvider.GetRequiredService<PayPalPaymentProcessor>(),
            PaymentMethod.Bitcoin => _serviceProvider.GetRequiredService<BitcoinPaymentProcessor>(),
            _ => throw new ArgumentException($"Unknown payment method: {method}", nameof(method))
        };
    }
}

public enum PaymentMethod
{
    CreditCard,
    PayPal,
    Bitcoin
}
```

#### Builder Pattern

**Purpose:** Construct complex objects step by step.

```csharp
// ✅ CORRECT - Builder pattern
public sealed class {Entity}Builder
{
    private string _name = string.Empty;
    private decimal _amount;
    private DateTimeOffset _startDate = DateTimeOffset.UtcNow;
    private readonly List<{ChildEntity}> _{childEntities} = new();

    public {Entity}Builder WithName(string name)
    {
        _name = name;
        return this;
    }

    public {Entity}Builder WithAmount(decimal amount)
    {
        _amount = amount;
        return this;
    }

    public {Entity}Builder WithStartDate(DateTimeOffset startDate)
    {
        _startDate = startDate;
        return this;
    }

    public {Entity}Builder Add{ChildEntity}({ChildEntity} {childEntity})
    {
        _{childEntities}.Add({childEntity});
        return this;
    }

    public {Entity} Build()
    {
        var {entity} = new {Entity}
        {
            {Entity}Id = Guid.NewGuid(),
            Name = _name,
            Amount = _amount,
            StartDate = _startDate,
            CreatedDate = DateTimeOffset.UtcNow
        };

        foreach (var {childEntity} in _{childEntities})
        {
            {entity}.Add{ChildEntity}({childEntity});
        }

        return {entity};
    }
}

// Usage
var {entity} = new {Entity}Builder()
    .WithName("Example")
    .WithAmount(50000m)
    .WithStartDate(new DateTimeOffset(2025, 1, 1, 0, 0, 0, TimeSpan.Zero))
    .Add{ChildEntity}(new {ChildEntity} { Name = "Example", Amount = 10000m })
    .Build();
```

#### Singleton Pattern

**Purpose:** Ensure only one instance exists.

```csharp
// ✅ CORRECT - Singleton via DI (preferred in .NET)
public interface IApplicationCache
{
    void Set(string key, object value);
    object? Get(string key);
}

public sealed class ApplicationCache : IApplicationCache
{
    private readonly ConcurrentDictionary<string, object> _cache = new();

    public void Set(string key, object value)
    {
        _cache[key] = value;
    }

    public object? Get(string key)
    {
        _cache.TryGetValue(key, out var value);
        return value;
    }
}

// Register as singleton in DI
services.AddSingleton<IApplicationCache, ApplicationCache>();

// ❌ WRONG - Classic singleton (anti-pattern in modern .NET)
public sealed class ApplicationCache
{
    private static readonly Lazy<ApplicationCache> _instance =
        new(() => new ApplicationCache());

    public static ApplicationCache Instance => _instance.Value;

    private ApplicationCache() { } // Private constructor
}
```

#### Prototype Pattern

**Purpose:** Create new objects by copying existing ones.

```csharp
// ✅ CORRECT - Prototype pattern
public interface ICloneable<T>
{
    T Clone();
}

public sealed class {Entity}Template : ICloneable<{Entity}Template>
{
    public string Name { get; init; } = string.Empty;
    public decimal Amount { get; init; }
    public List<{ChildEntity}Template> {ChildEntities} { get; init; } = new();

    public {Entity}Template Clone()
    {
        return new {Entity}Template
        {
            Name = Name,
            Amount = Amount,
            {ChildEntities} = {ChildEntities}.Select(child => child.Clone()).ToList()
        };
    }

    public {Entity} Create{Entity}()
    {
        var {entity} = new {Entity}
        {
            {Entity}Id = Guid.NewGuid(),
            Name = Name,
            Amount = Amount,
            CreatedDate = DateTimeOffset.UtcNow
        };

        foreach (var {childEntity}Template in {ChildEntities})
        {
            {entity}.Add{ChildEntity}({childEntity}Template.Create{ChildEntity}());
        }

        return {entity};
    }
}

public sealed class {ChildEntity}Template : ICloneable<{ChildEntity}Template>
{
    public string Name { get; init; } = string.Empty;
    public decimal Amount { get; init; }

    public {ChildEntity}Template Clone()
    {
        return new {ChildEntity}Template
        {
            Name = Name,
            Amount = Amount
        };
    }

    public {ChildEntity} Create{ChildEntity}()
    {
        return new {ChildEntity}
        {
            {ChildEntity}Id = Guid.NewGuid(),
            Name = Name,
            Amount = Amount,
            CreatedDate = DateTimeOffset.UtcNow
        };
    }
}
```

### Structural Patterns

#### Adapter Pattern

**Purpose:** Allow incompatible interfaces to work together.

```csharp
// ✅ CORRECT - Adapter pattern
// Legacy system interface
public interface ILegacy{Entity}System
{
    string Get{Entity}Data(int {entity}Id);
}

// New system interface
public interface I{Entity}Service
{
    Task<{Entity}> Get{Entity}Async(Guid {entity}Id, CancellationToken ct);
}

// Adapter
public sealed class Legacy{Entity}Adapter : I{Entity}Service
{
    private readonly ILegacy{Entity}System _legacySystem;

    public Legacy{Entity}Adapter(ILegacy{Entity}System legacySystem)
    {
        _legacySystem = legacySystem;
    }

    public async Task<{Entity}> Get{Entity}Async(Guid {entity}Id, CancellationToken ct)
    {
        // Convert Guid to int for legacy system
        var legacyId = Math.Abs({entity}Id.GetHashCode());

        // Call legacy system
        var legacyData = _legacySystem.Get{Entity}Data(legacyId);

        // Parse and adapt to new format
        var parts = legacyData.Split('|');

        return await Task.FromResult(new {Entity}
        {
            {Entity}Id = {entity}Id,
            Name = parts[0],
            Amount = decimal.Parse(parts[1]),
            CreatedDate = DateTimeOffset.Parse(parts[2])
        });
    }
}
```

#### Decorator Pattern

**Purpose:** Add behavior to objects dynamically.

```csharp
// ✅ CORRECT - Decorator pattern
public interface I{Entity}Calculator
{
    decimal CalculateRemaining({Entity} {entity});
}

// Base implementation
public sealed class Simple{Entity}Calculator : I{Entity}Calculator
{
    public decimal CalculateRemaining({Entity} {entity})
    {
        var allocated = {entity}.{ChildEntities}.Sum(g => g.Amount);
        return {entity}.Amount - allocated;
    }
}

// Decorator: Add logging
public sealed class Logging{Entity}CalculatorDecorator : I{Entity}Calculator
{
    private readonly I{Entity}Calculator _inner;
    private readonly ILogger<Logging{Entity}CalculatorDecorator> _logger;

    public Logging{Entity}CalculatorDecorator(
        I{Entity}Calculator inner,
        ILogger<Logging{Entity}CalculatorDecorator> logger)
    {
        _inner = inner;
        _logger = logger;
    }

    public decimal CalculateRemaining({Entity} {entity})
    {
        _logger.LogDebug("Calculating remaining for {entity} {Entity}Id", {entity}.{Entity}Id);

        var result = _inner.CalculateRemaining({entity});

        _logger.LogDebug(
            "{Entity}Id has {Remaining} remaining",
            {entity}.{Entity}Id, result);

        return result;
    }
}

// Decorator: Add caching
public sealed class Caching{Entity}CalculatorDecorator : I{Entity}Calculator
{
    private readonly I{Entity}Calculator _inner;
    private readonly IDistributedCache _cache;

    public Caching{Entity}CalculatorDecorator(
        I{Entity}Calculator inner,
        IDistributedCache cache)
    {
        _inner = inner;
        _cache = cache;
    }

    public decimal CalculateRemaining({Entity} {entity})
    {
        var cacheKey = $"{entity}:remaining:{entity}.{Entity}Id}";
        var cached = _cache.GetString(cacheKey);

        if (cached is not null)
            return decimal.Parse(cached);

        var result = _inner.CalculateRemaining({entity});

        _cache.SetString(cacheKey, result.ToString(), new DistributedCacheEntryOptions
        {
            AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5)
        });

        return result;
    }
}

// Registration with multiple decorators
services.AddScoped<Simple{Entity}Calculator>();
services.AddScoped<I{Entity}Calculator>(sp =>
{
    var simple = sp.GetRequiredService<Simple{Entity}Calculator>();
    var logger = sp.GetRequiredService<ILogger<Logging{Entity}CalculatorDecorator>>();
    var cache = sp.GetRequiredService<IDistributedCache>();

    // Wrap with logging, then caching
    var withLogging = new Logging{Entity}CalculatorDecorator(simple, logger);
    return new Caching{Entity}CalculatorDecorator(withLogging, cache);
});
```

#### Facade Pattern

**Purpose:** Provide simplified interface to complex subsystem.

```csharp
// ✅ CORRECT - Facade pattern
public interface I{Entity}ManagementFacade
{
    Task<{Entity}Summary> Create{Entity}With{ChildEntities}Async(
        string {entity}Name,
        decimal {entity}Amount,
        List<{ChildEntity}Data> {childEntities},
        CancellationToken ct);
}

public sealed class {Entity}ManagementFacade : I{Entity}ManagementFacade
{
    private readonly ICommandHandler<Create{Entity}Command, Create{Entity}Response> _create{Entity}Handler;
    private readonly ICommandHandler<Create{ChildEntity}Command, Create{ChildEntity}Response> _create{ChildEntity}Handler;
    private readonly IQueryHandler<Get{Entity}ByIdQuery, {Entity}Response> _get{Entity}Handler;
    private readonly I{Entity}Calculator _calculator;
    private readonly ILogger<{Entity}ManagementFacade> _logger;

    public {Entity}ManagementFacade(
        ICommandHandler<Create{Entity}Command, Create{Entity}Response> create{Entity}Handler,
        ICommandHandler<Create{ChildEntity}Command, Create{ChildEntity}Response> create{ChildEntity}Handler,
        IQueryHandler<Get{Entity}ByIdQuery, {Entity}Response> get{Entity}Handler,
        I{Entity}Calculator calculator,
        ILogger<{Entity}ManagementFacade> logger)
    {
        _create{Entity}Handler = create{Entity}Handler;
        _create{ChildEntity}Handler = create{ChildEntity}Handler;
        _get{Entity}Handler = get{Entity}Handler;
        _calculator = calculator;
        _logger = logger;
    }

    public async Task<{Entity}Summary> Create{Entity}With{ChildEntities}Async(
        string {entity}Name,
        decimal {entity}Amount,
        List<{ChildEntity}Data> {childEntities},
        CancellationToken ct)
    {
        _logger.LogInformation("Creating {entity} {Entity}Name with {ChildEntity}Count {childEntities}",
            {entity}Name, {childEntities}.Count);

        // Step 1: Create {entity}
        var create{Entity}Command = new Create{Entity}Command(
            {entity}Name,
            {entity}Amount,
            DateTimeOffset.UtcNow);

        var {entity}Response = await _create{Entity}Handler.HandleAsync(create{Entity}Command, ct);

        // Step 2: Create all {childEntities}
        foreach (var {childEntity}Data in {childEntities})
        {
            var create{ChildEntity}Command = new Create{ChildEntity}Command(
                {entity}Response.{Entity}Id,
                {childEntity}Data.Name,
                {childEntity}Data.Amount,
                {childEntity}Data.TargetDate);

            await _create{ChildEntity}Handler.HandleAsync(create{ChildEntity}Command, ct);
        }

        // Step 3: Get {entity} details
        var get{Entity}Query = new Get{Entity}ByIdQuery({entity}Response.{Entity}Id);
        var {entity} = await _get{Entity}Handler.HandleAsync(get{Entity}Query, ct);

        // Step 4: Calculate summary
        return new {Entity}Summary(
            {entity}.{Entity}Id,
            {entity}.Name,
            {entity}.Amount,
            {childEntities}.Sum(g => g.Amount),
            {entity}.Amount - {childEntities}.Sum(g => g.Amount));
    }
}

public record {ChildEntity}Data(string Name, decimal Amount, DateTimeOffset TargetDate);
public record {Entity}Summary(Guid {Entity}Id, string Name, decimal Total, decimal Allocated, decimal Remaining);
```

#### Proxy Pattern

**Purpose:** Provide substitute or placeholder for another object.

```csharp
// ✅ CORRECT - Proxy pattern (caching proxy)
public interface I{Entity}Service
{
    Task<{Entity}> Get{Entity}Async(Guid {entity}Id, CancellationToken ct);
}

public sealed class {Entity}Service : I{Entity}Service
{
    private readonly DataContext _dataContext;

    public {Entity}Service(DataContext dataContext)
    {
        _dataContext = dataContext;
    }

    public async Task<{Entity}> Get{Entity}Async(Guid {entity}Id, CancellationToken ct)
    {
        return await _dataContext.{Entities}.FirstOrDefaultAsync(e => e.{Entity}Id == {entity}Id, ct);
    }
}

public sealed class Caching{Entity}ServiceProxy : I{Entity}Service
{
    private readonly I{Entity}Service _realService;
    private readonly IDistributedCache _cache;

    public Caching{Entity}ServiceProxy(
        I{Entity}Service realService,
        IDistributedCache cache)
    {
        _realService = realService;
        _cache = cache;
    }

    public async Task<{Entity}> Get{Entity}Async(Guid {entity}Id, CancellationToken ct)
    {
        var cacheKey = $"{entity}:{entity}Id";
        var cached = await _cache.GetStringAsync(cacheKey, ct);

        if (cached is not null)
        {
            return JsonSerializer.Deserialize<{Entity}>(cached)!;
        }

        var {entity} = await _realService.Get{Entity}Async({entity}Id, ct);

        await _cache.SetStringAsync(
            cacheKey,
            JsonSerializer.Serialize({entity}),
            new DistributedCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(10)
            },
            ct);

        return {entity};
    }
}
```

### Behavioral Patterns

#### Strategy Pattern

**Purpose:** Define family of algorithms, encapsulate each one, make them interchangeable.

```csharp
// ✅ CORRECT - Strategy pattern
public interface I{Entity}AllocationStrategy
{
    List<{ChildEntity}Allocation> Allocate(decimal totalAmount, List<{ChildEntity}> {childEntities});
}

public sealed class EqualAllocationStrategy : I{Entity}AllocationStrategy
{
    public List<{ChildEntity}Allocation> Allocate(decimal totalAmount, List<{ChildEntity}> {childEntities})
    {
        var amountPer{ChildEntity} = totalAmount / {childEntities}.Count;

        return {childEntities}.Select(g => new {ChildEntity}Allocation(
            g.{ChildEntity}Id,
            g.Name,
            amountPer{ChildEntity})).ToList();
    }
}

public sealed class ProportionalAllocationStrategy : I{Entity}AllocationStrategy
{
    public List<{ChildEntity}Allocation> Allocate(decimal totalAmount, List<{ChildEntity}> {childEntities})
    {
        var totalTarget = {childEntities}.Sum(g => g.Amount);

        return {childEntities}.Select(g => new {ChildEntity}Allocation(
            g.{ChildEntity}Id,
            g.Name,
            totalAmount * (g.Amount / totalTarget))).ToList();
    }
}

public sealed class PriorityAllocationStrategy : I{Entity}AllocationStrategy
{
    public List<{ChildEntity}Allocation> Allocate(decimal totalAmount, List<{ChildEntity}> {childEntities})
    {
        var allocations = new List<{ChildEntity}Allocation>();
        var remaining = totalAmount;

        foreach (var {childEntity} in {childEntities}.OrderByDescending(g => g.Priority))
        {
            var allocation = Math.Min(remaining, {childEntity}.Amount);
            allocations.Add(new {ChildEntity}Allocation({childEntity}.{ChildEntity}Id, {childEntity}.Name, allocation));
            remaining -= allocation;

            if (remaining <= 0)
                break;
        }

        return allocations;
    }
}

public sealed class {Entity}Allocator
{
    private readonly I{Entity}AllocationStrategy _strategy;

    public {Entity}Allocator(I{Entity}AllocationStrategy strategy)
    {
        _strategy = strategy;
    }

    public List<{ChildEntity}Allocation> Allocate{Entity}(decimal totalAmount, List<{ChildEntity}> {childEntities})
    {
        return _strategy.Allocate(totalAmount, {childEntities});
    }
}

public record {ChildEntity}Allocation(Guid {ChildEntity}Id, string Name, decimal Amount);
```

#### Observer Pattern

**Purpose:** Define one-to-many dependency so when one object changes, dependents are notified.

```csharp
// ✅ CORRECT - Observer pattern (domain events)
public interface I{Entity}Observer
{
    Task On{Entity}ChangedAsync({Entity} {entity}, CancellationToken ct);
}

public sealed class {Entity}AlertObserver : I{Entity}Observer
{
    private readonly ILogger<{Entity}AlertObserver> _logger;

    public {Entity}AlertObserver(ILogger<{Entity}AlertObserver> logger)
    {
        _logger = logger;
    }

    public async Task On{Entity}ChangedAsync({Entity} {entity}, CancellationToken ct)
    {
        var allocated = {entity}.{ChildEntities}.Sum(g => g.Amount);
        var remaining = {entity}.Amount - allocated;

        if (remaining < 0)
        {
            _logger.LogWarning(
                "{Entity}Id is over its limit by {Amount}",
                {entity}.{Entity}Id, Math.Abs(remaining));
        }

        await Task.CompletedTask;
    }
}

public sealed class {Entity}CacheInvalidationObserver : I{Entity}Observer
{
    private readonly IDistributedCache _cache;

    public {Entity}CacheInvalidationObserver(IDistributedCache cache)
    {
        _cache = cache;
    }

    public async Task On{Entity}ChangedAsync({Entity} {entity}, CancellationToken ct)
    {
        var cacheKey = $"{entity}:{entity}.{Entity}Id}";
        await _cache.RemoveAsync(cacheKey, ct);
    }
}

public sealed class {Entity}Subject
{
    private readonly List<I{Entity}Observer> _observers = new();

    public void Attach(I{Entity}Observer observer)
    {
        _observers.Add(observer);
    }

    public void Detach(I{Entity}Observer observer)
    {
        _observers.Remove(observer);
    }

    public async Task NotifyAsync({Entity} {entity}, CancellationToken ct)
    {
        foreach (var observer in _observers)
        {
            await observer.On{Entity}ChangedAsync({entity}, ct);
        }
    }
}
```

#### Command Pattern

**Purpose:** Encapsulate request as an object.

```csharp
// ✅ CORRECT - Command pattern (CQRS implementation)
public interface ICommand<TResponse>
{
}

public interface ICommandHandler<TCommand, TResponse>
    where TCommand : ICommand<TResponse>
{
    Task<TResponse> HandleAsync(TCommand command, CancellationToken ct);
}

public sealed record Create{Entity}Command(
    string Name,
    decimal Amount,
    DateTimeOffset StartDate
) : ICommand<Create{Entity}Response>;

public sealed record Create{Entity}Response(Guid {Entity}Id);

public sealed class Create{Entity}CommandHandler : ICommandHandler<Create{Entity}Command, Create{Entity}Response>
{
    private readonly DataContext _dataContext;
    private readonly ILogger<Create{Entity}CommandHandler> _logger;

    public Create{Entity}CommandHandler(DataContext dataContext, ILogger<Create{Entity}CommandHandler> logger)
    {
        _dataContext = dataContext;
        _logger = logger;
    }

    public async Task<Create{Entity}Response> HandleAsync(
        Create{Entity}Command command,
        CancellationToken ct)
    {
        _logger.LogInformation("Creating {entity} {Name}", command.Name);

        var {entity} = new {Entity}
        {
            {Entity}Id = Guid.NewGuid(),
            Name = command.Name,
            Amount = command.Amount,
            StartDate = command.StartDate,
            CreatedDate = DateTimeOffset.UtcNow
        };

        _dataContext.{Entities}.Add({entity});
        await _dataContext.SaveChangesAsync(ct);

        return new Create{Entity}Response({entity}.{Entity}Id);
    }
}
```

#### Template Method Pattern

**Purpose:** Define skeleton of algorithm, let subclasses override specific steps.

```csharp
// ✅ CORRECT - Template method pattern
public abstract class ReportGenerator
{
    public async Task<byte[]> GenerateReportAsync(Guid {entity}Id, CancellationToken ct)
    {
        // Template method defining the algorithm
        var data = await FetchDataAsync({entity}Id, ct);
        var processedData = ProcessData(data);
        ValidateData(processedData);
        var formatted = FormatData(processedData);
        return await RenderAsync(formatted, ct);
    }

    protected abstract Task<{Entity}Data> FetchDataAsync(Guid {entity}Id, CancellationToken ct);
    protected abstract Processed{Entity}Data ProcessData({Entity}Data data);
    protected abstract string FormatData(Processed{Entity}Data data);
    protected abstract Task<byte[]> RenderAsync(string formatted, CancellationToken ct);

    protected virtual void ValidateData(Processed{Entity}Data data)
    {
        // Default validation (can be overridden)
        if (data.TotalAmount <= 0)
            throw new InvalidOperationException("Invalid {entity} data");
    }
}

public sealed class PdfReportGenerator : ReportGenerator
{
    private readonly DataContext _dataContext;

    public PdfReportGenerator(DataContext dataContext)
    {
        _dataContext = dataContext;
    }

    protected override async Task<{Entity}Data> FetchDataAsync(Guid {entity}Id, CancellationToken ct)
    {
        var {entity} = await _dataContext.{Entities}.FirstOrDefaultAsync(e => e.{Entity}Id == {entity}Id, ct);
        return new {Entity}Data({entity}.Name, {entity}.Amount);
    }

    protected override Processed{Entity}Data ProcessData({Entity}Data data)
    {
        return new Processed{Entity}Data(data.Name, data.Amount, DateTimeOffset.UtcNow);
    }

    protected override string FormatData(Processed{Entity}Data data)
    {
        return $"{Entity} Report: {data.Name}\nAmount: {data.TotalAmount:C}\nGenerated: {data.GeneratedAt}";
    }

    protected override async Task<byte[]> RenderAsync(string formatted, CancellationToken ct)
    {
        // PDF rendering logic
        await Task.CompletedTask;
        return Encoding.UTF8.GetBytes(formatted); // Simplified
    }
}

public record {Entity}Data(string Name, decimal Amount);
public record Processed{Entity}Data(string Name, decimal TotalAmount, DateTimeOffset GeneratedAt);
```

---

## C# 14 OOP Features

### Records

```csharp
// ✅ CORRECT - Using records for immutable data
public sealed record {Entity}Summary(
    Guid {Entity}Id,
    string Name,
    decimal TotalAmount,
    decimal AllocatedAmount)
{
    public decimal RemainingAmount => TotalAmount - AllocatedAmount;
    public bool IsOver{Entity} => RemainingAmount < 0;
}

// With expressions for non-destructive mutation
var original = new {Entity}Summary(Guid.NewGuid(), "Example {Entity}", 50000m, 30000m);
var updated = original with { AllocatedAmount = 35000m };

// Value equality
var {entity}1 = new {Entity}Summary(Guid.NewGuid(), "Test", 1000m, 500m);
var {entity}2 = new {Entity}Summary({entity}1.{Entity}Id, "Test", 1000m, 500m);
var areEqual = {entity}1 == {entity}2; // True - value equality
```

### Init-Only Properties

```csharp
// ✅ CORRECT - Init-only properties for immutability
public sealed class {Entity}
{
    public Guid {Entity}Id { get; init; }
    public string Name { get; init; } = string.Empty;
    public decimal Amount { get; init; }
    public DateTimeOffset CreatedDate { get; init; }

    // Can only be set during object initialization
    public {Entity}()
    {
        {Entity}Id = Guid.NewGuid();
        CreatedDate = DateTimeOffset.UtcNow;
    }
}

// Usage
var {entity} = new {Entity}
{
    Name = "Example {Entity}",
    Amount = 50000m
    // {Entity}Id and CreatedDate set by constructor
};

// {entity}.Name = "New Name"; // Compile error!
```

### Required Members (C# 11+)

```csharp
// ✅ CORRECT - Required members
public sealed class Create{Entity}Request
{
    public required string Name { get; init; }
    public required decimal Amount { get; init; }
    public DateTimeOffset? StartDate { get; init; }
}

// Usage
var request = new Create{Entity}Request
{
    Name = "Example {Entity}",
    Amount = 50000m
    // StartDate is optional
};

// var invalid = new Create{Entity}Request { Amount = 1000m }; // Compile error - Name required!
```

### Pattern Matching

```csharp
// ✅ CORRECT - Advanced pattern matching
public sealed class {Entity}StatusCalculator
{
    public string GetStatus({Entity} {entity})
    {
        var remaining = {entity}.Amount - {entity}.{ChildEntities}.Sum(g => g.Amount);

        return {entity} switch
        {
            { Amount: <= 0 } => "Invalid",
            _ when remaining < 0 => "Over Limit",
            _ when remaining == 0 => "Fully Allocated",
            _ when remaining < {entity}.Amount * 0.1m => "Nearly Allocated",
            _ => "Available"
        };
    }

    public decimal CalculateFee({Entity} {entity}) => {entity}.Amount switch
    {
        < 1000m => 0m,
        >= 1000m and < 10000m => {entity}.Amount * 0.01m,
        >= 10000m and < 100000m => {entity}.Amount * 0.005m,
        _ => {entity}.Amount * 0.001m
    };
}
```

---

## Anti-Patterns to Avoid

### God Object

```csharp
// ❌ WRONG - God object doing everything
public sealed class {Entity}Manager
{
    // Data access
    public async Task<{Entity}> Get{Entity}Async(Guid id) { /* ... */ }
    public async Task Save{Entity}Async({Entity} {entity}) { /* ... */ }

    // Validation
    public bool Validate{Entity}({Entity} {entity}) { /* ... */ }

    // Calculations
    public decimal CalculateRemaining({Entity} {entity}) { /* ... */ }
    public decimal CalculateAllocated({Entity} {entity}) { /* ... */ }

    // Notifications
    public async Task SendEmailAsync({Entity} {entity}) { /* ... */ }
    public async Task SendSmsAsync({Entity} {entity}) { /* ... */ }

    // Reporting
    public async Task<byte[]> GeneratePdfAsync({Entity} {entity}) { /* ... */ }
    public async Task<byte[]> GenerateExcelAsync({Entity} {entity}) { /* ... */ }

    // Caching
    public void Cache{Entity}({Entity} {entity}) { /* ... */ }
    public {Entity}? GetCached{Entity}(Guid id) { /* ... */ }
}

// ✅ CORRECT - Separated responsibilities
public sealed class {Entity}Repository { /* Data access only */ }
public sealed class {Entity}Validator { /* Validation only */ }
public sealed class {Entity}Calculator { /* Calculations only */ }
public sealed class {Entity}NotificationService { /* Notifications only */ }
public sealed class {Entity}ReportGenerator { /* Reporting only */ }
public sealed class {Entity}CacheService { /* Caching only */ }
```

### Anemic Domain Model

```csharp
// ❌ WRONG - Anemic domain model (data bag with no behavior)
public sealed class {Entity}
{
    public Guid {Entity}Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public decimal Amount { get; set; }
    public List<{ChildEntity}> {ChildEntities} { get; set; } = new();
}

public sealed class {Entity}Service
{
    public decimal CalculateRemaining({Entity} {entity})
    {
        return {entity}.Amount - {entity}.{ChildEntities}.Sum(g => g.Amount);
    }

    public bool CanAdd{ChildEntity}({Entity} {entity}, {ChildEntity} {childEntity})
    {
        var remaining = CalculateRemaining({entity});
        return remaining >= {childEntity}.Amount;
    }
}

// ✅ CORRECT - Rich domain model with behavior
public sealed class {Entity}
{
    private readonly List<{ChildEntity}> _{childEntities} = new();

    public Guid {Entity}Id { get; init; }
    public string Name { get; init; } = string.Empty;
    public decimal Amount { get; init; }
    public IReadOnlyCollection<{ChildEntity}> {ChildEntities} => _{childEntities}.AsReadOnly();

    public decimal CalculateRemaining()
    {
        return Amount - _{childEntities}.Sum(g => g.Amount);
    }

    public bool CanAdd{ChildEntity}({ChildEntity} {childEntity})
    {
        ArgumentNullException.ThrowIfNull({childEntity});
        return CalculateRemaining() >= {childEntity}.Amount;
    }

    public void Add{ChildEntity}({ChildEntity} {childEntity})
    {
        ArgumentNullException.ThrowIfNull({childEntity});

        if (!CanAdd{ChildEntity}({childEntity}))
            throw new InvalidOperationException("Insufficient {entity} for {childEntity}");

        if (_{childEntities}.Any(g => g.{ChildEntity}Id == {childEntity}.{ChildEntity}Id))
            throw new InvalidOperationException("{ChildEntity} already exists");

        _{childEntities}.Add({childEntity});
    }
}
```

---

## Common Pitfalls

### Pitfall 1: Breaking Encapsulation

```csharp
// ❌ WRONG - Direct access to mutable collection
public sealed class {Entity}
{
    public List<{ChildEntity}> {ChildEntities} { get; set; } = new();
}

// Client can bypass business rules
{entity}.{ChildEntities}.Add(invalid{ChildEntity}); // No validation!

// ✅ CORRECT - Controlled access through methods
public sealed class {Entity}
{
    private readonly List<{ChildEntity}> _{childEntities} = new();
    public IReadOnlyCollection<{ChildEntity}> {ChildEntities} => _{childEntities}.AsReadOnly();

    public void Add{ChildEntity}({ChildEntity} {childEntity})
    {
        // Validation and business rules enforced
        ArgumentNullException.ThrowIfNull({childEntity});

        if (!CanAdd{ChildEntity}({childEntity}))
            throw new InvalidOperationException("Cannot add {childEntity}");

        _{childEntities}.Add({childEntity});
    }
}
```

### Pitfall 2: Violating LSP with Exceptions

```csharp
// ❌ WRONG - Derived type throws unexpected exception
public abstract class DocumentGenerator
{
    public abstract Task<byte[]> GenerateAsync({Entity} {entity});
}

public sealed class ReadOnlyDocumentGenerator : DocumentGenerator
{
    public override Task<byte[]> GenerateAsync({Entity} {entity})
    {
        throw new NotSupportedException(); // Violates LSP!
    }
}

// ✅ CORRECT - Don't inherit if contract can't be honored
public interface IDocumentGenerator
{
    Task<byte[]> GenerateAsync({Entity} {entity});
}

public interface IReadOnlyDocument
{
    Task<byte[]> GetAsync(Guid documentId);
}

// Separate interfaces for different capabilities
```

### Pitfall 3: Tight Coupling

```csharp
// ❌ WRONG - Tight coupling to concrete implementation
public sealed class {Entity}Service
{
    private readonly Sql{Entity}Repository _repository; // Concrete!

    public {Entity}Service()
    {
        _repository = new Sql{Entity}Repository(); // Direct instantiation!
    }
}

// ✅ CORRECT - Loose coupling via abstraction
public sealed class {Entity}Service
{
    private readonly I{Entity}Repository _repository; // Abstraction!

    public {Entity}Service(I{Entity}Repository repository) // DI!
    {
        _repository = repository;
    }
}
```

---

## Summary Checklist

- [ ] **SOLID principles** applied throughout
- [ ] **Encapsulation** - Private fields, controlled access
- [ ] **Abstraction** - Clean interfaces, hidden complexity
- [ ] **Polymorphism** - Interface/abstract class usage
- [ ] **Composition over inheritance** - Favor composition
- [ ] **Design patterns** - Used appropriately, not forced
- [ ] **Immutability** - Records, init-only properties
- [ ] **Guard clauses** - All public methods validate inputs
- [ ] **No god objects** - Single responsibility respected
- [ ] **Rich domain models** - Behavior in entities, not services
- [ ] **Loose coupling** - Depend on abstractions via DI
- [ ] **C# modern features** - Records, pattern matching, init

---

## Related Patterns

- [Service-Oriented Architecture](./service-oriented-architecture.md) - SOA patterns and principles
- [Microservices](./microservices.md) - Microservices architecture
- [MVVM](./mvvm.md) - Model-View-ViewModel pattern
- [Test-Driven Development](./test-driven-development.md) - TDD methodology
