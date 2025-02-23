# model/book_model.py
from transformers import pipeline

# Initialize pipelines for CPU (device=-1) using smaller models for faster inference.
pipelines = {
    "summarization": pipeline("summarization", model="t5-small", device=-1),
    "classification": pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english", device=-1),
    "sentiment": pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", device=-1)
}

def process_description(description: str, mode: str = "summarization") -> str:
    """
    Process the book's description using one of the pipelines.
    
    mode can be:
      - "summarization"
      - "classification"
      - "sentiment"
      - "all" (returns all three combined)
    """
    if not description or len(description.strip()) == 0:
        return "No description available."
    
    if mode not in pipelines and mode != "all":
        return f"Mode '{mode}' not supported. Choose from summarization, classification, sentiment, or all."
    
    if mode == "summarization":
        result = pipelines["summarization"](description, max_length=50, min_length=25, do_sample=False)
        return result[0]['summary_text']
    elif mode == "classification":
        result = pipelines["classification"](description)
        return ", ".join([f"{item['label']}: {item['score']:.2f}" for item in result])
    elif mode == "sentiment":
        result = pipelines["sentiment"](description)
        return ", ".join([f"{item['label']}: {item['score']:.2f}" for item in result])
    elif mode == "all":
        summary = pipelines["summarization"](description, max_length=300, min_length=50, do_sample=False)[0]['summary_text']
        classification = ", ".join([f"{item['label']}: {item['score']:.2f}" for item in pipelines["classification"](description)])
        sentiment = ", ".join([f"{item['label']}: {item['score']:.2f}" for item in pipelines["sentiment"](description)])
        return f"Summary:\n{summary}\n\nClassification:\n{classification}\n\nSentiment:\n{sentiment}"
