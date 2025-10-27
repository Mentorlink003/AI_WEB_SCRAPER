from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re

def analyze_sentiment(text):
    """Return sentiment label and polarity score for a text chunk."""
    blob = TextBlob(text)
    score = blob.sentiment.polarity
    if score > 0.1:
        sentiment = "Positive"
    elif score < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    return sentiment, score

def generate_sentiment_report(cleaned_content):
    """Analyze sentiment for each paragraph and return aggregated results."""
    paragraphs = [p for p in cleaned_content.split("\n") if len(p.strip()) > 40]
    sentiments = {"Positive": 0, "Neutral": 0, "Negative": 0}
    results = []
    all_text = ""

    for para in paragraphs:
        sentiment, score = analyze_sentiment(para)
        sentiments[sentiment] += 1
        results.append({
            "text": para,
            "sentiment": sentiment,
            "score": score
        })
        all_text += " " + para

    return results, sentiments, all_text

def plot_sentiment_chart(sentiments):
    """Generate a sentiment bar chart."""
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(sentiments.keys(), sentiments.values(), color=["green", "gray", "red"])
    ax.set_title("Overall Sentiment Distribution")
    ax.set_ylabel("Count")
    ax.set_xlabel("Sentiment Type")
    return fig

def generate_wordcloud(text):
    """Create a word cloud image from text frequency."""
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text)
    freq = Counter(words)
    wordcloud = WordCloud(
        width=800, height=400, background_color="white"
    ).generate_from_frequencies(freq)
    return wordcloud
