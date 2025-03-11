from prometheus_client import Counter, Histogram

ask_counter = Counter('custom_ask_counter', 'Ask query counter')

ask_duration = Histogram(
    name = 'ask_duration_seconds_histogram',
    documentation = 'Measure duration of ask',
    buckets = [
        0.25,
        0.5,
        0.75
    ]
)
