# {ApplicationName}.Service.Api

HTTP host for the application. It composes the telemetry, data context, CQRS handlers, rate limiting, API versioning, OpenAPI document and health probes, then maps the endpoint groups from `{ApplicationName}.Services`.

- The API is anonymous. No route requires authentication and no route declares `401`. Add an authentication module before the API is reachable outside a trusted network.

- `/health` is liveness and does no I/O. `/health/ready` also checks the database.
- The OpenAPI document is written to `openapi/{ApplicationName}.Service.Api.json` on Debug builds. The Kiota client in `{ApplicationName}.Clients/Api/` is regenerated from it and committed. Set `{ApplicationName}GenerateApiClient=false` to skip regeneration.
- The connection string is `ConnectionStrings:{applicationname}-db`. Outside Development it must come from the environment or a secret store; it is not in `appsettings.Production.json`.
- Response compression is off. It is an opt-in: enabling it on responses that combine secrets with request-reflected input exposes them to BREACH-style attacks.
