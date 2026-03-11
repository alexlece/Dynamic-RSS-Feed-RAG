# Dynamic RSS RAG System

Sistema de **ingestión, indexación y consulta inteligente de información** basado en **RAG (Retrieval-Augmented Generation)** para **fuentes RSS dinámicas**.

El proyecto captura contenido desde **RSS feeds configurables**, lo **preprocesa y normaliza**, genera **embeddings semánticos** utilizando **Google Gemini** y los almacena en una **base de datos vectorial (Qdrant)**.

A partir de estos datos indexados, el sistema expone una **API basada en FastAPI** que permite realizar **consultas en lenguaje natural**, recuperando la información más relevante mediante **búsqueda semántica** y generando respuestas contextualizadas usando un **LLM**.

El sistema está diseñado para funcionar de forma **dinámica e incremental**, permitiendo actualizar continuamente la base de conocimiento a medida que aparecen nuevos contenidos en los feeds.

## Características principales

- 📡 **Ingestión dinámica de RSS feeds**
- 🧹 **Preprocesamiento y normalización de contenidos**
- 🧠 **Generación de embeddings con Google Gemini**
- 🗂 **Indexación vectorial en Qdrant**
- 🔎 **Búsqueda semántica sobre documentos indexados**
- ⚡ **API REST con FastAPI para consultas RAG**
- 📈 **Indexación incremental que mantiene el histórico**

## Ejemplos de uso

El sistema puede aplicarse a múltiples tipos de fuentes RSS, por ejemplo:

- 📰 **Medios de comunicación y agregadores de noticias**
- ⚖️ **Publicaciones oficiales** como el **BOE**
- 💰 **Feeds económicos o financieros**
- ⚽ **Noticias deportivas**
- 🧑‍💻 **Blogs técnicos o documentación**

---





# 🚀 Guía de Uso
---

# 1. Requisitos Previos

Antes de empezar, asegúrate de tener instalado:

- **uv**: gestor de entornos y dependencias  
  https://astral.sh/uv

- **Docker**: necesario para levantar la base de datos vectorial

- **Google Gemini API Key**: utilizada para generar **embeddings** y para el **LLM**

---

# 2. Instalación y Configuración

## Inicializar el entorno y dependencias

```bash
uv sync
```

Esto creará el entorno virtual e instalará todas las dependencias del proyecto.

---

## Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
GOOGLE_API_KEY=tu_api_key_aqui
```

---

# 3. Configuración de Fuentes

Antes de ejecutar el sistema debes definir qué fuentes quieres monitorizar.

Edita el archivo:

```
data/RSS_Info.json
```
y añade las URLs de los feeds RSS o secciones XML del BOE.

### Ejemplo

```json
{
  "futbol": "https://url-del-rss-de-deportes.xml",
  "economia": "https://url-del-rss-de-economia.xml",
  "boe": "https://www.boe.es/datosabiertos/xml/boe/ultimo_dia.xml"
}
```

- Cada **clave** representa una categoría o fuente lógica.
- Cada **valor** es la URL del feed RSS o XML que se procesará.

---

# 4. Puesta en Marcha (Workflow)

Debes ejecutar los componentes en el siguiente orden.

---

## Paso 1: Levantar la Base Vectorial

Levanta el contenedor de **Qdrant** mediante Docker:

```bash
docker-compose up -d
```

Esto iniciará la base de datos vectorial donde se almacenarán los embeddings.

---

## Paso 2: Preprocesamiento de Datos

Captura las noticias de los RSS/BOE y genera los archivos JSON locales:

```bash
uv run scripts/preprocessing_rss.py
```

Este proceso:

- Descarga los feeds configurados
- Normaliza los datos
- Genera archivos JSON listos para indexar

---

## Paso 3: Indexación

Crea los embeddings y puebla la base de datos **Qdrant**.

```bash
uv run scripts/create_llamaindex_index.py
```

Características del proceso:

- Genera embeddings con **Gemini**
- Inserta los vectores en **Qdrant**

---

# 5. Ejecutar la API

Una vez indexados los datos, puedes levantar la API **RAG** para realizar consultas.

La aplicación está definida en:

```
src/main.py
```

Ejecuta el servidor **FastAPI**:

```bash
uv run fastapi run src/main.py
```

---

# 6. Acceso a la API

Una vez iniciada:

### Documentación interactiva (Swagger)

```
http://localhost:8000/docs
```

Desde esta interfaz podrás probar los endpoints y realizar consultas al sistema **RAG**.
