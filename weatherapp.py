from fastapi import FastAPI, HTTPException
import requests
from transformers import pipeline

app = FastAPI()

# Replace with your actual NewsAPI key
NEWS_API_KEY = "YOUR_NEWSAPI_KEY"

# Initialize summarization pipeline (this downloads the model on first run)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@app.get("/summarize-news")
def summarize_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&pageSize=5&apiKey={NEWS_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch news")

    articles = response.json().get("articles", [])
    summarized_articles = []

    for article in articles:
        title = article.get("title")
        description = article.get("description") or ""
        content = article.get("content") or ""

        # Use description or content as input for summarization
        text_to_summarize = description if description else content

        if not text_to_summarize.strip():
            summary = "No summary available"
        else:
            # Hugging Face summarizer has a max token limit, truncate if necessary
            text_to_summarize = text_to_summarize[:1000]
            summary_result = summarizer(text_to_summarize, max_length=60, min_length=25, do_sample=False)
            summary = summary_result[0]['summary_text']

        summarized_articles.append({
            "title": title,
            "summary": summary,
            "url": article.get("url")
        })

    return {"articles": summarized_articles}
