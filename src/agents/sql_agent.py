"""
SQL Agent — SQL Generation, Execution, and Lineage Tagging

Responsibilities:
  - Generate SQL from a structured QueryIntent
  - Execute against the curated data layer
  - Tag results with full lineage: source tables, join paths, filters applied, grain
  - Return raw results + lineage metadata for the Validation Agent

Design Note:
  The SQL Agent does NOT validate business correctness — that's the Validation Agent's job.
  It does perform syntax and semantic checks (does the SQL compile? do the tables exist?).
  Think of this as Snowflake Cortex Analyst's SQL Generation + Error Correction in your own stack.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SQLResult:
    """Raw output from the SQL Agent."""
    query_intent_id: str
    sql: str
    rows: list[dict[str, Any]] = field(default_factory=list)
    row_count: int = 0
    lineage: dict[str, Any] = field(default_factory=dict)  # tables, joins, filters
    execution_ms: int = 0
    error: str | None = None


class SQLAgent:
    """
    Generates SQL from a QueryIntent, executes it, and returns results
    with full lineage metadata.
    """

    def __init__(self, database_connection, semantic_layer, llm):
        self.db = database_connection
        self.semantic_layer = semantic_layer
        self.llm = llm

    def run(self, query_intent) -> SQLResult:
        """
        Generate and execute SQL for the given QueryIntent.

        Args:
            query_intent: Structured QueryIntent from QueryAgent.

        Returns:
            SQLResult with raw rows and lineage metadata.
        """
        raise NotImplementedError("SQLAgent.run() — implementation pending")
