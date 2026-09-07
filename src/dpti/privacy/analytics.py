"""Differential Privacy Analytics engine."""

from typing import Optional
from .mechanisms import LaplaceNoise, GaussianNoise


class DPAnalytics:
    """Privacy-preserving analytics engine with privacy budget management."""

    def __init__(self, epsilon: float, delta: Optional[float] = None):
        """Initialize DPAnalytics with privacy parameters.
        
        Args:
            epsilon: Total privacy budget (lower = more privacy, typical: 0.1-10).
            delta: Failure probability (optional, typical: 1e-6).
        """
        if epsilon <= 0:
            raise ValueError(f"epsilon must be positive, got {epsilon}")
        if delta is not None and (delta <= 0 or delta >= 1):
            raise ValueError(f"delta must be in (0, 1), got {delta}")
        
        self.total_epsilon = epsilon
        self.total_delta = delta
        self.epsilon_used = 0.0
        self.delta_used = 0.0

    def count(
        self, value: int, sensitivity: int = 1, use_gaussian: bool = False
    ) -> float:
        """Perform a differentially private count query.
        
        Args:
            value: The true count value.
            sensitivity: Maximum change from removing one record (default: 1).
            use_gaussian: Whether to use Gaussian mechanism (requires delta).
        
        Returns:
            The noisy count.
        
        Raises:
            RuntimeError: If privacy budget is exhausted.
            ValueError: If parameters are invalid.
        """
        epsilon_needed = self.total_epsilon - self.epsilon_used
        if epsilon_needed <= 0:
            raise RuntimeError("Privacy budget exhausted")
        
        if use_gaussian:
            if self.total_delta is None:
                raise ValueError("delta required for Gaussian mechanism")
            delta_needed = self.total_delta - self.delta_used
            if delta_needed <= 0:
                raise RuntimeError("Delta budget exhausted")
            
            result = GaussianNoise.add_noise(
                value, sensitivity, epsilon_needed, delta_needed
            )
            self.delta_used += delta_needed
        else:
            result = LaplaceNoise.add_noise(value, sensitivity, epsilon_needed)
        
        self.epsilon_used += epsilon_needed
        return result

    def budget_remaining(self) -> float:
        """Get remaining epsilon budget.
        
        Returns:
            Remaining epsilon.
        """
        return self.total_epsilon - self.epsilon_used

    def reset_budget(self) -> None:
        """Reset privacy budgets."""
        self.epsilon_used = 0.0
        self.delta_used = 0.0
