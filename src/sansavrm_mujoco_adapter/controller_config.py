"""controller_config helpers for SansaVRM-MuJoCo-Adapter.

This module defines minimum data structures for building controller_config
objects. The structures are intentionally small and schema-oriented so that they
can be extended after the adapter writer is implemented.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal


ControlMode = Literal["position", "velocity", "torque", "force", "external_controller"]
RuntimeControlMode = Literal[
    "none",
    "position_pid",
    "velocity_pid",
    "torque_passthrough",
    "external",
]


@dataclass(frozen=True)
class ControllerTarget:
    """Target information for a controller_config artifact.

    Attributes:
        adapter: Adapter name that produced the artifact.
        mujoco_version: Target MuJoCo version, or None when unspecified.
    """

    adapter: str
    mujoco_version: str | None = None


@dataclass(frozen=True)
class ControllerActuator:
    """Actuator entry in a controller_config artifact.

    Attributes:
        actuator_id: Adapter-level actuator identifier.
        target_joint: Target joint name.
        control_mode: Source control mode.
        runtime_control_mode: Runtime control mode used by the adapter runtime.
        parameters: Controller-side parameters that are not directly represented in MJCF.
        diagnostics_ref: Diagnostic identifiers related to this actuator.
    """

    actuator_id: str
    target_joint: str
    control_mode: ControlMode
    runtime_control_mode: RuntimeControlMode
    parameters: dict[str, Any] = field(default_factory=dict)
    diagnostics_ref: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ControllerConfig:
    """Root controller_config artifact.

    Attributes:
        schema_version: controller_config schema version.
        target: Target adapter and MuJoCo version information.
        actuators: Actuator entries.
    """

    schema_version: str
    target: ControllerTarget
    actuators: list[ControllerActuator]

    def to_dict(self) -> dict[str, Any]:
        """Convert the controller_config into a JSON-serializable dictionary.

        Returns:
            JSON-serializable controller_config dictionary.
        """
        return asdict(self)
