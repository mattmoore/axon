# Axon

AI Examples

## Run

```shell
poetry run start
```

> [!NOTE]
> Can set up custom interceptors with this:
> 
> ```python
> def http_requested_languages_total() -> Callable[[Info], None]:
>     METRIC = Counter(
>         "http_requested_languages_total",
>         "Number of times ask API is queried.",
>         labelnames = ("lang",)
>     )
> 
>     def instrumentation(info: Info) -> None:
>         langs = set()
>         lang_str = info.request.headers["Accept-Language"]
>         for element in lang_str.split(","):
>             element = element.split(";")[0].strip().lower()
>             langs.add(element)
>         for language in langs:
>             METRIC.labels(language).inc()
> 
>     return instrumentation
> instrumentator.add(http_requested_languages_total())
> ```

## Docker Compose

```shell
docker compose up -d
docker compose down
```

## K8s/kind

To fully start:

```shell
# Create the kind cluster
kind create cluster --config k8s/cluster-config.yml

# Build and load the axon image
docker build . -t axon:0.1.0
kind load docker-image axon:0.1.0

# Can monitor the images on kind with
docker exec -it $(kind get clusters | head -1)-control-plane crictl images

# Deploy
kubectl apply -f k8s/axon.yml

# To test:
curl -X POST http://localhost:30000/api/ask -H 'content-type: application/json' -d '{ "text": "What is Roald'\''s full name?" }'
```

Delete things:

```shell
# Delete the cluster
kind delete clusters kind

# Delete k8s config:
kubectl delete -f k8s/axon.yml
```
