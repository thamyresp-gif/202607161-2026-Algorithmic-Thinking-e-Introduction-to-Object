from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.streamlit import StreamlitInstrumentor

RESOURCE = Resource.create(
    {
        "service.name": "orcamento-aluguel",
        "service.version": "1.0.0",
        "deployment.environment": "production",
    }
)

tracer_provider = TracerProvider(resource=RESOURCE)
trace.set_tracer_provider(tracer_provider)

try:
    otlp_exporter = OTLPSpanExporter(endpoint="otel-collector:4317", insecure=True)
    span_processor = BatchSpanProcessor(otlp_exporter)
    tracer_provider.add_span_processor(span_processor)
except Exception:
    pass

StreamlitInstrumentor().instrument(tracer_provider=tracer_provider)

tracer = trace.get_tracer(__name__)