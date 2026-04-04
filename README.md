# Lucid Analytics

> **Analytics you can trust, explain, and verify — clarity and confidence for the LLM era.**

---

## The Problem

Replacing BI dashboards with LLMs is easy. Making LLM-generated analytics **trustworthy enough for real business decisions** is the actual hard problem.

Snowflake has Cortex Analyst with a Verified Query Repository (VQR). Databricks has Genie with Trusted Answers. Both are excellent. Both stop at verified *queries*.

Neither validates whether the *result* makes business sense.

**This project completes the picture.**

---

## What Is Lucid Analytics?

Lucid Analytics is an **architectural pattern** that sits on top of your existing data platform and LLM tooling. It adds the trust loop that vendors haven't built yet:

| What Vendors Do | What's Still Missing |
|---|---|
| Text-to-SQL with semantic context | Multi-angle *result* validation |
| Query verification (static templates) | Dynamic comparison against approved numbers |
| SQL syntax/semantic error correction | Business correctness checks |
| Basic confidence score ("did VQR match?") | Multi-dimensional confidence scoring with lineage |
| Semantic Layer (metrics, entities) | Knowledge Graph-enriched context for deeper relationships |

The gap is not in SQL generation. It's in **knowing the answer is right** before it reaches the analyst.

---

## Architecture Overview

```
                          ┌──────────────────────────────────────────────────────────┐
                          │                   Lucid Analytics                        │
                          │                                                          │
  User / Analyst ──────►  │  ┌─────────┐  ┌──────────┐  ┌────────────┐  ┌────────┐ │ ──► Answer
  Natural Language        │  │  Query  │  │   SQL    │  │ Validation │  │ Pres.  │ │     + Confidence
                          │  │  Agent  │─►│  Agent   │─►│  Agent     │─►│ Agent  │ │     + Lineage
                          │  └────┬────┘  └──────────┘  └─────┬──────┘  └────────┘ │     + Flags
                          │       │                            │                     │
                          │   KG + Semantic Layer          Approved Numbers          │
                          │   Vector Store                 Data Quality Rules        │
                          └──────────────────────────────────────────────────────────┘
```

### The Four Agents

| Agent | Role |
|---|---|
| **Query Agent** | Interprets intent, entities, time ranges, and filters using semantic layer + KG context |
| **SQL Agent** | Generates SQL, executes against the curated data layer, tags results with lineage |
| **Validation Agent** | Runs 5 validation checks — temporal trends, cross-metric consistency, source agreement, known adjustments, approved numbers comparison |
| **Presentation Agent** | Assembles validated results with confidence score, flags, and lineage trail |

### The Five Validation Checks

1. **Approved Numbers** — Compare result against analyst-verified figures for the same period
2. **Temporal Trends** — Does the value make sense vs. prior periods? Anomalies flagged
3. **Cross-Metric Consistency** — Revenue up 20% but orders flat? Flag the contradiction
4. **Source Agreement** — Does the number match across source systems?
5. **Known Adjustments** — Are there one-time events that explain a deviation?

---

## Repository Structure

```
trusted-ai-analytics/
├── README.md                         ← This file (architecture + positioning)
├── LICENSE                           ← Apache 2.0
├── requirements.txt                  ← Python dependencies
├── .gitignore
│
├── docs/
│   ├── architecture.md               ← Full architectural reasoning (living whitepaper)
│   ├── competitive-landscape.md      ← How this compares to Snowflake VQR, Databricks Genie
│   └── diagrams/                     ← Mermaid source + exported PNGs
│
├── src/
│   ├── agents/
│   │   ├── query_agent.py            ← Intent extraction, entity resolution via KG
│   │   ├── sql_agent.py              ← SQL generation + execution + lineage tagging
│   │   ├── validation_agent.py       ← The 5-check validation engine
│   │   └── presentation_agent.py    ← Confidence scoring + result assembly
│   │
│   ├── semantic_layer/
│   │   ├── metrics.yaml              ← Metric definitions (dbt MetricFlow compatible)
│   │   └── README.md
│   │
│   ├── knowledge_graph/
│   │   ├── schema.py                 ← Node/edge definitions for the business KG
│   │   ├── loaders.py                ← Load dbt metadata → KG
│   │   └── README.md
│   │
│   ├── approved_numbers/
│   │   ├── schema.sql                ← Benchmark store schema
│   │   ├── store.py                  ← CRUD operations for approved figures
│   │   └── README.md
│   │
│   └── vector_store/
│       ├── setup.py                  ← Embed and index analyst docs, reports
│       └── README.md
│
└── examples/
    ├── demo_notebook.ipynb           ← End-to-end walkthrough
    └── README.md
```

---

## Key Principle

> The README should be compelling enough that someone who never runs the code still understands and credits the architecture.

**Lucid Analytics is not a vendor product.** It's a named architectural pattern — built to be assembled using the tools you already have (dbt, Snowflake, Databricks, Neo4j, LangGraph) — with the validation layer that's currently missing from all of them.

---

## Status

- [x] Architecture defined and documented
- [x] Competitive landscape analysis complete
- [ ] Agent implementations (in progress)
- [ ] Demo notebook
- [ ] Article series (Medium / Towards Data Science)

---

## Author

Built and named by a Data Engineer who got tired of black-box analytics.

*April 2026*

---

## License

Apache 2.0 — use it, build on it, credit the pattern.
