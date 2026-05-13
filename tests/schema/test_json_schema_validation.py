"""JSON schema validation tests for SansaVRM-MuJoCo-Adapter.

This module verifies that the minimum JSON fixtures conform to the JSON schemas
used by the adapter. Each test function maps to a documented test target for
schema validation and keeps the fixtures usable before adapter implementation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = REPOSITORY_ROOT / "schemas"
FIXTURE_DIR = REPOSITORY_ROOT / "tests" / "fixtures"


def _load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object from disk.

    Args:
        path: Path to the JSON file.

    Returns:
        Parsed JSON object.

    Raises:
        AssertionError: If the parsed JSON value is not an object.
    """
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    assert isinstance(data, dict), f"JSON root must be an object: {path}"
    return data


def _validate_json(schema_path: Path, fixture_path: Path) -> None:
    """Validate a fixture JSON object with a JSON schema.

    Args:
        schema_path: Path to the JSON schema file.
        fixture_path: Path to the fixture JSON file.

    Raises:
        jsonschema.exceptions.ValidationError: If the fixture is invalid.
    """
    schema = _load_json(schema_path)
    fixture = _load_json(fixture_path)
    validator = Draft202012Validator(schema)
    validator.validate(fixture)


def test_t_controllerconfig_001_minimal_controller_config_matches_schema() -> None:
    """T-CONTROLLERCONFIG-001: Validate the minimum controller_config fixture."""
    _validate_json(
        SCHEMA_DIR / "controller_config.schema.json",
        FIXTURE_DIR / "controller_config" / "minimal_controller_config.json",
    )


def test_t_diagnostics_001_minimal_diagnostics_matches_schema() -> None:
    """T-DIAGNOSTICS-001: Validate the minimum diagnostics fixture."""
    _validate_json(
        SCHEMA_DIR / "diagnostics.schema.json",
        FIXTURE_DIR / "diagnostics" / "minimal_diagnostics.json",
    )


def test_t_runtimerequirements_001_minimal_runtime_requirements_matches_schema() -> None:
    """T-RUNTIMEREQUIREMENTS-001: Validate the minimum runtime_requirements fixture."""
    _validate_json(
        SCHEMA_DIR / "runtime_requirements.schema.json",
        FIXTURE_DIR / "runtime_requirements" / "minimal_runtime_requirements.json",
    )


def test_t_updatedextensionproperties_001_minimal_updated_extension_properties_matches_schema() -> None:
    """T-UPDATEDEXTENSIONPROPERTIES-001: Validate the minimum updated_extension_properties fixture."""
    _validate_json(
        SCHEMA_DIR / "updated_extension_properties.schema.json",
        FIXTURE_DIR
        / "updated_extension_properties"
        / "minimal_updated_extension_properties.json",
    )


def test_t_sansavrminput_001_minimal_adapter_input_matches_draft_schema() -> None:
    """T-SANSAVRMINPUT-001: Validate the minimum draft Adapter input fixture."""
    _validate_json(
        SCHEMA_DIR / "sansavrm_adapter_input.schema.draft.json",
        FIXTURE_DIR / "sansavrm_adapter_input" / "minimal_sansavrm_adapter_input.json",
    )
