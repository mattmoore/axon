from prometheus_client import Histogram

sentiment_analysis_duration = Histogram(
    name = 'sentiment_analysis_duration_seconds_histogram',
    documentation = 'Measure duration of sentiment analysis',
    buckets = [
        0.25,
        0.5,
        0.75
    ]
)
