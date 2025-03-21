import requests
from bs4 import BeautifulSoup
from collections import Counter
from gtts import gTTS
from deep_translator import GoogleTranslator
from transformers import pipeline
from keybert import KeyBERT

# News Extraction
def extract_news(topic):
    url = f"https://economictimes.indiatimes.com/topic/{topic}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve page. Status Code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    article_blocks = soup.find_all("div", class_="clr flt topicstry story_list")  # Find all articles

    for article in article_blocks:
        title_tag = article.find("a", class_="wrapLines l2")
        summary_tag = article.find("p", class_="wrapLines l3")

        title = title_tag.text.strip() if title_tag else "Title not found"
        summary = summary_tag.text.strip() if summary_tag else "Summary not found"

        articles.append({"title": title, "summary": summary})

    return articles


# Sentiment Analysis
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Function to analyze sentiment
def analyze_sentiment(text):
    result = sentiment_pipeline(text)[0]  # Run text through the model
    sentiment = result["label"]  # Extract sentiment label
    return sentiment  # Returns 'POSITIVE' or 'NEGATIVE'


# Keyword Extraction
kw_model = KeyBERT('distilbert-base-nli-mean-tokens')

def extract_keywords_keybert(text):
    return [kw[0] for kw in kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), top_n=3)]


# Comparative Analysis
def comparison_sentiments(articles):
    sentiments = [analyze_sentiment(article["summary"]) for article in articles]
    sentiment_counts = Counter(sentiments)
    final_sentiment = f"Overall sentiment is {max(sentiment_counts, key=sentiment_counts.get)} with {sentiment_counts} distribution."

    return {
        "Sentiment Distribution": sentiment_counts,
        "Final Sentiment Analysis": final_sentiment
    }


# Summarized Text to Hindi Speech
def generate_hindi_speech(text, filename="output.mp3"):
    hindi_text = GoogleTranslator(source="auto", target="hi").translate(text)  # Translate to Hindi
    tts = gTTS(hindi_text, lang="hi")
    tts.save(filename)
    return filename