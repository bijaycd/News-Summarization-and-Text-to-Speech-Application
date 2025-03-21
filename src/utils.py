import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from collections import Counter
from gtts import gTTS

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
def analyze_sentiment(text):
    score = TextBlob(text).sentiment.polarity
    if score > 0.05:
        return "Positive"
    elif score < -0.05:
        return "Negative"
    else:
        return "Neutral"
    
# Comparative Analysis
def comparative_analysis(articles):
    sentiments = [analyze_sentiment(article["summary"]) for article in articles]
    sentiment_counts = Counter(sentiments)

    return {
        "Sentiment Distribution": sentiment_counts,
        "Overall Sentiment": "Mostly Positive" if sentiment_counts["Positive"] > sentiment_counts["Negative"] else "Mostly Negative"
    }


# Summarized Text to Hindi Speech
def generate_hindi_speech(text, filename="output.mp3"):
    tts = gTTS(text, lang="hi")
    tts.save(filename)
    return filename