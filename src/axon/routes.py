import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from .ai.sentiment_analysis import sentiment_analysis

app = FastAPI()

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


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("axon.routes:app", host="0.0.0.0", port=8000, reload=True)
