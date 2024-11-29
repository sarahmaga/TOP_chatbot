import streamlit as st
import google.generativeai as genai
# Import the OpenAI library.
# Show title and description.
st.title("💬 Chatbot")
st.write(
   "Faça uma pergunta e eu responderei com a melhor resposta possível!"
   "É possível mandar um conjunto de pdfs para que eu possa responder com base neles."
)
key = 'AIzaSyA7IywZsH4XRjUopxTLpG7jmqPAQoLzyHI'

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
# openai_api_key = st.text_input("OpenAI API Key", type="password")

API_KEY = key
model = genai.GenerativeModel('gemini-1.5-flash-latest')
genai.configure(api_key=API_KEY)
# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []



# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("What is up?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    stream = model.generate_content(prompt)

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        response = st.write(stream.text)
    st.session_state.messages.append({"role": "assistant", "content": response})
