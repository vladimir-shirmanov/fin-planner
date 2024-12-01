using System.Diagnostics;
using OpenTelemetry.Context.Propagation;
using Serilog.Context;

namespace UserManagement;

public static class SerilogEnrichment
{
    private static readonly ActivitySource ActivitySource = new ActivitySource(nameof(UserManagement));
    private static readonly TextMapPropagator Propagator = new TraceContextPropagator();

    public static void EnrichLogContext()
    {
        var currentActivity = Activity.Current;
        if (currentActivity != null)
        {
            LogContext.PushProperty("TraceId", currentActivity.TraceId);
            LogContext.PushProperty("SpanId", currentActivity.SpanId);
            LogContext.PushProperty("ParentId", currentActivity.ParentSpanId);
        }
    }
}