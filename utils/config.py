import os
from dotenv import load_dotenv

load_dotenv()
APIFY_API_KEY = os.getenv("APIFY_API_KEY")

CATEGORY_MAP = {
    0: "battery",
    1: "camera",
    2: "design",
    3: "others",
    4: "performance",
    5: "price",
}

def decode_category(label):
    """Convert numeric or LABEL_X into readable category name."""
    if isinstance(label, str) and label.upper().startswith("LABEL_"):
        try:
            idx = int(label.split("_")[1])
            return CATEGORY_MAP.get(idx, "unknown")
        except:
            return "unknown"
    elif isinstance(label, (int, float)):
        return CATEGORY_MAP.get(int(label), "unknown")
    return label
