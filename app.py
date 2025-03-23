import streamlit as st
import requests

# Define API URL
FASTAPI_URL = "http://127.0.0.1:8000"

# Configure Streamlit app layout
st.set_page_config(page_title="Insightful News AI", page_icon="🤖", layout="centered")
st.title("Sentiment-Driven News Summarization with AI-Powered Speech")

# Sidebar Controls
st.sidebar.header("Controls")
company = st.sidebar.text_input("Enter Company Name")
get_news = st.sidebar.button("Get News Summary")
compare_news = st.sidebar.button("Comparative Analysis")
generate_audio = st.sidebar.button("Generate Audio")


def fetch_data(endpoint, params=None):
    """
    Fetch data from the given API endpoint.
    
    Args:
        endpoint (str): API endpoint to fetch data from.
        params (dict, optional): Query parameters for the request.
    
    Returns:
        dict: JSON response if successful, else None.
    """
    response = requests.get(f"{FASTAPI_URL}/{endpoint}", params=params)
    return response.json() if response.status_code == 200 else None


# Fetch News Summary
if get_news:
    st.write("## Company: ", company)
    news_data = fetch_data("news-analysis", {"company": company})

    if news_data:
        for i, article in enumerate(news_data.get("Articles", []), start=1):
            st.write(f"### {i}. {article.get('Title', 'No Title')}")
            st.write(f"**Summary:** {article.get('Summary', 'No Summary')}")
            st.write(f"**Sentiment:** {article.get('Sentiment', 'Unknown')}")
            st.write(f"**Topics:** {', '.join(article.get('Topics', []))}")
            st.markdown("---")  # Separator between articles
    else:
        st.error("Error fetching news. Please try again.")


# Comparative Analysis
if compare_news:
    st.write("## Comparative Analysis")
    comparison_data = fetch_data("comparative-analyst", {"company": company})

    if comparison_data:
        # Extract overall sentiment analysis
        sentiment_data = comparison_data.get("Sentiment Analysis", {})
        sentiment_distribution = sentiment_data.get("Sentiment Distribution", {})
        final_sentiment = sentiment_data.get("Final Sentiment Summary", "No sentiment summary available.")

        # Extract sentiment counts safely
        positive_count = sentiment_distribution.get("Positive", 0)
        negative_count = sentiment_distribution.get("Negative", 0)
        neutral_count = sentiment_distribution.get("Neutral", 0)

        # Display sentiment distribution
        st.write("### Sentiment Distribution")
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Positive", value=positive_count)
        col2.metric(label="Negative", value=negative_count)
        col3.metric(label="Neutral", value=neutral_count)

        # Display final sentiment summary
        st.write("### Final Sentiment")
        if positive_count > negative_count:
            st.success(f"**{final_sentiment}**")  # Green for Positive
        elif positive_count < negative_count:
            st.error(f"**{final_sentiment}**")  # Red for Negative
        else:
            st.warning(f"**{final_sentiment}**")  # Yellow for Neutral

        # Display topic overlap
        st.write("### Topic Overlap")
        topic_overlap = comparison_data.get("Topic Overlap", {})

        # Display common topics
        common_topics = topic_overlap.get("Common Topics", [])
        st.write(f"**Common Topics (Appearing in ≥3 articles):** {', '.join(common_topics) if common_topics else 'None'}")

        # Display unique topics per article
        unique_topics_per_article = topic_overlap.get("Unique Topics Per Article", [])
        for topic_data in unique_topics_per_article:
            article_number = topic_data.get("Article", "Unknown")
            unique_topics = topic_data.get("Unique Topics", [])
            st.write(f"**Unique Topics in Article {article_number}:** {', '.join(unique_topics) if unique_topics else 'None'}")

        # Display Final LLM-Based Sentiment Analysis
        st.write("## Overall Sentiment Summary")
        final_llm_summary = comparison_data.get("Final Sentiment Analysis", "No summary available.")
        st.info(f"**{final_llm_summary}**")

    else:
        st.error("Error fetching comparative analysis. Please try again.")


# Generate Hindi Speech Audio
if generate_audio:
    st.write("### Hindi Audio Summary")

    audio_url = f"{FASTAPI_URL}/generate-audio/?company={company}"
    response = requests.get(audio_url)

    if response.status_code == 200:
        audio_data = response.content

        # Play the audio
        st.audio(audio_data, format="audio/mp3")

        # Provide a download button
        st.download_button(
            label="Download Hindi Audio",
            data=audio_data,
            file_name="hindi_summary.mp3",
            mime="audio/mpeg"
        )
    else:
        st.error("Failed to generate audio. Please try again.")