using Microsoft.Extensions.Diagnostics.HealthChecks;

namespace UserManagement;

public class KeycloakHealthCheck : IHealthCheck
{
    public async Task<HealthCheckResult> CheckHealthAsync(HealthCheckContext context, CancellationToken cancellationToken = new CancellationToken())
    {
        using var client = new HttpClient();
        try
        {
            var response = await client.GetAsync("http://keycloak:9000/health/ready", cancellationToken);
            return response.IsSuccessStatusCode ?
                HealthCheckResult.Healthy("Keycloak is ready") :
                HealthCheckResult.Unhealthy("Keycloak is unhealthy");
        }
        catch
        {
            return HealthCheckResult.Unhealthy();
        }
    }
}

public static class KeycloakHealthCheckExtensions
{
    public static IHealthChecksBuilder AddKeycloakHealthCheck(this IHealthChecksBuilder builder)
    {
        return builder.AddCheck<KeycloakHealthCheck>("keycloak");
    }
}