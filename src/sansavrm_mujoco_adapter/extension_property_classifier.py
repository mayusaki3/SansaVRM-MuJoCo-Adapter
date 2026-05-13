"""Draft Extension Property classifier for SansaVRM-MuJoCo-Adapter.

This module classifies Extension Property-like dictionaries from the draft
SansaVRM Adapter input schema. The implementation is intentionally limited to
adapter-side draft behavior and must be revalidated after the canonical SansaVRM
schema is finalized.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal


ClassificationTarget = Literal[
    "mjcf",
    "adapter_artifact",
    "runtime_artifact",
    "preserve_only",
    "unsupported",
    "source_raw",
]


@dataclass(frozen=True)
class ExtensionPropertyClassification:
    """Classification result for one Extension Property.

    Attributes:
        extension_property_id: Identifier of the classified Extension Property.
        namespace: Extension namespace.
        target_type: Target type from the Extension Property.
        target_id: Target identifier from the Extension Property.
        property_role: Semantic role from the Extension Property.
        io_scope: Output or preservation scope from the Extension Property.
        adapter_scope: Adapter or runtime scope from the Extension Property.
        classification_target: Adapter-side classification target.
        reason: Human-readable classification reason.
        is_draft: True because this classifier follows the draft input schema.
    """

    extension_property_id: str
    namespace: str
    target_type: str
    target_id: str | None
    property_role: str
    io_scope: str
    adapter_scope: str
    classification_target: ClassificationTarget
    reason: str
    is_draft: bool = True

    def to_dict(self) -> dict[str, Any]:
        """Convert the classification result into a JSON-serializable dictionary.

        Returns:
            JSON-serializable classification dictionary.
        """
        return asdict(self)


@dataclass(frozen=True)
class ExtensionPropertyClassificationReport:
    """Collection of Extension Property classification results.

    Attributes:
        schema_status: Classification schema status. This is always draft.
        classifications: Classification results.
        warnings: Non-fatal classifier warnings.
    """

    schema_status: str = "draft"
    classifications: list[ExtensionPropertyClassification] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert the classification report into a JSON-serializable dictionary.

        Returns:
            JSON-serializable classification report dictionary.
        """
        return {
            "schema_status": self.schema_status,
            "classifications": [item.to_dict() for item in self.classifications],
            "warnings": list(self.warnings),
        }


def classify_extension_property(extension_property: dict[str, Any]) -> ExtensionPropertyClassification:
    """Classify a single Extension Property dictionary.

    Args:
        extension_property: Extension Property-like dictionary following the draft
            Adapter input schema.

    Returns:
        Classification result.

    Raises:
        KeyError: If a required draft field is missing.
    """
    io_scope = str(extension_property["io_scope"])
    adapter_scope = str(extension_property["adapter_scope"])

    classification_target = _classify_target(io_scope=io_scope, adapter_scope=adapter_scope)
    reason = _build_reason(classification_target=classification_target, io_scope=io_scope, adapter_scope=adapter_scope)

    return ExtensionPropertyClassification(
        extension_property_id=str(extension_property["extension_property_id"]),
        namespace=str(extension_property["namespace"]),
        target_type=str(extension_property["target_type"]),
        target_id=extension_property.get("target_id"),
        property_role=str(extension_property["property_role"]),
        io_scope=io_scope,
        adapter_scope=adapter_scope,
        classification_target=classification_target,
        reason=reason,
    )


def classify_extension_properties(extension_properties: list[dict[str, Any]]) -> ExtensionPropertyClassificationReport:
    """Classify multiple Extension Property dictionaries.

    Args:
        extension_properties: Extension Property-like dictionaries.

    Returns:
        Classification report.
    """
    classifications = [classify_extension_property(item) for item in extension_properties]
    warnings = [
        "This classification report is based on a draft Adapter input schema and is not canonical SansaVRM behavior."
    ]
    return ExtensionPropertyClassificationReport(classifications=classifications, warnings=warnings)


def _classify_target(io_scope: str, adapter_scope: str) -> ClassificationTarget:
    """Return the adapter-side classification target.

    Args:
        io_scope: Draft io_scope value.
        adapter_scope: Draft adapter_scope value.

    Returns:
        Classification target.
    """
    if io_scope == "mjcf":
        return "mjcf"
    if io_scope == "adapter_artifact" or (io_scope == "both" and adapter_scope == "sansavrm_mujoco_adapter"):
        return "adapter_artifact"
    if io_scope == "runtime_artifact" or adapter_scope == "meridian_mujoco_runtime":
        return "runtime_artifact"
    if io_scope == "preserve_only" or adapter_scope in {"preserve_only", "nisocon_vr_battle_runtime"}:
        return "preserve_only"
    if io_scope == "source_raw":
        return "source_raw"
    return "unsupported"


def _build_reason(classification_target: ClassificationTarget, io_scope: str, adapter_scope: str) -> str:
    """Build a human-readable classification reason.

    Args:
        classification_target: Classification target.
        io_scope: Draft io_scope value.
        adapter_scope: Draft adapter_scope value.

    Returns:
        Classification reason.
    """
    return (
        f"classified as {classification_target} because io_scope={io_scope} "
        f"and adapter_scope={adapter_scope} in draft Adapter input schema"
    )
