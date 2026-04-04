"""
Vector Store Setup — RAG for Analyst Context

Embeds and indexes unstructured analyst knowledge for retrieval by the Validation Agent.

What gets embedded:
  - Past analyst reports and quarterly commentary
  - Board presentation slide narratives
  - Meeting notes from budget and forecast reviews
  - BI documentation and data dictionary notes
  - Manually written anomaly explanations

Why this is different from the Knowledge Graph:
  - KG handles structured relationships (Revenue CORRELATES_WITH Orders)
  - Vector store handles unstructured narrative ("Q3 drop was due to a distribution delay")
  - Together: structured + unstructured context = richer agent reasoning

Supported backends: Pinecone, Weaviate, pgvector (Postgres), ChromaDB
"""

from pathlib import Path


class VectorStoreSetup:
    """
    Embeds analyst documents and indexes them for RAG retrieval.
    Backend-agnostic: configure with any supported vector store client.
    """

    def __init__(self, embedding_model, vector_store_client):
        self.embedder = embedding_model
        self.store = vector_store_client

    def ingest_documents(self, docs_dir: str | Path):
        """
        Chunk, embed, and index all documents in a directory.

        Args:
            docs_dir: Path to folder containing analyst docs (PDF, MD, TXT).
        """
        raise NotImplementedError("VectorStoreSetup.ingest_documents() — implementation pending")

    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        """
        Retrieve the top_k most relevant document chunks for a query.

        Used by the Validation Agent to find analyst commentary that may
        explain a deviation or provide historical context.
        """
        raise NotImplementedError("VectorStoreSetup.retrieve() — implementation pending")
