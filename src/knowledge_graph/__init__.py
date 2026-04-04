"""
Knowledge Graph Module

Provides the schema definitions, loaders, and query interface for the
Lucid Analytics Knowledge Graph.

The KG enriches LLM agent context with:
  - Business entity relationships (Product → Category → Business Unit)
  - Metric correlations (Revenue depends on Orders × ASP)
  - Temporal patterns (Q4 seasonality, fiscal year conventions)
  - Known events (one-time adjustments that explain deviations)
  - Anomaly baselines (what's a 'normal' variance for each metric)

Tools: Neo4j, Amazon Neptune, TigerGraph, or lightweight property graph.
"""

from .schema import NodeType, EdgeType
from .loaders import DbtMetadataLoader

__all__ = ["NodeType", "EdgeType", "DbtMetadataLoader"]
