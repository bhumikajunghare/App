import gradio as gr
from gtts import gTTS
import requests
from textblob import TextBlob
from deep_translator import GoogleTranslator
import os

NEWS_API_URL = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "a2c8427597a64a0fafd9a61c4230e1d4"

def fetch_news(company_name):
    params = {
        "q": company_name,
        "apiKey": NEWS_API_KEY,
        "pageSize": 3,
        "language": "en"
    }
    # Sending get rquest to news api 
    response = requests.get(NEWS_API_URL, params=params)

    # if request successful
    if response.status_code == 200:
      
      # returing the list of news articles from the API response
        return response.json().get("articles", [])
    else:
        return []

  def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

    def translate_to_hindi(text):
    try:
        return GoogleTranslator(source="auto", target="hi").translate(text)
    except Exception as e:
        return f"Translation failed: {str(e)}"

    def text_to_speech(text):
    tts = gTTS(text=text, lang="hi", slow=False)
    audio_path = "output.mp3"
    tts.save(audio_path)
    return audio_path

def process_news(company_name):
    articles = fetch_news(company_name)
    results = []
    
    # Extracting the description of the article, analyzing sentiments, translating content and converting translation into Hindi
    for article in articles:
        content = article.get("description", "")
        sentiment = analyze_sentiment(content)
        hindi_text = translate_to_hindi(content)
        audio = text_to_speech(hindi_text)
        results.append((content, sentiment, hindi_text, audio))
    return results

