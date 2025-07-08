import streamlit as st
import pandas as pd
import numpy as np

# --------------------------------------
# UI CONFIG
# --------------------------------------
st.set_page_config(page_title="Product Carbon Estimator", page_icon="🌍", layout="centered")
st.title("🌍 Product Carbon Footprint Estimator")
st.markdown("Estimate the carbon footprint (in kg CO₂) of commonly used products based on average lifecycle emissions data.")

# --------------------------------------
# SAMPLE DATA
# --------------------------------------
data = {
    "Product": [
        "T-shirt", "Pair of Jeans", "Smartphone", "Laptop", "Plastic Bottle (1L)",
        "Beef (1kg)", "Chicken (1kg)", "Milk (1L)", "Bananas (1kg)", "Coffee (1 cup)"
    ],
    "Carbon Footprint (kg CO₂)": [
        6.75, 20.0, 55.0, 200.0, 0.25, 60.0, 6.9, 1.2, 0.8, 0.21
    ]
}
df = pd.DataFrame(data)

# --------------------------------------
# SELECT PRODUCT
# --------------------------------------
st.header("📦 Estimate from Product List")
product = st.selectbox("Choose a product:", df["Product"])

if st.button("Estimate Footprint"):
    carbon = df[df["Product"] == product]["Carbon Footprint (kg CO₂)"].values[0]
    st.success(f"Estimated carbon footprint of **{product}**: **{carbon} kg CO₂**")

# --------------------------------------
# CUSTOM INPUT
# --------------------------------------
st.markdown("---")
st.header("📝 Custom Estimate")
custom_product = st.text_input("Enter your own product:")
custom_value = st.number_input("Estimated kg CO₂ for this product:", min_value=0.0, step=0.1)

if st.button("Add Custom Product"):
    if custom_product:
        st.success(f"Your custom product **{custom_product}** emits **{custom_value} kg CO₂**")
    else:
        st.warning("Please enter a product name.")

# --------------------------------------
# DISPLAY TABLE
# --------------------------------------
st.markdown("---")
with st.expander("📊 See Emission Table"):
    st.dataframe(df.set_index("Product"))

# --------------------------------------
# FOOTER
# --------------------------------------
st.markdown(
    """
    <hr>
    <small>
    🌱 Data sourced from lifecycle assessment studies. This is a simplified estimator.
    <br>Built with ❤️ using Streamlit.
    </small>
    """,
    unsafe_allow_html=True
)

