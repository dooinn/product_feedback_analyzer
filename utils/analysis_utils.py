import streamlit as st
from utils.config import decode_category

def analyze_comments(df, category_classifier, sentiment_analyzer):
    st.info("Analyzing comments... This may take a few minutes ⏳")

    df = df.copy()
    df.dropna(subset=["comment"], inplace=True)
    comments = df["comment"].astype(str).tolist()

    cat_results = category_classifier(comments, truncation=True, max_length=512, batch_size=8)
    sent_results = sentiment_analyzer(comments, truncation=True, max_length=512, batch_size=8)

    df["Category"] = [decode_category(r["label"]) for r in cat_results]
    df["Category_Confidence"] = [r["score"] for r in cat_results]
    df["Sentiment"] = [r["label"] for r in sent_results]
    df["Sentiment_Confidence"] = [r["score"] for r in sent_results]

    return df
