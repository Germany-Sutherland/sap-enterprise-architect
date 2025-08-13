import streamlit as st
import pandas as pd
import numpy as np
import pytesseract
from PIL import Image
import networkx as nx
import matplotlib.pyplot as plt
import requests

# App title
st.set_page_config(page_title="SAP AI Architect", layout="wide")
st.title("🧠 SAP AI Architect – Free Tier Edition")
st.write("An AI-powered assistant to simulate tasks of a SAP Solution Architect using lightweight 2025 technologies.")

# Sidebar
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Optional: OpenAI API Key", type="password")
st.sidebar.caption("Optional: set OPENAI_API_KEY in Secrets for richer text output")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Requirements Intake", "Architecture Design", "Document OCR", "IoT Simulation"])

# Requirements Intake
with tab1:
    st.subheader("1️⃣ Requirements Intake (Simulated Agentic AI)")
    user_req = st.text_area("Enter business requirements")
    if st.button("Analyze Requirements"):
        st.success("Simulated AI Analysis:")
        st.write(f"- Detected Modules: {['FI', 'CO', 'MM']}")
        st.write(f"- Suggested Landscape: S/4HANA Cloud with IoT integration")

# Architecture Design
with tab2:
    st.subheader("2️⃣ Architecture Design (Knowledge Graph)")
    G = nx.Graph()
    G.add_edges_from([
        ("S/4HANA", "FI"),
        ("S/4HANA", "CO"),
        ("S/4HANA", "MM"),
        ("MM", "IoT Gateway"),
        ("IoT Gateway", "Edge Device")
    ])
    fig, ax = plt.subplots()
    nx.draw(G, with_labels=True, node_color='lightblue', font_weight='bold', ax=ax)
    st.pyplot(fig)

# Document OCR
with tab3:
    st.subheader("3️⃣ Document OCR")
    uploaded_file = st.file_uploader("Upload an image or scanned document", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Document", use_column_width=True)
        text = pytesseract.image_to_string(image)
        st.text_area("Extracted Text", text, height=200)

# IoT Simulation
with tab4:
    st.subheader("4️⃣ IoT Data Simulation")
    if st.button("Generate IoT Data"):
        df = pd.DataFrame({
            "SensorID": np.arange(1, 6),
            "Temperature": np.random.normal(25, 2, 5),
            "Vibration": np.random.normal(0.5, 0.1, 5)
        })
        st.dataframe(df)
