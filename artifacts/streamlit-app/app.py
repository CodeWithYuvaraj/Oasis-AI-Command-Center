import streamlit as st
import requests
import os

st.set_page_config(page_title="Oasis AI", page_icon="🛵", layout="centered")

st.title("🛵 Oasis AI: Gig-Worker Co-Pilot")
st.markdown("Real-time safety and peak demand routing for two-wheeler delivery partners.")
st.divider()

st.subheader("📍 Shift Details")
col1, col2 = st.columns(2)

with col1:
    zone = st.selectbox("Current Zone (Hyderabad)", 
                       ["Madhapur", "Ameerpet", "Kukatpally", "Secunderabad", "Gachibowli"])

with col2:
    vehicle = st.selectbox("Vehicle Type", ["TVS Activa (Scooter)", "Motorcycle", "EV"])

if st.button("Generate Safe Ride Strategy 🚀", use_container_width=True):
    with st.spinner('Analyzing environmental and demand data via Hugging Face...'):
        API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
        hf_token = os.environ.get("HUGGING_FACE_TOKEN", "")
        HEADERS = {"Authorization": f"Bearer {hf_token}"}
        
        prompt = f"""
        Act as an expert logistics coordinator and safety assistant for a gig worker riding a {vehicle} in the {zone} area of Hyderabad, India. 
        Provide a highly practical, realistic shift strategy structured into three distinct sections:
        1. 🌡️ Environment & Thermal Safety (Address heat risks, shaded routing options, hydration targets).
        2. 💰 Peak Slot Optimization (Predict where the highest quick-commerce/ride-share order volume will pool).
        3. 📍 Hyper-Local Zone Focus (Suggest specific local landmarks, tech parks, or hubs to wait near for maximum orders).
        Keep the tone encouraging and write the actionable layout advice clearly. Use simple terminology.
        """
        
        try:
            response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt, "parameters": {"max_new_tokens": 500}})
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0 and 'generated_text' in result[0]:
                ai_strategy = result[0]['generated_text'].replace(prompt, "").strip()
                st.success("Strategy Compiled Successfully!")
                st.markdown(ai_strategy)
            else:
                st.error("API Response error. Please verify your Hugging Face Token.")
                
        except Exception as e:
            st.error(f"Failed to connect to AI engine: {e}")
