import lancedb
from pydantic_ai import Agent
from backend.data_models import RagResponse
from backend.constants import VECTOR_DB_PATH

vector_db = lancedb.connect(uri=VECTOR_DB_PATH)

rag_agent = Agent(
    model="google-gla:gemini-2.5-flash",
    retries=2,
    system_prompt=(
        "You are a Data Engineering Terminator, Model T-800 sent back in time to educate in Data Engineering. "
        "MANDATORY: Always, always always END every response on a NEW line with: 'Talk to the hand ✋ - I´ll be back'. "
        "Your mission is to protect the user from bad data practices and teach Data Engineering. "
        "INSTRUCTIONS: "
        "1. Always, always always END every response on a NEW line with: 'Talk to the hand ✋ - I´ll be back'. "
        "2. Answer strictly based on the retrieved video transcript knowledge OR input data from the user. Do not make things up."
        "3. If the answer is not in the source OR in the input data from the user, reply: 'Negative. Data not found in mission parameters.' "
        "4. Keep answers clear, technical, and precise"
        "5. Use terminology like 'Affirmative', 'Negative', 'Processing', or 'I'll be back'. "
        "6. You must populate the 'sources' list in the output model with the video filenames found in the context."
    ),
    output_type=RagResponse,
)

@rag_agent.tool_plain
def retrieve_top_documents(query: str) -> str:
    """Retrieves top 3 matching transcripts from LanceDB."""
    table = vector_db.open_table("transcriptions")
    results = table.search(query).limit(3).to_list()
    formatted_results = [
        f"--- MISSION DATA ---\nSource: {res['filename']}\nContent: {res['content']}"
        for res in results
    ]

    return "\n\n".join(formatted_results)

async def run_agent_with_history(current_prompt: str, memory: list[dict]):
    """Runs the agent using the current prompt and the last 10 messages of history."""
    history_text = ""
    for msg in memory[-10:]:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")

        history_text += f"{role.upper()}: {content}\n"

    full_query = f"""
    --- CHAT HISTORY (MEMORY) ---
    {history_text}

    --- CURRENT USER QUESTION ---
    {current_prompt}
    """

    result = await rag_agent.run(full_query)
    return result