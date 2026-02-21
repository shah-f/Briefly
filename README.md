# Briefly

Briefly is a modern, AI-powered news aggregator that transforms top news stories into concise audio podcasts. Choose your preferred news category, and Briefly will fetch, summarize, and generate a high-quality audio summary for you to listen to.

## Features

- **Personalized News:** Select from categories like Technology, Business, Science, Health, and more.
- **AI Summarization:** Uses advanced language models (via OpenRouter) to condense articles into focused summaries.
- **Text-to-Speech:** Generates natural-sounding audio summaries using Google's Gemini TTS.
- **Instant Access:** Audio is generated on-the-fly and served directly in your browser.

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML5, CSS3 (Frosted Glass UI, Custom Animations)
- **APIs:**
  - [NewsData.io](https://newsdata.io/) for fetching the latest news.
  - [OpenRouter](https://openrouter.ai/) (GPT-4o mini) for text summarization.
  - [Google Gemini API](https://ai.google.dev/) for high-quality text-to-speech.
- **Content Extraction:** [Trafilatura](https://trafilatura.readthedocs.io/) for clean web scraping.

## Getting Started

### Prerequisites

- Python 3.8+
- API keys for NewsData.io, OpenRouter, and Google Gemini.

### Running the App

1. Start the Flask server:
   ```bash
   python news.py
   ```
2. Open your browser and navigate to `http://127.0.0.1:5000`.

## Usage

1. Select a news category from the dropdown.
2. Click the arrow button.
3. Wait for the progress bar to complete.
4. Click play on the generated audio player to hear your news summary!
