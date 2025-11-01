import os
import pickle
import streamlit as st
import gdown
from transformers import pipeline


MODEL_FILE_ID = "1jbOh9eZISQo73MxBkX72EiNhzNWoL5Or"  

@st.cache_resource
def load_models():
    """Load category classifier and sentiment analyzer, downloading the model if needed."""
    model_dir = "final_model"
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "final_model.pkl")

    if not os.path.exists(model_path):
        st.info("📥 Downloading model from Google Drive (first-time setup)...")
        url = f"https://drive.google.com/uc?id={MODEL_FILE_ID}"
        try:
            gdown.download(url, model_path, quiet=False)
            st.success("✅ Model downloaded successfully!")
        except Exception as e:
            st.error(f"❌ Failed to download model from Google Drive: {e}")
            raise e

    try:
        with open(model_path, "rb") as f:
            model_bundle = pickle.load(f)
    except Exception as e:
        st.error(f"❌ Error loading model file: {e}")
        raise e

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
