from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from src.news_report import generate_pdf_report
import uvicorn
from src.utils import extract_news, analyze_sentiment, extract_keywords_keybert, generate_hindi_speech
from src.comparison import comparison_analysis
from src.summarization import summarize_overall_sentiment
from typing import Dict

app = FastAPI()


@app.get("/")
def home() -> Dict[str, str]:
    """Home route for API"""
    return {"message": "Welcome to the News Analysis API!"}


@app.get("/news-analysis/")
def get_news_analysis(company: str) -> JSONResponse:
    """Extracts news, analyzes sentiment, and provides a JSON response."""
    articles = extract_news(company)[:10]  # Extract first 10 articles
    
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found for the given company.")

    news_data = {
        "Company": company,
        "Articles": [
            {
                "Title": article.get("title", "No Title"),
                "Summary": article.get("summary", "No Summary"),
                "Sentiment": analyze_sentiment(article.get("summary", "")),  # Sentiment analysis
                "Topics": extract_keywords_keybert(article.get("summary", ""))  # Extract topics
            }
            for article in articles
        ]
    }

    return JSONResponse(content=news_data)


@app.get("/comparative-analyst/")
def get_comparative_analysis(company: str) -> JSONResponse:
    """Performs comparative sentiment analysis for a given company."""
    articles = extract_news(company)[:10]
    
    if len(articles) < 10:
        raise HTTPException(status_code=400, detail="Not enough articles for a full comparison.")

    comparison_data = comparison_analysis(articles)  # Perform comparative analysis

    return JSONResponse(content=comparison_data)


@app.get("/generate-audio/")
def generate_audio(company: str) -> StreamingResponse:
    """Generates a Hindi audio summary using LLM response."""
    articles = extract_news(company)[:10]

    if not articles:
        raise HTTPException(status_code=404, detail="No articles found for the given company.")

    summary_text = summarize_overall_sentiment(articles)  # Generate summary text
    audio_buffer = generate_hindi_speech(summary_text)  # Convert summary to speech

    return StreamingResponse(
        audio_buffer,
        media_type="audio/mpeg",
        headers={"Content-Disposition": "attachment; filename=hindi_summary.mp3"}
    )


# (BONUS) PDF report for news analysis
@app.get("/generate-report/")
def generate_report(company: str):
    """API to generate a PDF report for news analysis."""

    # ✅ Extract 29 articles & analyze them
    articles = extract_news(company)
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found.")

    # ✅ Run sentiment & topic analysis
    analysis_data = comparison_analysis(articles)

    # ✅ Generate the PDF Report
    pdf_filename = generate_pdf_report(company, analysis_data)

    return FileResponse(pdf_filename, media_type="application/pdf", filename=pdf_filename)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)