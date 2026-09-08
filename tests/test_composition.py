"""Tests for privacy budget and composition."""

import pytest
from src.dpti.privacy.composition import (
    PrivacyBudget,
    PrivacyComposition,
    CompositionType,
)


class TestPrivacyBudget:
    """Test PrivacyBudget class."""

    def test_initialization(self):
        """Test budget initialization."""
        budget = PrivacyBudget(total_epsilon=1.0, total_delta=1e-6)
        assert budget.total_epsilon == 1.0
        assert budget.total_delta == 1e-6
        assert budget.spent_epsilon == 0.0
        assert budget.spent_delta == 0.0

    def test_invalid_epsilon(self):
        """Test that invalid epsilon raises error."""
        with pytest.raises(ValueError):
            PrivacyBudget(total_epsilon=0.0, total_delta=1e-6)
        with pytest.raises(ValueError):
            PrivacyBudget(total_epsilon=-1.0, total_delta=1e-6)

    def test_spend(self):
        """Test spending budget."""
        budget = PrivacyBudget(total_epsilon=1.0, total_delta=1e-6)
        budget.spend(0.3, 3e-7)
        assert budget.spent_epsilon == pytest.approx(0.3)
        assert budget.spent_delta == pytest.approx(3e-7)

    def test_spend_exhaustion(self):
        """Test that spending exhausts budget."""
        budget = PrivacyBudget(total_epsilon=0.5, total_delta=1e-6)
        budget.spend(0.3, 5e-7)
        with pytest.raises(RuntimeError):
            budget.spend(0.3, 5e-7)  # Would exceed epsilon

    def test_remaining(self):
        """Test remaining budget calculation."""
        budget = PrivacyBudget(total_epsilon=1.0, total_delta=1e-6)
        budget.spend(0.3, 3e-7)
        assert budget.remaining_epsilon == pytest.approx(0.7)
        assert budget.remaining_delta == pytest.approx(7e-7)


class TestPrivacyComposition:
    """Test PrivacyComposition class."""

    def test_basic_composition(self):
        """Test basic composition."""
        result = PrivacyComposition.basic_composition(epsilon=0.1, delta=1e-6, k=5)
        assert result.total_epsilon == pytest.approx(0.5)
        assert result.total_delta == pytest.approx(5e-6)
        assert result.composition_type == CompositionType.BASIC

    def test_sequential_composition(self):
        """Test sequential composition."""
        epsilons = [0.1, 0.2, 0.15]
        deltas = [1e-6, 2e-6, 1.5e-6]
        result = PrivacyComposition.sequential_composition(epsilons, deltas)
        assert result.total_epsilon == pytest.approx(0.45)
        assert result.total_delta == pytest.approx(4.5e-6)
        assert result.composition_type == CompositionType.SEQUENTIAL

    def test_parallel_composition(self):
        """Test parallel composition."""
        result = PrivacyComposition.parallel_composition(
            epsilon=0.1, delta=1e-6, k=5
        )
        assert result.total_epsilon == pytest.approx(0.1)
        assert result.total_delta == pytest.approx(1e-6)
        assert result.composition_type == CompositionType.PARALLEL

    def test_advanced_composition(self):
        """Test advanced composition."""
        result = PrivacyComposition.advanced_composition(
            epsilon=0.1, delta=1e-6, k=5, delta_prime=1e-6
        )
        # Advanced composition gives tighter bounds than basic
        assert result.total_epsilon < 0.5  # Better than basic
        assert result.composition_type == CompositionType.ADVANCED
