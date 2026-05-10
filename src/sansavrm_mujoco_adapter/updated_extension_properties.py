"""updated_extension_properties helpers for SansaVRM-MuJoCo-Adapter.

This module defines minimum data structures for building updated_extension_properties
objects. The artifact is used to return adapter or runtime-derived values as
SansaVRM Extension Property candidates without modifying SansaVRM Core semantics.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal


IoScope = Literal[
    "mjcf",
    "adapter_artifact",
    "runtime_artifact",
    "both",
    "preserve_only",
    "unsupported",
    "source_raw",
]


@dataclass(frozen=True)
class UpdatedExtensionProperty:
    """Single updated Extension Property candidate.

    Attributes:
        extension_property_id: Stable identifier for the Extension Property candidate.
        namespace: Extension namespace such as mujoco or meridian.
        target_type: Target type of this Extension Property.
        target_id: Target identifier, or None for model/runtime-wide properties.
        property_role: Semantic role of the property.
        io_scope: Output or preservation scope.
        adapter_scope: Adapter or runtime scope that handles this property.
        source_format: Source format name.
        source_raw: Raw source value, when available.
        normalized_value: Normalized value for adapter/runtime use.
        schema_ref: Schema reference for this property, or None when unavailable.
        diagnostics_ref: Related diagnostic identifiers.
        conversion_report_ref: Related conversion report identifiers.
    """

    extension_property_id: str
    namespace: str
    target_type: str
    target_id: str | None
    property_role: str
    io_scope: IoScope
    adapter_scope: str
    source_format: str
    source_raw: Any = None
    normalized_value: Any = None
    schema_ref: str | None = None
    diagnostics_ref: list[str] = field(default_factory=list)
    conversion_report_ref: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class UpdatedExtensionProperties:
    """Root updated_extension_properties artifact.

    Attributes:
        schema_version: updated_extension_properties schema version.
        extension_properties: Extension Property candidates.
    """

    schema_version: str
    extension_properties: list[UpdatedExtensionProperty]

    def to_dict(self) -> dict[str, Any]:
        """Convert the artifact into a JSON-serializable dictionary.

        Returns:
            JSON-serializable updated_extension_properties dictionary.
        """
        return asdict(self)
