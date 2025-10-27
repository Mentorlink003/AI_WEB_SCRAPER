import streamlit as st
import matplotlib.pyplot as plt
from scrape import scrape_website, extract_body_content, clean_body_content, split_dom_content
from parse import parse_with_ollama
from sentiment import generate_sentiment_report, plot_sentiment_chart, generate_wordcloud

st.set_page_config(page_title="AI Web Scraper & Sentiment Monitor", layout="wide")
st.title("🌐 AI Web Scraper & Sentiment & Brand Reputation Monitor")

# Sidebar for mode selection
mode = st.sidebar.radio(
    "Choose Mode:",
    ["Content Extraction", "Sentiment & Brand Reputation Monitor"]
)

url = st.text_input("Enter Website URL:")

if st.button("Scrape Site"):
    if not url:
        st.warning("⚠️ Please enter a valid website URL.")
    else:
        st.write("🔍 Scraping website... Please wait.")
        html = scrape_website(url)
        body = extract_body_content(html)
        cleaned = clean_body_content(body)
        st.session_state["dom_content"] = cleaned
        st.success("✅ Website scraped successfully!")

        with st.expander("View Cleaned Content"):
            st.text_area("Cleaned HTML Content", cleaned, height=300)

# ---- MODE 1: CONTENT EXTRACTION ----
if "dom_content" in st.session_state and mode == "Content Extraction":
    st.subheader("📄 LLM-based Content Extraction")

    parse_description = st.text_area(
        "Enter a description or prompt for extraction (e.g., 'Extract all financial data or company names'):"
    )

    if st.button("Parse Content"):
        if not parse_description.strip():
            st.warning("⚠️ Please enter a description for extraction.")
        else:
            st.write("🧠 Parsing content using Ollama model...")
            dom_chunks = split_dom_content(st.session_state["dom_content"])
            result = parse_with_ollama(dom_chunks, parse_description)
            st.subheader("✅ Extracted Results")
            st.write(result)

# ---- MODE 2: SENTIMENT ANALYSIS ----
elif "dom_content" in st.session_state and mode == "Sentiment & Brand Reputation Monitor":
    st.subheader("💬 Sentiment & Brand Reputation Analysis")

    if st.button("Analyze Sentiment"):
        st.write("🧠 Performing sentiment analysis...")
        results, sentiments, all_text = generate_sentiment_report(st.session_state["dom_content"])

        # Sentiment Distribution Chart
        st.subheader("📊 Sentiment Distribution")
        st.pyplot(plot_sentiment_chart(sentiments))

        # Word Cloud of Mentions
        st.subheader("☁️ Word Cloud of Top Mentions")
        wordcloud = generate_wordcloud(all_text)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

        # Detailed sentiment results
        st.subheader("🧾 Detailed Sentiment Report")
        for r in results:
            color = "🟢" if r["sentiment"] == "Positive" else "🔴" if r["sentiment"] == "Negative" else "⚪"
            st.markdown(f"{color} **{r['sentiment']} ({r['score']:.2f})** → {r['text'][:250]}...")

else:
    st.info("👆 Please enter a URL above and scrape the content first.")
