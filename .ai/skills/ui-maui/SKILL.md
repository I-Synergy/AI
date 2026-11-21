---
name: ui-maui
description: >-
  .NET MAUI implementation of the I-Synergy UI stack: ConfigureServices bootstrapper, cross-platform dialog/navigation/theme/file/camera services, NavigationMenu controls, and dynamic theme system. Use when implementing .NET MAUI dialog/navigation/theme/file/camera services, NavigationMenu controls, or the dynamic theme system.
version: 2026.02.10
sources:
  - src/ISynergy.Framework.UI.Maui
  - samples/Sample.Maui
  - docs/MAUI-Dynamic-Theme-System.md
license: See license.md in repository root
---

# .NET MAUI Head (I-Synergy UI)

This skill covers the MAUI head of a generated solution, `{ApplicationName}.App`, and the framework services it uses. For the view, view model, and command pattern, read `.ai/patterns/mvvm.md`. For the bootstrap of both heads, read `.ai/skills/maui-blazor/SKILL.md`.

## 1. Bootstrap: `MauiProgram.CreateMauiApp`

The bootstrap has four parts, in this order:

1. **Configuration.** The base `appsettings.json` and the environment file (`appsettings.Development.json` or `appsettings.Production.json`) are embedded resources. `MauiProgram` reads them by name. The environment comes from the launch arguments, then the `Environment` variable, then defaults to Production.
2. **Telemetry.** `builder.Logging.AddTelemetry(...)` with the framework's OpenTelemetry extension. Development exports over OTLP; other environments export to Application Insights.
3. **Head and framework.** `UseMauiAppForCurrentHead<App>()`, `UseFonts(...)`, `UseThemeColors(...)`, and `ConfigureServices<...>(...)` (six type arguments, see `maui-blazor`).
4. **Debug-only tooling.** `builder.AddMauiDevFlowAgent()` under `#if DEBUG`. The package is referenced for Debug builds only.

```csharp
// Correct: the application's services are added in the callback; the framework's are left to ConfigureServices.
builder
    .UseMauiAppForCurrentHead<App>()
    .ConfigureServices<App, Context, CommonServices, ExceptionHandlerService, SettingsService, global::{ApplicationName}.Resources.Properties.Resources>(
        appBuilder => appBuilder.Add{ApplicationName}ApiServices(),
        mainAssembly,
        assemblyName => assemblyName.Name!.StartsWith(typeof(App).Namespace!, StringComparison.Ordinal));

// Wrong: a second registration of a framework service, and the wrong head entry point.
builder.Services.AddSingleton<INavigationService, NavigationService>();   // already registered by ConfigureServices
builder.UseMauiApp<App>();                                               // not used by this template
```

## 2. What the framework registers

`ConfigureServices` registers the framework's UI services (navigation, dialogs, theme, lifecycle, settings, exception handling, and the application context) against the types you pass. The application's own services are added in the callback. The sample adds two:

- `appBuilder.Add{ApplicationName}ApiServices()`: the API client and `I{ApplicationName}ApiService`, from `{ApplicationName}.App.Shared`.
- `appBuilder.Services.AddDeviceStore()`: the device-local SQLite store, from `{ApplicationName}.App/Extensions`, which calls `AddLocalSqliteStore` in `{ApplicationName}.Data.Sqlite`.

Do not register a framework service a second time. Add application services in the callback and leave the framework's own registrations to `ConfigureServices`.

## 3. Context and settings

- `Context` (`Context.cs`, in the root namespace) implements the framework's `IContext`. It holds the signed-in profile, the time zone, and the offline flag. The sample has no sign-in, so the profile stays empty.
- `SettingsService` (`Services/SettingsService.cs`) implements the framework's `ISettingsService`. Its JSON serialization uses a source-generated context, `SettingsJsonContext`, in its own file, so the code is trimming- and NativeAOT-safe. Each serializable type needs a `[JsonSerializable]` entry on that context; the sample lists only `Themes`.

## 4. Startup and the shell

- `App.InitializeApplicationAsync()` runs the startup work once, with a busy message through `_commonServices.BusyService`, and signals initialization at the end.
- `App.OnApplicationLoaded` opens `ShellViewModel` with `NavigateModalAsync`.
- `ShellView` derives from `Shell` and implements `IShellView`. Its `ViewModel` property sets the binding context and binds the title. Its `Dispose` releases the view model.
- The shell's `TabBar` lists the tabs. The sample has one tab, `ItemsView`, with `FlyoutBehavior="Disabled"`.

## 5. Localisation

Strings come from `{ApplicationName}.Resources` (`Properties/Resources.resx`). In code, `_commonServices.LanguageService.GetString(key)`. In XAML, `{m:GetString Key}` with the `ISynergy.Framework.UI.Markup` namespace. A missing key shows the key itself, so check the resource file when a label shows a key name.

## 6. Dependencies

The MAUI head references `I-Synergy.Framework.UI.Maui`, `I-Synergy.Framework.OpenTelemetry.ApplicationInsights`, and `Microsoft.Extensions.ServiceDiscovery`. The `Using` aliases in `{ApplicationName}.App.csproj` (`View`, `IView`) let the XAML code-behind resolve the framework base class. Do not add `CommunityToolkit.Mvvm` to this head: the framework's MVVM base classes and commands are used instead.

## 7. Platform heads

`Platforms/` holds the entry points of each target: `Android/MainActivity.cs` and `MainApplication.cs`, `iOS/AppDelegate.cs`, `MacCatalyst/AppDelegate.cs`, and `Windows/App.xaml`. Each calls `MauiProgram.CreateMauiApp()`. The Apple targets ship `PrivacyInfo.xcprivacy` as a bundle resource, because the app reads its preferences through MAUI `Preferences`.

Target selection in `{ApplicationName}.App.csproj` follows the host: Apple targets are added on every host except Linux, Android is added with `ANDROID_HOME` or on Windows, and the Windows target is added on Windows only. The AppHost adds a Windows device and, on macOS only, a Mac Catalyst device.

## Pitfalls

- A view that does not appear: the view model's constructor parameters must be registered services; a missing one throws at navigation time, not at build time.
- A binding that fails to build: `x:DataType` is required on every binding (compiled bindings are on).
- A cold start that hangs on the busy message: `SignalApplicationInitialized()` was not called. The sample calls it after the try/catch, so the failure path signals too.
- Under Aspire, the device cannot reach the API: `HttpClientSettings:BaseAddress` must use the API's Aspire resource name, the `AspireNames` constant from `{ApplicationName}.Common`.
