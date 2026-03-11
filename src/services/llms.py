#from langchain_openrouter import ChatOpenRouter
from llama_index.llms.google_genai import GoogleGenAI
from google import genai

#ChatOpenRouter(
#    model="google/gemini-2.5-flash-lite",
#    temperature=0,
#    max_retries=3
#)

llm_llama_index = GoogleGenAI(
    model="gemini-2.5-flash-lite",
    temperature=0,
)

llm_google_genai = genai.Client()
