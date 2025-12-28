"""Tests for experiment tracking."""

import pytest
from omegaconf import OmegaConf

from utils.experiment_tracking import ExperimentTracker


@pytest.fixture
def mock_config():
    """Create a mock configuration."""
    config_dict = {
        "experiment_name": "test_experiment",
        "run_name": "test_run",
        "tracking": {
            "enabled": True,
            "tracking_uri": "./test_mlruns",
            "experiment_name": "test_experiment",
            "run_name": "test_run",
            "log_params": True,
            "log_metrics": True,
            "log_models": False,
            "log_artifacts": False,
            "autolog": False,
        },
    }
    return OmegaConf.create(config_dict)


def test_tracker_initialization_disabled():
    """Test tracker initialization when disabled."""
    config_dict = {
        "experiment_name": "test",
        "run_name": "test",
        "tracking": {"enabled": False},
    }
    config = OmegaConf.create(config_dict)

    # Should not raise error
    tracker = ExperimentTracker(config, tracking_backend="mlflow")
    assert tracker is not None


def test_flatten_dict():
    """Test dictionary flattening."""
    config_dict = {
        "experiment_name": "test",
        "run_name": "test",
        "tracking": {"enabled": True},
    }
    config = OmegaConf.create(config_dict)

    tracker = ExperimentTracker(config, tracking_backend="mlflow")

    nested_dict = {"a": {"b": {"c": 1}, "d": 2}, "e": 3}

    flat = tracker._flatten_dict(nested_dict)

    assert flat["a.b.c"] == 1
    assert flat["a.d"] == 2
    assert flat["e"] == 3


def test_log_params_structure():
    """Test that log_params handles various data types."""
    config_dict = {
        "experiment_name": "test",
        "run_name": "test",
        "tracking": {"enabled": False},
    }
    config = OmegaConf.create(config_dict)

    tracker = ExperimentTracker(config, tracking_backend="mlflow")

    # Should handle different types without error
    params = {
        "int_param": 42,
        "float_param": 3.14,
        "str_param": "test",
        "bool_param": True,
        "none_param": None,
        "nested": {"value": 1},
    }

    # Should not raise error even if tracking is disabled
    tracker.log_params(params)


def test_log_metrics_structure():
    """Test that log_metrics handles various scenarios."""
    config_dict = {
        "experiment_name": "test",
        "run_name": "test",
        "tracking": {"enabled": False},
    }
    config = OmegaConf.create(config_dict)

    tracker = ExperimentTracker(config, tracking_backend="mlflow")

    metrics = {"accuracy": 0.95, "loss": 0.05}

    # Should not raise error
    tracker.log_metrics(metrics)
    tracker.log_metrics(metrics, step=1)


def test_context_manager():
    """Test tracker as context manager."""
    config_dict = {
        "experiment_name": "test",
        "run_name": "test",
        "tracking": {"enabled": False},
    }
    config = OmegaConf.create(config_dict)

    # Should work as context manager
    with ExperimentTracker(config, tracking_backend="mlflow") as tracker:
        tracker.log_params({"test": 1})
        tracker.log_metrics({"test": 0.5})


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
