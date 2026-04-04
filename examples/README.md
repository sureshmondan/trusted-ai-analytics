# Examples

End-to-end walkthrough of the Lucid Analytics pipeline.

## demo_notebook.ipynb (coming soon)

The demo notebook will walk through:

1. **Setup** — Connect to a sample Snowflake / DuckDB database with the Curated layer seeded
2. **Semantic Layer** — Define metrics and entities using the `metrics.yaml` sample
3. **Knowledge Graph** — Load the seed KG (metric correlations, temporal patterns)
4. **Approved Numbers** — Populate the benchmark store with sample approved figures
5. **Ask a question** — Run a natural language question through the full agent pipeline
6. **See the difference** — Same question with and without the Validation Agent, showing how a plausible-but-wrong answer gets flagged

## Sample Question Scenarios

| Question | What the Validation Agent Catches |
|---|---|
| "What was revenue in January 2026?" | Result deviates 12% from approved finance close — flagged |
| "How did Q4 2025 orders compare to Q3?" | Q4 higher, but KG explains Q4 seasonality — EXPLAINED (confidence restored) |
| "What's our churn rate this month?" | Revenue source and CRM source disagree by 8% — SOURCE AGREEMENT fail |
| "Show me AOV by region for February" | AOV up 15% but order count flat AND revenue flat — CROSS-METRIC contradiction flagged |
