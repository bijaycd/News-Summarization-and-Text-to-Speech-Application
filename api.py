from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
import uvicorn
from src.utils import extract_news, analyze_sentiment, extract_keywords_keybert, comparison_sentiments, generate_hindi_speech
from src.comparison import comparative_analysis
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



@app.get("/comparative-analysis/")
def get_comparative_analysis(company: str):
    """Provides a comparative analysis between two articles and overall sentiment analysis."""
    articles = extract_news(company)[:10]

    if len(articles) < 2:
        raise HTTPException(status_code=400, detail="Not enough articles for comparison.")

    # ✅ Use the function from utils.py
    sentiment_analysis = comparison_sentiments(articles)

    # ✅ Comparative analysis of the first 2 articles
    comparison_result = comparative_analysis(articles[:2])

    # ✅ Include sentiment data in the response
    comparison_data = {
        "Overall Sentiment Analysis": sentiment_analysis,
        "Comparison": comparison_result
    }

    return JSONResponse(content=comparison_data)



@app.get("/generate-audio/")
def generate_audio(company: str):
    """Generates an LLM-based summary and provides a Hindi audio output."""
    
    # ✅ Step 1: Extract news articles
    articles = extract_news(company)[:10]
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found for the given company.")

    # ✅ Step 2: Generate the LLM-based summary
    summary_text = summarize_overall_sentiment(articles)

    # ✅ Step 3: Convert summary to Hindi audio (returns a buffer)
    audio_buffer = generate_hindi_speech(summary_text)

    # ✅ Step 4: Store the audio file in memory
    audio_filename = "hindi_summary.mp3"
    audio_buffer.seek(0)

    # ✅ Step 5: Return JSON response with summary and audio file link
    return JSONResponse(
        content={
            "summary": summary_text,
            "audio_url": f"/download-audio/?filename={audio_filename}"
        }
    )

@app.get("/download-audio/")
def download_audio(filename: str):
    """Streams the generated audio file."""
    audio_buffer = generate_hindi_speech("Placeholder text")  # Replace with actual generated buffer
    audio_buffer.seek(0)

    return StreamingResponse(audio_buffer, media_type="audio/mpeg", headers={
        "Content-Disposition": f"attachment; filename={filename}"
    })



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)