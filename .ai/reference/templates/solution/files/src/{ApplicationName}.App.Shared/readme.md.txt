# {ApplicationName}.App.Shared

UI-neutral application layer for the heads (`{ApplicationName}.App` and `{ApplicationName}.App.Web`). It targets plain `net11.0`, so it builds without any workload.

- `Abstractions/Services/I{ApplicationName}ApiService` is the only API surface the heads use. The implementation in `Services/` maps the generated Kiota models to the application models, so no head sees generated types.
- `Extensions/HostApplicationBuilderExtensions` registers the named HTTP client, the service-discovery settings and the scoped Kiota client. It reads the `HttpClientSettings` section key by key. `FallbackBaseAddress` is used when the base address is a service-discovery URI and no resolver is present; the project never names a public host.
- `Services/CommonServices` and `Services/ExceptionHandlerService` implement the framework contracts. Restart and quit depend on the host process, so they are virtual and a head that supports them overrides them.
- `Models/GlobalSettings`, `LocalSettings` and `RoamingSettings` are the settings models. The head owns their persistence; its roaming store is a no-op, not an exception.
- `Abstractions/Services/ISqliteLocalDataService` and `Models/Favorite` exist only with the `sqlite-device` flag. `{ApplicationName}.Data.Sqlite` implements the interface.
