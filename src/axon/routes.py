import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

#classifier = pipeline("sentiment-analysis")

@app.get("/")
async def root():
    return {"message": "Hello World"}


class SentimentAnalysisRequest(BaseModel):
    text: str

class SentimentAnalysisResponse(BaseModel):
    analysis: str

@app.post("/api/sentiment-analysis")
async def sentiment_analysis(request: SentimentAnalysisRequest):
    #res = classifier(request.text)
    return SentimentAnalysisResponse(analysis = "TEST")


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("axon.routes:app", host="0.0.0.0", port=8000, reload=True)
