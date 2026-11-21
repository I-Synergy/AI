# Kiota Client Generation

## Naming Convention

The solution has one client project, `{ApplicationName}.Clients`, regardless of how many heads consume it. It is flat under `src/`, like every other project, and its generated source sits in `Api/`.

## Client Project .csproj

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net11.0</TargetFramework>
    <RootNamespace>{ApplicationName}.Clients</RootNamespace>
    <EnableDefaultCompileItems>false</EnableDefaultCompileItems>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.Extensions.Http" />
    <PackageReference Include="Microsoft.Kiota.Bundle" />
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\{ApplicationName}.Service.Api\{ApplicationName}.Service.Api.csproj" ReferenceOutputAssembly="false" />
  </ItemGroup>

  <Target Name="IncludeGeneratedApiClient" BeforeTargets="CoreCompile">
    <ItemGroup>
      <Compile Include="$([System.IO.Directory]::GetFiles('$(MSBuildProjectDirectory)/Api', '*.cs', System.IO.SearchOption.AllDirectories))" Condition="Exists('$(MSBuildProjectDirectory)/Api')" />
    </ItemGroup>
  </Target>
</Project>
```

The `ProjectReference` to the API is build order only (`ReferenceOutputAssembly="false"`): the API's Debug build regenerates `Api/`, and the client compiles after it. The `Target` reads the compile list from disk, so a removed generated file is not compiled. See `.ai/patterns/api-patterns.md`, "Kiota API Client Generation".

## Kiota Tool Version

Pin the Kiota CLI version in `.config/dotnet-tools.json`:

```json
{
  "version": 1,
  "isRoot": true,
  "tools": {
    "microsoft.openapi.kiota": {
      "version": "1.31.1",
      "commands": ["kiota"],
      "rollForward": false
    }
  }
}
```

Setup commands:
```bash
dotnet new tool-manifest          # Skip if .config/dotnet-tools.json exists
dotnet tool install Microsoft.OpenApi.Kiota
dotnet tool restore               # On fresh checkout
```

## DI Registration

The client is registered in the shared UI layer, `{ApplicationName}.App.Shared`, in its `HostApplicationBuilderExtensions` (`Add{ApplicationName}ApiServices`). The client project itself has no registration class. The registration reads the base address from the `HttpClientSettings` configuration section, adds service discovery, and registers an anonymous Kiota authentication provider and the scoped `ApiClient`. See `.ai/patterns/api-patterns.md`, "Kiota API Client Generation", for the code.

## Using the Generated Client

```csharp
public sealed class GetEntityListQueryHandler(
    ApiClient client
) : IQueryHandler<GetEntityListQuery, GetEntityListResponse>
{
    public async Task<GetEntityListResponse> HandleAsync(
        GetEntityListQuery query,
        CancellationToken cancellationToken = default)
    {
        var result = await client.Api.V1.Entities.GetAsync(config =>
        {
            config.QueryParameters.Page = query.PageIndex;
            config.QueryParameters.PageSize = query.PageSize;
        }, cancellationToken);

        return new GetEntityListResponse(
            result?.Select(e => /* map to model */).ToList() ?? []);
    }
}
```

## Key Rules

- One Kiota client per solution, the flat `{ApplicationName}.Clients` project
- `Microsoft.Kiota.Bundle` is the single metapackage, not individual packages
- `dotnet-tools.json` pins the Kiota CLI with `rollForward: false`
- Regeneration runs on the API's **Debug** build only; Release never rewrites the committed client. Opt out with `-p:{ApplicationName}GenerateApiClient=false`
- Client source files (`Api/`, `Models/`, `ApiClient.cs`) are committed. `kiota-lock.json` holds a hash of the document and is written by the generator
- The base address is the Aspire service-discovery name of the API (`https+http://{applicationname}-service-api`), set in the head's configuration
- Never use raw `HttpClient` to call an internal API
- The API's schema transformer and operation transformer keep Kiota from falling back to `UntypedNode` or to a `string` member for `[FromQuery] int` (see `references/openapi.md`)
