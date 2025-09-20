from opentelemetry import trace, metrics

from opentelemetry.sdk.resources import Resource

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader
)
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter

def init_tracer():
    provider = TracerProvider()
    processor = BatchSpanProcessor(OTLPSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer("axon")

    return tracer

def init_meter():
    metric_reader = PeriodicExportingMetricReader(
        exporter = OTLPMetricExporter(),
        export_interval_millis = 1000
    )
    provider = MeterProvider(metric_readers = [metric_reader])
    metrics.set_meter_provider(provider)
    meter = metrics.get_meter("axon")

    return meter
