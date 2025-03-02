import sys
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Callable
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_fastapi_instrumentator.metrics import Info
from prometheus_client import Counter
import json
import logging
from logging import Formatter, LogRecord

class JsonFormatter(Formatter):
    def __init__(self):
        super(JsonFormatter, self).__init__()

    def format(self, record: LogRecord) -> str:
        record_dict = {
            "level": record.levelname,
            "date": self.formatTime(record),
            "message": record.getMessage(),
            "module": record.module,
            "lineno": record.lineno,
        }
        return json.dumps(record_dict)

def makeLogger(name):
    logger = logging.getLogger(name)
    logging_handler = logging.StreamHandler()
    logging_handler.setFormatter(JsonFormatter())
    logger.handlers = [logging_handler]
    logger.setLevel(logging.DEBUG)
    return logger

logger = makeLogger(__name__)
makeLogger('uvicorn.access')


from .ai.sentiment_analysis import sentiment_analysis
from .ai.ask import ask

app = FastAPI()

instrumentator = Instrumentator(
    excluded_handlers = [".*admin.*", "/metrics"],
)
instrumentator.instrument(app, metric_namespace = 'axon', metric_subsystem = 'ai')
instrumentator.expose(app, include_in_schema = False, should_gzip = True)

@app.get("/")
async def root():
    logger.info("Hello World")
    return {"message": "Hello World"}


class SentimentAnalysisRequest(BaseModel):
    text: str

class SentimentAnalysisResponse(BaseModel):
    label: str
    score: float

@app.post("/api/sentiment-analysis")
async def sentiment_analysis_endpoint(request: SentimentAnalysisRequest):
    res = sentiment_analysis(request.text)
    return SentimentAnalysisResponse(
        label = str(res[0]['label']),
        score = str(res[0]['score']),
    )


class AskRequest(BaseModel):
    text: str

class AskResponse(BaseModel):
    answer: str


# Note: Can set up custom interceptors with this
#def http_requested_languages_total() -> Callable[[Info], None]:
#    METRIC = Counter(
#        "http_requested_languages_total",
#        "Number of times ask API is queried.",
#        labelnames = ("lang",)
#    )
#
#    def instrumentation(info: Info) -> None:
#        langs = set()
#        lang_str = info.request.headers["Accept-Language"]
#        for element in lang_str.split(","):
#            element = element.split(";")[0].strip().lower()
#            langs.add(element)
#        for language in langs:
#            METRIC.labels(language).inc()
#
#    return instrumentation
#instrumentator.add(http_requested_languages_total())

ask_counter = Counter('custom_ask_counter', 'Ask query counter')
@app.post("/api/ask")
async def ask_endpoint(request: AskRequest):
    res = ask(request.text)['answer']
    logger.info("Query: {}, Answer: {}".format(request.text, res))
    ask_counter.inc()
    return AskResponse(answer = str(res))

def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("axon.routes:app", host="0.0.0.0", port=8000, reload=True)
