import pickle
import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_models():
    with open("final_model/final_model.pkl", "rb") as f:
        model_bundle = pickle.load(f)

    category_classifier = pipeline(
        "text-classification",
        model=model_bundle["model"],
        tokenizer=model_bundle["tokenizer"]
    )

    sentiment_analyzer = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )

    return category_classifier, sentiment_analyzer
