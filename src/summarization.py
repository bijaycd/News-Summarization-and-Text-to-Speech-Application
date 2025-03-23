import os
import groq

working_dir = os.path.dirname(os.path.abspath(__file__))
GROQ_API_KEY = os.environ["GROQ_API_KEY"]

# Initialize Groq Client
client = groq.Client(api_key=GROQ_API_KEY)

def summarize_overall_sentiment(articles):
    """Uses Groq API (LLama-3, Mixtral, etc.) to summarize sentiment analysis."""
    concatenated_text = " ".join(article["summary"] for article in articles)

    prompt = f"""
    You are an AI language model designed for news sentiment summarization.
    Analyze the following news articles and provide an **overall sentiment summary** (Positive, Negative, or Neutral) 
    along with a brief explanation:
    
    {concatenated_text}
    
    Your response should be structured as follows:
    - **Sentiment:** [Positive/Negative/Neutral]
    - **Explanation:** [Brief summary of why this sentiment was chosen]
    """

    response = client.chat.completions.create(
        model="mistral-saba-24b",  # ✅ Use a powerful model from Groq
        messages=[{"role": "system", "content": "You are a sentiment analysis assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=250
    )

    return response.choices[0].message.content.strip()