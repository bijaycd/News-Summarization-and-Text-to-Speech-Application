---
title: SentimentNews
emoji: 🌍
colorFrom: yellow
colorTo: yellow
sdk: docker
pinned: false
---

# **Insightful News AI** 🤖

## Overview
Insightful News AI is a FastAPI-based application tool that fetches news articles for a given company, analyzes their sentiment, extracts key topics, and provides Hindi audio summaries. The application uses NLP models for text processing and an AI-powered TTS engine for speech synthesis.

## **Project Setup**  
### Prerequisites
- Python 3.10 (Virtual Environment: `tts`)
- FastAPI
- Streamlit
- Required Python packages (listed in `requirements.txt`)

## 🚀 Installation Steps

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/bijaycd/News-Summarization-and-Text-to-Speech-Application.git
cd News-Summarization-and-Text-to-Speech-Application
```

### **2️⃣ Create and Activate a Virtual Environment**  
```bash
python -m venv tts
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### **3️⃣ Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **4️⃣ Set Up Environment Variables**  
Create a `.env` file and add your API keys:  
```
GROQ_API_KEY=your_api_key_here
```

### **5️⃣ Run the Backend (FastAPI Server)**  
```bash
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

### **6️⃣ Run the Frontend (Streamlit UI)**  
```bash
streamlit run app.py
```

---

## **🧠 Model Details**  

This project uses **three AI models**:  

1. **Summarization Model** (Mistral)  
   - Extracts key insights from news articles.  
   - Uses the `mistral-saba-24b` model for concise summarization.  

2. **Sentiment Analysis Model** (DistilBERT)
   - Categorizes sentiment as **Positive, Negative, or Neutral**.  
   - Analyzes news sentiment using pre-trained NLP models.  

3. **Text-to-Speech (TTS) Model** (Google Text-to-Speech)
   - Converts AI-generated summaries into **Hindi speech**.  
   - Uses a custom speech synthesis model.  

---

## **🛠 API Development**  

### **Endpoints**  

| Method | Endpoint                  | Description |
|--------|---------------------------|-------------|
| `GET`  | `/`                        | Welcome message. |
| `GET`  | `/news-analysis/?company=XYZ` | Extracts news titles, summaries and analyzes sentiments |
| `GET`  | `/comparative-analyst/?company=XYZ` | Performs a comparative sentiment analysis. |
| `GET`  | `/generate-audio/?company=XYZ` | Generates a Hindi audio summary. |

---

## **📡 API Usage**  

### **1️⃣ Fetch News Sentiment Summary**  
**Request (Postman, cURL, Python)**  
```bash
curl -X GET "http://127.0.0.1:8000/news-analysis/?company=Google"
```
**Response (JSON)**  
```json
{
    "Company": "Google",
    "Articles": [
        {
            "Title": "Google removes 331 malicious apps from Play Store",
            "Summary": "Vapor Operation infected 331 apps with 60M+ downloads, engaging in ad fraud and phishing...",
            "Sentiment": "Negative",
            "Topics": ["Vapor Operation", "Andriod 13", "Security"]
        }
    ]
}
```

### **2️⃣ Comparative Sentiment Analysis**  
```bash
curl -X GET "http://127.0.0.1:8000/comparative-analyst/?company=Google"
```
**Response Example**
```json
{
    "Sentiment Analysis": {
        "Sentiment Distribution": {"Positive": 5, "Negative": 4, "Neutral": 1},
        "Final Sentiment Summary": "Overall, Google news has a positive sentiment..."
    }
}
```

### **3️⃣ Generate Hindi Audio Summary**  
```bash
curl -X GET "http://127.0.0.1:8000/generate-audio/?company=Google"
```
**Response**  
- Returns an `mp3` file with the Hindi audio summary.

---

## **🔗 Third-Party APIs Used**  

| API       | Purpose |
|-----------|---------|
| **Groq API** | Used for text summarization (Mistral). |

---

## **⚠ Assumptions & Limitations**  

### **✅ Assumptions**  
1. **Company Name Input**: The company name entered exists in publicly available news.  
2. **Sentiment Accuracy**: The sentiment analysis model is trained on general news data but may not capture sarcasm or nuanced sentiment.  
3. **Keyword Extraction**: Uses KeyBERT for topic extraction, assuming that key topics can be identified from short summaries.  

### **🚨 Limitations**  
1. **News Data Availability**: If fewer than 10 articles are found, comparative analysis may not be performed.  
2. **TTS Language Support**: Currently, speech generation is limited to **Hindi** only.  
3. **Rate Limits**: Using the Groq API requires an API key with rate limits.  

---

## **📌 Future Enhancements**  
✅ **Expand TTS support to more languages**  
✅ **Improve sentiment classification using fine-tuned LLMs**  
✅ **Enable real-time news updates using WebSockets**

---

### **🔗 Contributors**  
👤 **Bijay Chandra Das**  
📧 **bijaydasiitb@example.com**  

📌 **GitHub Repo**: [GitHub](https://github.com/bijaycd/News-Summarization-and-Text-to-Speech-Application)  

---
