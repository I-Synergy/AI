# {ApplicationName}.Services

Minimal API endpoint groups for the application. One static class per entity maps its routes, calls the CQRS handlers from `{ApplicationName}.Domains` and translates the outcome into typed HTTP results. The endpoints are anonymous by default; authentication is added by a host module, not here.
