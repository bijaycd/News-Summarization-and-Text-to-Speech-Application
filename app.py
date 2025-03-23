import streamlit as st
import requests

FASTAPI_URL = "http://127.0.0.1:8000"

# Use normal width layout
st.set_page_config(page_title="Insightful News AI", page_icon = "🤖", layout="centered")
st.title("Sentiment-Driven News Summarization with AI-Powered Speech")

# Sidebar Controls
st.sidebar.header("Controls")
company = st.sidebar.text_input("Enter Company Name")
get_news = st.sidebar.button("Get News Summary")
compare_news = st.sidebar.button("Comparative Analysis")
generate_audio = st.sidebar.button("Generate Audio")

# Get News Summary
if get_news:
    st.write("## Comany: ", company)

    response = requests.get(f"{FASTAPI_URL}/news-analysis/", params={"company": company})
    
    if response.status_code == 200:
        news_data = response.json()

        for i, article in enumerate(news_data["Articles"], start=1):
            st.write(f"### {i}. {article['Title']}")
            st.write(f"**Summary:** {article['Summary']}")
            st.write(f"**Sentiment:** {article['Sentiment']}")
            st.write(f"**Topics:** {', '.join(article['Topics'])}")
            st.markdown("---")  # Adds a separator between articles

    else:
        st.error("Error fetching news. Please try again.")


# ✅ Comparative Analysis
if compare_news:
    st.write("## Comparative Analysis")

    response = requests.get(f"{FASTAPI_URL}/comparative-analyst/", params={"company": company})

    if response.status_code == 200:
        comparison_data = response.json()

        # ✅ Extract overall sentiment analysis
        sentiment_data = comparison_data.get("Sentiment Analysis", {})
        sentiment_distribution = sentiment_data.get("Sentiment Distribution", {})
        final_sentiment = sentiment_data.get("Final Sentiment Summary", "No sentiment summary available.")

        # ✅ Extract sentiment counts safely
        positive_count = sentiment_distribution.get("Positive", 0)
        negative_count = sentiment_distribution.get("Negative", 0)
        neutral_count = sentiment_distribution.get("Neutral", 0)

        # ✅ Display sentiment distribution with metrics
        st.write("### Sentiment Distribution")
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Positive", value=positive_count)
        col2.metric(label="Negative", value=negative_count)
        col3.metric(label="Neutral", value=neutral_count)

        # ✅ Display final sentiment
        st.write("### Final Sentiment")
        if positive_count > negative_count:
            st.success(f"**{final_sentiment}**")  # ✅ Green for Positive
        elif positive_count < negative_count:
            st.error(f"**{final_sentiment}**")  # ✅ Red for Negative
        else:
            st.warning(f"**{final_sentiment}**")  # ✅ Yellow for Neutral

        # ✅ Display topic overlap
        st.write("### Topic Overlap")
        topic_overlap = comparison_data.get("Topic Overlap", {})

        # ✅ Display common topics
        common_topics = topic_overlap.get("Common Topics", [])
        if common_topics:
            st.write(f"**Common Topics (Appearing in ≥3 articles):** {', '.join(common_topics)}")
        else:
            st.write("No significant common topics found.")

        # ✅ Display unique topics per article
        unique_topics_per_article = topic_overlap.get("Unique Topics Per Article", [])
        if unique_topics_per_article:
            for topic_data in unique_topics_per_article:
                article_number = topic_data.get("Article", "Unknown")
                unique_topics = topic_data.get("Unique Topics", [])
                st.write(f"**Unique Topics in Article {article_number}:** {', '.join(unique_topics) if unique_topics else 'None'}")

        # ✅ Display Final LLM-Based Sentiment Analysis
        st.write("### LLM-Based Sentiment Summary")
        final_llm_summary = comparison_data.get("Final Sentiment Analysis", "No summary available.")
        st.info(f"**{final_llm_summary}**")

    else:
        st.error(f"🚨 Error fetching comparative analysis: {response.status_code}")



# Generate Hindi Speech Audio
if generate_audio:
    st.write("## Overall Summary")

    response = requests.get(f"{FASTAPI_URL}/generate-audio/", params={"company": company})

    if response.status_code == 200:
        data = response.json()
        summary_text = data.get("summary", "No summary available.")
        audio_url = data.get("audio_url", "")

        # ✅ Display the text summary
        st.write("### Text Summary")
        st.info(f"**{summary_text}**")

        # ✅ Play the audio output (Correct URL)
        if audio_url:
            st.audio(f"{FASTAPI_URL}{audio_url}")  # Use the correct audio download link
        else:
            st.warning("Audio file is not available.")

    else:
        st.error(f"Error generating audio: {response.status_code}")