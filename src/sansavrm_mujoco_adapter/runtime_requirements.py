"""runtime_requirements helpers for SansaVRM-MuJoCo-Adapter.

This module defines minimum data structures for building runtime_requirements
objects. The artifact is used to describe requirements for external runtimes such
as meridian-mujoco-runtime without implementing those runtimes in this adapter.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class VersionRange:
    """Version range for an external runtime requirement.

    Attributes:
        min: Minimum required version, or None when unspecified.
        max: Maximum supported version, or None when unspecified.
    """

    min: str | None = None
    max: str | None = None


@dataclass(frozen=True)
class RuntimeRequirementFlags:
    """Runtime feature requirement flags.

    Attributes:
        requires_external_control_loop: Whether an external control loop is required.
        requires_sysid_result: Whether sysid_result data is required.
        requires_hil: Whether HIL support is required.
        requires_sil: Whether SIL support is required.
        requires_sensor_frame: Whether sensor frame output is required.
        requires_contact_events: Whether contact event output is required.
        requires_device_raw_mapping: Whether device raw mapping is required.
    """

    requires_external_control_loop: bool = False
    requires_sysid_result: bool = False
    requires_hil: bool = False
    requires_sil: bool = False
    requires_sensor_frame: bool = False
    requires_contact_events: bool = False
    requires_device_raw_mapping: bool = False


@dataclass(frozen=True)
class RuntimeRequirements:
    """Root runtime_requirements artifact.

    Attributes:
        schema_version: runtime_requirements schema version.
        required_runtime: Required external runtime name.
        required_runtime_version: Required runtime version range, or None when unspecified.
        requirements: Runtime requirement flags.
        required_features: Required named runtime features.
        unsupported_without_runtime: Features that are unsupported without the runtime.
        diagnostics_ref: Diagnostic identifiers related to the runtime requirements.
    """

    schema_version: str
    required_runtime: str
    required_runtime_version: VersionRange | None
    requirements: RuntimeRequirementFlags
    required_features: list[str] = field(default_factory=list)
    unsupported_without_runtime: list[str] = field(default_factory=list)
    diagnostics_ref: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        """Convert the runtime_requirements into a JSON-serializable dictionary.

        Returns:
            JSON-serializable runtime_requirements dictionary.
        """
        return asdict(self)
