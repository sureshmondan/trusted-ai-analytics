"""
Presentation Agent — Confidence Scoring and Response Assembly

Responsibilities:
  - Assemble the final response from a ValidatedResult
  - Adjust tone and prominence of caveats based on confidence score
  - Include answer, confidence score, lineage summary, active flags, and follow-up suggestions
  - Format for multiple consumer surfaces (chat, API, dashboard annotation)

Response Tone Guidelines:
  - confidence >= 90: Direct answer. Lineage available but not foregrounded.
  - confidence 75–89: Answer with brief note. Flags mentioned once, not alarmist.
  - confidence 50–74: Answer with prominent caveats. Flags foregrounded. Analyst must review.
  - confidence < 50: Do not return a number as fact. Surface flags, request analyst review.

Design Note:
  The Presentation Agent must never suppress flags. Low-confidence answers should be
  unmistakably caveated. The analyst makes the final call on flagged results.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AnalyticsResponse:
    """Final response for the analyst surface."""
    question: str
    answer: str                        # human-readable result with context
    value: Any                         # the raw numeric/tabular result
    confidence_score: int              # 0–100
    is_trustworthy: bool
    flags: list[str] = field(default_factory=list)
    lineage_summary: str = ""
    follow_up_suggestions: list[str] = field(default_factory=list)
    format: str = "chat"               # 'chat', 'api', 'dashboard'


class PresentationAgent:
    """
    Assembles the final analyst-facing response from a ValidatedResult.
    Adjusts tone and caveats based on confidence score.
    """

    def __init__(self, llm):
        self.llm = llm

    def run(self, validated_result, original_question: str) -> AnalyticsResponse:
        """
        Assemble and format the final response.

        Args:
            validated_result: ValidatedResult from the Validation Agent.
            original_question: The original natural language question.

        Returns:
            AnalyticsResponse ready for delivery to the analyst surface.
        """
        raise NotImplementedError("PresentationAgent.run() — implementation pending")

    def _format_confidence_narrative(self, confidence_score: int, flags: list[str]) -> str:
        """
        Generate the confidence narrative string based on score and flags.
        High confidence = minimal caveat. Low confidence = prominent warning.
        """
        raise NotImplementedError
