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
