"""
Approved Numbers Store — CRUD interface for the Validation Agent

The Approved Numbers Store is the dynamic benchmark used by the Validation Agent
to check whether a SQL result is within the range of analyst-approved figures.

Maintenance responsibility:
  - Analytics team and Finance maintain this store after each financial close.
  - The DE team owns the schema and the validation logic that reads from it.
  - New approved figures are inserted via the `add_approved_number()` method or
    direct SQL (e.g., from a dbt seed file or spreadsheet import).

Usage:
    store = ApprovedNumbersStore(db_connection)
    benchmark = store.get(metric_name="revenue", entity="global",
                          granularity="monthly", period="2026-01-01")
    if benchmark:
        deviation = abs(actual_value - benchmark.approved_value) / benchmark.approved_value
        if deviation > benchmark.tolerance_pct / 100:
            # flag the result
"""

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Any


@dataclass
class ApprovedNumber:
    """A single approved benchmark value."""
    id: int
    metric_name: str
    entity: str
    granularity: str
    period: date
    approved_value: Decimal
    tolerance_pct: Decimal
    approved_by: str
    approval_date: datetime
    source: str
    notes: str | None = None


class ApprovedNumbersStore:
    """
    Interface to the approved_numbers table.
    Used primarily by the Validation Agent's _check_approved_numbers() method.
    """

    def __init__(self, db_connection):
        self.db = db_connection

    def get(
        self,
        metric_name: str,
        entity: str,
        granularity: str,
        period: str | date,
    ) -> ApprovedNumber | None:
        """
        Retrieve the active approved value for a given metric + entity + period.

        Returns None if no approved figure exists (Validation Agent skips this check).
        """
        raise NotImplementedError("ApprovedNumbersStore.get() — implementation pending")

    def add(self, record: dict[str, Any]) -> ApprovedNumber:
        """
        Insert a new approved number. Supersedes any existing active record
        for the same metric/entity/granularity/period.
        """
        raise NotImplementedError("ApprovedNumbersStore.add() — implementation pending")

    def list_recent(self, metric_name: str, limit: int = 12) -> list[ApprovedNumber]:
        """
        Retrieve the most recent approved values for a metric (for trend context).
        """
        raise NotImplementedError("ApprovedNumbersStore.list_recent() — implementation pending")
