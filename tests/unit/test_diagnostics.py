"""Unit tests for diagnostics helpers."""

from __future__ import annotations

from sansavrm_mujoco_adapter.diagnostics import Diagnostic, make_diagnostics


def test_diagnostic_to_dict_contains_required_fields() -> None:
    """Verify that Diagnostic.to_dict returns schema-oriented fields."""
    diagnostic = Diagnostic(
        diagnostic_id="diag-000001",
        severity="info",
        category="adapter_artifact",
        code="D-ADAPTER-001",
        message="Separated command_delay_ms into controller_config.",
        target_type="actuator",
        target_id="left_knee_servo",
        source="controller_config_writer",
        detail={"parameter": "command_delay_ms"},
    )

    data = diagnostic.to_dict()

    assert data["diagnostic_id"] == "diag-000001"
    assert data["severity"] == "info"
    assert data["category"] == "adapter_artifact"
    assert data["detail"] == {"parameter": "command_delay_ms"}


def test_make_diagnostics_builds_root_object() -> None:
    """Verify that make_diagnostics returns a diagnostics root object."""
    diagnostic = Diagnostic(
        diagnostic_id="diag-000001",
        severity="info",
        category="adapter_artifact",
        code="D-ADAPTER-001",
        message="Separated command_delay_ms into controller_config.",
        target_type="actuator",
        target_id="left_knee_servo",
        source="controller_config_writer",
        detail={},
    )

    root = make_diagnostics([diagnostic])

    assert "diagnostics" in root
    assert len(root["diagnostics"]) == 1
    assert root["diagnostics"][0]["diagnostic_id"] == "diag-000001"
