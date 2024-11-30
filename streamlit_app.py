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

API_KEY = key
model = genai.GenerativeModel('gemini-1.5-flash-latest')
genai.configure(api_key=API_KEY)
# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Função para lidar com o upload de arquivos
def handle_file_upload(uploaded_files):
    # Mostrar os nomes dos arquivos carregados
    if uploaded_files:
        st.markdown("### Arquivos PDF carregados:")
        for uploaded_file in uploaded_files:
            st.text(uploaded_file.name)

uploaded_files = st.file_uploader("Escolha arquivos PDF para anexar", accept_multiple_files=True, type=["pdf"])


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