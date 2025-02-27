import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import make_asgi_app
from prometheus_fastapi_instrumentator import Instrumentator

from .ai.sentiment_analysis import sentiment_analysis
from .ai.ask import ask

app = FastAPI()

instrumentator = Instrumentator().instrument(app, metric_namespace = 'axon')
instrumentator.expose(app, include_in_schema = False, should_gzip = True)

@app.get("/")
async def root():
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

@app.post("/api/ask")
async def ask_endpoint(request: AskRequest):
    res = ask(request.text)
    return AskResponse(answer = str(res['answer']))

def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("axon.routes:app", host="0.0.0.0", port=8000, reload=True)
