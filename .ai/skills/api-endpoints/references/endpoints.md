# Endpoint Code Patterns

## Core Rules

- **Named static methods** — endpoints are static classes with named methods, not inline lambdas
- **`TypedResults.*`** — return `Results<T1, T2>` with typed factory methods, never `IResult`
- **Explicit parameter binding** — `[FromServices]`, `[FromBody]`, `[FromRoute]`, `[FromQuery]` on all parameters
- **Version set created inside** — each endpoint class creates its own `ApiVersionSet`
- **Authorization at the group** — `RequireAuthorization` on the route group when an API needs it; the generated sample has no sign-in and declares none

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
| Create | POST | `""` | `Results<Created<Guid>, BadRequest>` | 201, 400, 401 |
| Read Single | GET | `"{id}"` | `Results<Ok<T>, NotFound>` | 200, 404, 401 |
| Read List | GET | `""` | `Ok<List<T>>` | 200, 401 |
| Update | PUT | `""` | `Results<Ok<bool>, BadRequest>` | 200, 400, 401 |
| Delete | DELETE | `"{id}"` | `Results<NoContent, NotFound>` | 204, 404, 401 |
| Search | GET | `"search"` | `Ok<List<T>>` | 200, 401 |
| Download | GET | `"{id}/download"` | `Results<FileContentHttpResult, NotFound>` | 200, 404, 401 |
| Count | GET | `"count"` | `Ok<int>` | 200, 401 |

## Produces Metadata

Every route must declare ALL possible response types:

```csharp
// POST — success type + auth error + validation error
.Produces<Guid>(StatusCodes.Status201Created)
.Produces(StatusCodes.Status401Unauthorized)
.ProducesValidationProblem()

// GET by ID — success type + auth error + not found
.Produces<{Entity}>(StatusCodes.Status200OK)
.Produces(StatusCodes.Status401Unauthorized)
.Produces(StatusCodes.Status404NotFound)

// GET list — success type + auth error
.Produces<List<{Entity}>>(StatusCodes.Status200OK)
.Produces(StatusCodes.Status401Unauthorized)

// PUT — success type + auth error + validation error
.Produces<bool>(StatusCodes.Status200OK)
.Produces(StatusCodes.Status401Unauthorized)
.ProducesValidationProblem()

// DELETE — success code + auth error + not found
.Produces(StatusCodes.Status204NoContent)
.Produces(StatusCodes.Status401Unauthorized)
.Produces(StatusCodes.Status404NotFound)
```

## TypedResults Factory Methods

```csharp
TypedResults.Ok(result)                                     // 200
TypedResults.Created($"/route/{id}", result.Id)             // 201
TypedResults.NoContent()                                    // 204
TypedResults.File(content, "application/octet-stream")      // 200 with file
TypedResults.NotFound()                                     // 404
TypedResults.BadRequest()                                   // 400
TypedResults.BadRequest("message")                          // 400 with message
TypedResults.Unauthorized()                                 // 401
```

## Program.cs Registration

```csharp
// File: {ApplicationName}.Service.Api/Program.cs
using {ApplicationName}.Domains.Extensions;
using {ApplicationName}.Services.Endpoints;

builder.Services
    .AddScoped<IDataContext>(services => services.GetRequiredService<DataContext>())
    .With{ApplicationName}DomainHandlers();

var app = builder.Build();

app.UseRateLimiter();
app.Map{Entities}Endpoints();
app.Run();
```

Each entity's endpoints class maps itself with one call. The handlers are registered once, from the Domains project. Full host setup is in `.ai/patterns/api-patterns.md`, "Endpoint Registration in Program.cs".
