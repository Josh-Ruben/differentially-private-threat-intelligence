"""Tests for differential privacy mechanisms."""

import pytest
import numpy as np
from src.dpti.privacy.mechanisms import LaplaceNoise, GaussianNoise, ExponentialMechanism


class TestLaplaceNoise:
    """Test Laplace mechanism."""

    def test_add_noise_basic(self):
        """Test basic noise addition."""
        value = 100.0
        sensitivity = 1.0
        epsilon = 1.0
        
        result = LaplaceNoise.add_noise(value, sensitivity, epsilon)
        assert isinstance(result, float)

    def test_add_noise_invalid_epsilon(self):
        """Test that invalid epsilon raises error."""
        with pytest.raises(ValueError):
            LaplaceNoise.add_noise(100.0, 1.0, -1.0)
        
        with pytest.raises(ValueError):
            LaplaceNoise.add_noise(100.0, 1.0, 0.0)

    def test_add_noise_invalid_sensitivity(self):
        """Test that invalid sensitivity raises error."""
        with pytest.raises(ValueError):
            LaplaceNoise.add_noise(100.0, -1.0, 1.0)


class TestGaussianNoise:
    """Test Gaussian mechanism."""

    def test_add_noise_basic(self):
        """Test basic noise addition."""
        value = 100.0
        sensitivity = 1.0
        epsilon = 1.0
        delta = 1e-6
        
        result = GaussianNoise.add_noise(value, sensitivity, epsilon, delta)
        assert isinstance(result, float)

    def test_add_noise_invalid_delta(self):
        """Test that invalid delta raises error."""
        with pytest.raises(ValueError):
            GaussianNoise.add_noise(100.0, 1.0, 1.0, 0.0)
        
        with pytest.raises(ValueError):
            GaussianNoise.add_noise(100.0, 1.0, 1.0, 1.5)


class TestExponentialMechanism:
    """Test Exponential mechanism."""

    def test_select_basic(self):
        """Test basic selection."""
        options = ["A", "B", "C"]
        scores = [10.0, 20.0, 30.0]
        sensitivity = 1.0
        epsilon = 1.0
        
        result = ExponentialMechanism.select(options, scores, sensitivity, epsilon)
        assert result in options

    def test_select_prefers_high_scores(self):
        """Test that mechanism prefers high scores."""
        options = [0, 1]
        scores = [1.0, 100.0]  # Option 1 much better
        sensitivity = 1.0
        epsilon = 10.0  # High epsilon = less noise
        
        # Run multiple times and check option 1 is selected more often
        results = [
            ExponentialMechanism.select(options, scores, sensitivity, epsilon)
            for _ in range(100)
        ]
        assert results.count(1) > results.count(0)
