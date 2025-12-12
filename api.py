from fastapi import FastAPI
from backend.rag import run_agent_with_history
from backend.data_models import Prompt, RagResponse

app = FastAPI()

@app.post("/rag/query", response_model=RagResponse)
async def query_documentation(query: Prompt):
    """Processes a user query and returns a Terminator-styled RAG response."""
    result = await run_agent_with_history(query.prompt, query.memory)

    response_data = result.data if hasattr(result, 'data') else result.output

    catchphrase = "\n\nTalk to the hand ✋ - I´ll be back"

    if "Talk to the hand" not in response_data.answer:
        response_data.answer += catchphrase

    return response_data