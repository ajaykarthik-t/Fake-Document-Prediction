import streamlit as st
import json
import difflib

def load_json_db():
    with open("users_db.json", "r") as file:
        return json.load(file)

def check_user_in_db(username, db):
    return username in db

def spell_checker(text, dictionary):
    words = text.split()
    corrected_words = [difflib.get_close_matches(word, dictionary, n=1, cutoff=0.8)[0] if difflib.get_close_matches(word, dictionary, n=1, cutoff=0.8) else word for word in words]
    return " ".join(corrected_words)

db = load_json_db()

st.set_page_config(page_title="Fake Document Prediction", layout="wide")
st.markdown("""
    <style>
    .main {
        background-color: #f4f4f4;
    }
    .stTextInput, .stNumberInput, .stSelectbox, .stTextArea, .stFileUploader {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📄 Fake Document Prediction")
st.markdown("---")

st.subheader("🔍 User Verification")
username = st.text_input("👤 Enter Username", placeholder="Enter your username here...")
user_exists = check_user_in_db(username, db)
if username and user_exists:
    st.success("✅ User found in database")
elif username:
    st.error("❌ User not found in database")

st.markdown("---")

st.subheader("📑 Document Features")
signature = st.file_uploader("✍️ Upload Signature (Image/PDF)", type=["png", "jpg", "jpeg", "pdf"])

gsm = st.number_input("📜 GSM of Paper", min_value=50, max_value=500, step=5)
font_image = st.file_uploader("🔤 Upload Font Sample (Image)", type=["png", "jpg", "jpeg"])

document_text = st.text_area("📝 Paste Document Text for Spell Check", placeholder="Enter document text here...")
if st.button("🛠️ Check Spelling"):
    corrected_text = spell_checker(document_text, ["example", "document", "text", "words", "correction", "sample"])
    st.text_area("✅ Corrected Text", corrected_text, height=200)

st.markdown("---")

if st.button("🔎 Predict Fake Document"):
    if not username or not user_exists:
        st.error("❌ Please enter a valid username found in the database")
    elif not signature:
        st.error("❌ Please upload a signature")
    elif not font_image:
        st.error("❌ Please upload a font sample image")
    elif not document_text:
        st.error("❌ Please enter document text")
    else:
        st.success("✅ Document Verified! Further Analysis Required.")
