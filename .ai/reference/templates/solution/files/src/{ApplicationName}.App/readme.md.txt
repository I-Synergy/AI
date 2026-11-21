# {ApplicationName}.App

MAUI head: one codebase for Android, iOS, Mac Catalyst and Windows. The head reaches the API only through `I{ApplicationName}ApiService` from `{ApplicationName}.App.Shared`.

- `MauiProgram` composes configuration, telemetry, the framework and the application services. `App` runs the startup and opens the shell.
- Views and ViewModels pair by name: `{Entities}View` with `{Entities}ViewModel`, `{Entity}DetailView` with `{Entity}DetailViewModel`, `ShellView` with `ShellViewModel`. Pages use compiled bindings (`x:DataType`).
- `Services/SettingsService` stores the device settings in MAUI preferences. Roaming and global settings have no store in this head.
- Configuration is embedded: `appsettings.json` plus one environment file. `HttpClientSettings:BaseAddress` is a service-discovery name that the AppHost resolves on a local run. A production build sets the API address through configuration; no public host is written into the repository.
- Platform folders hold the entry points and manifests. Signing keys, provisioning profiles and store identities are not in the repository.
- Target frameworks follow the host: Android needs `ANDROID_HOME` (Windows hosts always add it), Apple heads are added on macOS and Windows, the Windows head on Windows only.
