from pydantic import BaseModel, Field
from app.db import search_vector_db
from app.openai import get_embedding

class QueryKnowledgeBaseTool(BaseModel):
    """Consulta la base de conocimientos para responder preguntas de los usuarios sobre los productos y servicios de Datapar, sus características y soluciones a problemas comunes."""
    query_input: str = Field(description='La consulta en lenguaje natural. La consulta debe ser clara y autónoma para obtener la mejor respuesta posible.')

    async def __call__(self, rdb):
        query_vector = await get_embedding(self.query_input)
        chunks = await search_vector_db(rdb, query_vector)
        formatted_sources = [f"SOURCE: {c['doc_name']}\n\"\"\"\n{c['text']}\n\"\"\"" for c in chunks]
        return f"\n\n---\n\n".join(formatted_sources) + f"\n\n---"
