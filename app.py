import streamlit as st
import numpy as np
from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import img_to_array
import random

# Set page config first
st.set_page_config(
    page_title="Smart Carbon Footprint Predictor",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="auto"
)

# Load model once and cache it
@st.cache_resource(show_spinner=False)
def load_model():
    return MobileNetV2(weights="imagenet")

model = load_model()

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

    image_resized = uploaded_image.resize((224, 224))
    image_array = img_to_array(image_resized)
    image_batch = np.expand_dims(image_array, axis=0)
    processed_img = preprocess_input(image_batch)

    preds = model.predict(processed_img)
    decoded_preds = decode_predictions(preds, top=3)[0]

    st.subheader("Top Predictions:")
    for i, (imagenet_id, label, prob) in enumerate(decoded_preds):
        st.write(f"{i + 1}. {label.replace('_', ' ').title()} — {prob * 100:.2f}%")

    best_label = decoded_preds[0][1].replace('_', ' ').title()
    carbon_footprint_kg = round(random.uniform(1, 100), 2)

    st.subheader("🌍 Estimated Carbon Footprint")
    st.write(f"Product: **{best_label}**")
    st.write(f"Estimated Carbon Emissions: **{carbon_footprint_kg} kg CO₂**")

else:
    st.info("Please upload or capture a product image to get started.")
