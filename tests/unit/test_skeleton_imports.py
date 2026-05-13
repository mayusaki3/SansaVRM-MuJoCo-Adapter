"""Unit tests for package skeleton imports.

These tests verify that the initial adapter package skeleton can be imported
before detailed adapter implementation is added.
"""

from __future__ import annotations

import sansavrm_mujoco_adapter
from sansavrm_mujoco_adapter import (
    controller_config,
    diagnostics,
    extension_property_classifier,
    mjcf_loader,
    runtime_requirements,
    updated_extension_properties,
)


def test_package_has_version() -> None:
    """Verify that the package exposes a non-empty version string."""
    assert isinstance(sansavrm_mujoco_adapter.__version__, str)
    assert sansavrm_mujoco_adapter.__version__


def test_skeleton_modules_are_importable() -> None:
    """Verify that skeleton modules are importable."""
    assert diagnostics is not None
    assert controller_config is not None
    assert mjcf_loader is not None
    assert runtime_requirements is not None
    assert updated_extension_properties is not None
    assert extension_property_classifier is not None
