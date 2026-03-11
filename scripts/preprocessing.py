import json
import os
import feedparser
import re
from datetime import datetime

# Configuración de rutas
JSON_PATH = "data/RSS_Info.json"
# Definimos la carpeta base donde caerán todas las ejecuciones
BASE_RESULTS_DIR = "data/resultados"

def preprocess_rss():
    if not os.path.exists(JSON_PATH):
        print(f"Error: No se encuentra el archivo {JSON_PATH}")
        return

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    # 1. Generar el nombre de la carpeta: fecha_hora
    folder_name = datetime.now().strftime("%Y%m%d_%H%M")
    
    # 2. Ruta completa: data/resultados/20260310_004628
    current_run_path = os.path.join(BASE_RESULTS_DIR, folder_name)
    
    # 3. Crear la carpeta (makedirs crea los padres si no existen)
    os.makedirs(current_run_path, exist_ok=True)

    for item in config["rss_feeds"]:
        # Limpieza de nombre para el archivo .json
        nombre_categoria = re.sub(r'[^\w\-]', '_', item["categoria"].lower())
        
        url = item["url"]
        fuente = item["fuente"]

        print(f"Procesando {fuente} -> {folder_name}/{nombre_categoria}.json")

        feed = feedparser.parse(url)
        resultados = []
        
        for entry in feed.entries:
            resultados.append({
                "titulo": entry.get("title", ""),
                "enlace": entry.get("link", ""),
                "resumen": entry.get("summary", ""),
                "fecha_publicacion": entry.get("published", ""),
                "fuente": fuente,
                "categoria": item["categoria"]
            })

        # 4. Guardar dentro de la carpeta fecha_hora
        file_path = os.path.join(current_run_path, f"{nombre_categoria}.json")

        with open(file_path, "w", encoding="utf-8") as out_f:
            json.dump(resultados, out_f, ensure_ascii=False, indent=4)

    print(f"\n✅ Completado: Archivos guardados en {current_run_path}")

if __name__ == "__main__":
    preprocess_rss()