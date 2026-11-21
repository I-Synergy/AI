# Testing Patterns

Patterns for the test projects the solution generator writes: MSTest on the Microsoft Testing Platform runner, real EF Core providers behind the handlers, and `WebApplicationFactory` for the API. The unit-test approach is in `.ai/patterns/test-driven-development.md`.

## Test projects

One project per layer. The generator writes these, and new layers follow the same rules.

| Project | Covers | Data | Notes |
|---|---|---|---|
| `{Name}.Domains.Tests` | Command and query handlers | EF Core InMemory through the real `DataContext` | Fast; no indexes or foreign keys are enforced |
| `{Name}.Service.Tests` | Endpoints through the real pipeline (`WebApplicationFactory<Program>`) | InMemory, swapped in by the factory | Pins the HTTP contract (status codes, JSON) |
| `{Name}.Data.{Provider}.Tests` | Model shape of the provider `DataContext` | None; built offline from the design-time factory | Checks keys, required columns, enum storage, the migrations history table |

Every test project is a plain MSTest project:

```xml
<PropertyGroup>
  <TargetFramework>net11.0</TargetFramework>
  <EnableMSTestRunner>true</EnableMSTestRunner>
  <OutputType>Exe</OutputType>
</PropertyGroup>
<ItemGroup>
  <PackageReference Include="MSTest.TestAdapter" />
  <PackageReference Include="Microsoft.Testing.Extensions.TrxReport" />
</ItemGroup>
```

Add `Microsoft.EntityFrameworkCore.InMemory` to the two projects that run handlers or endpoints. Add `Microsoft.AspNetCore.Mvc.Testing` to the service tests. Do not add Moq. A mock is allowed only for a narrow seam the handler must not call (an external service), and it needs a reason written in the project file.

## Real provider, not a mocked DataContext

Handlers take `IDataContext`, and the tests hand them the real `DataContext`. A mocked context cannot prove that a query translates, that a change is tracked, or that `SaveChangesAsync` writes anything. The InMemory provider does all three.

`TestDatabase` (in `Infrastructure/`) gives each test its own store:

```csharp
public sealed class TestDatabase : IDisposable
{
    public TestDatabase(string? databaseName = null)
    {
        DatabaseName = databaseName ?? Guid.NewGuid().ToString();

        var options = new DbContextOptionsBuilder<DataContext>()
            .UseInMemoryDatabase(DatabaseName)
            // A handler that opens a transaction would otherwise fail on the InMemory provider.
            .ConfigureWarnings(warnings => warnings.Ignore(InMemoryEventId.TransactionIgnoredWarning))
            .Options;

        Context = new DataContext(options);
    }

    public DataContext Context { get; }
    public string DatabaseName { get; }
    public void Dispose() => Context.Dispose();
}
```

Each test creates its own `TestDatabase` with `using var db = new TestDatabase();`. Tests never share rows, so they run in any order.

Arrange rows through a small helper (`{Entity}TestData.AddAsync(db.Context, ...)`), not through the handler under test. Read results back through `db.Context`, which is the same store the handler wrote to.

## Handler test

```csharp
// File: tests/{ApplicationName}.Domains.Tests/Handlers/{Entities}/Create{Entity}CommandHandlerTests.cs
// Traces: US-{Domain}-{NNN} / AC-{Domain}-{NNN}.{n}

using {ApplicationName}.Domains.Features.{Entities}.Commands.Create{Entity};
using {ApplicationName}.Domains.Tests.Infrastructure;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging.Abstractions;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace {ApplicationName}.Domains.Tests.Handlers.{Entities};

[TestClass]
public sealed class Create{Entity}CommandHandlerTests
{
    [TestMethod]
    [TestCategory("AC-{Domain}-{NNN}.{n}")]
    public async Task HandleAsync_ValidCommand_PersistsTheGivenValues()
    {
        // Arrange
        using var db = new TestDatabase();
        var handler = new Create{Entity}CommandHandler(db.Context, NullLogger<Create{Entity}CommandHandler>.Instance);

        // Act
        var result = await handler.HandleAsync(new Create{Entity}Command(Name: "Alpha", Description: "First sample"));

        // Assert
        var stored = await db.Context.{Entities}.SingleAsync(e => e.{Entity}Id == result.{Entity}Id);
        Assert.AreEqual("Alpha", stored.Name);
    }
}
```

Full template: `.ai/reference/templates/test-class.cs.txt`.

### Failure paths

Assert refusals with `Assert.ThrowsExactlyAsync` (or `Assert.ThrowsExactly` for a synchronous call). It fails when the type is wrong, which `Assert.ThrowsAsync` would allow. Do not use `[ExpectedException]`: it cannot assert the message, and it hides the line that threw.

```csharp
[TestMethod]
public async Task HandleAsync_MissingItem_ThrowsResourceNotFoundException()
{
    using var db = new TestDatabase();
    var handler = new Delete{Entity}CommandHandler(db.Context, NullLogger<Delete{Entity}CommandHandler>.Instance);

    await Assert.ThrowsExactlyAsync<ResourceNotFoundException>(() => handler.HandleAsync(new Delete{Entity}Command(Guid.NewGuid())));
}
```

### Logging

`NullLogger<T>.Instance` is the logger for every handler test. Do not assert on log output in a unit test. If a log line is the behaviour under test, use a fake `ILogger<T>` that records calls, written by hand in the test project. Do not use `Mock<ILogger>`.

Correct and wrong, side by side:

```csharp
// Correct: the handler runs on the real DataContext; the assertion reads the stored row.
using var db = new TestDatabase();
var handler = new Create{Entity}CommandHandler(db.Context, NullLogger<Create{Entity}CommandHandler>.Instance);
await handler.HandleAsync(new Create{Entity}Command(Name: "Alpha", Description: null));
Assert.AreEqual(1, await db.Context.{Entities}.CountAsync());

// Wrong: a mocked context proves only which methods were called, not that the row was saved.
var dataContextMock = new Mock<DataContext>();
dataContextMock.Verify(x => x.{Entities}.Add(It.IsAny<{Entity}>()), Times.Once);
```

## Endpoint test

The service tests boot the real host through `WebApplicationFactory`. The factory replaces the provider-backed context with InMemory, so no database is needed:

```csharp
public class CustomWebApplicationFactory : WebApplicationFactory<Program>
{
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.ConfigureServices(services =>
        {
            services.RemoveAll<DataContext>();
            services.RemoveAll<DbContextOptions<DataContext>>();
            services.RemoveAll<IDataContext>();
            services.RemoveAll<IDbContextOptionsConfiguration<DataContext>>();

            services.AddDbContext<DataContext>(
                options => options.UseInMemoryDatabase(Guid.NewGuid().ToString())
                    .ConfigureWarnings(warnings => warnings.Ignore(InMemoryEventId.TransactionIgnoredWarning)),
                contextLifetime: ServiceLifetime.Scoped,
                optionsLifetime: ServiceLifetime.Singleton);

            services.AddScoped<IDataContext>(provider => provider.GetRequiredService<DataContext>());
        });
    }
}
```

`Program` is public because the host declares `public partial class Program` in `Program.Partial.cs`. The test project does not need `InternalsVisibleTo`.

Each test creates its own factory and client:

```csharp
[TestMethod]
public async Task GetById_UnknownId_ReturnsNotFound()
{
    await using var factory = new CustomWebApplicationFactory();
    using var client = factory.CreateClient();

    using var response = await client.GetAsync($"/items/{Guid.NewGuid()}");

    Assert.AreEqual(HttpStatusCode.NotFound, response.StatusCode);
}
```

Request bodies are anonymous objects and responses are read as `JsonElement`. The tests pin the wire contract, not the C# types behind it.

## Data layer tests

`{Name}.Data.{Provider}.Tests` checks the model without a server. The design-time factory is the same path `dotnet ef migrations add` uses, so these tests see the configuration the migrations come from:

```csharp
[TestMethod]
public void Model_Item_IsKeyedByItemId()
{
    using var context = ModelProbe.CreateContext();   // new DataContextFactory().CreateDbContext([])
    var entityType = ModelProbe.GetModel(context).FindEntityType(typeof(Item));

    Assert.IsNotNull(entityType, "The Item entity is not part of the model.");
    Assert.AreEqual(nameof(Item.ItemId), entityType.FindPrimaryKey()!.Properties[0].Name);
}
```

What these tests cannot see: how the server stores a value, what an index enforces, or whether a migration does what the model says. Those need a real server, which the generated project does not start.

## Traceability

Every test file carries a `// Traces:` header below its `// File:` line, and every test method that is evidence for a criterion carries exactly one `[TestCategory("AC-…")]`, written after `[TestMethod]`:

```csharp
// Traces: US-{Domain}-014 / AC-{Domain}-014.1, AC-{Domain}-014.2

[TestMethod]
[TestCategory("AC-{Domain}-014.1")]
public async Task HandleAsync_ValidCommand_PersistsTheGivenValues()
```

A method that checks a guard clause, a log line, or infrastructure carries no `AC-` category and sits outside the trace. Extra categories such as `Integration` are allowed. The full convention, including how identifiers are allocated and retired, is `.ai/reference/traceability.md`. The validator is `.ai/tests/validate-traceability.py`.

Generated stubs carry the placeholder `US-<Domain>-NNN` until the story exists. Replace it with the real identifiers before the stub counts as evidence.

## Test naming

`MethodName_Scenario_ExpectedResult`, in the sample's style:

```
HandleAsync_ValidCommand_PersistsTheGivenValues
HandleAsync_MissingItem_ThrowsResourceNotFoundException
GetById_UnknownId_ReturnsNotFound
```

## Test layout

```
tests/
  {ApplicationName}.Domains.Tests/
    Infrastructure/
      TestDatabase.cs
      {Entity}TestData.cs
    Handlers/
      {Entities}/
        Create{Entity}CommandHandlerTests.cs
        Get{Entity}ByIdQueryHandlerTests.cs
  {ApplicationName}.Service.Tests/
    CustomWebApplicationFactory.cs
    {Entities}EndpointsTests.cs
  {ApplicationName}.Data.{Provider}.Tests/
    Infrastructure/
      ModelProbe.cs
    DataContextModelTests.cs
```

## Reqnroll (not generated)

Reqnroll acceptance tests are the `tests-acceptance` flag. Its templates do not exist yet, so the generator does not write them. When they are added, feature files carry the traceability tag on the line directly above each `Scenario:`:

```gherkin
@AC-{Domain}-{NNN}.1
Scenario: Create a new {entity}
  Given ...
```

Exactly one traceability tag per scenario; other tags (`@smoke`) may sit alongside it. `Feature:` and `Background:` carry none. Step definitions call the same handlers the unit tests use, through a `TestDatabase`, and do not mock the context.
