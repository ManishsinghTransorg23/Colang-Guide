import streamlit as st
from nemoguardrails import LLMRails, RailsConfig
import openai
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# def get_weather_data(city_name: str):
#     weather_api_key = os.getenv("WEATHER_API_KEY")
#     url = "https://api.weatherstack.com/current?access_key={}".format(
#         weather_api_key)
#     querystring = {"query": city_name}
#     response = requests.get(url, params=querystring)
#     print(response.json())

# Load Nemo Guardrails
config = RailsConfig.from_path("guardrails")
rails = LLMRails(config)

# Register actions
# rails.register_action(action=get_weather_data, name="check_live_weather")

st.title("LLM Chatbot with Nemo Guardrails")

# Correct session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your message here...")
# user_input = "Hi"

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare input for rails.generate()
    try:
        # Modify the conversation history format if needed
        conversation_history = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in st.session_state.messages
        ]

        # Add current user input to conversation history
        conversation_history.append({"role": "user", "content": user_input})

        # Generate response
        response = rails.generate(user_input)

        # Extract response text
        if isinstance(response, dict):
            response_text = response.get('content', str(response))
        elif isinstance(response, str):
            response_text = response
        else:
            response_text = str(response)

        # Display and store response
        with st.chat_message("assistant"):
            st.markdown(response_text)

        # Update session state
        st.session_state.messages.append(
            {"role": "user", "content": user_input})
        st.session_state.messages.append(
            {"role": "assistant", "content": response_text})

    except openai.BadRequestError as e:
        st.error(f"OpenAI API Error: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
