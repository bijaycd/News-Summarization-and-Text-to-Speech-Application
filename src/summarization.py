import os
import groq

working_dir = os.path.dirname(os.path.abspath(__file__))
GROQ_API_KEY = os.environ["GROQ_API_KEY"]

# ✅ Check if API Key is available
if not GROQ_API_KEY:
    raise ValueError("🚨 Error: GROQ_API_KEY is missing! Set it as an environment variable.")

# ✅ Initialize Groq Client
client = groq.Groq(api_key=GROQ_API_KEY)

def summarize_overall_sentiment(articles):
    """Uses Groq API (LLaMA-3, Mixtral) to summarize sentiment analysis."""
    
    # ✅ Concatenate all article summaries
    concatenated_text = " ".join(article["summary"] for article in articles)

    # ✅ Define the prompt
    prompt = f"""
    You are an AI model designed for news sentiment summarization.
    Analyze the following news articles and provide an **overall sentiment summary** (Positive, Negative, or Neutral) 
    along with a brief explanation:

    {concatenated_text}

    Your response should be structured as follows:
    - [Brief reason why this sentiment was chosen]
    """

    # ✅ Use a valid Groq model (Mixtral or LLaMA-3)
    response = client.chat.completions.create(
        model="mistral-saba-24b",
        messages=[
            {"role": "system", "content": "You are a sentiment analysis assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=250
    )

    return response.choices[0].message.content.strip()