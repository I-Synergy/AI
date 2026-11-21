# {ApplicationName}.App.Web

Blazor web head: interactive server rendering with plain Razor components. It has no component library and no licence key. It reaches the API only through `I{ApplicationName}ApiService` from `{ApplicationName}.App.Shared`.

- `Program.cs` composes telemetry, the Razor components, the API services and the health checks. `/health/live` does no I/O; `/health/ready` probes the API.
- `HealthChecks/ApiHealthCheck` is a documented exception to the Kiota-only rule: it sends a GET to the API liveness route with the named client from `IHttpClientFactory` and reads only the status code.
- `HttpClientSettings` in `appsettings*.json` holds the service-discovery address the AppHost resolves. Every environment that runs the head without the AppHost sets `FallbackBaseAddress`: Development points at the local API, and Production leaves it empty on purpose, so a production host must supply a resolver or a fallback. No public host is configured anywhere.
- Layout: `App.razor` and `Routes.razor` at the root, `Layouts/` for the shell, `Pages/{Entities}/` for pages, `Components/` for reusable markup.
