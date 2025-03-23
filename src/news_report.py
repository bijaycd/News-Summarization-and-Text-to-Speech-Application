import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from fpdf import FPDF


def generate_pdf_report(company: str, analysis_data: dict) -> str:
    """
    Generates a comprehensive PDF report including sentiment analysis, topic analysis, and charts.

    Args:
        company (str): The company name for which the news was analyzed.
        analysis_data (dict): The analysis data including articles, sentiments, and topics.

    Returns:
        str: The filename of the generated PDF report.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)

    # Report Title
    pdf.cell(200, 10, f"News Analysis Report for {company}", ln=True, align="C")
    pdf.ln(10)

    # Sentiment Analysis Overview
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Sentiment Analysis Overview", ln=True)
    pdf.set_font("Arial", "", 10)
    
    sentiment_data = analysis_data.get("Sentiment Analysis", {}).get("Sentiment Distribution", {})
    for sentiment, count in sentiment_data.items():
        pdf.cell(200, 8, f"{sentiment}: {count} articles", ln=True)
    
    pdf.ln(5)

    # Final Sentiment Summary
    final_sentiment = analysis_data.get("Sentiment Analysis", {}).get("Final Sentiment Summary", "N/A")
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Overall Sentiment Summary:", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 8, final_sentiment)
    pdf.ln(5)

    # Generate Sentiment Bar Chart
    sentiment_chart_path = f"{company}_sentiment_chart.png"
    generate_sentiment_chart(sentiment_data, sentiment_chart_path)
    pdf.image(sentiment_chart_path, x=30, w=150)
    pdf.ln(10)
    
    # Topic Analysis Overview
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Key Topics from News Articles", ln=True)
    pdf.set_font("Arial", "", 10)
    
    common_topics = analysis_data.get("Topic Overlap", {}).get("Common Topics", [])
    pdf.multi_cell(0, 8, ", ".join(common_topics) if common_topics else "No common topics found.")
    pdf.ln(5)

    # Generate Word Cloud for Topics
    wordcloud_path = f"{company}_wordcloud.png"
    generate_wordcloud(common_topics, wordcloud_path)
    pdf.image(wordcloud_path, x=30, w=150)
    pdf.ln(10)

    # Individual Article Analysis (All 29 Articles)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Detailed Article Analysis", ln=True)
    pdf.ln(5)

    for idx, article in enumerate(analysis_data["Articles"], 1):
        pdf.set_font("Arial", "B", 10)
        pdf.cell(200, 8, f"Article {idx}: {article['Title']}", ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 8, f"Summary: {article['Summary']}")
        pdf.cell(200, 8, f"Sentiment: {article['Sentiment']}", ln=True)
        pdf.cell(200, 8, f"Key Topics: {', '.join(article['Topics']) if article['Topics'] else 'N/A'}", ln=True)
        pdf.ln(5)

    # Save the PDF
    pdf_filename = f"{company}_news_report.pdf"
    pdf.output(pdf_filename)

    # Cleanup Temporary Images
    os.remove(sentiment_chart_path)
    os.remove(wordcloud_path)

    return pdf_filename


def generate_sentiment_chart(sentiment_data, filename):
    """Generates a bar chart for sentiment distribution."""
    labels = list(sentiment_data.keys())
    values = list(sentiment_data.values())

    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color=['red', 'blue', 'green'])
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Articles")
    plt.title("Sentiment Distribution")
    plt.savefig(filename)
    plt.close()


def generate_wordcloud(topics, filename):
    """Generates a word cloud for topics."""
    text = " ".join(topics)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(8, 4))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(filename)
    plt.close()