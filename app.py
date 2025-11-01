import streamlit as st
import pandas as pd
from utils.config import APIFY_API_KEY
from utils.model_utils import load_models
from utils.scraping_utils import scrape_comments, load_comments_from_csv
from utils.analysis_utils import analyze_comments
from utils.dashboard_utils import show_dashboard

st.set_page_config(page_title="YouTube Comment Analyzer", layout="wide")

st.title("🎥 YouTube Comment Analyzer Dashboard")

# About section
st.markdown("""
### 💡 About this App

**"Get unfiltered customer opinions on your product — instantly."**

This tool helps you explore and understand authentic customer feedback gathered from social media.
It analyzes both the **sentiment** (positive/negative) and the **specific product features** customers talk about.



**🔍 Current Capabilities**
- The classifier currently supports **smartphone-related comments**, identifying mentions of: `Price`, `Performance`, `Battery`, `Camera`, `Design`.
- The sentiment analysis model detects **positive** and **negative** tone in comments.
- Only CSV uploads are supported. The file must contain **a single column** named `comment`, `content`, or `text`.



**⚠️ Disclaimer**
- The **automatic scraping function** currently works only for **YouTube** videos and requires a [paid Apify account](https://console.apify.com).
- Only **smartphone review videos** are supported for accurate categorization.


""")

category_classifier, sentiment_analyzer = load_models()
st.success("✅ Models loaded successfully!")

# Input source
st.markdown("### 🧭 Choose Input Source")
input_mode = st.radio(
    "Select how you want to provide comments:",
    ("Scrape from YouTube (via Apify)", "Upload CSV file"),
    horizontal=True
)

comments_df = pd.DataFrame()

if input_mode == "Scrape from YouTube (via Apify)":
    with st.form("youtube_form"):
        video_url = st.text_input("Enter YouTube Video URL:")
        submitted = st.form_submit_button("Analyze")

    if submitted and video_url:
        if not APIFY_API_KEY:
            st.error("❌ Apify API key not found in .env")
        else:
            comments_df = scrape_comments(video_url, APIFY_API_KEY)

elif input_mode == "Upload CSV file":
    uploaded_file = st.file_uploader("📤 Upload CSV with comment text", type=["csv"])
    if uploaded_file:
        comments_df = load_comments_from_csv(uploaded_file)

# Analysis and dashboard
if not comments_df.empty:
    analyzed_df = analyze_comments(comments_df, category_classifier, sentiment_analyzer)
    show_dashboard(analyzed_df)
else:
    st.info("Please upload a CSV or enter a YouTube URL to begin.")


