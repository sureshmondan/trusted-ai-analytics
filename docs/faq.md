# Lucid Analytics — Frequently Asked Questions

*Captures real architectural questions, objections, and their answers. Updated as new ones emerge.*

---

## Q1: Don't dbt tests already catch wrong numbers?

**Short answer:** dbt tests catch dirty data. Lucid Analytics catches wrong answers. These are different problems at different layers.

dbt tests run at the pipeline layer during transformation. They validate the *data in your tables*:
- Null values, duplicate keys, referential integrity
- Custom assertions: `revenue > 0`, row count in expected range

What dbt tests **cannot** catch:
- **LLM-generated query fan-out** — the LLM writes SQL you've never seen before. If it joins `orders` to `order_items` at the wrong grain, you get row multiplication. Both tables pass every dbt test. The *join* is the bug, and it lives in a query that didn't exist when you wrote your tests.
- **Business-range violations** — dbt has no concept of "this metric should be in the 40s this month, not 400." A test can check `revenue > 0`. It cannot check whether the result is in the neighborhood your team expects.
- **Cross-metric incoherence** — nobody writes a dbt test that says "if revenue increases >50% MoM, verify customer count moved directionally." That's business judgment, not data quality.

**The clean framing:**
> dbt asks: *"is the data clean?"*
> Lucid Analytics asks: *"is the answer true?"*

Both are necessary. Neither replaces the other.

---

## Q2: Doesn't the CFO get numbers from the DW? Why would the Approved Numbers Store be different?

**Short answer:** Yes — the CFO's numbers come from the DW. The Approved Numbers Store IS the DW, at a specific moment in time, with the human judgment that blessed it.

The distinction is not *where* the number came from. It's *when* and *whether a human validated it.*

Finance approves a number at close. The DW keeps running. The same query run three weeks later may return a different result due to late-arriving records, pipeline backfills, or ERP adjustments that applied at the reporting layer. The LLM queries live data. Finance approved a specific state of that data.

The Approved Numbers Store stores the historical record of what humans have validated — same DW, specific point in time, human-stamped. It is not a separate source of truth; it's a timestamped fingerprint of agreed-upon DW outputs used as a sanity baseline for validation.

---

## Q3: Why not just frame this as "Finance expectations" for the numbers?

**Short answer:** Too narrow. The real value is encoding tribal knowledge from *any* domain team, not just Finance at close.

Every experienced analyst, data lead, and ops manager carries a mental model of what the numbers should look like — thresholds that matter, ranges that are normal, combinations that should trigger a second look. None of that is in the schema. None of it is in the semantic layer. When that person leaves, it walks out with them.

The Finance-at-close framing accidentally makes the Approved Numbers Store sound like a frozen accounting artifact. The tribal knowledge framing makes it sound like what it actually is: a systematic way to give the AI the institutional memory your team has built over years.

**The line that captures it:**
> *Text-to-SQL gave the model business language. Nobody gave it business judgment.*

---

## Q4: What if a scheduled agent pre-calculates the numbers so validation is a fast lookup?

**Short answer:** Correct instinct on performance — but the critical missing piece is a human approval gate to break the circular validation risk.

**Pros of pre-calculated baselines:**
- Fast — validation is a lookup, not a re-query at runtime
- Deterministic — the baseline is always the same reference for a given period
- Reduces DW load — no expensive on-demand validation queries
- Versionable — you know exactly when the number was calculated and from what state of the data

**Cons of pure machine pre-calculation:**
- **Circular validation risk** — if the pipeline has a bug, both the pre-calculated baseline and the LLM's live query run against the same broken pipeline. You compare two wrong numbers, get a "pass," and the bad number ships. Faster, but not safer.
- **Coverage gap** — you can only validate metrics you thought to pre-calculate. Novel LLM questions have no pre-calculated baseline.
- **False authority** — machine-calculated numbers look as authoritative as human-approved ones in the store. You've encoded machine judgment, not tribal knowledge.

**The recommended pattern — Human-Gated Pre-Calculation:**

```
Scheduled Agent  →  Calculates metric snapshots at period close
       ↓
Surfaces for review  →  Slack notification / lightweight dashboard
       ↓
Human stamps it  →  "Looks right" (one click, not a full audit)
       ↓
Approved Numbers Store  ←  Carries human judgment, not just machine output
```

The agent does the heavy lifting. The human provides the judgment stamp at the business moments that matter — close, QBR, board prep. Pre-calculation gives you speed. Human gating gives you signal. Together, they break the circular validation problem and encode tribal knowledge systematically.

---

*Add new questions here as they come up in conversations, reviews, or conference Q&A.*
