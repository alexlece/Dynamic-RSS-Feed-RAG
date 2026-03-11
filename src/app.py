from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

# Routers
from api.router_llamaindex import router as llamaindex_rag_router

logger = logging.getLogger('uvicorn')

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML models and other resources
    logger.info("Starting up...")
    yield
    # Clean up the ML models and other resources
    logger.info("Shutting down...")

app = FastAPI(
    title="RAG and Semantic Search API",
    description="An API for RAG and Semantic Search with LlamaIndex for RSS feeds",
    version="0.1.0",
    lifespan=lifespan
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the RAG and Semantic Search API for RSS feeds!"}

# Adding Routers
app.include_router(llamaindex_rag_router, prefix='/llama_index',tags=["Llama Index System"])