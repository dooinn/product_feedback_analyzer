import streamlit as st
import pandas as pd
from apify_client import ApifyClient

@st.cache_data(show_spinner=False)
def scrape_comments(video_url, apify_token):
    """Scrape YouTube comments using Apify API (handles nested JSON)."""
    st.info("Scraping comments from YouTube using Apify API...")

    try:
        client = ApifyClient(apify_token)
        run_input = {
            "urlOrVideoId": video_url,
            "max_comments": 100,
            "sort_by": "top",
            "language": "en",
        }

        run = client.actor("X8vJSXp6FaneeNClD").call(run_input=run_input)
        items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

        if not items:
            st.warning("No comments found in Apify response.")
            return pd.DataFrame(columns=["comment"])

        comments = items[0].get("comments", items)
        df = pd.DataFrame(comments)

        text_col = next((c for c in ["text", "comment", "content", "body"] if c in df.columns), None)
        if not text_col:
            st.error("No text/comment/content/body field found in API data.")
            return pd.DataFrame(columns=["comment"])

        df = df.rename(columns={text_col: "comment"})[["comment"]]
        st.success(f"✅ Retrieved {len(df)} comments successfully!")
        return df

    except Exception as e:
        st.error(f"❌ Error while scraping: {e}")
        return pd.DataFrame(columns=["comment"])


@st.cache_data(show_spinner=False)
def load_comments_from_csv(uploaded_file):
    """Load user-uploaded CSV with a 'comment' column."""
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = [c.lower().strip() for c in df.columns]
        text_col = next((c for c in ["comment", "text", "content", "body"] if c in df.columns), None)
        if not text_col:
            st.error("❌ Uploaded CSV must have a 'comment' or 'text' column.")
            return pd.DataFrame(columns=["comment"])
        df = df.rename(columns={text_col: "comment"})[["comment"]]
        st.success(f"✅ Loaded {len(df)} comments from CSV successfully!")
        return df
    except Exception as e:
        st.error(f"❌ Error reading CSV file: {e}")
        return pd.DataFrame(columns=["comment"])
