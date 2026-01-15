import os
import io
import struct
import wave
import base64
import uuid
import requests
import json
from flask import Flask, request, jsonify, render_template, session, url_for, redirect
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
import trafilatura

_ = load_dotenv(find_dotenv())

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
CORS(app)

def summarize(text):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        },
        json={
            "model": "openai/gpt-5-mini",
            "messages": [
                {
                    "role": "user",
                    "content": "You are responsible for summarizing this news article so it can be converted to a concise summary to be included in a daily news audio podcast. Make sure to make it 40 seconds or less.\n\n" + text
                }
            ],
        }
    )
    data = response.json()
    return data["choices"][0]["message"]["content"]

def text_to_speech(text, filename):
    """Convert text to speech using Gemini TTS and save as WAV."""
    # Truncate to ~4000 chars to stay within TTS limits
    if len(text) > 4000:
        text = text[:4000]
    response = requests.post(
        url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key={os.getenv('GEMINI_API_KEY')}",
        headers={"Content-Type": "application/json"},
        json={
            "contents": [{
                "parts": [{"text": text}]
            }],
            "generationConfig": {
                "responseModalities": ["AUDIO"],
                "speechConfig": {
                    "voiceConfig": {
                        "prebuiltVoiceConfig": {
                            "voiceName": "Kore"
                        }
                    }
                }
            }
        }
    )
    data = response.json()
    if "candidates" not in data:
        print(f"TTS API error: {data}")
        return None
    audio_data = data["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
    raw_audio = base64.b64decode(audio_data)

    # Wrap raw PCM in a proper WAV file (Gemini returns 24kHz 16-bit mono PCM)
    filepath = os.path.join(app.static_folder, "audio", filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with wave.open(filepath, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframes(raw_audio)
    return filename

@app.route("/", methods=["GET", "POST"])
def index():
    audio_file = None
    category = None
    if request.method == "POST":
        category = request.form.get("category")
        url = f"https://newsdata.io/api/1/latest?apikey={os.getenv('NEWS_API_KEY')}&category={category}&language=en&removeduplicate=1"
        response = requests.get(url)
        articles = response.json().get('results', [])
        summaries = []
        for art in articles:
            if len(summaries) >= 3:
                break
            downloaded = trafilatura.fetch_url(art['link'])
            if not downloaded:
                continue
            content = trafilatura.extract(downloaded, output_format="markdown")
            if content:
                summaries.append(summarize(content))
        if summaries:
            combined = "\n\n".join(f"Article {i+1}. {s}" for i, s in enumerate(summaries))
            result = text_to_speech(combined, f"{uuid.uuid4().hex}.wav")
            if result:
                audio_file = result
    return render_template("index.html", audio_file=audio_file, category=category)





if __name__ == '__main__':
    app.run(debug=True)