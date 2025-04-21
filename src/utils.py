import requests
import io
from bs4 import BeautifulSoup
from gtts import gTTS
from deep_translator import GoogleTranslator
from transformers import pipeline
from keybert import KeyBERT
from TTS.api import TTS
import soundfile as sf

# News Extraction
def extract_news(topic):
    """
    Extracts news articles related to the given topic from the Economic Times website.

    Args:
        topic (str): The topic for which news articles need to be extracted.

    Returns:
        list[dict]: A list of dictionaries containing news titles and summaries.
    """
    url = f"https://economictimes.indiatimes.com/topic/{topic}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    article_blocks = soup.find_all("div", class_="clr flt topicstry story_list")  

    for article in article_blocks:
        title_tag = article.find("a", class_="wrapLines l2")
        summary_tag = article.find("p", class_="wrapLines l3")

        title = title_tag.text.strip() if title_tag else "Title not found"
        summary = summary_tag.text.strip() if summary_tag else "Summary not found"

        articles.append({"title": title, "summary": summary})

    return articles


# Sentiment Analysis Pipeline
sentiment_pipeline = pipeline(
    "sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english"
)

def analyze_sentiment(text):
    """
    Analyzes the sentiment of the given text using a pre-trained model.

    Args:
        text (str): The input text to analyze.

    Returns:
        str: Sentiment label ('POSITIVE' or 'NEGATIVE').
    """
    result = sentiment_pipeline(text)[0]  # Process text through the model
    return result["label"]  # Extract and return sentiment label


# Keyword Extraction using KeyBERT
kw_model = KeyBERT("distilbert-base-nli-mean-tokens")

def extract_keywords_keybert(text):
    """
    Extracts keywords from the given text using KeyBERT.

    Args:
        text (str): The input text for keyword extraction.

    Returns:
        list[str]: A list of extracted keywords (title-cased).
    """
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), top_n=3)
    return [kw[0].title() for kw in keywords]


# Hindi Speech Generation
# def generate_hindi_speech(text):
#     """
#     Converts the given text into Hindi speech.

#     Args:
#         text (str): The input text to be translated and converted to speech.

#     Returns:
#         io.BytesIO: A buffer containing the generated speech audio.
#     """
#     # Translate text to Hindi
#     hindi_text = GoogleTranslator(source="auto", target="hi").translate(text)

#     # Convert translated text to speech
#     tts = gTTS(hindi_text, lang="hi")

#     # Store the generated speech in memory
#     audio_buffer = io.BytesIO()
#     tts.write_to_fp(audio_buffer)
#     audio_buffer.seek(0)  # Reset buffer position for playback

#     return audio_buffer

# Load Coqui multilingual model only once
tts_model = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False)

def generate_hindi_speech(text):
    # Translate text to Hindi
    hindi_text = GoogleTranslator(source="auto", target="hi").translate(text)

    # Generate speech as numpy waveform and sample rate
    wav, sr = tts_model.tts(hindi_text, speaker="hin", language="hi", return_type="np")

    # Save WAV to an in-memory buffer
    audio_buffer = io.BytesIO()
    sf.write(audio_buffer, wav, sr, format='WAV')
    audio_buffer.seek(0)  # Reset buffer position

    return audio_buffer
