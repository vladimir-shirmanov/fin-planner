using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using OpenTelemetry;
using OpenTelemetry.Exporter;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;
using Serilog;
using UserManagement;
using UserManagement.Models;
using UserManagement.Services;

var logDirectory = Path.Combine(Directory.GetCurrentDirectory(), "Logs");
if (!Directory.Exists(logDirectory))
{
    Directory.CreateDirectory(logDirectory);
}

var builder = WebApplication.CreateBuilder(args);

builder.Host.UseSerilog((context, services, loggerConfiguration) =>
{
    loggerConfiguration
        .ReadFrom.Configuration(context.Configuration)
        .ReadFrom.Services(services);
});

string serviceName = builder.Configuration.GetValue<string>("OpenTelemetry:Tracing:ServiceName") ??
                     "user-management-api";
string serviceVersion = builder.Configuration.GetValue<string>("OpenTelemetry:Tracing:ServiceVersion") ??
                     "1.0.0";
string otlpEndpoint = builder.Configuration.GetValue<string>("OpenTelemetry:Tracing:Endpoint") ??
                      throw new InvalidOperationException();
builder.Services.AddOpenTelemetry()
    .ConfigureResource(resourceBuilder => resourceBuilder.AddService(serviceName, serviceVersion))
    .WithTracing(traceBuilder => traceBuilder
        .AddSource(serviceName)
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation())
    .WithMetrics(metrics => metrics.AddMeter(serviceName))
    .UseOtlpExporter(OtlpExportProtocol.Grpc, new Uri(otlpEndpoint));

builder.Services.Configure<MongoDbSettings>(builder.Configuration.GetSection("MongoDb"));
builder.Services.AddSingleton<IMongoDbService, MongoDbService>();
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.Authority = builder.Configuration["Authority"];
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = builder.Configuration["Jwt:Authority"],
            ValidAudience = builder.Configuration["Jwt:Audience"],
            IssuerSigningKeyResolver = (_, _, _, _) =>
            {
                var keyUri = builder.Configuration["Jwt:keyUri"];
                var keys = new HttpClient().GetFromJsonAsync<JsonWebKeySet>(keyUri).Result;
                return keys != null ? keys.Keys : throw new KeyNotFoundException("Can't get key from the Keycloak");
            }
        };
    });
builder.Services.AddAuthorization();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddOpenApi();

var app = builder.Build();

app.UseSerilogRequestLogging();
app.UseAuthentication();
app.UseAuthorization();

app.MapOpenApi();
app.MapUserSettingsEndpoints();

app.Run();
