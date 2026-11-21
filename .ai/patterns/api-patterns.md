# API Endpoint Patterns

Patterns for implementing Minimal API endpoints that delegate to CQRS handlers.
Based on the reference implementation in `ISynergy.Service.Api/Endpoints/`.

## Core Principles

- **Static extension methods** — endpoints are static classes with named methods, not inline lambdas
- **Named method references** — route registrations reference method names (`group.MapPost("", AddEntityAsync)`)
- **Explicit parameter binding** — `[FromServices]`, `[FromBody]`, `[FromRoute]`, `[FromQuery]` on all parameters
- **Typed results** — return `Results<T1, T2>` with `TypedResults.*` factory methods
- **Version set created inside** — each endpoint class creates its own `ApiVersionSet`
- **Authentication schemes passed in** — via `params string[] authenticationSchemes`

---

## Complete Endpoint Example

The endpoints of one entity live in one class in the `{ApplicationName}.Services` project, `Endpoints/{Entities}Endpoints.cs`. The class exposes one `Map{Entities}Endpoints` extension that the host calls once. Handlers are injected with `[FromServices]`, and each handler method returns `Results<...>` so the OpenAPI document and the code declare the same status codes.

```csharp
// File: {ApplicationName}.Services/Endpoints/{Entities}Endpoints.cs
using Asp.Versioning;
using Asp.Versioning.Builder;
using ISynergy.Framework.CQRS.Abstractions.Commands;
using ISynergy.Framework.CQRS.Queries;
using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.AspNetCore.Mvc;
using {ApplicationName}.Common.Constants;
using {ApplicationName}.Domains;
using {ApplicationName}.Domains.Features.{Entities}.Commands.Create{Entity};
using {ApplicationName}.Domains.Features.{Entities}.Queries.Get{Entity}ById;

namespace {ApplicationName}.Services.Endpoints;

/// <summary>
/// Defines the endpoints for {entity} operations.
/// </summary>
public static class {Entities}Endpoints
{
    /// <summary>The key a refusal is reported under in a validation problem.</summary>
    private const string RefusalKey = "{Entity}";

    /// <summary>
    /// Maps the {entity} endpoints to the application route builder.
    /// </summary>
    /// <param name="app">The route builder to map into.</param>
    /// <returns>The same route builder, so calls can be chained.</returns>
    public static IEndpointRouteBuilder Map{Entities}Endpoints(this IEndpointRouteBuilder app)
    {
        var version = app.NewApiVersionSet()
            .HasApiVersion(new ApiVersion(1, 0))
            .ReportApiVersions()
            .Build();

        var group = app
            .MapGroup("/{entities}")
            .WithDisplayName("{Entities}")
            .WithTags("{Entities}")
            .WithApiVersionSet(version)
            .RequireRateLimiting(RateLimits.Api);

        group.MapPost("", Add{Entity}Async)
            .WithSummary("Create {entity}")
            .WithDescription("Creates the {entity} from the provided details")
            .Produces(StatusCodes.Status429TooManyRequests)
            .Accepts<Models.Create{Entity}Request>("application/json")
            .WithValidation<Models.Create{Entity}Request>()
            .Produces<Guid>(StatusCodes.Status201Created)
            .ProducesValidationProblem();

        group.MapGet("{id:guid}", Get{Entity}ByIdAsync)
            .WithSummary("Get {entity} by ID")
            .WithDescription("Retrieves a specific {entity} by its unique identifier")
            .Produces(StatusCodes.Status429TooManyRequests)
            .Produces<Models.{Entity}>(StatusCodes.Status200OK)
            .Produces(StatusCodes.Status404NotFound);

        return app;
    }

    /// <summary>
    /// Creates the {entity}.
    /// </summary>
    /// <param name="handler">The command handler.</param>
    /// <param name="request">The request body.</param>
    /// <param name="cancellationToken">Cancels the operation.</param>
    /// <returns>201 with the new identifier, or a validation problem when the handler refuses the command.</returns>
    public static async Task<Results<Created<Guid>, ValidationProblem>> Add{Entity}Async(
        [FromServices] ICommandHandler<Create{Entity}Command, Create{Entity}Response> handler,
        [FromBody] Models.Create{Entity}Request request,
        CancellationToken cancellationToken = default)
    {
        var command = new Create{Entity}Command(request.Name, request.Description);

        try
        {
            var result = await handler.HandleAsync(command, cancellationToken);
            return TypedResults.Created($"/{entities}/{result.{Entity}Id}", result.{Entity}Id);
        }
        catch (InvalidOperationException exception)
        {
            return Refused(exception.Message);
        }
    }

    /// <summary>
    /// Retrieves the {entity} with the given identifier.
    /// </summary>
    /// <param name="handler">The query handler.</param>
    /// <param name="id">The identifier of the {entity}.</param>
    /// <param name="cancellationToken">Cancels the operation.</param>
    /// <returns>200 with the {entity}, or 404 when it does not exist.</returns>
    public static async Task<Results<Ok<Models.{Entity}>, NotFound>> Get{Entity}ByIdAsync(
        [FromServices] IQueryHandler<Get{Entity}ByIdQuery, Get{Entity}ByIdResponse> handler,
        [FromRoute] Guid id,
        CancellationToken cancellationToken = default)
    {
        var response = await handler.HandleAsync(new Get{Entity}ByIdQuery(id), cancellationToken);

        if (response.{Entity} is null)
            return TypedResults.NotFound();

        return TypedResults.Ok(response.{Entity});
    }

    /// <summary>
    /// Answers a refused command with the declared validation problem.
    /// </summary>
    /// <param name="reason">The caller-facing reason.</param>
    /// <returns>A validation problem carrying the reason.</returns>
    private static ValidationProblem Refused(string reason) =>
        TypedResults.ValidationProblem(new Dictionary<string, string[]>
        {
            [RefusalKey] = [reason]
        });
}
```

Rules this example follows:

- **Catch `ResourceNotFoundException` before the generic case.** It derives from `InvalidOperationException`, so a `catch (ResourceNotFoundException)` placed after `catch (InvalidOperationException)` never runs. Update and delete routes catch it first and return `TypedResults.NotFound()`. Every other `InvalidOperationException` is a refusal, answered as a validation problem (400).
- **Update and delete routes** follow the same shape: `Results<Ok<bool>, NotFound, ValidationProblem>` for update, `Results<NoContent, NotFound, ValidationProblem>` for delete. Bodies use `Accepts<T>` and `WithValidation<T>`.
- **Declare every status code.** Each route lists 429 (rate limit), its success type, 404 where the target can be missing, and `ProducesValidationProblem()` where a body or a refusal can fail. See "Produces Metadata".
- **Pass the request's values into the command.** The command takes individual parameters, never the request object.
- **Thread the cancellation token.** The endpoint method takes `CancellationToken cancellationToken = default` and passes it to the handler.

## HTTP Method Patterns

| Operation | HTTP Method | Route | Return Type | Status Codes |
|-----------|-------------|-------|-------------|--------------|
| **Create** | POST | `""` | `Results<Created<Guid>, BadRequest>` | 201, 400, 401 |
| **Read Single** | GET | `"{id}"` | `Results<Ok<T>, NotFound>` | 200, 404, 401 |
| **Read List** | GET | `""` | `Ok<List<T>>` | 200, 401 |
| **Update** | PUT | `""` | `Results<Ok<bool>, BadRequest>` | 200, 400, 401 |
| **Delete** | DELETE | `"{id}"` | `Results<NoContent, NotFound>` | 204, 404, 401 |
| **Search** | GET | `"search"` | `Ok<List<T>>` | 200, 401 |
| **Download** | GET | `"{id}/download"` | `Results<FileContentHttpResult, NotFound>` | 200, 404, 401 |
| **Count** | GET | `"count"` | `Ok<int>` | 200, 401 |

---

## Route Registration

### Route Group Setup

```csharp
// Version set created INSIDE the endpoint class
var version = app.NewApiVersionSet()
    .HasApiVersion(new ApiVersion(1, 0))
    .ReportApiVersions()
    .Build();

// Group with full configuration
var group = app
    .MapGroup("/{entities}")
    .WithDisplayName("{Entities}")        // OpenAPI display name
    .WithTags("{Entities}")               // OpenAPI grouping tag
    .WithGroupName("v1")                  // API version group
    .WithApiVersionSet(version)           // Attach version set
    .RequireAuthorization(options =>       // Default auth for all routes
    {
        options.RequireAuthenticatedUser();
        options.AddAuthenticationSchemes(authenticationSchemes);
    });
```

### Route Mapping — Named Methods (NOT Lambdas)

```csharp
// CORRECT: Reference named static methods
group.MapPost("", Add{Entity}Async)
    .WithSummary("Create a new {entity}")
    .Accepts<{Entity}>("application/json")
    .WithValidation<{Entity}>()
    .Produces<Guid>(StatusCodes.Status201Created)
    .Produces(StatusCodes.Status401Unauthorized)
    .ProducesValidationProblem();

// WRONG: Inline lambda (do NOT use this pattern)
group.MapPost("/", async ({Entity} model, ...) => { ... })
    .WithName("Create{Entity}")
    .WithOpenApi();
```

### Nested/Sub-Entity Routes

```csharp
// Sub-entity routes using nameof() for type safety
group.MapPost($"{nameof(SubEntity)}", AddSubEntityAsync)
    .WithSummary("Create a new sub-entity");

// Parameterized nested routes
group.MapGet($"{nameof(SubEntity)}/{nameof(ParentEntity)}/{{id}}/list", GetSubEntitiesFromParentAsync)
    .WithSummary("Get sub-entities for parent");
```

---

## Parameter Binding

### Explicit Attribute Binding

```csharp
// All parameters must use explicit binding attributes
public static async Task<Results<Created<Guid>, BadRequest>> Add{Entity}Async(
    [FromServices] ICommandHandler<Create{Entity}Command, Create{Entity}Response> handler,
    [FromBody] {Entity} e,
    CancellationToken cancellationToken = default)
```

### Route Parameters

```csharp
public static async Task<Results<Ok<{Entity}>, NotFound>> Get{Entity}ByIdAsync(
    [FromServices] IQueryHandler<Get{Entity}ByIdQuery, Get{Entity}ByIdResponse> handler,
    [FromRoute] Guid id,
    CancellationToken cancellationToken = default)
```

### Query Parameters

```csharp
public static async Task<Ok<List<{Entity}>>> Get{Entity}ListAsync(
    [FromServices] IQueryHandler<Get{Entity}ListQuery, Get{Entity}ListResponse> handler,
    [FromQuery] int pageIndex = 0,
    [FromQuery] int pageSize = GenericConstants.DefaultPageSize,
    CancellationToken cancellationToken = default)
```

### Multiple Service Injection

```csharp
public static async Task<Results<Ok<List<Account>>, NotFound>> GetAccountsAsync(
    [FromServices] IQueryHandler<GetAccountsQuery, List<Account>> handler,
    [FromServices] IHttpContextAccessor context,
    CancellationToken cancellationToken = default)
```

---

## CQRS Integration

### Command Dispatching (Individual Parameters Only)

```csharp
// CORRECT: Extract properties from request model into command parameters
var command = new Create{Entity}Command(
    e.Property1,
    e.Property2,
    e.Property3);

var result = await handler.HandleAsync(command, cancellationToken);

// WRONG: Passing model object directly
var command = new Create{Entity}Command(e);
```

### Query Dispatching with Named Parameters

```csharp
// Named parameters for optional filters
var query = new GetDepositsTotalAmountQuery({ChildEntity}Id: id);
var query = new GetDepositsTotalAmountQuery({Entity}Id: id);

// Positional parameters for simple queries
var query = new Get{Entity}ByIdQuery(id);
```

---

## TypedResults Return Patterns

### Success Responses

```csharp
TypedResults.Ok(result)                                     // 200 OK
TypedResults.Created($"/route/{id}", result.{Entity}Id)     // 201 Created
TypedResults.NoContent()                                    // 204 No Content
TypedResults.File(content, "application/octet-stream")      // 200 with file
```

### Error Responses

```csharp
TypedResults.NotFound()                      // 404
TypedResults.BadRequest()                    // 400
TypedResults.BadRequest("error message")     // 400 with message
TypedResults.Unauthorized()                  // 401
```

### Return Type Signatures

```csharp
// Single result type (no error path)
Task<Ok<List<{Entity}>>>

// Multiple possible results
Task<Results<Ok<{Entity}>, NotFound>>
Task<Results<Created<Guid>, BadRequest>>
Task<Results<NoContent, NotFound>>

// File download
Task<Results<FileContentHttpResult, NotFound>>
```

---

## Authorization Patterns

### Group-Level Default Authorization

```csharp
var group = app
    .MapGroup("/{entities}")
    .RequireAuthorization(options =>
    {
        options.RequireAuthenticatedUser();
        options.AddAuthenticationSchemes(authenticationSchemes);
    });
```

### Per-Endpoint Role-Based Authorization

```csharp
group.MapGet("accounts", GetAccountsAsync)
    .RequireAuthorization(options =>
    {
        options.RequireAuthenticatedUser();
        options.RequireRole(
            nameof(Roles.LicenseManager),
            nameof(Roles.LicenseAdministrator));
    })
    .WithSummary("Get all accounts");
```

### Accessing User Context in Endpoints

```csharp
public static async Task<Results<Created<string>, UnauthorizedHttpResult>> CreateApiKeyAsync(
    [FromServices] ICommandHandler<CreateApiKeyCommand, CreateApiKeyResponse> handler,
    [FromServices] IHttpContextAccessor context,
    CancellationToken cancellationToken = default)
{
    if (context.HttpContext?.User is null)
        return TypedResults.Unauthorized();

    var userIdClaim = context.HttpContext.User.FindFirst(
        System.Security.Claims.ClaimTypes.NameIdentifier)?.Value;

    if (string.IsNullOrEmpty(userIdClaim) || !Guid.TryParse(userIdClaim, out var userId))
        return TypedResults.Unauthorized();

    var command = new CreateApiKeyCommand(userId);
    var response = await handler.HandleAsync(command, cancellationToken);

    return TypedResults.Created(string.Empty, response.ApiKey);
}
```

### Anti-Forgery Protection

```csharp
group.MapPost("verify/accept", VerifyAcceptAsync)
    .RequireAuthorization(options => options.RequireAuthenticatedUser())
    .ValidateAntiforgeryToken()
    .WithSummary("Accept authorization");
```

### Input Validation (Data Annotations)

Use Data Annotations on request models and a reusable validation filter. Every POST/PUT route that accepts a body must include `.ProducesValidationProblem()` and the validation filter.

**Model with validation attributes:**

```csharp
// File: {ApplicationName}.Models/{Entity}.cs

using System.ComponentModel.DataAnnotations;

public sealed record {Entity}
{
    [Required, MaxLength(100)]
    public string Property1 { get; init; }

    [Required, Range(1, 10000)]
    public int Property2 { get; init; }

    [MaxLength(500)]
    public string? Property3 { get; init; }
}
```

**Reusable validation filter:**

```csharp
// File: {ApplicationName}.Services/Extensions/ValidationExtensions.cs

using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Http.HttpResults;

namespace Microsoft.AspNetCore.Builder;

public static class ValidationExtensions
{
    public static RouteHandlerBuilder WithValidation<T>(this RouteHandlerBuilder builder)
    {
        builder.AddEndpointFilter(async (context, next) =>
        {
            var argument = context.Arguments.OfType<T>().FirstOrDefault();
            if (argument is null)
                return TypedResults.BadRequest("Invalid request body");

            var results = new List<ValidationResult>();
            if (!Validator.TryValidateObject(argument, new ValidationContext(argument), results, true))
            {
                return TypedResults.ValidationProblem(
                    results.ToDictionary(
                        r => r.MemberNames.FirstOrDefault() ?? "Error",
                        r => new[] { r.ErrorMessage! }));
            }

            return await next(context);
        });

        return builder;
    }
}
```

**Usage on the route:**

```csharp
group.MapPost("", Add{Entity}Async)
    .Accepts<{Entity}>("application/json")
    .WithValidation<{Entity}>()
    .ProducesValidationProblem();
```

The filter runs before the endpoint. If validation fails, it returns a 400 with the validation errors — matching the `.ProducesValidationProblem()` declaration. If it passes, the endpoint executes normally.

### Rate Limiting

All API endpoints must be protected by rate limiting to prevent abuse and DoS:

```csharp
// File: {ApplicationName}.Service.Api/Program.cs

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

app.UseRateLimiter();
```

Per-route policy override when needed:

```csharp
group.MapPost("", Add{Entity}Async)
    .RequireRateLimiting("api");
```

### CORS

Cross-Origin Resource Sharing must be explicitly configured for web clients:

```csharp
// File: {ApplicationName}.Service.Api/Program.cs

builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
    {
        policy.WithOrigins("https://{ApplicationName}.App.Api")
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});

var app = builder.Build();

app.UseCors();
```

**Rules:**
- Never use `.AllowAnyOrigin()` with `AllowCredentials()` — they're mutually exclusive
- Always specify explicit origins; never use `AllowAnyOrigin()` in production
- Call `UseCors()` after `UseRouting()` but before `UseAuthorization()` and `UseRateLimiter()`

### Middleware Order

The middleware pipeline in Program.cs must follow this order:

```csharp
var app = builder.Build();

app.UseHttpsRedirection();
app.UseCors();
app.UseRateLimiter();
app.UseAuthentication();
app.UseAuthorization();

app.Map{Entity}Endpoints("Bearer", "ApiKey");

app.Run();
```

### HTTPS Enforcement

HTTPS redirection is mandatory for all environments:

```csharp
// File: {ApplicationName}.Service.Api/Program.cs

var app = builder.Build();

app.UseHttpsRedirection();
```

Note: .NET Aspire handles TLS termination at the infrastructure level; `UseHttpsRedirection` remains for non-Aspire scenarios.

---

## OpenAPI Configuration

### Route Metadata

Every route MUST declare all possible response types via `.Produces<T>()` or `.Produces(statusCode)`. This includes both success and error codes. Never rely on inference — OpenAPI/Swagger needs explicit metadata for accurate documentation.

```csharp
group.MapPost("", Add{Entity}Async)
    .WithSummary("Create a new {entity}")                       // Short title
    .WithDescription("Creates a new {entity} with details")     // Detailed description
    .Accepts<{Entity}>("application/json")                      // Expected input type
    .WithValidation<{Entity}>()                                 // Data Annotations validation
    .Produces<Guid>(StatusCodes.Status201Created)               // Success (created)
    .Produces(StatusCodes.Status401Unauthorized)                // Auth failure
    .ProducesValidationProblem();                               // 400 with validation errors

group.MapGet("{id}", Get{Entity}ByIdAsync)
    .WithSummary("Get {entity} by ID")
    .WithDescription("Retrieves a specific {entity} by its unique identifier")
    .Produces<{Entity}>(StatusCodes.Status200OK)                // Success
    .Produces(StatusCodes.Status401Unauthorized)                // Auth failure
    .Produces(StatusCodes.Status404NotFound);                   // Not found

group.MapGet("", Get{Entity}ListAsync)
    .WithSummary("Get all {entities}")
    .WithDescription("Retrieves a paginated list of {entities}")
    .Produces<List<{Entity}>>(StatusCodes.Status200OK)          // Success
    .Produces(StatusCodes.Status401Unauthorized);               // Auth failure

group.MapPut("", Update{Entity}Async)
    .WithSummary("Update an existing {entity}")
    .WithDescription("Updates an existing {entity} with the provided details")
    .Accepts<{Entity}>("application/json")
    .WithValidation<{Entity}>()
    .Produces<bool>(StatusCodes.Status200OK)                    // Success
    .Produces(StatusCodes.Status401Unauthorized)                // Auth failure
    .ProducesValidationProblem();                               // 400 with validation errors

group.MapDelete("{id}", Remove{Entity}Async)
    .WithSummary("Delete a {entity}")
    .WithDescription("Deletes a {entity} by its unique identifier")
    .Produces(StatusCodes.Status204NoContent)                   // Success (no content)
    .Produces(StatusCodes.Status401Unauthorized)                // Auth failure
    .Produces(StatusCodes.Status404NotFound);                   // Not found
```

### Produces Metadata — Required

- **Every route** must explicitly declare every status code it can return, both success and failure
- Use `.Produces<T>(statusCode)` for typed success responses (the `T` matches the return type's success branch)
- Use `.Produces(statusCode)` for untyped responses (204, 401, 404, etc.)
- Use `.ProducesValidationProblem()` for automatic 400 validation error handling
- Do NOT omit success codes — OpenAPI generators cannot infer them from `Results<T1, T2, ...>`

### Project Configuration for OpenAPI Document Generation

The API project writes its OpenAPI document on a **Debug** build only. The Debug configuration sets the output directory, the generation switches, and the environment the generator runs under. The `Microsoft.Extensions.ApiDescription.Server` package is referenced for Debug too, with `PrivateAssets=all` so it does not leak to consumers:

```xml
<!-- File: {ApplicationName}.Service.Api/{ApplicationName}.Service.Api.csproj -->
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net11.0</TargetFramework>
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
    <PackageReference Include="Microsoft.AspNetCore.OpenApi" />
    <PackageReference Include="Microsoft.Extensions.ApiDescription.Server" Condition="'$(Configuration)' == 'Debug'">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
    </PackageReference>
  </ItemGroup>

  <!-- Kiota client regeneration follows the Debug build of this project; see "Kiota API Client Generation". -->
</Project>
```

- `OpenApiDocumentsDirectory` is relative to the project file. `../../openapi` writes the document into the solution-level `openapi/` folder, which Kiota reads.
- `OpenApiGenerationEnvironment=Development` makes the generator run the pipeline in Development, so the API's Development-only configuration is in effect while it runs.
- The Release configuration neither writes the document nor regenerates the client. A Release build of the API is the artifact that ships.
- The API's `Program.cs` skips database initialization while the document is generated (it checks the command line for `GetDocument`), so generation never needs a reachable database.

### Document Transformer: Servers Entry

Without a `servers` entry, the generated OpenAPI spec has no base URL — Kiota clients won't know where to send requests. Always add a document transformer that sets the server URL:

```csharp
// File: {ApplicationName}.Service.Api/Program.cs

builder.Services.AddOpenApi(options =>
{
    options.AddDocumentTransformer((document, context, cancellationToken) =>
    {
        document.Servers = [new OpenApiServer { Url = "https://api" }];
        return Task.CompletedTask;
    });
});
```

The URL uses the .NET Aspire service discovery short name — `https://api`. Aspire resolves this at runtime to the actual endpoint, so no configuration or environment-specific URLs are needed.

### Schema Transformers for Accurate Type Mapping

**Without schema transformers, Kiota generates all model properties as `UntypedNode` instead of their actual types.** The default OpenAPI generation infers types incorrectly for many .NET primitives. Always add a schema transformer in `Program.cs` (or via `.AddOpenApi()`) that explicitly maps every .NET type to its correct JSON schema representation:

```csharp
// File: {ApplicationName}.Service.Api/Program.cs

builder.Services.AddOpenApi(options =>
{
    // ... document transformer (servers) goes here ...

    options.AddSchemaTransformer((schema, context, cancellationToken) =>
    {
        var propertyType = context.JsonPropertyInfo?.PropertyType;

        if (propertyType == null)
            return Task.CompletedTask;

        var nullableType = Nullable.GetUnderlyingType(propertyType);
        var actualType = nullableType ?? propertyType;

        // Date and Time types
        if (actualType == typeof(DateTimeOffset))
        {
            schema.Type = JsonSchemaType.String;
            schema.Format = "date-time";
        }
        else if (actualType == typeof(DateTime))
        {
            schema.Type = JsonSchemaType.String;
            schema.Format = "date-time";
        }
        else if (actualType == typeof(DateOnly))
        {
            schema.Type = JsonSchemaType.String;
            schema.Format = "date";
        }
        else if (actualType == typeof(TimeOnly))
        {
            schema.Type = JsonSchemaType.String;
            schema.Format = "time";
        }
        else if (actualType == typeof(TimeSpan))
        {
            schema.Type = JsonSchemaType.String;
            schema.Format = "duration";
        }

        // Numeric types
        else if (actualType == typeof(decimal))
        {
            schema.Type = JsonSchemaType.Number;
            schema.Format = "double";
        }
        else if (actualType == typeof(double))
        {
            schema.Type = JsonSchemaType.Number;
            schema.Format = "double";
        }
        else if (actualType == typeof(float))
        {
            schema.Type = JsonSchemaType.Number;
            schema.Format = "float";
        }

        // Integer types
        else if (actualType == typeof(int))
        {
            schema.Type = JsonSchemaType.Integer;
            schema.Format = "int32";
        }
        else if (actualType == typeof(long))
        {
            schema.Type = JsonSchemaType.Integer;
            schema.Format = "int64";
        }
        else if (actualType == typeof(short))
        {
            schema.Type = JsonSchemaType.Integer;
            schema.Format = "int16";
        }
        else if (actualType == typeof(byte))
        {
            schema.Type = JsonSchemaType.Integer;
            schema.Format = "int8";
            schema.Minimum = "0";
            schema.Maximum = "255";
        }
        else if (actualType == typeof(sbyte))
        {
            schema.Type = JsonSchemaType.Integer;
            schema.Format = "int8";
            schema.Minimum = "-128";
            schema.Maximum = "127";
        }
        else if (actualType == typeof(uint))
        {
            schema.Type = JsonSchemaType.Integer;
            schema.Format = "int32";
            schema.Minimum = "0";
        }
        else if (actualType == typeof(ulong))
        {
            schema.Type = JsonSchemaType.Integer;
            schema.Format = "int64";
            schema.Minimum = "0";
        }
        else if (actualType == typeof(ushort))
        {
            schema.Type = JsonSchemaType.Integer;
            schema.Format = "int16";
            schema.Minimum = "0";
        }

        // String and identifier types
        else if (actualType == typeof(Guid))
        {
            schema.Type = JsonSchemaType.String;
            schema.Format = "uuid";
        }
        else if (actualType == typeof(string))
        {
            schema.Type = JsonSchemaType.String;
        }
        else if (actualType == typeof(char))
        {
            schema.Type = JsonSchemaType.String;
            schema.MinLength = 1;
            schema.MaxLength = 1;
        }

        // Boolean type
        else if (actualType == typeof(bool))
        {
            schema.Type = JsonSchemaType.Boolean;
        }

        // Binary types
        else if (actualType == typeof(byte[]))
        {
            schema.Type = JsonSchemaType.String;
            schema.Format = "byte";
        }

        // URI type
        else if (actualType == typeof(Uri))
        {
            schema.Type = JsonSchemaType.String;
            schema.Format = "uri";
        }

        // Handle enums
        else if (actualType.IsEnum)
        {
            schema.Type = JsonSchemaType.String;
            var enumNames = Enum.GetNames(actualType);
            schema.Enum = enumNames
                .Select(name => System.Text.Json.Nodes.JsonValue.Create(name)!)
                .Cast<System.Text.Json.Nodes.JsonNode>()
                .ToList();
        }

        return Task.CompletedTask;
    });
});
```

This transformer is non-negotiable — without it, the OpenAPI spec omits type information and Kiota falls back to `UntypedNode` for every property, making the generated client useless.

### Do NOT Use

```csharp
// WRONG: These are the old Swashbuckle patterns
.WithName("Create{Entity}")    // Not used
.WithOpenApi()                 // Not used
```

---

## Kiota API Client Generation

Kiota turns the API's OpenAPI document into a strongly typed client. The heads call that client through an `I{ApplicationName}ApiService` abstraction, so they never reference the generated types.

### Layout

The generator writes one flat client project per solution, `{ApplicationName}.Clients`. It is not named per consuming app. Its generated source is in `Api/`:

```
src/{ApplicationName}.Clients/
├── {ApplicationName}.Clients.csproj
└── Api/                              # Kiota output, committed
    ├── ApiClient.cs                  # entry point (BaseRequestBuilder)
    ├── {Entities}/                   # request builders, one folder per path segment
    └── Models/                       # request and response models, enums
```

Kiota reads `openapi/{ApplicationName}.Service.Api.json` at the solution root. The API project writes that document on a Debug build.

### When the client regenerates

Generation is a Debug-only development step. The API project's csproj carries a target that runs `dotnet kiota generate` after the Debug build, writing into `{ApplicationName}.Clients/Api`. A Release build does not touch the committed client.

- A fresh render compiles with no generator run, in Debug and in Release: the template ships the Kiota output for the sample entity.
- A route change adds or removes generated files on the next Debug build of the API. The client compiles whatever is in `Api/` at that point.
- Opt out with `-p:{ApplicationName}GenerateApiClient=false` on the top-level build (CI, or a test run that must not rewrite committed files). The API project reads the option, so pass it on the command line of the build that runs.
- Kiota is pinned as a local tool in `.config/dotnet-tools.json`. Restore it with `dotnet tool restore`.

### Client project

The client project references the API project as a build-order dependency only:

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net11.0</TargetFramework>
    <RootNamespace>{ApplicationName}.Clients</RootNamespace>
    <!-- The compile list is built at compile time by IncludeGeneratedApiClient below, never from the default glob. -->
    <EnableDefaultCompileItems>false</EnableDefaultCompileItems>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.Extensions.Http" />
    <PackageReference Include="Microsoft.Kiota.Bundle" />
  </ItemGroup>

  <ItemGroup>
    <!-- Build-order reference only: the client builds after the API's Debug build has regenerated Api/. -->
    <ProjectReference Include="..\{ApplicationName}.Service.Api\{ApplicationName}.Service.Api.csproj" ReferenceOutputAssembly="false" />
  </ItemGroup>

  <!-- Reads Api/ through a property function, not a wildcard item, so a file the generator added or removed is seen. -->
  <Target Name="IncludeGeneratedApiClient" BeforeTargets="CoreCompile">
    <ItemGroup>
      <Compile Include="$([System.IO.Directory]::GetFiles('$(MSBuildProjectDirectory)/Api', '*.cs', System.IO.SearchOption.AllDirectories))" Condition="Exists('$(MSBuildProjectDirectory)/Api')" />
    </ItemGroup>
  </Target>
</Project>
```

- `EnableDefaultCompileItems=false` plus the target reads the compile list from disk at compile time. A wildcard item can come from MSBuild's file-enumeration cache, which may still list files a previous generation removed.
- `ReferenceOutputAssembly="false"` adds no assembly dependency on the API. The client never needs the server types.

### Registration

The client is registered in the shared UI layer (`{ApplicationName}.App.Shared`, in its `HostApplicationBuilderExtensions`), not in the API. The shared layer chooses the base address and the authentication provider:

```csharp
builder.Services.AddSingleton<IAuthenticationProvider, AnonymousAuthenticationProvider>();

builder.Services.AddScoped(serviceProvider =>
{
    var httpClientFactory = serviceProvider.GetRequiredService<IHttpClientFactory>();
    var authenticationProvider = serviceProvider.GetRequiredService<IAuthenticationProvider>();
    var requestAdapter = new HttpClientRequestAdapter(authenticationProvider, httpClient: httpClientFactory.CreateClient(HttpClientSettings.Name))
    {
        BaseUrl = baseAddress.TrimEnd('/'),
    };
    return new ApiClient(requestAdapter);
});

builder.Services.AddScoped<I{ApplicationName}ApiService, {ApplicationName}ApiService>();
```

The API service wraps the client and maps the generated models to the application models, so the heads never see generated types:

```csharp
public sealed class {ApplicationName}ApiService(ApiClient client) : I{ApplicationName}ApiService
{
    public async Task<IReadOnlyList<{Entity}>> Get{Entities}Async(CancellationToken cancellationToken = default)
    {
        var items = await client.{Entities}.GetAsync(cancellationToken: cancellationToken);
        return items?.Select(Map).ToList() ?? [];
    }
}
```

Handlers and heads depend on the abstraction, never on `ApiClient` directly.

### Schema types

Kiota generates typed members only when the OpenAPI document carries types. The schema transformer in `Program.cs` (see "Schema Transformers") is what keeps `UntypedNode` out of the generated client, so it stays in the API.

## File Download Pattern

```csharp
// Route registration
group.MapGet($"{nameof(Document)}/{{id}}/download", Download{Entity}DocumentByIdAsync)
    .WithSummary("Download {entity} document")
    .Produces(StatusCodes.Status200OK)
    .Produces(StatusCodes.Status401Unauthorized)
    .Produces(StatusCodes.Status404NotFound);

// Handler method
public static async Task<Results<FileContentHttpResult, NotFound>> Download{Entity}DocumentByIdAsync(
    [FromServices] IQueryHandler<DownloadDocumentQuery, DownloadDocumentResponse> handler,
    [FromRoute] Guid id,
    CancellationToken cancellationToken = default)
{
    var query = new DownloadDocumentQuery(id);
    var result = await handler.HandleAsync(query, cancellationToken);

    if (result.FileContent is not null)
        return TypedResults.File(result.FileContent, "application/octet-stream");

    return TypedResults.NotFound();
}
```

---

## Endpoint Registration in Program.cs

The API host registers the handlers once and maps each entity's endpoints. There is no per-domain registration class: the Domains project exposes `With{ApplicationName}DomainHandlers()`, and each endpoints class exposes its own `Map{Entities}Endpoints()`.

```csharp
// File: {ApplicationName}.Service.Api/Program.cs
using {ApplicationName}.Data;
using {ApplicationName}.Data.Abstractions;
using {ApplicationName}.Data.Initializers;
using {ApplicationName}.Domains.Extensions;
using {ApplicationName}.Services.Endpoints;

var builder = WebApplication.CreateBuilder(args);

// CQRS: the handlers depend on IDataContext, which resolves to the provider DataContext.
builder.Services
    .AddScoped<IDataContext>(services => services.GetRequiredService<DataContext>())
    .With{ApplicationName}DomainHandlers();

var app = builder.Build();

app.MapOpenApi();
app.UseHttpsRedirection();
app.UseRateLimiter();

app.Map{Entities}Endpoints();

// Skip initialization while the OpenAPI document is generated, so generation needs no reachable database.
if (!IsOpenApiDocumentGeneration())
    await DatabaseInitializer.InitializeAsync(app.Services);

app.Run();

static bool IsOpenApiDocumentGeneration() =>
    Environment.GetCommandLineArgs().Any(argument =>
        argument.Contains("GetDocument", StringComparison.OrdinalIgnoreCase));
```

The sample's `Program.cs` also wires telemetry, the provider `DataContext`, health checks, API versioning, and the OpenAPI transformers. Those sections of this file describe each one. The `DataContext` is registered by the provider project, not here.

`Program.Partial.cs` in the API project declares `public partial class Program`, so `WebApplicationFactory<Program>` in the service tests can reach the host.

---

## Multi-Entity Endpoint Organization

When a single domain has multiple entities, organize with `#region` blocks:

```csharp
public static class {Entity}Endpoints
{
    public static void Map{Entity}Endpoints(
        this IEndpointRouteBuilder app,
        params string[] authenticationSchemes)
    {
        // ... version set and group setup ...

        // {Entity} routes
        group.MapPost("", Add{Entity}Async);
        group.MapGet("{id}", Get{Entity}ByIdAsync);
        group.MapPut("", Update{Entity}Async);
        group.MapDelete("{id}", Remove{Entity}Async);

        // {ChildEntity} sub-entity routes
        group.MapPost($"{nameof({ChildEntity})}", Add{ChildEntity}Async);
        group.MapGet($"{nameof({ChildEntity})}/{nameof({Entity})}/{{id}}/list", Get{ChildEntities}From{Entity}Async);
        group.MapPut($"{nameof({ChildEntity})}", Update{ChildEntity}Async);
        group.MapDelete($"{nameof({ChildEntity})}/{{id}}", Remove{ChildEntity}Async);
    }

    #region {Entity} Methods
    public static async Task<Results<Created<Guid>, BadRequest>> Add{Entity}Async(...) { ... }
    public static async Task<Results<Ok<{Entity}>, NotFound>> Get{Entity}ByIdAsync(...) { ... }
    #endregion

    #region {ChildEntity} Methods
    public static async Task<Results<Created<Guid>, BadRequest>> Add{ChildEntity}Async(...) { ... }
    public static async Task<Ok<List<{ChildEntity}>>> Get{ChildEntities}From{Entity}Async(...) { ... }
    #endregion
}
```

---

## Key Conventions Summary

1. **Named static methods** — never inline lambdas
2. **`[FromServices]` injection** — handler interfaces injected per method
3. **`TypedResults.*`** — not `Results.*` (typed return values)
4. **Individual command parameters** — never pass model objects to commands
5. **Named query parameters** — use `{ChildEntity}Id: id` syntax for clarity
6. **Version set inside method** — not passed as parameter
7. **`params string[] authenticationSchemes`** — auth schemes passed from Program.cs
8. **`.WithSummary()` + `.WithDescription()`** — not `.WithName()` + `.WithOpenApi()`
9. **`.Accepts<T>("application/json")`** — for POST/PUT body types
10. **`CancellationToken cancellationToken = default`** — on all async methods
11. **`nameof()` for nested routes** — type-safe sub-entity route segments
12. **`#region` blocks** — organize methods by entity type
13. **Explicit `.Produces<T>()` on every route** — always declare both success and error response types; never rely on inference
14. **OpenAPI document generation in `.csproj`** — the API project sets `OpenApiGenerateDocumentsOnBuild`, `OpenApiDocumentsDirectory` and the `Microsoft.Extensions.ApiDescription.Server` package reference in its Debug configuration
15. **Document + schema transformers in `AddOpenApi()`** — always register a document transformer (servers URL) and a schema transformer (type mapping); missing either breaks Kiota client generation
16. **One Kiota client per solution** — the flat `{ApplicationName}.Clients` project, regenerated on the API's Debug build; never use raw `HttpClient` to call an internal API
17. **Data Annotations validation** — every POST/PUT route uses `.WithValidation<T>()` with `[Required]`, `[MaxLength]`, `[Range]` on request models
18. **Rate limiting + HTTPS** — every API project configures `AddRateLimiter` + `UseRateLimiter` + `UseHttpsRedirection`; add CORS only when a browser calls the API directly (the generated sample does not register it)
