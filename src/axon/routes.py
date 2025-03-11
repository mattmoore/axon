import sys
import uvicorn
import time
from fastapi import FastAPI
from typing import Callable
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_fastapi_instrumentator.metrics import Info
from .request_models.ask_request import AskRequest, AskResponse
from .request_models.semantic_analysis_request import SentimentAnalysisRequest, SentimentAnalysisResponse
from .logging import JsonFormatter, makeLogger
from .metrics.instrumentator import make_instrumentator
from .metrics.ask import ask_counter, ask_duration
from .metrics.sentiment_analysis import sentiment_analysis_duration
from .ai.sentiment_analysis import sentiment_analysis
from .ai.ask import ask

logger = makeLogger(__name__)
makeLogger('uvicorn.access')

app = FastAPI()
instrumentator = make_instrumentator(app)

@app.get("/")
async def root():
    logger.info("Hello World")
    return {"message": "Hello World"}

@app.post("/api/sentiment-analysis")
async def sentiment_analysis_endpoint(request: SentimentAnalysisRequest):
    start = time.perf_counter()
    res = sentiment_analysis(request.text)
    end = time.perf_counter()
    sentiment_analysis_duration.observe(end - start)
    return SentimentAnalysisResponse(
        label = str(res[0]['label']),
        score = str(res[0]['score']),
    )

@app.post("/api/ask")
async def ask_endpoint(request: AskRequest):
    with ask_duration.time():
        res = ask(request.text)['answer']
    logger.info("Query: {}, Answer: {}".format(request.text, res))
    ask_counter.inc()
    return AskResponse(answer = str(res))

def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("axon.routes:app", host="0.0.0.0", port=8000, reload=True)
