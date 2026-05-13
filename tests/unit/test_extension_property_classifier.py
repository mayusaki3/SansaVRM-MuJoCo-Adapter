"""Unit tests for the draft Extension Property classifier."""

from __future__ import annotations

from sansavrm_mujoco_adapter.extension_property_classifier import (
    classify_extension_properties,
    classify_extension_property,
)


def _extension_property(io_scope: str, adapter_scope: str) -> dict[str, object]:
    """Create a minimum draft Extension Property dictionary for classifier tests.

    Args:
        io_scope: Draft io_scope value.
        adapter_scope: Draft adapter_scope value.

    Returns:
        Extension Property-like dictionary.
    """
    return {
        "extension_property_id": f"ext-{io_scope}-{adapter_scope}",
        "namespace": "mujoco",
        "target_type": "actuator",
        "target_id": "left_knee_servo",
        "property_role": "control",
        "io_scope": io_scope,
        "adapter_scope": adapter_scope,
        "source_format": "sansavrm_extension_property",
        "source_raw": None,
        "normalized_value": {"value": 1},
        "schema_ref": "schemas/example.schema.json",
    }


def test_classify_extension_property_mjcf() -> None:
    """T-EXTENSIONPROPERTY-001: io_scope=mjcf is classified as mjcf."""
    result = classify_extension_property(_extension_property("mjcf", "sansavrm_mujoco_adapter"))

    assert result.classification_target == "mjcf"
    assert result.is_draft is True
    assert "io_scope=mjcf" in result.reason


def test_classify_extension_property_adapter_artifact() -> None:
    """T-EXTENSIONPROPERTY-002: io_scope=adapter_artifact is classified as adapter_artifact."""
    result = classify_extension_property(
        _extension_property("adapter_artifact", "sansavrm_mujoco_adapter")
    )

    assert result.classification_target == "adapter_artifact"


def test_classify_extension_property_runtime_artifact_by_io_scope() -> None:
    """T-EXTENSIONPROPERTY-003: io_scope=runtime_artifact is classified as runtime_artifact."""
    result = classify_extension_property(
        _extension_property("runtime_artifact", "sansavrm_mujoco_adapter")
    )

    assert result.classification_target == "runtime_artifact"


def test_classify_extension_property_runtime_artifact_by_adapter_scope() -> None:
    """T-EXTENSIONPROPERTY-006: meridian_mujoco_runtime scope is classified as runtime_artifact."""
    result = classify_extension_property(
        _extension_property("adapter_artifact", "meridian_mujoco_runtime")
    )

    assert result.classification_target == "runtime_artifact"


def test_classify_extension_property_preserve_only() -> None:
    """T-EXTENSIONPROPERTY-004: io_scope=preserve_only is classified as preserve_only."""
    result = classify_extension_property(_extension_property("preserve_only", "preserve_only"))

    assert result.classification_target == "preserve_only"


def test_classify_extension_property_nisocon_scope_is_preserve_only() -> None:
    """T-EXTENSIONPROPERTY-006: nisocon scope is preserved by the adapter."""
    result = classify_extension_property(
        _extension_property("adapter_artifact", "nisocon_vr_battle_runtime")
    )

    assert result.classification_target == "preserve_only"


def test_classify_extension_property_source_raw() -> None:
    """T-EXTENSIONPROPERTY-005: io_scope=source_raw is classified as source_raw."""
    result = classify_extension_property(_extension_property("source_raw", "unknown"))

    assert result.classification_target == "source_raw"


def test_classify_extension_property_unsupported() -> None:
    """T-EXTENSIONPROPERTY-007: unknown io_scope is classified as unsupported."""
    result = classify_extension_property(_extension_property("unknown", "unknown"))

    assert result.classification_target == "unsupported"


def test_classify_extension_properties_report_contains_warning() -> None:
    """Verify that the draft classifier report includes a draft warning."""
    report = classify_extension_properties(
        [
            _extension_property("mjcf", "sansavrm_mujoco_adapter"),
            _extension_property("runtime_artifact", "meridian_mujoco_runtime"),
        ]
    )
    data = report.to_dict()

    assert data["schema_status"] == "draft"
    assert len(data["classifications"]) == 2
    assert data["warnings"]
    assert "draft Adapter input schema" in data["warnings"][0]
