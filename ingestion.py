import lancedb
from backend.constants import FILE_PATH, VECTOR_DB_PATH
from backend.data_models import Transcriptions
import time

def setup_vector_db(path):
    """Connects to LanceDB and creates the table."""
    vector_db = lancedb.connect(uri = path)
    vector_db.create_table("transcriptions", schema=Transcriptions, exist_ok=True)

    return vector_db

def ingest_docs_to_vector_db(table):
    """Reads all .md files from data directory and inserts them into the database."""
    for file in FILE_PATH.glob("*.md"):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        doc_id = file.stem
        table.delete(f"doc_id = '{doc_id}'")

        table.add([
            {
                "doc_id": doc_id,
                "filepath": str(file),
                "filename": file.stem,
                "content": content,
            }
        ])
        print(table.to_pandas()["filename"])
        time.sleep(5)

if __name__ == "__main__":
    vector_db = setup_vector_db(VECTOR_DB_PATH)
    ingest_docs_to_vector_db(vector_db["transcriptions"])