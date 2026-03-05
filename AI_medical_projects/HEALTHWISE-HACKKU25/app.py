# app.py

import streamlit as st
import google.generativeai as genai

from dotenv import load_dotenv
import os

# 1. Load environment variables first
load_dotenv()

# 2. Configure the Google Generative AI API client
# It's good practice to get the key and then configure.
# Ensure your .env file has GEMINI_API_KEY=YOUR_ACTUAL_API_KEY
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not found in environment variables. Please set it in your .env file.")
    st.stop() # Stop the Streamlit app if the key is missing

genai.configure(api_key=api_key)

# 3. Initialize the Generative Model (using the full model path)
# This is the more common and recommended way to interact with Gemini models now.
try:
    # Use the full model name as recommended for reliability
    model = genai.GenerativeModel('models/gemini-2.0-flash')
except Exception as e:
    st.error(f"Failed to initialize Gemini model: {e}. Check your API key and model name.")
    st.stop()


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Set page config
st.set_page_config(
    page_title="HealthWise Chat",
    page_icon="🏥",
    layout="centered"
)

# Title
st.title("🏥 HealthWise Chat")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What's your health concern?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Generate response using the configured model
            # No need for client.models.generate_content if using genai.GenerativeModel
            response = model.generate_content(prompt)
            
            # Display the response
            message_placeholder.markdown(response.text)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            error_message = f"Error communicating with Gemini API: {str(e)}"
            message_placeholder.markdown(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})