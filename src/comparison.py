from collections import Counter
from transformers import pipeline
from keybert import KeyBERT
from src.utils import extract_keywords_keybert

# ✅ Load necessary models
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
kw_model = KeyBERT("distilbert-base-nli-mean-tokens")


def comparative_analysis(articles):
    """ Compares articles based on topics, sentiment, and coverage differences """

    if len(articles) < 2:
        return "Not enough articles for comparison."

    # Extract keywords for each article
    article_keywords = [extract_keywords_keybert(article["summary"]) for article in articles]

    # Identify Common & Unique Topics
    all_keywords = [kw for sublist in article_keywords for kw in sublist]
    keyword_counts = Counter(all_keywords)
    
    common_topics = [kw for kw, count in keyword_counts.items() if count > 1]
    unique_topics_per_article = [
        list(set(article_keywords[i]) - set(common_topics)) for i in range(len(articles))
    ]

    # Coverage Differences
    coverage_differences = []
    for i in range(len(articles) - 1):
        comparison_text = f"Article {i+1} discusses {', '.join(article_keywords[i])}, while Article {i+2} focuses on {', '.join(article_keywords[i+1])}."
        coverage_differences.append({"Comparison": comparison_text})    

    # Return final comparative analysis
    return {
        "Coverage Differences": coverage_differences,
        "Topic Overlap": {
            "Common Topics": common_topics,
            "Unique Topics Per Article": unique_topics_per_article
        }
    }