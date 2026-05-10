"""Unit tests for runtime_requirements helpers."""

from __future__ import annotations

from pathlib import Path

from jsonschema import Draft202012Validator

from sansavrm_mujoco_adapter.runtime_requirements import (
    RuntimeRequirementFlags,
    RuntimeRequirements,
    VersionRange,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPOSITORY_ROOT / "schemas" / "runtime_requirements.schema.json"


def _load_schema() -> dict[str, object]:
    """Load the runtime_requirements JSON schema.

    Returns:
        Parsed JSON schema object.
    """
    import json

    with SCHEMA_PATH.open("r", encoding="utf-8") as file:
        schema = json.load(file)

    assert isinstance(schema, dict)
    return schema


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


def test_runtime_requirements_to_dict_matches_schema() -> None:
    """Verify that RuntimeRequirements.to_dict output matches the JSON schema."""
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

    Draft202012Validator(_load_schema()).validate(runtime_requirements.to_dict())
