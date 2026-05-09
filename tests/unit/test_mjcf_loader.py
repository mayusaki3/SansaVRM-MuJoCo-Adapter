"""Unit tests for MJCF loader helpers."""

from __future__ import annotations

from pathlib import Path

import pytest

from sansavrm_mujoco_adapter.mjcf_loader import (
    create_data,
    load_model_from_xml_path,
    step_once,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
MINIMAL_MJCF_PATH = REPOSITORY_ROOT / "examples" / "mujoco" / "minimal_body" / "model.xml"


def test_load_model_from_xml_path_loads_minimal_model() -> None:
    """Verify that load_model_from_xml_path loads the minimum MJCF sample."""
    model = load_model_from_xml_path(MINIMAL_MJCF_PATH)

    assert model.nbody >= 1
    assert model.ngeom >= 1


def test_load_model_from_xml_path_rejects_missing_file() -> None:
    """Verify that load_model_from_xml_path rejects missing files."""
    with pytest.raises(FileNotFoundError):
        load_model_from_xml_path(REPOSITORY_ROOT / "missing.xml")


def test_load_model_from_xml_path_rejects_directory() -> None:
    """Verify that load_model_from_xml_path rejects directory paths."""
    with pytest.raises(ValueError):
        load_model_from_xml_path(REPOSITORY_ROOT)


def test_create_data_and_step_once() -> None:
    """Verify that create_data and step_once execute one simulation step."""
    model = load_model_from_xml_path(MINIMAL_MJCF_PATH)
    data = create_data(model)
    initial_time = data.time

    step_once(model, data)

    assert data.time > initial_time
