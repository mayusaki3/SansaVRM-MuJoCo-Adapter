"""Unit tests for runtime_requirements helpers."""

from __future__ import annotations

from sansavrm_mujoco_adapter.runtime_requirements import (
    RuntimeRequirementFlags,
    RuntimeRequirements,
    VersionRange,
)


def test_runtime_requirements_to_dict_contains_required_structure() -> None:
    """Verify that RuntimeRequirements.to_dict returns schema-oriented fields."""
    runtime_requirements = RuntimeRequirements(
        schema_version="0.1.0",
        required_runtime="meridian_mujoco_runtime",
        required_runtime_version=VersionRange(min="0.1.0", max=None),
        requirements=RuntimeRequirementFlags(
            requires_external_control_loop=True,
            requires_sysid_result=False,
            requires_hil=False,
            requires_sil=True,
            requires_sensor_frame=True,
            requires_contact_events=False,
            requires_device_raw_mapping=False,
        ),
        required_features=["controller_config", "sensor_frame"],
        unsupported_without_runtime=[],
        diagnostics_ref=["diag-000002"],
    )

    data = runtime_requirements.to_dict()

    assert data["schema_version"] == "0.1.0"
    assert data["required_runtime"] == "meridian_mujoco_runtime"
    assert data["required_runtime_version"]["min"] == "0.1.0"
    assert data["required_runtime_version"]["max"] is None
    assert data["requirements"]["requires_external_control_loop"] is True
    assert data["requirements"]["requires_sil"] is True
    assert data["required_features"] == ["controller_config", "sensor_frame"]
    assert data["diagnostics_ref"] == ["diag-000002"]
