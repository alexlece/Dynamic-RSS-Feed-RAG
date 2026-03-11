import json
from pathlib import Path

# Ruta al archivo de configuración
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = BASE_DIR / "data" / "RSS_Info.json"

rss_categories = {}

try:
    with open(CONFIG_PATH, "r", encoding='utf-8') as f:
        data = json.load(f)
        # Mapeamos: { "Economía": "Noticias económicas..." }
        for item in data.get("rss_feeds", []):
            rss_categories[item["categoria"]] = item["descripcion"]
except Exception as e:
    print(f"⚠️ Error cargando configuración: {e}")

# Añadimos el caso por defecto
rss_categories['none'] = "Usa esta opción si la pregunta no tiene relación con los temas disponibles."

__all__ = ['rss_categories']