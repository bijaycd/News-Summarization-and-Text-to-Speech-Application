import streamlit as st
from src.utils import extract_news, analyze_sentiment, generate_hindi_speech, extract_keywords_keybert, comparison_sentiments
from src.comparison import comparative_analysis
import json

# Set Full-Screen Mode with Sidebar
st.set_page_config(layout="centered")

st.title("News Summarization & TTS App")

# Sidebar for Input and Buttons
st.sidebar.header("Controls")
company = st.sidebar.text_input("Enter Company Name")

# Sidebar Buttons
get_news = st.sidebar.button("Get News Summary")
compare_news = st.sidebar.button("Comparative Analysis")
generate_audio = st.sidebar.button("Generate Audio")

# Fetch articles only once when needed
if get_news or compare_news or generate_audio:
    articles = extract_news(company)[:10]  # Extract only 10 articles

# Main Page Content
if get_news:
    articles = extract_news(company)[:5]  # Get first 5 articles
    news_data = {"Company": company, "Articles": []}  # Initialize structured output

    for article in articles:
        sentiment = analyze_sentiment(article["summary"])  # Analyze sentiment
        topics = extract_keywords_keybert(article["summary"])  # Extract key topics
        
        news_data["Articles"].append({
            "Title": article["title"],
            "Summary": article["summary"],
            "Sentiment": sentiment,
            "Topics": topics
        })

    # Display structured JSON output
    st.write("## Extracted News Data")
    st.json(news_data)  # Displays output in formatted JSON

if compare_news:
    st.write("## Comparative Analysis")
    st.write(comparison_sentiments(articles))
    st.write(comparative_analysis(articles[:2]))  # Comparing first 2 articles

if generate_audio:
    st.write("## Hindi Audio Summary")

    text = " ".join([
        json.dumps(comparison_sentiments(articles), ensure_ascii=False, indent=2),
        json.dumps(comparative_analysis(articles[:2]), ensure_ascii=False, indent=2)
    ])

    audio_file = generate_hindi_speech(text)
    st.audio(audio_file)