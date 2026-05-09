"""controller_config fixture tests.

This module verifies the minimum controller_config fixture before the adapter
implementation is added. Each test maps to a documented T-CONTROLLERCONFIG test
number.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPOSITORY_ROOT / "schemas" / "controller_config.schema.json"
FIXTURE_PATH = (
    REPOSITORY_ROOT
    / "tests"
    / "fixtures"
    / "controller_config"
    / "minimal_controller_config.json"
)


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


def _load_controller_config() -> dict[str, Any]:
    """Load the minimum controller_config fixture.

    Returns:
        Parsed controller_config fixture.
    """
    return _load_json(FIXTURE_PATH)


def _first_actuator(config: dict[str, Any]) -> dict[str, Any]:
    """Return the first actuator object from a controller_config fixture.

    Args:
        config: Parsed controller_config fixture.

    Returns:
        First actuator object.
    """
    actuators = config["actuators"]
    assert isinstance(actuators, list)
    assert actuators, "controller_config must contain at least one actuator"
    actuator = actuators[0]
    assert isinstance(actuator, dict)
    return actuator


def _parameters(actuator: dict[str, Any]) -> dict[str, Any]:
    """Return actuator parameters from a controller_config actuator object.

    Args:
        actuator: Parsed actuator object.

    Returns:
        Parameters object.
    """
    parameters = actuator["parameters"]
    assert isinstance(parameters, dict)
    return parameters


def test_t_controllerconfig_001_generate_controller_config_fixture() -> None:
    """T-CONTROLLERCONFIG-001: Validate the minimum controller_config fixture."""
    schema = _load_json(SCHEMA_PATH)
    config = _load_controller_config()

    Draft202012Validator(schema).validate(config)
    assert config["schema_version"] == "0.1.0"
    assert config["target"]["adapter"] == "SansaVRM-MuJoCo-Adapter"
    assert isinstance(config["actuators"], list)


def test_t_controllerconfig_002_output_actuator_settings() -> None:
    """T-CONTROLLERCONFIG-002: Verify actuator-level settings are present."""
    actuator = _first_actuator(_load_controller_config())

    assert actuator["actuator_id"] == "left_knee_servo"
    assert actuator["target_joint"] == "left_knee"
    assert actuator["control_mode"] == "position"
    assert actuator["runtime_control_mode"] == "position_pid"
    assert isinstance(actuator["parameters"], dict)


def test_t_controllerconfig_003_output_command_delay() -> None:
    """T-CONTROLLERCONFIG-003: Verify command_delay is present in parameters."""
    actuator = _first_actuator(_load_controller_config())
    parameters = _parameters(actuator)

    assert parameters["command_delay_ms"] == 5


def test_t_controllerconfig_004_output_deadband() -> None:
    """T-CONTROLLERCONFIG-004: Verify deadband is present in parameters."""
    actuator = _first_actuator(_load_controller_config())
    parameters = _parameters(actuator)

    assert parameters["deadband_rad"] == 0.01


def test_t_controllerconfig_005_keep_diagnostics_ref() -> None:
    """T-CONTROLLERCONFIG-005: Verify diagnostics_ref is retained."""
    actuator = _first_actuator(_load_controller_config())

    assert actuator["diagnostics_ref"] == ["diag-000001"]


def test_t_controllerconfig_006_output_current_limit() -> None:
    """T-CONTROLLERCONFIG-006: Verify current_limit is present in parameters."""
    actuator = _first_actuator(_load_controller_config())
    parameters = _parameters(actuator)

    assert parameters["current_limit_a"] == 12.0


def test_t_controllerconfig_007_output_voltage_limit() -> None:
    """T-CONTROLLERCONFIG-007: Verify voltage_limit is present in parameters."""
    actuator = _first_actuator(_load_controller_config())
    parameters = _parameters(actuator)

    assert parameters["voltage_limit_v"] == 12.0
