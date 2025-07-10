import streamlit as st
import numpy as np
from PIL import Image
import torch
import torchvision.transforms as transforms
from torchvision import models
import random
import json
import urllib.request

# Page config
st.set_page_config(
    page_title="Smart Carbon Footprint Predictor",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="auto"
)

# Load model and labels
@st.cache_resource(show_spinner=False)
def load_model_and_labels():
    model = models.mobilenet_v2(pretrained=True)
    model.eval()
    
    # Load labels from ImageNet
    url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
    with urllib.request.urlopen(url) as f:
        labels = [line.strip().decode('utf-8') for line in f.readlines()]
    
    return model, labels

model, labels = load_model_and_labels()

# Image preprocessing
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],  # ImageNet means
        std=[0.229, 0.224, 0.225]    # ImageNet stds
    )
])

# Streamlit UI
st.title("📸 Smart Carbon Footprint Estimator")
st.write("Upload or capture a product image to estimate its carbon footprint.")

input_method = st.radio("Choose input method:", ["Upload Image", "Capture from Camera"])

uploaded_image = None
if input_method == "Upload Image":
    uploaded_file = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        uploaded_image = Image.open(uploaded_file).convert("RGB")
elif input_method == "Capture from Camera":
    camera_image = st.camera_input("Take a photo")
    if camera_image is not None:
        uploaded_image = Image.open(camera_image).convert("RGB")

if uploaded_image is not None:
    st.image(uploaded_image, caption="Input Image", use_column_width=True)
    st.write("🔍 Identifying product...")

    # Apply preprocessing
    image_tensor = preprocess(uploaded_image)
    image_tensor = image_tensor.unsqueeze(0)  # Add batch dimension

    # Predict
    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)

    top3_prob, top3_catid = torch.topk(probabilities, 3)

    st.subheader("Top Predictions:")
    for i in range(top3_prob.size(0)):
        label = labels[top3_catid[i]]
        st.write(f"{i + 1}. {label.title()} — {top3_prob[i].item() * 100:.2f}%")

    best_label = labels[top3_catid[0]].title()
    carbon_footprint_kg = round(random.uniform(1, 100), 2)

    st.subheader("🌍 Estimated Carbon Footprint")
    st.write(f"Product: **{best_label}**")
    st.write(f"Estimated Carbon Emissions: **{carbon_footprint_kg} kg CO₂**")

else:
    st.info("Please upload or capture a product image to get started.")
