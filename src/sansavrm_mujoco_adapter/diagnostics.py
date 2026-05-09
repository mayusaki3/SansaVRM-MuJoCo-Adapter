"""Diagnostics helpers for SansaVRM-MuJoCo-Adapter.

This module defines a small diagnostic data structure used by adapter-side
validation and conversion code. The structure mirrors the minimum diagnostics
schema used by the repository fixtures.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal


DiagnosticSeverity = Literal["info", "warning", "error", "fatal"]
DiagnosticCategory = Literal[
    "input",
    "schema",
    "mapping",
    "mjcf",
    "adapter_artifact",
    "version",
    "fallback",
    "non_reversible",
    "unsupported",
    "output",
    "runtime",
]


@dataclass(frozen=True)
class Diagnostic:
    """Single diagnostic entry.

    Attributes:
        diagnostic_id: Stable identifier for the diagnostic entry.
        severity: Diagnostic severity.
        category: Diagnostic category.
        code: Machine-readable diagnostic code.
        message: Human-readable diagnostic message.
        target_type: Type of the diagnostic target.
        target_id: Identifier of the diagnostic target, or None for global items.
        source: Component that produced the diagnostic.
        detail: Additional machine-readable diagnostic details.
    """

    diagnostic_id: str
    severity: DiagnosticSeverity
    category: DiagnosticCategory
    code: str
    message: str
    target_type: str
    target_id: str | None
    source: str
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert the diagnostic entry into a JSON-serializable dictionary.

        Returns:
            JSON-serializable diagnostic dictionary.
        """
        return asdict(self)


def make_diagnostics(entries: list[Diagnostic]) -> dict[str, Any]:
    """Build the root diagnostics object from diagnostic entries.

    Args:
        entries: Diagnostic entries to include.

    Returns:
        Diagnostics root object compatible with diagnostics.schema.json.
    """
    return {"diagnostics": [entry.to_dict() for entry in entries]}
