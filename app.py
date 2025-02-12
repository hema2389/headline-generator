# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1552DTY9kcfjqqFrTaY_GGjZz3qal-Z1c
"""

import streamlit as st
from transformers import BartTokenizer, BartForConditionalGeneration
import torch

# Replace this with your model link or path
model_path = "https://drive.google.com/drive/folders/12ERv3Tl22Ukici91HH0Lp5qw8y-yL_bI?usp=drive_link"
tokenizer = BartTokenizer.from_pretrained(model_path)
model = BartForConditionalGeneration.from_pretrained(model_path)

# Download and unzip the model
gdown.download(model_url, output_path, quiet=False)
!unzip headline-generator.zip -d headline-generator/

# Title
st.title("Headline Generator")

# Sidebar for Model Selection
use_gpu = torch.cuda.is_available()
'''
# Load Model and Tokenizer
model_name = "facebook/bart-base"
tokenizer = BartTokenizer.from_pretrained("headline_generator_model")
model = BartForConditionalGeneration.from_pretrained("headline_generator_model")
'''
device = torch.device("cuda" if use_gpu else "cpu")
model.to(device)

# Input Text
article_input = st.text_area("Enter the News Article:")

# Generate Headline Button
if st.button("Generate Headline"):
    if article_input:
        # Tokenize input
        inputs = tokenizer("generate headline: " + article_input, return_tensors="pt", truncation=True, padding="max_length", max_length=512)
        inputs = {key: val.to(device) for key, val in inputs.items()}

        # Generate headline
        outputs = model.generate(**inputs, max_length=128, num_beams=5, early_stopping=True)
        headline = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Display headline
        st.success("Generated Headline:")
        st.write(headline)
    else:
        st.warning("Please enter a news article.")
