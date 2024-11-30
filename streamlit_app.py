import streamlit as st
import google.generativeai as genai
import handling_pdfs
import os
# Show title and description.
st.title("💬 Chatbot")
st.markdown(
   "Faça uma pergunta e eu responderei com a melhor resposta possível!  \n"
   "É possível mandar um conjunto de pdfs para que eu possa responder com base neles."
)
key = 'AIzaSyDlroY8fjB1bt-eS2Tro9_zUNhgNu_mRc8'

API_KEY = key
model = genai.GenerativeModel('gemini-1.5-flash-latest')
genai.configure(api_key=API_KEY)
# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []


def save_uploaded_file(uploaded_file):
    with open(os.path.join("uploaded_pdfs", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    return os.path.join("uploaded_pdfs", uploaded_file.name)


# Função para lidar com o upload de arquivos
def handle_file_upload(uploaded_files):
    # Mostrar os nomes dos arquivos carregados
    if uploaded_files:
        st.markdown("### Arquivos PDF carregados:")
        for uploaded_file in uploaded_files:
            st.text(uploaded_file.name)
            # Salvar os arquivos carregados
            save_uploaded_file(uploaded_file)


def awser_question_based_on_pdf(uploaded_files, question=None):
    if uploaded_files:
        all_text = ""
        for uploaded_file in uploaded_files:
            path = os.path.join("uploaded_pdfs", uploaded_file.name)
            text = handling_pdfs.extract_text_from_pdf(path)
            all_text += text

        sentences, embeddings = handling_pdfs.generate_embeddings(all_text)
        index = handling_pdfs.index_embeddings(embeddings)

        if question:
            answer = handling_pdfs.find_similar_question(question, index, sentences)
            st.write(f"Resposta: {answer}")
            
os.makedirs("uploaded_pdfs", exist_ok=True)
uploaded_files = st.file_uploader("Escolha arquivos PDF para anexar", accept_multiple_files=True, type=["pdf"])
handle_file_upload(uploaded_files)

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("E aí?"):
    if uploaded_files:
        awser_question_based_on_pdf(uploaded_files, prompt)
    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    if not uploaded_files:
        # Generate a response using the Genai API.
        stream = model.generate_content(prompt)

        # Stream the response to the chat using `st.write`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write(stream.text)
        st.session_state.messages.append({"role": "assistant", "content": response})
