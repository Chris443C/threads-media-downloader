import os
import cv2
import numpy as np
import requests
import pytesseract
import nltk
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import BlipProcessor, BlipForConditionalGeneration
from tensorflow.keras.models import load_model

# Load AI Models
MODEL_PATH = "nsfw_model.h5"
if os.path.exists(MODEL_PATH):
    nsfw_model = load_model(MODEL_PATH)

blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

nltk.download("vader_lexicon")
nltk.download("punkt")
sia = SentimentIntensityAnalyzer()

# Preprocess Image for AI Model
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))  
    img = np.expand_dims(img, axis=0) / 255.0  
    return img

# AI-Based Caption Generation
def generate_caption(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    inputs = blip_processor(image, return_tensors="pt")
    output = blip_model.generate(**inputs)
    caption = blip_processor.decode(output[0], skip_special_tokens=True)
    return caption

# Extract Text from Image (OCR)
def extract_text(image_path):
    return pytesseract.image_to_string(image_path)

# Perform Sentiment Analysis
def analyze_sentiment(text):
    return sia.polarity_scores(text)

# Detect NSFW Content
def is_nsfw(image_path):
    image = preprocess_image(image_path)
    prediction = nsfw_model.predict(image)[0]
    return prediction[0] > 0.7  

# Download & Analyze Media
def download_file(url, output_folder):
    filename = os.path.join(output_folder, url.split("?")[0].split("/")[-1])
    response = requests.get(url, stream=True)
    
    with open(filename, "wb") as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)

    caption = generate_caption(filename)
    extracted_text = extract_text(filename)
    sentiment = analyze_sentiment(extracted_text)

    nsfw_tag = "_NSFW" if is_nsfw(filename) else ""
    new_filename = filename.replace(".", f"{nsfw_tag}.")
    os.rename(filename, new_filename)

    print(f"📜 Caption: {caption}")
    print(f"🔍 Extracted Text: {extracted_text}")
    print(f"📊 Sentiment Analysis: {sentiment}")
