"""Unit tests for updated_extension_properties helpers."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from sansavrm_mujoco_adapter.updated_extension_properties import (
    UpdatedExtensionProperties,
    UpdatedExtensionProperty,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPOSITORY_ROOT / "schemas" / "updated_extension_properties.schema.json"


def _load_schema() -> dict[str, object]:
    """Load the updated_extension_properties JSON schema.

    Returns:
        Parsed JSON schema object.
    """
    with SCHEMA_PATH.open("r", encoding="utf-8") as file:
        schema = json.load(file)

    assert isinstance(schema, dict)
    return schema


def _create_artifact() -> UpdatedExtensionProperties:
    """Create a minimum updated_extension_properties artifact for tests.

    Returns:
        Minimum updated_extension_properties artifact.
    """
    return UpdatedExtensionProperties(
        schema_version="0.1.0",
        extension_properties=[
            UpdatedExtensionProperty(
                extension_property_id="ext-prop-000001",
                namespace="mujoco",
                target_type="actuator",
                target_id="left_knee_servo",
                property_role="control",
                io_scope="adapter_artifact",
                adapter_scope="sansavrm_mujoco_adapter",
                source_format="sansavrm_extension_property",
                source_raw=None,
                normalized_value={"command_delay_ms": 5},
                schema_ref="schemas/extension_property/mujoco/control/command_delay.schema.json",
                diagnostics_ref=["diag-000001"],
                conversion_report_ref=["conv-000001"],
            )
        ],
    )


def test_updated_extension_properties_to_dict_contains_required_structure() -> None:
    """Verify that UpdatedExtensionProperties.to_dict returns schema-oriented fields."""
    data = _create_artifact().to_dict()
    extension_property = data["extension_properties"][0]

    assert data["schema_version"] == "0.1.0"
    assert extension_property["extension_property_id"] == "ext-prop-000001"
    assert extension_property["namespace"] == "mujoco"
    assert extension_property["target_type"] == "actuator"
    assert extension_property["target_id"] == "left_knee_servo"
    assert extension_property["io_scope"] == "adapter_artifact"
    assert extension_property["normalized_value"] == {"command_delay_ms": 5}
    assert extension_property["diagnostics_ref"] == ["diag-000001"]
    assert extension_property["conversion_report_ref"] == ["conv-000001"]


def test_updated_extension_properties_to_dict_matches_schema() -> None:
    """Verify that UpdatedExtensionProperties.to_dict output matches the JSON schema."""
    Draft202012Validator(_load_schema()).validate(_create_artifact().to_dict())
