from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
from ..scraper import scrape

model_name = "deepset/roberta-base-squad2"

model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

nlp = pipeline('question-answering', model = model, tokenizer = tokenizer)

def ask(text):
    context = "Matt Moore is a developer working for Writer. Born February 25, 1987, Matt has always had a love for computer science ever since he was a child."
    scraped = scrape("https://en.wikipedia.org/wiki/Roald_Amundsen")
    print(scraped)
    return nlp(question = text, context = scraped)
