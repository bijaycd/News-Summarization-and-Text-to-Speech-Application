from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
import uvicorn
from src.utils import extract_news, analyze_sentiment, extract_keywords_keybert, generate_hindi_speech, clean_llm_response
from src.comparison import comparison_analysis
from src.summarization import summarize_overall_sentiment


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



@app.get("/comparative-analyst/")
def get_comparative_analysis(company: str):
    
    # ✅ Extract 10 articles
    articles = extract_news(company)[:10]
    
    if len(articles) < 10:
        raise HTTPException(status_code=400, detail="Not enough articles for a full comparison.")

    # ✅ Run comprehensive comparative analysis
    comparison_data = comparison_analysis(articles)

    return JSONResponse(content=comparison_data)



# Generate audio summary
@app.get("/generate-audio/")
def generate_audio(company: str):
    """Generates a Hindi audio summary using LLM response."""
    
    # ✅ Extract 10 news articles
    articles = extract_news(company)[:10]
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found for the given company.")

    # ✅ Generate LLM-based sentiment summary
    summary_text = summarize_overall_sentiment(articles)
    cleaned_summary = clean_llm_response(summary_text)

    # ✅ Convert summary to Hindi speech
    audio_buffer = generate_hindi_speech(cleaned_summary)

    # ✅ Return only the Hindi audio as a file response
    return StreamingResponse(audio_buffer, media_type="audio/mpeg", headers={
        "Content-Disposition": "attachment; filename=hindi_summary.mp3"
    })



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)