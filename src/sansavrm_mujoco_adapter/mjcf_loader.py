"""MJCF loading helpers for SansaVRM-MuJoCo-Adapter.

This module wraps the minimum MuJoCo loading operations used by local validation
and future adapter tests.
"""

from __future__ import annotations

from pathlib import Path

import mujoco


def load_model_from_xml_path(path: str | Path) -> mujoco.MjModel:
    """Load a MuJoCo model from an MJCF XML file.

    Args:
        path: Path to the MJCF XML file.

    Returns:
        Loaded MuJoCo model.

    Raises:
        FileNotFoundError: If the MJCF file does not exist.
        ValueError: If the path does not point to a file.
    """
    xml_path = Path(path)
    if not xml_path.exists():
        raise FileNotFoundError(f"MJCF file does not exist: {xml_path}")
    if not xml_path.is_file():
        raise ValueError(f"MJCF path must be a file: {xml_path}")

    return mujoco.MjModel.from_xml_path(str(xml_path))


def create_data(model: mujoco.MjModel) -> mujoco.MjData:
    """Create MuJoCo runtime data for a model.

    Args:
        model: MuJoCo model.

    Returns:
        Runtime data for the model.
    """
    return mujoco.MjData(model)


def step_once(model: mujoco.MjModel, data: mujoco.MjData) -> None:
    """Execute one MuJoCo simulation step.

    Args:
        model: MuJoCo model.
        data: Runtime data for the model.
    """
    mujoco.mj_step(model, data)
