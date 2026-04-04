# Semantic Layer

Business logic encoded as metrics, entities, and relationships. Compatible with **dbt MetricFlow** and **Cube** schemas.

## What Lives Here

| File | Purpose |
|---|---|
| `metrics.yaml` | Metric definitions: name, description, SQL expression, dimensions, time grain |
| `entities.yaml` | Business entity definitions and join paths |

## Design Principle

The semantic layer is a *flat* definition store. It knows what `revenue` means. It does **not** know that `revenue` and `orders` should move together — that's the Knowledge Graph's job.

The semantic layer feeds the Query Agent (entity/metric resolution) and the SQL Agent (join paths, formula expansion).
