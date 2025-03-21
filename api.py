from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
import uvicorn
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
    text = f"Audio summary for {company}."
    audio_buffer = generate_hindi_speech(text)

    return StreamingResponse(audio_buffer, media_type="audio/mpeg", headers={
        "Content-Disposition": "attachment; filename=hindi_summary.mp3"
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)