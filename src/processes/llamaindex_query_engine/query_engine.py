from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import PydanticSingleSelector
from llama_index.core.tools import QueryEngineTool
from src.processes import rss_categories
from src.services.vector_store import qdrant_llama_index
from llama_index.core.vector_stores import ExactMatchFilter, MetadataFilters
from src.services.llms import llm_llama_index

# Create query engine tools for each category in rss_categories
query_engine_tools = []
for category, description in rss_categories.items():
    # Evitamos crear una herramienta para la opción de escape 'none'
    if category == "none":
        continue

    query_engine = qdrant_llama_index.as_query_engine(llm=llm_llama_index, **{
            "filters": MetadataFilters(
                filters=[ExactMatchFilter(key="categoria", value=category)]
            ), "similarity_top_k": 5
        })
    
    tool = QueryEngineTool.from_defaults(
        query_engine=query_engine,
        description=description,
    )
    query_engine_tools.append(tool)

router_query_engine = RouterQueryEngine(
    selector=PydanticSingleSelector.from_defaults(llm=llm_llama_index),
    query_engine_tools=query_engine_tools,
    llm=llm_llama_index
)