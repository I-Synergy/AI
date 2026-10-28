# Forbidden Technologies

## Explicitly Forbidden Packages

These packages are NOT allowed in this template architecture. Always use the specified alternatives.

| ❌ DO NOT USE | ✅ USE INSTEAD | Why? |
|---------------|---------------|------|
| **MediatR** | CQRS framework of choice | Project uses different CQRS implementation |
| **SpecFlow** | Reqnroll | SpecFlow requires license, Reqnroll is OSS fork |
| **xUnit** | MSTest | Project standard, better VS integration |
| **NUnit** | MSTest | Project standard, consistency |
| **Swashbuckle** | Microsoft.AspNetCore.OpenApi + NSwag | Modern Microsoft approach |
| **Serilog** | Logging framework of choice | Use project's logging framework |
| **FluentValidation** | Data Annotations + IValidatableObject | Simpler, built-in framework support |
| **Standalone Polly** | Microsoft.Extensions.Resilience | Microsoft's integrated resilience library |

## Why These Are Forbidden

### MediatR vs. Project CQRS

**Problem:** MediatR adds unnecessary abstraction and dependencies.

**Solution:** Use your project's CQRS framework directly:

```csharp
❌ WRONG - MediatR
public class Create{Entity}Handler : IRequestHandler<Create{Entity}Command, Create{Entity}Response>
{
    public async Task<Create{Entity}Response> Handle(
        Create{Entity}Command request,
        CancellationToken cancellationToken)
    {
        // MediatR pattern
    }
}

✅ CORRECT - Direct CQRS
public class Create{Entity}CommandHandler : ICommandHandler<Create{Entity}Command, Create{Entity}Response>
{
    public async Task<Create{Entity}Response> HandleAsync(
        Create{Entity}Command command,
        CancellationToken cancellationToken = default)
    {
        // Project's CQRS pattern
    }
}
```


### SpecFlow vs. Reqnroll

**Problem:** SpecFlow requires commercial license for many scenarios.

**Solution:** Use Reqnroll (open-source SpecFlow fork):

```gherkin
✅ CORRECT - Reqnroll
Feature: {Entity} Management
  Scenario: Create a new {entity}
    Given I am an authenticated user
    When I create a {entity} with name "Example"
    Then the {entity} should be created successfully
```

### xUnit/NUnit vs. MSTest

**Problem:** Mixing test frameworks causes inconsistency.

**Solution:** Use MSTest exclusively:

```csharp
❌ WRONG - xUnit
[Fact]
public async Task ShouldCreate{Entity}()
{
    // xUnit pattern
}

❌ WRONG - NUnit
[Test]
public async Task ShouldCreate{Entity}()
{
    // NUnit pattern
}

✅ CORRECT - MSTest
[TestMethod]
public async Task HandleAsync_ValidCommand_Creates{Entity}Successfully()
{
    // MSTest pattern
}
```

### Swashbuckle vs. Microsoft.AspNetCore.OpenApi

**Problem:** Swashbuckle is legacy, not actively maintained by Microsoft.

**Solution:** Use Microsoft's official OpenAPI package:

```csharp
❌ WRONG - Swashbuckle
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo { Title = "API", Version = "v1" });
});

✅ CORRECT - Microsoft.AspNetCore.OpenApi
builder.Services.AddOpenApi();
```

### Serilog vs. Project Logging

**Problem:** Serilog adds another logging abstraction layer.

**Solution:** Use the project's configured logging framework:

```csharp
❌ WRONG - Serilog
Log.Information("Created {EntityType} with ID {EntityId}", nameof({Entity}), {entity}Id);

✅ CORRECT - ILogger
_logger.LogInformation(
    "Created {EntityType} with ID {EntityId}",
    nameof({Entity}), {entity}Id);
```

### FluentValidation vs. Data Annotations

**Problem:** FluentValidation adds complexity and external dependency.

**Solution:** Use built-in Data Annotations:

```csharp
❌ WRONG - FluentValidation
public class Create{Entity}CommandValidator : AbstractValidator<Create{Entity}Command>
{
    public Create{Entity}CommandValidator()
    {
        RuleFor(x => x.Name).NotEmpty().MaximumLength(100);
        RuleFor(x => x.Amount).GreaterThan(0);
    }
}

✅ CORRECT - Data Annotations
public sealed record Create{Entity}Command(
    [Required]
    [StringLength(100, MinimumLength = 3)]
    string Name,

    [Range(0.01, double.MaxValue)]
    decimal Amount
) : ICommand<Create{Entity}Response>, IValidatableObject
{
    public IEnumerable<ValidationResult> Validate(ValidationContext validationContext)
    {
        if (Amount <= 0)
            yield return new ValidationResult(
                "Amount must be positive",
                new[] { nameof(Amount) });
    }
}
```

### Standalone Polly vs. Microsoft.Extensions.Resilience

**Problem:** Standalone Polly requires manual configuration and integration.

**Solution:** Use Microsoft's integrated resilience library:

```csharp
❌ WRONG - Standalone Polly
var retryPolicy = Policy
    .Handle<HttpRequestException>()
    .WaitAndRetryAsync(3, retryAttempt => TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)));

✅ CORRECT - Microsoft.Extensions.Resilience
services.AddHttpClient("external-api")
    .AddStandardResilienceHandler(options =>
    {
        options.Retry.MaxRetryAttempts = 3;
        options.Retry.BackoffType = DelayBackoffType.Exponential;
    });
```

## Package Management Rules

### CRITICAL: Version Verification

- **Verify ALL NuGet versions** on nuget.org before adding
- **NO fake version numbers** - only use versions that actually exist
- **Prefer Microsoft packages** over third-party alternatives
- **Central Package Management:** All versions in `Directory.Packages.props`

### How to Verify Packages

1. Go to https://nuget.org
2. Search for the exact package name
3. Check the latest stable version
4. Use that version in `Directory.Packages.props`

```xml
✅ CORRECT - Verified version
<PackageVersion Include="Microsoft.EntityFrameworkCore" Version="10.0.0" />

❌ WRONG - Fake/guessed version
<PackageVersion Include="SomePackage" Version="999.0.0" />
```

## Detection During Code Review

If you see any of these patterns, flag immediately:

```csharp
// MediatR
using MediatR;
IRequestHandler<T, R>

// AutoMapper
using AutoMapper;
IMapper _mapper

// xUnit
using Xunit;
[Fact]

// NUnit
using NUnit.Framework;
[Test]

// FluentValidation
using FluentValidation;
AbstractValidator<T>

// Swashbuckle
using Swashbuckle.AspNetCore;
AddSwaggerGen()

// Serilog
using Serilog;
Log.Information()
```

## Migration Guide

If you encounter forbidden packages in existing code:

1. **Identify all usages** - Search codebase for forbidden package references
2. **Plan replacement** - Map each usage to allowed alternative
3. **Create migration task** - Document the replacement in session context
4. **Execute systematically** - Replace one package at a time
5. **Test thoroughly** - Ensure behavior unchanged
6. **Update documentation** - Document the change in session context
