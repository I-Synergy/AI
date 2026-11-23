---
name: ui-blazor
description: >-
  Blazor UI library implementation (View<TViewModel>, ConfigureServices bootstrapper, Fluent UI integration, form-factor + antiforgery services, HTTP resilience). Use when implementing the Blazor UI library's View<TViewModel>, Fluent UI integration, form-factor/antiforgery services, or HTTP resilience.
version: 2026.02.10
sources:
  - src/ISynergy.Framework.UI.Blazor
  - samples/Sample.Blazor
  - docs/IndicatorControl.md
license: See license.md in repository root
requires:
  - ui-core
  - blazor-fluentui
---

# Blazor Web Head (plain Razor)

This skill covers the Blazor web head of a generated solution, `{ApplicationName}.App.Web`. The head is plain Razor on interactive server rendering. It is not built on the I-Synergy Blazor UI library, so there is no `View<TViewModel>`, no ViewModel layer, and no `ConfigureServices` bootstrapper in this head.

If you need the I-Synergy Blazor UI library instead (`View<TViewModel>`, its bootstrapper, and its services), that is a different head design. Take it through the architect; it is not what the generator writes.

## 1. Program.cs

```csharp
var builder = WebApplication.CreateBuilder(args);

// telemetry: builder.Logging.AddTelemetry(...), then OTLP in Development, Application Insights elsewhere

builder.Services.AddRazorComponents().AddInteractiveServerComponents();

// Registers the API client and I{ApplicationName}ApiService from the HttpClientSettings section.
builder.AddAcmeApiServices();   // Acme = {ApplicationName}

builder.Services.AddWebHealthChecks();

var app = builder.Build();

if (!app.Environment.IsDevelopment())
    app.UseHsts();

app.UseHttpsRedirection();
app.UseAntiforgery();
app.MapStaticAssets();

app.MapHealthChecks("/health/live", new HealthCheckOptions { Predicate = check => check.Tags.Contains("live") });
app.MapHealthChecks("/health/ready", new HealthCheckOptions { Predicate = check => check.Tags.Contains("ready") });

app.MapRazorComponents<App>().AddInteractiveServerRenderMode();

app.Run();
```

`/health/live` does no I/O. `/health/ready` also runs `ApiHealthCheck`, which calls the API's `/health` route with a 5-second timeout. That probe uses a raw `HttpClient`: it is the one documented exception to the Kiota-only rule, because a health check must not depend on the generated client.

## 2. Components and pages

- `App.razor` is the document root. `Routes.razor` maps the router. `Layouts/MainLayout.razor` is the shell layout.
- Pages live under `Pages/{Entities}/` and declare their route with `@page`.
- A page injects the API service directly:

```razor
@page "/items"
@inject I{ApplicationName}ApiService ApiService
@implements IDisposable
```

- Loading and error state are fields. Load in `OnInitializedAsync`, and handle the failure on the page, not with an exception that escapes the component.
- Work that outlives the page is cancelled in `Dispose` through a `CancellationTokenSource`. The sample's `ItemsList` page does this.
- Forms bind a private class with Data Annotations (`[Required]`, `[MaxLength]`) through `EditForm` and `DataAnnotationsValidator`.

## 3. State

The sample keeps no shared state between components. When a page needs state that outlives it, add a scoped class (one per circuit under interactive server rendering) and register it in the head's `ServiceCollectionExtensions`:

```csharp
services.AddScoped<ItemFilterState>();
```

Inject it into the components that share it. Do not put state in a static field: under interactive server rendering a static field is shared between every user.

## 4. Where an optional component library goes

The generated head uses no component library. If you add one:

1. Reference the NuGet package in `{ApplicationName}.App.Web.csproj`.
2. Register its services in `Program.cs` (for Microsoft Fluent UI, `AddFluentUIComponents()`).
3. Import its namespaces in `_Imports.razor`.
4. Load its stylesheet or script from `App.razor` if it does not add them itself.

Keep the component library out of `{ApplicationName}.App.Shared`. The shared layer has no UI dependency.

For Fluent UI specifically, `.ai/skills/blazor-fluentui/SKILL.md` is an optional add-on guide. Its I-Synergy-specific sections (`View<TViewModel>`, the `ConfigureServices` bootstrapper) do not apply to this head.

## 5. Styling

Styles are in `wwwroot/css/app.css`, referenced from `App.razor`. Keep the styles plain CSS unless the component library above is added.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| Page shows an error but the API is up | The API base address does not match the service-discovery name | Check `HttpClientSettings:BaseAddress` and the AppHost resource name |
| Button clicks do nothing | Interactive render mode is not applied to the page | Confirm `AddInteractiveServerRenderMode()` on `MapRazorComponents` |
| Form posts without validation messages | `DataAnnotationsValidator` missing from the `EditForm` | Add it inside the form |
| Antiforgery error on a form | `UseAntiforgery()` missing or out of order | Call it after `UseHttpsRedirection` |
