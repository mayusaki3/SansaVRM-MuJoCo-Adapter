"""Unit tests for controller_config helpers."""

from __future__ import annotations

from sansavrm_mujoco_adapter.controller_config import (
    ControllerActuator,
    ControllerConfig,
    ControllerTarget,
)


def test_controller_config_to_dict_contains_required_structure() -> None:
    """Verify that ControllerConfig.to_dict returns schema-oriented fields."""
    config = ControllerConfig(
        schema_version="0.1.0",
        target=ControllerTarget(
            adapter="SansaVRM-MuJoCo-Adapter",
            mujoco_version=None,
        ),
        actuators=[
            ControllerActuator(
                actuator_id="left_knee_servo",
                target_joint="left_knee",
                control_mode="position",
                runtime_control_mode="position_pid",
                parameters={
                    "command_delay_ms": 5,
                    "deadband_rad": 0.01,
                },
                diagnostics_ref=["diag-000001"],
            )
        ],
    )

    data = config.to_dict()

    assert data["schema_version"] == "0.1.0"
    assert data["target"]["adapter"] == "SansaVRM-MuJoCo-Adapter"
    assert data["target"]["mujoco_version"] is None
    assert data["actuators"][0]["actuator_id"] == "left_knee_servo"
    assert data["actuators"][0]["parameters"]["command_delay_ms"] == 5
    assert data["actuators"][0]["diagnostics_ref"] == ["diag-000001"]
