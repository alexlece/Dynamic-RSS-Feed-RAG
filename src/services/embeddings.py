from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from google import genai

MODEL_NAME = 'models/gemini-embedding-001'

embeddings_google_genai = genai.Client()



embeddings_model_llama_index = GoogleGenAIEmbedding(
    model_name=MODEL_NAME,
    embed_batch_size=1,
)
