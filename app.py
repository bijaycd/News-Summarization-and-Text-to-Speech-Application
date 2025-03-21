import streamlit as st
from src.utils import extract_news
from src.utils import analyze_sentiment
from src.utils import comparative_analysis
from src.utils import generate_hindi_speech

st.title("News Summarization & TTS App")
company = st.text_input("Enter Company Name")

if st.button("Get News Summary"):
    articles = extract_news(company)
    sentiment_results = [analyze_sentiment(article["summary"]) for article in articles]
    
    st.write("### News Articles:")
    for i, article in enumerate(articles):
        st.write(f"**{article['title']}**")
        st.write(f"Sentiment: {sentiment_results[i]}")

    st.write("### Comparative Analysis")
    st.write(comparative_analysis(articles))

    hindi_text = " ".join([article["summary"] for article in articles])
    audio_file = generate_hindi_speech(hindi_text)
    st.audio(audio_file)