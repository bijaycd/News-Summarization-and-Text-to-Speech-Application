from collections import Counter
from transformers import pipeline
from keybert import KeyBERT
from src.utils import extract_keywords_keybert, analyze_sentiment
from src.summarization import summarize_overall_sentiment

# ✅ Load necessary models
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
kw_model = KeyBERT("distilbert-base-nli-mean-tokens")

def comparison_analysis(articles):
    """Compares articles based on sentiment, topics, and provides a final sentiment summary."""

    if len(articles) < 10:
        return {"error": "Not enough articles for a full comparison."}

    # ✅ Extract keywords from all 10 articles
    article_keywords = [extract_keywords_keybert(article["summary"]) for article in articles]

    # ✅ Count occurrences of each keyword
    all_keywords = [kw for sublist in article_keywords for kw in sublist]
    keyword_counts = Counter(all_keywords)

    # ✅ Identify Common & Unique Topics
    common_topics = [kw for kw, count in keyword_counts.items() if count >= 3]  # ✅ Common if in ≥3 articles
    unique_topics_per_article = [
        {"Article": i+1, "Unique Topics": list(set(article_keywords[i]) - set(common_topics))}
        for i in range(len(articles))
    ]

    # ✅ Sentiment Distribution
    sentiments = [analyze_sentiment(article["summary"]) for article in articles]
    sentiment_counts = Counter(sentiments)
    formatted_counts = {sent.capitalize(): count for sent, count in sentiment_counts.items()}  # Proper Case

    # ✅ Determine Overall Sentiment
    overall_sentiment = max(sentiment_counts, key=sentiment_counts.get, default="Neutral").capitalize()
    sentiment_summary = f"Overall sentiment is {overall_sentiment} ({formatted_counts.get('Negative', 0)} Negative, {formatted_counts.get('Positive', 0)} Positive)."

    # ✅ LLM-Based Sentiment Summary
    overall_summary = summarize_overall_sentiment(articles)

    # ✅ Return the final comparative analysis
    return {
        "Sentiment Analysis": {
            "Sentiment Distribution": formatted_counts,
            "Final Sentiment Summary": sentiment_summary
        },
        "Topic Overlap": {
            "Common Topics": common_topics,
            "Unique Topics Per Article": unique_topics_per_article
        },
        "Final Sentiment Analysis": overall_summary  # ✅ LLM-generated summary
    }