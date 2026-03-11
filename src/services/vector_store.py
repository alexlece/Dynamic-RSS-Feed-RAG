from llama_index.vector_stores.qdrant import QdrantVectorStore as LlamaQdrantVectorStore
from src.services.embeddings import  embeddings_model_llama_index
from llama_index.core import VectorStoreIndex, StorageContext
from qdrant_client import QdrantClient, AsyncQdrantClient


### LLAMA INDEX
vector_store = LlamaQdrantVectorStore(
    client=QdrantClient(url="http://localhost:6333"), 
    aclient=AsyncQdrantClient(url="http://localhost:6333"),
    collection_name="rss_news_index",
    batch_size=1
    )
storage_context = StorageContext.from_defaults(vector_store=vector_store)
qdrant_llama_index = VectorStoreIndex.from_documents(
    [], 
    storage_context=storage_context, 
    embed_model=embeddings_model_llama_index
    )