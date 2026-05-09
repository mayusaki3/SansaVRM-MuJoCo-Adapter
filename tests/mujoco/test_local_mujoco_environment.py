"""Local MuJoCo environment tests.

This module verifies the minimum local MuJoCo execution requirements before the
adapter implementation is added. Each test maps to a documented T-LOCAL test
number.
"""

from __future__ import annotations

from pathlib import Path

import mujoco


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
MINIMAL_MJCF_PATH = REPOSITORY_ROOT / "examples" / "mujoco" / "minimal_body" / "model.xml"


def _load_minimal_model() -> mujoco.MjModel:
    """Load the minimum MJCF model used for local validation.

    Returns:
        Loaded MuJoCo model.

    Raises:
        AssertionError: If the minimum MJCF file does not exist.
    """
    assert MINIMAL_MJCF_PATH.exists(), f"Missing MJCF file: {MINIMAL_MJCF_PATH}"
    return mujoco.MjModel.from_xml_path(str(MINIMAL_MJCF_PATH))


def test_t_local_001_import_mujoco() -> None:
    """T-LOCAL-001: Verify that the mujoco package can be imported."""
    assert isinstance(mujoco.__version__, str)
    assert mujoco.__version__, "mujoco.__version__ must not be empty"


def test_t_local_002_load_minimal_mjcf() -> None:
    """T-LOCAL-002: Verify that the minimum MJCF can be loaded."""
    model = _load_minimal_model()
    assert model.nbody >= 1
    assert model.ngeom >= 1


def test_t_local_003_create_mjdata() -> None:
    """T-LOCAL-003: Verify that MjData can be created from the minimum model."""
    model = _load_minimal_model()
    data = mujoco.MjData(model)
    assert data.time == 0.0


def test_t_local_004_run_single_mj_step() -> None:
    """T-LOCAL-004: Verify that one MuJoCo simulation step can be executed."""
    model = _load_minimal_model()
    data = mujoco.MjData(model)
    initial_time = data.time

    mujoco.mj_step(model, data)

    assert data.time > initial_time


def test_t_local_005_validate_minimal_model_counts() -> None:
    """T-LOCAL-005: Verify that the minimum model has expected core elements."""
    model = _load_minimal_model()

    assert model.nbody >= 2  # world body + box_body
    assert model.ngeom >= 2  # floor + box_geom
    assert model.njnt >= 1
