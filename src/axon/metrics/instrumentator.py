from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_fastapi_instrumentator.metrics import Info

def make_instrumentator(app):
    instrumentator = Instrumentator(
        excluded_handlers = [".*admin.*", "/metrics"],
    )
    instrumentator.instrument(app, metric_namespace = 'axon', metric_subsystem = 'ai')
    instrumentator.expose(app, include_in_schema = False, should_gzip = True)
    return instrumentator
