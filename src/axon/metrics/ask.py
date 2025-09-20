from opentelemetry import metrics

class AskMetrics:
    def __init__(self, meter):
        self.ask_counter = meter.create_counter(
            name = 'ask_counter',
            description = "Count of ask queries"
        )

        self.ask_duration = meter.create_histogram(
            name = 'ask_duration_seconds_histogram',
            description = "Duration of ask process",
            unit = "s"
        )

    def record_ask_counter(self):
        return self.ask_counter.add(1)

    def record_ask_duration(self, duration):
        return self.ask_duration.record(duration)
