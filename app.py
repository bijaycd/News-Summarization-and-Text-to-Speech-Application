import streamlit as st
import requests

# FastAPI Server URL
FASTAPI_URL = "http://127.0.0.1:8000"

# Use normal width layout
st.set_page_config(layout="centered")
st.title("News Summarization & TTS App")

# Sidebar Controls
st.sidebar.header("Controls")
company = st.sidebar.text_input("Enter Company Name")
get_news = st.sidebar.button("Get News Summary")
compare_news = st.sidebar.button("Comparative Analysis")
generate_audio = st.sidebar.button("Generate Audio")

# Get News Summary
if get_news:
    st.write("## News Summary")

    response = requests.get(f"{FASTAPI_URL}/news-analysis/", params={"company": company})
    
    if response.status_code == 200:
        news_data = response.json()

        for i, article in enumerate(news_data["Articles"], start=1):
            st.write(f"### {i}. {article['Title']}")
            st.write(f"**Sentiment:** {article['Sentiment']}")
            st.write(f"**Summary:** {article['Summary']}")
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

        # Display coverage differences
        st.write("### Coverage Differences")
        for diff in comparison_data.get("Coverage Differences", []):
            st.write(f"- **Comparison:** {diff['Comparison']}")
            st.markdown("---")

        # Display topic overlap
        st.write("### Topic Overlap")
        common_topics = comparison_data.get("Topic Overlap", {}).get("Common Topics", [])
        unique_topics_1 = comparison_data.get("Topic Overlap", {}).get("Unique Topics Per Article", [[], []])[0]
        unique_topics_2 = comparison_data.get("Topic Overlap", {}).get("Unique Topics Per Article", [[], []])[1]

        st.write(f"**Common Topics:** {', '.join(common_topics) if common_topics else 'None'}")
        st.write(f"**Unique Topics in Article 1:** {', '.join(unique_topics_1) if unique_topics_1 else 'None'}")
        st.write(f"**Unique Topics in Article 2:** {', '.join(unique_topics_2) if unique_topics_2 else 'None'}")

        # Display final sentiment analysis
        st.write("### Final Sentiment Analysis")
        st.write(comparison_data.get("Final Sentiment Analysis", "No sentiment summary available."))

    else:
        st.error("Error fetching comparative analysis.")

# Generate Hindi Speech Audio
if generate_audio:
    st.write("## Hindi Audio Summary")

    response = requests.get(f"{FASTAPI_URL}/generate-audio/", params={"company": company})

    if response.status_code == 200:
        # Provide a download button for the audio file
        st.audio(response.url)
        st.write(f" **Click [here]({response.url}) to download the Hindi summary.**")
    else:
        st.error("Error generating Hindi speech.")