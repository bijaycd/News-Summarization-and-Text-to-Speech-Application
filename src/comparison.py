from collections import Counter
from transformers import pipeline
from keybert import KeyBERT
from src.utils import extract_keywords_keybert, analyze_sentiment
from src.summarization import summarize_overall_sentiment

def comparison_analysis(articles):
    """
    Compares articles based on sentiment and topics, providing a final sentiment summary.

    Args:
        articles (list[dict]): A list of articles, each containing a "summary" key.

    Returns:
        dict: A dictionary containing sentiment analysis, topic overlap, and final sentiment summary.
    """

    if len(articles) < 10:
        return {"error": "Not enough articles for a full comparison."}

    # Extract keywords from all articles
    article_keywords = [extract_keywords_keybert(article["summary"]) for article in articles]

    # Count occurrences of each keyword
    all_keywords = [kw for sublist in article_keywords for kw in sublist]
    keyword_counts = Counter(all_keywords)

    # Identify common and unique topics
    common_topics = [kw for kw, count in keyword_counts.items() if count >= 3]  # Common if in ≥3 articles
    unique_topics_per_article = [
        {"Article": i + 1, "Unique Topics": list(set(article_keywords[i]) - set(common_topics))}
        for i in range(len(articles))
    ]

    # Perform sentiment analysis
    sentiments = [analyze_sentiment(article["summary"]) for article in articles]
    sentiment_counts = Counter(sentiments)
    
    # Format sentiment counts for readability
    formatted_counts = {sent.capitalize(): count for sent, count in sentiment_counts.items()}

    # Determine overall sentiment
    overall_sentiment = max(sentiment_counts, key=sentiment_counts.get, default="Neutral").capitalize()
    sentiment_summary = (
        f"Overall sentiment is {overall_sentiment} "
        f"({formatted_counts.get('Negative', 0)} Negative, {formatted_counts.get('Positive', 0)} Positive)."
    )

    # Generate LLM-based sentiment summary
    overall_summary = summarize_overall_sentiment(articles)

    # Return the final comparative analysis
    return {
        "Sentiment Analysis": {
            "Sentiment Distribution": formatted_counts,
            "Final Sentiment Summary": sentiment_summary
        },
        "Topic Overlap": {
            "Common Topics": common_topics,
            "Unique Topics Per Article": unique_topics_per_article
        },
        "Final Sentiment Analysis": overall_summary  # LLM-generated summary
    }