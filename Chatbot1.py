import os
import streamlit as st
from deep_translator import GoogleTranslator
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Gemini Model
model = genai.GenerativeModel("gemini-1.5-pro")

# Translation functions
def translate_to_english(text, lang_code):
    return GoogleTranslator(source=lang_code, target='en').translate(text)

def translate_from_english(text, target_lang):
    return GoogleTranslator(source='en', target=target_lang).translate(text)

# Gemini query function
def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="Multilingual Restaurant Chatbot 🍽️", layout="centered")
st.title("🍽️ Multilingual Restaurant Chatbot")
st.markdown("Ask anything about our restaurant in your preferred language!")

# Language dropdown
language_map = {
    "English": "en",
    "Urdu": "ur",
    "Hindi": "hi",
    "Arabic": "ar",
    "French": "fr"
}

lang_display = st.selectbox("Select your language:", list(language_map.keys()))
lang_code = language_map[lang_display]

# User input
user_input = st.text_input("Ask your question:")

if st.button("Ask Gemini"):
    if not user_input.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking... 💭"):
            # Translate to English
            user_input_en = translate_to_english(user_input, lang_code)

            # Get response from Gemini
            prompt = f"You are a restaurant assistant. Answer politely and helpfully: {user_input_en}"
            response_en = ask_gemini(prompt)

            # Translate back to original language
            final_response = translate_from_english(response_en, lang_code)

            # Show response
            st.success("Gemini's Response:")
            st.markdown(f"**🗨️ {final_response}**")

def rule_based_response(user_input):
    if "timing" in user_input.lower():
        return "Hamare restaurant ke timings hain 12pm se 11pm tak."
    elif "location" in user_input.lower():
        return "Hamara restaurant Gulshan-e-Iqbal, Karachi mein hai."
    else:
        return None
try:
    response = model.generate_content(prompt)
except Exception as e:
    response = rule_based_response(user_input)
    if not response:
        response = "Maaf kijiye, abhi response nahi mil sakta. Thodi dair baad koshish karein."
