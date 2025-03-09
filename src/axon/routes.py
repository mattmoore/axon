import sys
import time
import uvicorn
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from typing import Callable
from .request_models.ask_request import AskRequest, AskResponse
from .request_models.semantic_analysis_request import SentimentAnalysisRequest, SentimentAnalysisResponse
from .logging import JsonFormatter, make_logger
from .metrics.ask import AskMetrics
from .metrics.sentiment_analysis import SentimentAnalysisMetrics
from .ai.sentiment_analysis import sentiment_analysis
from .ai.ask import ask

from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry import trace
from .otel import init_tracer, init_meter

logger = make_logger(__name__)
make_logger('uvicorn.access')
make_logger('uvicorn.error')

tracer = init_tracer()
meter = init_meter()

RequestsInstrumentor().instrument()
app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

ask_metrics = AskMetrics(meter)
sentiment_metrics = SentimentAnalysisMetrics(meter)

@app.get("/")
async def root():
    with tracer.start_as_current_span("root_request"):
        logger.info("Hello World")
        return {"message": "Hello World"}

@app.post("/api/sentiment-analysis")
async def sentiment_analysis_endpoint(request: SentimentAnalysisRequest):
    start = time.perf_counter()
    res = sentiment_analysis(request.text)
    end = time.perf_counter()
    duration = end - start
    sentiment_metrics.record_sentiment_analysis_duration(duration)
    return SentimentAnalysisResponse(
        label = str(res[0]['label']),
        score = str(res[0]['score']),
    )

@app.post("/api/ask")
async def ask_endpoint(request: AskRequest):
    start = time.perf_counter()
    with tracer.start_as_current_span("process-ask"):
        res = ask(request.text)['answer']
    end = time.perf_counter()
    duration = end - start
    ask_metrics.record_ask_duration(duration)
    ask_metrics.record_ask_counter()
    logger.info("Query: {}, Answer: {}".format(request.text, res))
    return AskResponse(answer = str(res))

def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("axon.routes:app", host="0.0.0.0", port=8000, reload=True)
