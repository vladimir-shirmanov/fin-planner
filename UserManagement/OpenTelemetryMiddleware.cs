namespace UserManagement;

public class OpenTelemetryMiddleware(RequestDelegate next)
{
    public async Task InvokeAsync(HttpContext httpContext)
    {
        SerilogEnrichment.EnrichLogContext();
        await next(httpContext);
    }
}

public static class OpenTelemetryMiddlewareExtensions
{
    public static IApplicationBuilder UseEnrichedOpenTelemetryLogging(this IApplicationBuilder builder)
    {
        return builder.UseMiddleware<OpenTelemetryMiddleware>();
    }
}