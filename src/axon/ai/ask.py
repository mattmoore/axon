from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

model_name = "deepset/roberta-base-squad2"

model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

nlp = pipeline('question-answering', model = model, tokenizer = tokenizer)

context = "Matt Moore is a developer working for Writer. Born February 25, 1987, Matt has always had a love for computer science ever since he was a child."

def ask(text):
    return nlp({
        'question': text,
        'context': context
    })
