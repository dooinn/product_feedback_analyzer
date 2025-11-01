import streamlit as st
import pandas as pd
from utils.model_utils import load_models
from utils.scraping_utils import scrape_comments, load_comments_from_csv
from utils.analysis_utils import analyze_comments
from utils.dashboard_utils import show_dashboard
from utils.config import APIFY_API_KEY

# ---------- CONFIG ----------
st.set_page_config(page_title="Product Feedback Analyzer", layout="wide")
st.title("🎥 Product Feedback Analyzer")

# ---------- ABOUT ----------
st.markdown("""
### 💡 About this App

**"Get unfiltered customer opinions on your product — instantly."**

This tool helps you explore and understand authentic customer feedback gathered from social media.
It analyzes both the **sentiment** (positive/negative) and the **specific product features** customers talk about.

**🔍 Current Capabilities**
- Supports smartphone-related comments (`Price`, `Performance`, `Battery`, `Camera`, `Design`).
- Detects positive and negative sentiment in comments.
- Accepts CSV uploads or YouTube video URLs.

**⚠️ Disclaimer**
- The **scraping** feature requires a [paid Apify account](https://console.apify.com).
- Works best for smartphone review videos.
""")

# ---------- LOAD MODELS ----------
category_classifier, sentiment_analyzer = load_models()
st.success("✅ Models loaded successfully!")

# ---------- INPUT SOURCE ----------
st.markdown("### 🧭 Choose Input Source")
input_mode = st.radio(
    "Select how you want to provide comments:",
    ("Scrape from YouTube (via Apify)", "Upload CSV file"),
    horizontal=True
)

comments_df = pd.DataFrame()

# ---------- SCRAPE FROM YOUTUBE ----------
if input_mode == "Scrape from YouTube (via Apify)":
    st.markdown("#### 🔑 Enter Your Apify API Key")
    user_apify_key = st.text_input("Apify API Key", type="password", help="Enter your Apify API key here.")

    with st.form("youtube_form"):
        video_url = st.text_input("Enter YouTube Video URL:")
        submitted = st.form_submit_button("Analyze")

    if submitted:
        if not user_apify_key:
            st.error("❌ Please enter your Apify API key.")
        elif not video_url:
            st.error("❌ Please enter a YouTube video URL.")
        else:
            comments_df = scrape_comments(video_url, user_apify_key)

# ---------- UPLOAD CSV ----------
elif input_mode == "Upload CSV file":
    uploaded_file = st.file_uploader("📤 Upload CSV with comment text", type=["csv"])
    if uploaded_file:
        comments_df = load_comments_from_csv(uploaded_file)

# ---------- ANALYZE & SHOW DASHBOARD ----------
if not comments_df.empty:
    analyzed_df = analyze_comments(comments_df, category_classifier, sentiment_analyzer)
    show_dashboard(analyzed_df)
else:
    st.info("Please upload a CSV or enter a YouTube URL to begin.")
