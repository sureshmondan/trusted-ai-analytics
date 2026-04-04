"""
Knowledge Graph Loaders

Utilities for populating the KG from existing data platform metadata.

Primary loader: DbtMetadataLoader
  - Reads dbt manifest.json and catalog.json
  - Extracts models, metrics, sources, and their relationships
  - Creates KG nodes and edges from the dbt graph

Planned loaders:
  - SnowflakeSchemaLoader    — Reads Snowflake information schema + Cortex Semantic Views
  - DatabricksUnityLoader    — Reads Unity Catalog lineage
  - ManualEventLoader        — Loads known events from a CSV/YAML maintained by analysts
"""

import json
from pathlib import Path


class DbtMetadataLoader:
    """
    Loads dbt manifest.json metadata into the Knowledge Graph.

    Extracts:
      - dbt models → Entity nodes
      - dbt metrics → Metric nodes
      - dbt model dependencies → DEPENDS_ON edges
      - dbt metric measures → CORRELATES_WITH edges (inferred from shared dimensions)
    """

    def __init__(self, manifest_path: str, graph_client):
        self.manifest_path = Path(manifest_path)
        self.graph = graph_client

    def load(self):
        """
        Parse the dbt manifest and upsert nodes and edges into the KG.
        """
        raise NotImplementedError("DbtMetadataLoader.load() — implementation pending")

    def _extract_models(self, manifest: dict) -> list[dict]:
        """Extract model nodes from the dbt manifest."""
        raise NotImplementedError

    def _extract_metrics(self, manifest: dict) -> list[dict]:
        """Extract metric nodes from the dbt manifest."""
        raise NotImplementedError

    def _extract_edges(self, manifest: dict) -> list[dict]:
        """Extract dependency edges from the dbt manifest node graph."""
        raise NotImplementedError
