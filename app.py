import streamlit as st
import json
import difflib
import numpy as np
import os
import language_tool_python  # Grammar check library
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image

# Set page config
st.set_page_config(page_title="Fake Document Prediction", layout="wide")

# Load LanguageTool for grammar checking
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
            data = json.load(file)
            if isinstance(data, dict):
                return data
            else:
                st.error("❌ Invalid JSON format in users_db.json")
                return {}
    except FileNotFoundError:
        st.error("❌ users_db.json file not found!")
        return {}
    except json.JSONDecodeError:
        st.error("❌ Error decoding users_db.json!")
        return {}

# Check if user exists in database (case-insensitive)
def check_user_in_db(username, db):
    return username.strip().lower() in [name.lower() for name in db.values()]

# Preprocess uploaded image
def preprocess_image(uploaded_file):
    img = Image.open(uploaded_file).convert("RGB")
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0  # Normalize
    img_array = img_array.reshape(1, 224, 224, 3)
    return img_array, img

# Predict signature authenticity
def predict_signature(img_array):
    label = signature_model.predict(img_array)
    return ['forged', 'genuine'][np.argmax(label)]

# Predict font authenticity
def predict_font(img_array):
    label = font_model.predict(img_array)
    return ['fake', 'real'][np.argmax(label)]

# Check grammar in document
def check_grammar(text):
    matches = tool.check(text)
    return len(matches)

# Load database
db = load_json_db()

# Streamlit UI
st.title("📄 Fake Document Prediction")
st.markdown("---")

# User verification
st.subheader("🔍 User Verification")
username = st.text_input("👤 Enter Username", placeholder="Enter your username here...")
user_exists = check_user_in_db(username, db)

if username:
    st.success("✅ User found in database") if user_exists else st.error("❌ User not found in database")

st.markdown("---")

# Document Upload Section
st.subheader("📑 Document Features")
signature = st.file_uploader("✍️ Upload Signature (Image)", type=["png", "jpg", "jpeg"])
gsm = st.number_input("📜 GSM of Paper", min_value=50, max_value=500, step=5)
font_image = st.file_uploader("🔤 Upload Font Sample (Image)", type=["png", "jpg", "jpeg"])
document_text = st.text_area("📝 Paste Document Text for Grammar Check", placeholder="Enter document text here...")

if st.button("🔎 Predict Fake Document"):
    if not username or not user_exists:
        st.error("❌ Please enter a valid username found in the database")
    elif gsm < 80:
        st.error("❌ Duplicate Bond Paper detected! Exiting prediction.")
    elif not signature:
        st.error("❌ Please upload a signature image")
    elif not font_image:
        st.error("❌ Please upload a font sample image")
    elif not document_text:
        st.error("❌ Please enter document text")
    else:
        # Process and predict signature authenticity
        sig_array, sig_display = preprocess_image(signature)
        sig_prediction = predict_signature(sig_array)

        # Process and predict font authenticity
        font_array, font_display = preprocess_image(font_image)
        font_prediction = predict_font(font_array)

        # Check grammar mistakes
        grammar_mistakes = check_grammar(document_text)
        grammar_status = "Fake" if grammar_mistakes > 0 else "Real"

        # Display results
        st.image(sig_display, caption="Uploaded Signature", use_column_width=True)
        st.success(f"✅ Signature Prediction: **{sig_prediction}**")

        st.image(font_display, caption="Uploaded Font Sample", use_column_width=True)
        st.success(f"✅ Font Prediction: **{font_prediction}**")

        st.info(f"📄 Grammar Mistakes Found: **{grammar_mistakes}**")
        if grammar_status == "Fake":
            st.error("❌ Fake Document Detected due to grammar mistakes!")
        else:
            st.success("✅ No grammar mistakes! Document seems real.")
