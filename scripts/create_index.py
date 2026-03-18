from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

print("Loading Docs...")
loader = DirectoryLoader("./files")
docs = loader.load()

print("Splitting Docs...")
doc_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=200)
doc_chunks = doc_splitter.split_documents(docs)

print("Loading embedding model...")
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

print("Creating vector store...")
vectorstore = FAISS.from_documents(doc_chunks, embeddings)
vectorstore.save_local("db")