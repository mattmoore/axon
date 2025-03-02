from prometheus_client import Counter

ask_counter = Counter('custom_ask_counter', 'Ask query counter')
