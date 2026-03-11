import sys 
import os 
import time
import json
import warnings
from datetime import datetime
from dotenv import load_dotenv

# Configuración de entorno y paths
sys.path.append('.')
load_dotenv()
warnings.filterwarnings("ignore")

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from llama_index.core import Document, VectorStoreIndex, StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from src.services.embeddings import embeddings_model_llama_index

def run_indexing():
    # 1. LOCALIZAR CARPETA MÁS RECIENTE
    base_results_path = 'data/resultados'
    
    if not os.path.exists(base_results_path):
        print(f"❌ La carpeta {base_results_path} no existe.")
        return

    all_subdirs = sorted([
        os.path.join(base_results_path, d) 
        for d in os.listdir(base_results_path) 
        if os.path.isdir(os.path.join(base_results_path, d))
    ])

    if not all_subdirs:
        print("❌ No se encontraron carpetas de resultados para indexar.")
        return

    latest_dir = all_subdirs[-1]
    folder_timestamp = os.path.basename(latest_dir)
    print(f"📂 Carpeta detectada para indexación: {latest_dir}")

    # 2. CONFIGURAR QDRANT
    collection_name = "rss_news_index"
    qdrant_url = "http://localhost:6333"
    client = QdrantClient(url=qdrant_url)

    # Nota: No borramos la colección para mantener el histórico. 
    # Si no existe, la creamos.
    try:
        client.get_collection(collection_name)
        print(f"♻️  Añadiendo datos a la colección existente: '{collection_name}'")
    except:
        print(f"✨ Creando nueva colección: '{collection_name}'")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
        )

    # 3. PREPARAR STORAGE CONTEXT
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=collection_name
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Inicializamos el índice vinculado a Qdrant
    index = VectorStoreIndex(
        nodes=[],
        storage_context=storage_context,
        embed_model=embeddings_model_llama_index
    )

    # 4. PROCESAR CADA JSON Y CADA NOTICIA INDIVIDUALMENTE
    json_files = [f for f in os.listdir(latest_dir) if f.endswith('.json')]
    
    total_indexed = 0
    print(f"🚀 Iniciando inserción granular...")

    for file_name in json_files:
        file_path = os.path.join(latest_dir, file_name)
        
        with open(file_path, "r", encoding="utf-8") as f:
            noticias = json.load(f)
        
        print(f"   Inyectando {len(noticias)} noticias desde {file_name}...")

        for n in noticias:
            # Creamos el cuerpo del texto combinando título y resumen
            text_content = f"TITULO: {n.get('titulo')}\nRESUMEN: {n.get('resumen')}"
            
            # Creamos el objeto Document de LlamaIndex por cada noticia
            doc = Document(
                text=text_content,
                metadata={
                    "categoria": n.get("categoria"),  # Clave fundamental para el Router
                    "fuente": n.get("fuente"),
                    "url": n.get("enlace"),
                    "ingestion_time": folder_timestamp,
                    "date_indexed": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            )
            
            # Insertamos el documento individual
            index.insert(doc)
            total_indexed += 1

            # Añade este delay para no quemar la cuota
            time.sleep(0.8)
            
        print(f"   ✅ Categoría {n.get('categoria')} completada.")

    print(f"\n✨ Proceso terminado: {total_indexed} noticias indexadas individualmente.")
    print(f"📍 Colección: {collection_name} | Timestamp: {folder_timestamp}")

if __name__ == "__main__":
    run_indexing()