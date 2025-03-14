from opentelemetry import metrics

class SentimentAnalysisMetrics:
    def __init__(self, meter):
        self.sentiment_analysis_duration = meter.create_histogram(
            name = 'sentiment_analysis_duration_seconds_histogram',
            description = 'Measure duration of sentiment analysis'
        )

    def record_sentiment_analysis_duration(self, duration):
        return self.sentiment_analysis_duration.record(duration)
