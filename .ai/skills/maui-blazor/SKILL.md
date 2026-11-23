---
name: maui-blazor
description: >-
  I-Synergy MVVM patterns for .NET MAUI + Blazor Hybrid shells (shared ViewModels, ConfigureServices bootstrapper, BlazorWebView orchestration). Use when wiring a .NET MAUI + Blazor Hybrid shell with shared ViewModels and BlazorWebView orchestration.
version: 2026.02.10
sources:
  - samples/Sample.Maui
  - src/ISynergy.Framework.UI.Maui
  - src/ISynergy.Framework.Mvvm
  - docs/MAUI-Dynamic-Theme-System.md
license: See license.md in repository root
requires:
  - blazor-fluentui
---

# MAUI and Blazor Heads (I-Synergy)

The generated solution has two heads over one shared layer. The heads do not share a page tree, and neither one is a Blazor Hybrid shell.

| Project | Head | UI | Role |
|---|---|---|---|
| `{ApplicationName}.App` | MAUI | I-Synergy MVVM, XAML views | Native app for Windows, Mac Catalyst, Android, iOS |
| `{ApplicationName}.App.Web` | Blazor web | Plain Razor, interactive server | Browser head; no ViewModels |
| `{ApplicationName}.App.Shared` | Shared | none | `I{ApplicationName}ApiService`, its implementation, `HttpClientSettings` wiring, settings models |

Both heads depend on `I{ApplicationName}ApiService`. Neither references the Kiota client types, which stay in `{ApplicationName}.Clients` behind the shared layer.

## MAUI head bootstrap

`MauiProgram.CreateMauiApp()` configures the framework, then the application's services:

```csharp
builder
    .UseMauiAppForCurrentHead<App>()
    .UseFonts(_ => { })
    .UseThemeColors(colors =>
    {
        colors.Add("#512BD4");
    })
    .ConfigureServices<App, Context, CommonServices, ExceptionHandlerService, SettingsService, global::{ApplicationName}.Resources.Properties.Resources>(
        appBuilder =>
        {
            appBuilder.Add{ApplicationName}ApiServices();
            appBuilder.Services.AddDeviceStore();
        },
        mainAssembly,
        assemblyName => assemblyName.Name!.StartsWith(typeof(App).Namespace!, StringComparison.Ordinal));
```

- `UseMauiAppForCurrentHead<App>()` is the entry point for every MAUI head. `UseMauiApp<App>()` is not used.
- `ConfigureServices` takes six type arguments in this order: the application, the context, the common services, the exception handler, the settings service, and the resource class. The callback receives the host builder, so the shared layer and the device store register there.
- `UseFonts` registers the fonts the framework ships. The sample adds none of its own, so the callback is empty. Add a font with `fonts.AddFont("file.ttf", "alias")` only when the application ships one.
- The assembly filter limits framework discovery to the application's own namespace.

## Startup

`App` (`App.xaml.cs`) derives from the framework `Application`. It does not set `MainPage`:

- `InitializeApplicationAsync()` runs once, before the shell. It shows a busy message, runs the startup work, and calls `_lifecycleService?.SignalApplicationInitialized()` at the end, whether or not the work succeeded.
- `OnApplicationLoaded(...)` runs after the UI and the startup are both ready. It opens the shell with `_navigationService.NavigateModalAsync<ShellViewModel>()`.

## Views

The root of every XAML view is the non-generic `c:View`. The code-behind passes the view model to the base class. There is no `x:TypeArguments`. See `.ai/patterns/mvvm.md` for the full view, view model, and command pattern.

## Blazor web head

`{ApplicationName}.App.Web` is plain Razor, not the I-Synergy Blazor UI library. Its `Program.cs`:

```csharp
builder.Services.AddRazorComponents().AddInteractiveServerComponents();
builder.AddAcmeApiServices();   // Acme = {ApplicationName}; registers the API client and I{ApplicationName}ApiService
builder.Services.AddWebHealthChecks();

app.MapRazorComponents<App>().AddInteractiveServerRenderMode();
```

Pages are `.razor` components that inject the API service directly. There is no `View<TViewModel>` and no ViewModel layer. Health checks: `/health/live` does no I/O; `/health/ready` also runs the API probe.

## Shared settings

`HttpClientSettings` (in `{ApplicationName}.Common`) holds the base address, the fallback address, the timeout, and the default headers. `HostApplicationBuilderExtensions.Add{ApplicationName}ApiServices` reads the `HttpClientSettings` section key by key, not by binding, so trimming and NativeAOT do not skip it. Service discovery replaces the base address with the configured fallback when no discovery resolver is present.

## Where an optional component library goes

The sample uses no component library. If one is added (a UI kit such as Microsoft Fluent UI), it is registered in the web head's `Program.cs` and its styles and namespaces are imported in `_Imports.razor`. For the MAUI head it is a NuGet package in `{ApplicationName}.App`. The Fluent UI guidance is an optional add-on in `.ai/skills/blazor-fluentui/SKILL.md`.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| A MAUI page does not open | View or view model is not named `{X}View` / `{X}ViewModel`, or is outside the head's namespace | Rename, or move it under `{ApplicationName}.App` |
| Build error on a binding | `x:DataType` missing (compiled bindings are on) | Set `x:DataType` to the view model or model type |
| Page compiles but the view model is `null` | Code-behind does not call `base(viewModel)` | Pass the view model to the base constructor |
| Blazor head cannot reach the API under Aspire | Service-discovery name does not match the AppHost resource name | Use the `AspireNames` constant in both places |
| Fonts missing on device | A font file is referenced without `UseFonts` | Add it with `UseFonts`, or remove the reference |
