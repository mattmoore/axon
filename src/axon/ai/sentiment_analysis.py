from transformers import pipeline

classifier = pipeline("sentiment-analysis")

def sentiment_analysis(text):
    return classifier(text)
