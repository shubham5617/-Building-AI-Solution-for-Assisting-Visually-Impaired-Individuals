import streamlit as st
from PIL import Image
import pytesseract
import pyttsx3
import os
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  

# Initialize Google Generative AI with API Key
genai.configure(api_key="gemini-api-key")

model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# Set up Streamlit page
st.set_page_config(page_title="VisionAid", layout="wide")
st.title("Building AI Powered Solution for Assisting Visually Impaired Individuals")
st.sidebar.title("🔧 Available Features")
st.sidebar.markdown("""
- Scene Interpretation
- Speech Conversion
- Object & Obstacle Recognition
""")

def extract_text_from_image(image):
    """Extracts text from the given image using OCR."""
    text = pytesseract.image_to_string(image)
    return text

def text_to_speech(text):
    """Converts the given text to speech."""
    engine.say(text)
    engine.runAndWait()

def generate_scene_description(input_prompt, image_data):
    """Generates a scene description using Google Generative AI."""
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([input_prompt, image_data[0]])
    return response.text

def input_image_setup(uploaded_file):
    """Prepares the uploaded image for processing."""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded.")

# Main app functionality
uploaded_file = st.file_uploader("📤 Upload an image...", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Buttons for functionalities
col1, col2, col3 = st.columns(3)
scene_button = col1.button("🔍 Describe Scene")
ocr_button = col2.button("📝 Extract Text")
tts_button = col3.button("🔊 Text-to-Speech")

# Input Prompt for AI Scene Understanding
input_prompt = """
You are an AI assistant helping visually impaired individuals by describing the scene in the image. Provide:
1. List of items detected in the image with their purpose.
2. Overall description of the image.
3. Suggestions for actions or precautions for the visually impaired.
"""

# Process based on user interaction
if uploaded_file:
    image_data = input_image_setup(uploaded_file)

    if scene_button:
        with st.spinner("Generating scene description..."):
            response = generate_scene_description(input_prompt, image_data)
            st.subheader("Scene Description")
            st.write(response)

    if ocr_button:
        with st.spinner("Extracting text from image..."):
            text = extract_text_from_image(image)
            st.subheader("Extracted Text")
            st.write(text)

    if tts_button:
        with st.spinner("Converting text to speech..."):
            text = extract_text_from_image(image)
            if text.strip():
                text_to_speech(text)
                st.success("Text-to-Speech Conversion Completed!")
            else:
                st.warning("No text found in the image.")
