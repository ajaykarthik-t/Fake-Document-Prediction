import streamlit as st
import json
import numpy as np
import os
import language_tool_python  # Grammar check
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image

# Set page config
st.set_page_config(page_title="Fake Document Prediction", layout="wide")

# Load LanguageTool
tool = language_tool_python.LanguageTool('en-US')

# Define model paths
SIGNATURE_MODEL_PATH = r"C:\Users\Ajay\Desktop\Fake-Document-Prediction\signature\my_model.keras"
FONT_MODEL_PATH = r"C:\Users\Ajay\Desktop\Fake-Document-Prediction\Font\my_model.keras"


# Load models
@st.cache_resource
def load_models():
    if os.path.exists(SIGNATURE_MODEL_PATH) and os.path.exists(FONT_MODEL_PATH):
        signature_model = load_model(SIGNATURE_MODEL_PATH)
        font_model = load_model(FONT_MODEL_PATH)
        return signature_model, font_model
    else:
        st.error("❌ Model files not found! Check the paths.")
        return None, None

signature_model, font_model = load_models()

# Load user database
def load_json_db():
    try:
        with open("users_db.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        st.error("❌ users_db.json file error!")
        return {}

db = load_json_db()

def check_user(username):
    return username.strip().lower() in [name.lower() for name in db.values()]

# Preprocess image
def preprocess_image(uploaded_file):
    img = Image.open(uploaded_file).convert("RGB").resize((224, 224))
    img_array = np.array(img) / 255.0  # Normalize
    return img_array.reshape(1, 224, 224, 3), img

def predict_signature(img_array):
    return ['forged', 'genuine'][np.argmax(signature_model.predict(img_array))]

def predict_font(img_array):
    return ['fake', 'real'][np.argmax(font_model.predict(img_array))]

def check_grammar(text):
    return len(tool.check(text))

# Streamlit UI
st.title("📄 Fake Document Prediction")
st.markdown("---")

# 1️⃣ Manual User Verification
st.subheader("👤 User Verification")
username = st.text_input("Enter Username")
if username:
    user_exists = check_user(username)
    st.success("✅ User found") if user_exists else st.error("❌ User not found")

st.markdown("---")

# 2️⃣ Automated Document Verification
st.subheader("🤖 Automated Document Verification")
options = st.multiselect("Select what to check:", ["Signature", "Font", "Grammar"])

signature = None
font_image = None
document_text = ""

if "Signature" in options:
    signature = st.file_uploader("✍️ Upload Signature", type=["png", "jpg", "jpeg"])
if "Font" in options:
    font_image = st.file_uploader("🔤 Upload Font Sample", type=["png", "jpg", "jpeg"])
if "Grammar" in options:
    document_text = st.text_area("📝 Paste Document Text for Grammar Check")

if st.button("🔎 Predict Fake Document"):
    if not username or not user_exists:
        st.error("❌ Invalid username")
    else:
        if "Signature" in options and signature:
            sig_array, sig_display = preprocess_image(signature)
            sig_prediction = predict_signature(sig_array)
            st.image(sig_display, caption="Uploaded Signature", use_column_width=True)
            st.success(f"✅ Signature: **{sig_prediction}**")
        elif "Signature" in options:
            st.error("❌ Upload a signature image")

        if "Font" in options and font_image:
            font_array, font_display = preprocess_image(font_image)
            font_prediction = predict_font(font_array)
            st.image(font_display, caption="Uploaded Font Sample", use_column_width=True)
            st.success(f"✅ Font: **{font_prediction}**")
        elif "Font" in options:
            st.error("❌ Upload a font sample image")

        if "Grammar" in options and document_text:
            grammar_mistakes = check_grammar(document_text)
            grammar_status = "Fake" if grammar_mistakes > 0 else "Real"
            st.info(f"📄 Grammar Mistakes: **{grammar_mistakes}**")
            if grammar_status == "Fake":
                st.error("❌ Fake Document Detected!")
            else:
                st.success("✅ Document is Real")
        elif "Grammar" in options:
            st.error("❌ Enter document text")
