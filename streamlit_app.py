import streamlit as st
import google.generativeai as genai
# Import the OpenAI library.
# Show title and description.
st.title("💬 Chatbot")
st.markdown(
   "Faça uma pergunta e eu responderei com a melhor resposta possível!  \n"
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

# Função para lidar com o upload de arquivos
def handle_file_upload(uploaded_file):
    if uploaded_file is not None:
        # Faça algo com o arquivo carregado
        st.write(f"Arquivo carregado: {uploaded_file.name}")
        # Você pode salvar o arquivo, processá-lo, etc.
        # Por exemplo, para salvar o arquivo:
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return uploaded_file.name
    return None

# Adicionando a funcionalidade de upload de arquivos
uploaded_file = st.file_uploader("Escolha um arquivo para anexar")

# Processando o arquivo carregado
file_name = handle_file_upload(uploaded_file)

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("E aí?"):

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

    # Se um arquivo foi carregado, adicione-o à mensagem
    if file_name:
        st.session_state.messages.append({"role": "assistant", "attachment": file_name})
