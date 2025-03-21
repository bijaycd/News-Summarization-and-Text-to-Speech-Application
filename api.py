from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import json
from src.utils import extract_news, analyze_sentiment, extract_keywords_keybert, comparison_sentiments, generate_hindi_speech
from src.comparison import comparative_analysis

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the News Analysis API!"}

@app.get("/news-analysis/")
def get_news_analysis(company: str):
    """Extracts news, analyzes sentiment, and provides a JSON response."""
    articles = extract_news(company)[:5]  # Extract first 5 articles
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found for the given company.")

    news_data = {"Company": company, "Articles": []}

    for article in articles:
        sentiment = analyze_sentiment(article["summary"])  # Analyze sentiment
        topics = extract_keywords_keybert(article["summary"])  # Extract key topics
        
        news_data["Articles"].append({
            "Title": article["title"],
            "Summary": article["summary"],
            "Sentiment": sentiment,
            "Topics": topics
        })

    return JSONResponse(content=news_data)

@app.get("/comparative-analysis/")
def get_comparative_analysis(company: str):
    """Provides a comparative analysis between two articles."""
    articles = extract_news(company)[:5]
    if len(articles) < 2:
        raise HTTPException(status_code=400, detail="Not enough articles for comparison.")

    comparison_result = comparative_analysis(articles[:2])
    return JSONResponse(content=comparison_result)

@app.get("/generate-audio/")
def generate_audio(company: str):
    """Generates Hindi speech from the news analysis and provides a downloadable file."""
    articles = extract_news(company)[:5]
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found for the given company.")

    # Generate the text to convert into speech
    text = f"""
    Sentiment Analysis Summary: {comparison_sentiments(articles).get("Final Sentiment Analysis", "No sentiment summary available.")}.
    Comparative Analysis: {comparative_analysis(articles[:2]).get("Generated Summary", "No comparison summary available.")}.
    """

    # Generate Hindi Speech
    audio_file = generate_hindi_speech(text)

    return FileResponse(audio_file, media_type="audio/mpeg", filename="hindi_summary.mp3")