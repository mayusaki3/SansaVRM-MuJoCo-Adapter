"""Actuator mapping fixture tests.

This module verifies actuator mapping fixtures before adapter implementation is
added. The tests check expected mapping metadata, controller_config separation,
and unsupported control mode diagnostics.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
ACTUATOR_FIXTURE_DIR = REPOSITORY_ROOT / "tests" / "fixtures" / "actuator"

SUPPORTED_CONTROL_MODE_TO_MJCF_ACTUATOR = {
    "position": "position",
    "velocity": "velocity",
    "torque": "motor",
    "force": "motor",
    "external_controller": "motor",
}


def _load_fixture(name: str) -> dict[str, Any]:
    """Load an actuator fixture JSON file.

    Args:
        name: Fixture file name.

    Returns:
        Parsed actuator fixture.

    Raises:
        AssertionError: If the parsed JSON root is not an object.
    """
    path = ACTUATOR_FIXTURE_DIR / name
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    assert isinstance(data, dict), f"Fixture root must be an object: {path}"
    return data


def _custom_parameter_names(fixture: dict[str, Any]) -> set[str]:
    """Return custom parameter names from an actuator fixture.

    Args:
        fixture: Parsed actuator fixture.

    Returns:
        Set of custom parameter names.
    """
    custom_parameters = fixture.get("custom_parameters", [])
    assert isinstance(custom_parameters, list)
    return {parameter["name"] for parameter in custom_parameters}


def _assert_expected_mjcf_actuator(fixture: dict[str, Any]) -> None:
    """Assert that fixture control_mode matches expected MJCF actuator type.

    Args:
        fixture: Parsed actuator fixture.
    """
    control_mode = fixture["control_mode"]
    expected = fixture["expected"]
    assert expected["mjcf_actuator_type"] == SUPPORTED_CONTROL_MODE_TO_MJCF_ACTUATOR[control_mode]


def test_t_actuator_001_position_actuator_mapping_fixture() -> None:
    """T-ACTUATOR-001: Verify position actuator mapping fixture metadata."""
    fixture = _load_fixture("position_actuator.json")

    assert fixture["control_mode"] == "position"
    _assert_expected_mjcf_actuator(fixture)
    assert fixture["expected"]["mjcf_actuator_type"] == "position"
    assert "position_limit_rad" in fixture
    assert "kp" in fixture


def test_t_actuator_002_velocity_actuator_mapping_fixture() -> None:
    """T-ACTUATOR-002: Verify velocity actuator mapping fixture metadata."""
    fixture = _load_fixture("velocity_actuator.json")

    assert fixture["control_mode"] == "velocity"
    _assert_expected_mjcf_actuator(fixture)
    assert fixture["expected"]["mjcf_actuator_type"] == "velocity"
    assert "velocity_limit_rad_s" in fixture
    assert set(fixture["expected"]["mjcf_attributes"]) == {"kv", "ctrlrange"}


def test_t_actuator_003_torque_actuator_mapping_fixture() -> None:
    """T-ACTUATOR-003: Verify torque actuator mapping fixture metadata."""
    fixture = _load_fixture("torque_actuator.json")

    assert fixture["control_mode"] == "torque"
    _assert_expected_mjcf_actuator(fixture)
    assert fixture["expected"]["mjcf_actuator_type"] == "motor"
    assert set(fixture["expected"]["mjcf_attributes"]) == {"gear", "forcerange"}


def test_t_actuator_004_command_delay_separation_fixture() -> None:
    """T-ACTUATOR-004: Verify command_delay is expected in controller_config."""
    fixture = _load_fixture("position_actuator.json")

    assert "command_delay_ms" in _custom_parameter_names(fixture)
    assert "command_delay_ms" in fixture["expected"]["controller_config_parameters"]


def test_t_actuator_005_deadband_separation_fixture() -> None:
    """T-ACTUATOR-005: Verify deadband is expected in controller_config."""
    fixture = _load_fixture("position_actuator.json")

    assert "deadband_rad" in _custom_parameter_names(fixture)
    assert "deadband_rad" in fixture["expected"]["controller_config_parameters"]


def test_t_actuator_006_torque_limit_mapping_fixture() -> None:
    """T-ACTUATOR-006: Verify torque_limit fixture mapping expectations."""
    fixture = _load_fixture("torque_actuator.json")

    assert fixture["torque_limit_nm"] > 0
    assert "torque_limit_nm" in _custom_parameter_names(fixture)
    assert "forcerange" in fixture["expected"]["mjcf_attributes"]


def test_t_actuator_007_unsupported_control_mode_diagnostics_fixture() -> None:
    """T-ACTUATOR-007: Verify unsupported control mode expected diagnostics."""
    fixture = _load_fixture("unsupported_control_mode.json")
    expected = fixture["expected"]
    diagnostic = expected["diagnostics"][0]

    assert fixture["control_mode"] not in SUPPORTED_CONTROL_MODE_TO_MJCF_ACTUATOR
    assert expected["mjcf_actuator_type"] is None
    assert expected["conversion_report_status"] == "skipped"
    assert diagnostic["severity"] == "error"
    assert diagnostic["category"] == "unsupported"
    assert diagnostic["target_type"] == "actuator"
    assert diagnostic["target_id"] == fixture["actuator_id"]
