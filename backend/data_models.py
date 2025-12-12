from pydantic import BaseModel, Field
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

embedding_model = get_registry().get("gemini-text").create(name="gemini-embedding-001")

EMBEDDING_DIM = 3072

class Transcriptions(LanceModel):
    """Schema for the LanceDB vector database table."""
    doc_id: str
    filepath: str
    filename: str = Field(description="YouTube video title")
    content: str = embedding_model.SourceField()
    embedding: Vector(EMBEDDING_DIM) = embedding_model.VectorField()

class Prompt(BaseModel):
    """Model for the user's API request."""
    prompt: str = Field(description="User query to T2 chat bot")
    memory: List[Dict[str, str]] = Field(default=[], description="Chat history for context")

class RagResponse(BaseModel):
    """Model for the structured API response."""
    answer: str = Field(description="T2 Terminator-style answer provided by the GeminAI")
    sources: list[str] = Field(description="List of filenames/titles for the videos used as context")