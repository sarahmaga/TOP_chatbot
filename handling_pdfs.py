import fitz  # PyMuPDF
import faiss
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def generate_embeddings(text):
    sentences = text.split('\n')
    embeddings = model.encode(sentences)
    return sentences, embeddings

def index_embeddings(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

def find_similar_question(question, index, sentences):
    question_embedding = model.encode([question])
    D, I = index.search(question_embedding, k=1)
    return sentences[I[0][0]]
