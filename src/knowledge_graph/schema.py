"""
Knowledge Graph Schema — Node and Edge Type Definitions

Defines the node types and edge types for the Lucid Analytics KG.
Implementation-agnostic: maps to Neo4j labels, Neptune vertex/edge labels,
or a property graph table structure.

Node Types:
  - Metric          — A named business metric (revenue, churn_rate, AOV)
  - Dimension       — A grouping attribute (region, product_category)
  - Entity          — A business entity (customer, product, order)
  - KnownEvent      — A documented event that explains a deviation
  - TemporalPattern — A recurring seasonal or cyclical pattern

Edge Types:
  - CORRELATES_WITH — Two metrics that historically move together
  - AFFECTS         — A known event or pattern that affects a metric's expected value
  - BELONGS_TO      — Hierarchy membership (Product BELONGS_TO Category)
  - DEPENDS_ON      — Metric derivation dependency (AOV DEPENDS_ON Revenue, OrderCount)
"""

from enum import Enum


class NodeType(str, Enum):
    METRIC = "Metric"
    DIMENSION = "Dimension"
    ENTITY = "Entity"
    KNOWN_EVENT = "KnownEvent"
    TEMPORAL_PATTERN = "TemporalPattern"


class EdgeType(str, Enum):
    CORRELATES_WITH = "CORRELATES_WITH"
    AFFECTS = "AFFECTS"
    BELONGS_TO = "BELONGS_TO"
    DEPENDS_ON = "DEPENDS_ON"


# Sample KG seed data (used for demo and testing)
SEED_NODES = [
    {"type": NodeType.METRIC, "name": "revenue", "label": "Gross Revenue"},
    {"type": NodeType.METRIC, "name": "order_count", "label": "Order Count"},
    {"type": NodeType.METRIC, "name": "average_order_value", "label": "Average Order Value (AOV)"},
    {"type": NodeType.METRIC, "name": "churn_rate", "label": "Monthly Churn Rate"},
    {"type": NodeType.TEMPORAL_PATTERN, "name": "q4_seasonality",
     "description": "Q4 revenue is typically 25-40% higher than Q3 due to holiday demand. Not an anomaly."},
    {"type": NodeType.TEMPORAL_PATTERN, "name": "fiscal_year_close",
     "description": "Month 12 figures may include year-end adjustments. Validate against finance close report."},
]

SEED_EDGES = [
    {"from": "revenue", "to": "order_count", "type": EdgeType.CORRELATES_WITH,
     "expected_direction": "same", "tolerance_pct": 15,
     "note": "Revenue and order count should move in the same direction. AOV explains divergence."},
    {"from": "average_order_value", "to": "revenue", "type": EdgeType.DEPENDS_ON},
    {"from": "average_order_value", "to": "order_count", "type": EdgeType.DEPENDS_ON},
    {"from": "q4_seasonality", "to": "revenue", "type": EdgeType.AFFECTS,
     "months": [10, 11, 12]},
]
