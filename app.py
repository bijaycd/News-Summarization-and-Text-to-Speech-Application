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


# Comparative Analysis
if compare_news:
    st.write("## Comparative Analysis")

    response = requests.get(f"{FASTAPI_URL}/comparative-analysis/", params={"company": company})

    if response.status_code == 200:
        comparison_data = response.json()

        # ✅ Extract overall sentiment analysis
        overall_sentiment_data = comparison_data.get("Overall Sentiment Analysis", {})       
        sentiment_distribution = overall_sentiment_data.get("Sentiment Distribution", {})
        final_sentiment = overall_sentiment_data.get("Final Sentiment Analysis", "No sentiment summary available.")

        # ✅ Extract calculated sentiment counts safely
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
            st.success(f"**{final_sentiment}**")  # ✅ Green box for Positive
        elif positive_count < negative_count:
            st.error(f"**{final_sentiment}**")  # ✅ Red box for Negative
        else:
            st.warning(f"**{final_sentiment}**")  # ✅ Yellow box for Neutral

        # ✅ Display coverage differences correctly
        st.write("### Coverage Differences")
        coverage_differences = comparison_data.get("Comparison", {}).get("Coverage Differences", [])
        if coverage_differences:
            for diff in coverage_differences:
                st.write(f"- **{diff.get('Comparison', 'No data available')}**")
        else:
            st.write("No coverage differences found.")
        st.markdown("---")

        # ✅ Display topic overlap correctly
        st.write("### Topic Overlap")
        topic_overlap = comparison_data.get("Comparison", {}).get("Topic Overlap", {})

        common_topics = topic_overlap.get("Common Topics", [])
        unique_topics_1 = topic_overlap.get("Unique Topics Per Article", [[], []])[0]
        unique_topics_2 = topic_overlap.get("Unique Topics Per Article", [[], []])[1]

        st.write(f"**Common Topics:** {', '.join(common_topics) if common_topics else 'None'}")
        st.write(f"**Unique Topics in Article 1:** {', '.join(unique_topics_1) if unique_topics_1 else 'None'}")
        st.write(f"**Unique Topics in Article 2:** {', '.join(unique_topics_2) if unique_topics_2 else 'None'}")

    else:
        st.error(f"Error fetching comparative analysis: {response.status_code}")



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