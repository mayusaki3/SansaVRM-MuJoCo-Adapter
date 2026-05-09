"""MJCF loading tests.

This module verifies that MJCF sample files can be loaded by MuJoCo in headless
mode. Tests for samples that are not added yet are skipped until the fixtures are
created.
"""

from __future__ import annotations

from pathlib import Path

import mujoco
import pytest


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
MUJOCO_EXAMPLES_DIR = REPOSITORY_ROOT / "examples" / "mujoco"


def _require_sample(relative_path: str) -> Path:
    """Return a sample MJCF path or skip the test when it is not available.

    Args:
        relative_path: Path relative to the MuJoCo examples directory.

    Returns:
        Existing MJCF file path.
    """
    path = MUJOCO_EXAMPLES_DIR / relative_path
    if not path.exists():
        pytest.skip(f"MJCF sample is not available yet: {path}")
    return path


def _load_model(path: Path) -> mujoco.MjModel:
    """Load a MuJoCo model from an MJCF file.

    Args:
        path: Path to the MJCF file.

    Returns:
        Loaded MuJoCo model.
    """
    return mujoco.MjModel.from_xml_path(str(path))


def test_t_mjcf_001_load_minimal_body() -> None:
    """T-MJCF-001: Load the minimum body and geom sample."""
    model = _load_model(_require_sample("minimal_body/model.xml"))

    assert model.nbody >= 1
    assert model.ngeom >= 1


def test_t_mjcf_002_load_joint_body() -> None:
    """T-MJCF-002: Load a sample that contains at least one joint."""
    model = _load_model(_require_sample("joint_body/model.xml"))

    assert model.njnt >= 1


def test_t_mjcf_003_load_position_servo() -> None:
    """T-MJCF-003: Load a sample that contains at least one actuator."""
    model = _load_model(_require_sample("position_servo/model.xml"))

    assert model.nu >= 1


def test_t_mjcf_004_load_sensor_body() -> None:
    """T-MJCF-004: Load a sample that contains at least one sensor."""
    model = _load_model(_require_sample("sensor_body/model.xml"))

    assert model.nsensor >= 1
