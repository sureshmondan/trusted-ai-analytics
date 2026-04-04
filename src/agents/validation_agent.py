"""
Validation Agent — The Core of Lucid Analytics

Responsibilities:
  - Run five parallel validation checks against the SQL result
  - Compute a confidence score (0–100) based on check outcomes
  - Produce flags, explanations, and lineage for each check
  - Return a ValidatedResult for the Presentation Agent

The Five Validation Checks:
  1. Approved Numbers    — Compare result vs. analyst-verified approved_numbers store
  2. Temporal Trends     — Is value within expected range vs. prior periods?
  3. Cross-Metric        — Do correlated metrics (KG-defined) move together as expected?
  4. Source Agreement    — Does this number match across multiple source systems?
  5. Known Adjustments   — Does the KG contain a known event explaining any deviation?

Design Note:
  These checks run in parallel. Each check is independently configurable and can be
  disabled per metric if not applicable. The confidence score starts at 100 and each
  failed check deducts a configured penalty. Explained deviations (check 5) can
  restore partial confidence.

  This is what Snowflake VQR and Databricks Trusted Answers do NOT do.
  They verify the query. This agent verifies the result.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class CheckStatus(Enum):
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    EXPLAINED = "explained"   # deviation present but a known reason was found in KG


@dataclass
class CheckResult:
    """Outcome of a single validation check."""
    check_name: str
    status: CheckStatus
    confidence_delta: int          # negative = deduct, positive = restore
    detail: str = ""               # human-readable explanation
    evidence: dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidatedResult:
    """Full output from the Validation Agent."""
    sql_result_id: str
    confidence_score: int          # 0–100
    check_results: list[CheckResult] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)
    is_trustworthy: bool = False   # confidence >= threshold (default: 75)
    explanation_summary: str = ""


class ValidationAgent:
    """
    Validates SQL results against five checks and produces a confidence-scored
    ValidatedResult with flags and lineage.
    """

    CONFIDENCE_THRESHOLD = 75

    def __init__(self, approved_numbers_store, knowledge_graph, data_quality_rules):
        self.approved_numbers = approved_numbers_store
        self.knowledge_graph = knowledge_graph
        self.dq_rules = data_quality_rules

    def run(self, sql_result) -> ValidatedResult:
        """
        Run all five validation checks and return a ValidatedResult.

        Args:
            sql_result: SQLResult from the SQL Agent.

        Returns:
            ValidatedResult with confidence score, flags, and check details.
        """
        raise NotImplementedError("ValidationAgent.run() — implementation pending")

    def _check_approved_numbers(self, sql_result) -> CheckResult:
        """Check 1: Compare result against the Approved Numbers Store."""
        raise NotImplementedError

    def _check_temporal_trends(self, sql_result) -> CheckResult:
        """Check 2: Validate result against prior-period trend baseline."""
        raise NotImplementedError

    def _check_cross_metric_consistency(self, sql_result) -> CheckResult:
        """Check 3: Verify correlated metrics (from KG) move in expected directions."""
        raise NotImplementedError

    def _check_source_agreement(self, sql_result) -> CheckResult:
        """Check 4: Confirm the number matches across source systems."""
        raise NotImplementedError

    def _check_known_adjustments(self, sql_result) -> CheckResult:
        """Check 5: Look up KG for known events that explain any deviation."""
        raise NotImplementedError
