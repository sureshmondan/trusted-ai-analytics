"""
Query Agent — Intent Extraction and Entity Resolution

Responsibilities:
  - Parse natural language into structured query intent
  - Resolve entities, metrics, and time ranges via the semantic layer
  - Enrich context using the Knowledge Graph (relationships, conventions, ambiguity resolution)
  - Output a structured QueryIntent for the SQL Agent

Design Note:
  This agent is the first contact point. It should be conservative: if intent is ambiguous,
  it should clarify rather than guess. The KG provides the org-specific disambiguation rules
  (e.g., "revenue" = gross revenue in this org, not net).
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class QueryIntent:
    """Structured output from the Query Agent."""
    original_question: str
    metric: str
    dimensions: list[str] = field(default_factory=list)
    filters: dict[str, Any] = field(default_factory=dict)
    time_range: dict[str, str] = field(default_factory=dict)
    grain: str = "monthly"
    kg_context: dict[str, Any] = field(default_factory=dict)  # relevant KG subgraph
    ambiguities: list[str] = field(default_factory=list)       # unresolved ambiguities


class QueryAgent:
    """
    Resolves natural language questions into structured query intent
    using the semantic layer and knowledge graph.
    """

    def __init__(self, semantic_layer, knowledge_graph, llm):
        self.semantic_layer = semantic_layer
        self.knowledge_graph = knowledge_graph
        self.llm = llm

    def run(self, question: str) -> QueryIntent:
        """
        Parse a natural language question into a structured QueryIntent.

        Args:
            question: Free-text question from the analyst.

        Returns:
            QueryIntent with resolved entities, time ranges, and KG context.
        """
        raise NotImplementedError("QueryAgent.run() — implementation pending")
