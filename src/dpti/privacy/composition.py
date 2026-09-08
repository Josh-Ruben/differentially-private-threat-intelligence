"""Privacy budget composition and accounting."""

from typing import List, Tuple
from dataclasses import dataclass
from enum import Enum


class CompositionType(Enum):
    """Types of composition theorems."""
    BASIC = "basic"
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    ADVANCED = "advanced"


@dataclass
class CompositionResult:
    """Result of composition calculation."""
    total_epsilon: float
    total_delta: float
    composition_type: CompositionType
    num_queries: int

    def __str__(self) -> str:
        return f"ε={self.total_epsilon:.4f}, δ={self.total_delta:.2e} (k={self.num_queries})" 


class PrivacyComposition:
    """Manages privacy budget composition across multiple queries."""

    @staticmethod
    def basic_composition(
        epsilon: float, delta: float, k: int
    ) -> CompositionResult:
        """Basic composition: sum all epsilons, sum all deltas.
        
        Args:
            epsilon: Privacy parameter per query.
            delta: Failure probability per query.
            k: Number of queries.
        
        Returns:
            Composition result with total privacy parameters.
        """
        total_epsilon = k * epsilon
        total_delta = k * delta
        return CompositionResult(
            total_epsilon=total_epsilon,
            total_delta=total_delta,
            composition_type=CompositionType.BASIC,
            num_queries=k,
        )

    @staticmethod
    def sequential_composition(
        epsilons: List[float], deltas: List[float]
    ) -> CompositionResult:
        """Sequential composition: sum epsilons and deltas.
        
        Args:
            epsilons: List of epsilon values for each query.
            deltas: List of delta values for each query.
        
        Returns:
            Composition result.
        
        Raises:
            ValueError: If lists have different lengths.
        """
        if len(epsilons) != len(deltas):
            raise ValueError("epsilons and deltas must have same length")
        
        total_epsilon = sum(epsilons)
        total_delta = sum(deltas)
        return CompositionResult(
            total_epsilon=total_epsilon,
            total_delta=total_delta,
            composition_type=CompositionType.SEQUENTIAL,
            num_queries=len(epsilons),
        )

    @staticmethod
    def parallel_composition(
        epsilon: float, delta: float, k: int
    ) -> CompositionResult:
        """Parallel composition: same epsilon and delta across disjoint datasets.
        
        Args:
            epsilon: Privacy parameter per query.
            delta: Failure probability per query.
            k: Number of parallel queries on disjoint data.
        
        Returns:
            Composition result (same as input for parallel queries).
        """
        return CompositionResult(
            total_epsilon=epsilon,
            total_delta=delta,
            composition_type=CompositionType.PARALLEL,
            num_queries=k,
        )

    @staticmethod
    def advanced_composition(
        epsilon: float, delta: float, k: int, delta_prime: float = 1e-6
    ) -> CompositionResult:
        """Advanced composition by Dwork et al.
        
        Provides better composition bound than basic composition.
        Total privacy: (k * epsilon^2 / ln(1/delta'), delta + k * delta')
        
        Args:
            epsilon: Privacy parameter per query.
            delta: Failure probability per query.
            k: Number of queries.
            delta_prime: Additional failure probability (default: 1e-6).
        
        Returns:
            Composition result with improved bounds.
        """
        import numpy as np
        
        if delta_prime <= 0 or delta_prime >= 1:
            raise ValueError(f"delta_prime must be in (0, 1), got {delta_prime}")
        
        # Advanced composition formula
        log_term = np.log(1.0 / delta_prime)
        total_epsilon = k * epsilon ** 2 / log_term
        total_delta = delta + k * delta_prime
        
        return CompositionResult(
            total_epsilon=total_epsilon,
            total_delta=total_delta,
            composition_type=CompositionType.ADVANCED,
            num_queries=k,
        )


class PrivacyBudget:
    """Tracks and manages privacy budget allocation."""

    def __init__(self, total_epsilon: float, total_delta: float):
        """Initialize privacy budget.
        
        Args:
            total_epsilon: Total epsilon budget.
            total_delta: Total delta budget.
        """
        if total_epsilon <= 0:
            raise ValueError(f"total_epsilon must be positive, got {total_epsilon}")
        if total_delta <= 0 or total_delta >= 1:
            raise ValueError(f"total_delta must be in (0, 1), got {total_delta}")
        
        self.total_epsilon = total_epsilon
        self.total_delta = total_delta
        self.spent_epsilon = 0.0
        self.spent_delta = 0.0
        self.queries_executed = 0

    def spend(
        self, epsilon: float, delta: float, query_name: str = ""
    ) -> None:
        """Spend privacy budget.
        
        Args:
            epsilon: Epsilon to spend.
            delta: Delta to spend.
            query_name: Name of query for tracking.
        
        Raises:
            RuntimeError: If budget is exhausted.
            ValueError: If amounts are negative.
        """
        if epsilon < 0 or delta < 0:
            raise ValueError("Budget amounts must be non-negative")
        
        if self.spent_epsilon + epsilon > self.total_epsilon:
            raise RuntimeError(
                f"Insufficient epsilon budget. "
                f"Requested: {epsilon}, Available: {self.remaining_epsilon}"
            )
        if self.spent_delta + delta > self.total_delta:
            raise RuntimeError(
                f"Insufficient delta budget. "
                f"Requested: {delta}, Available: {self.remaining_delta}"
            )
        
        self.spent_epsilon += epsilon
        self.spent_delta += delta
        self.queries_executed += 1

    @property
    def remaining_epsilon(self) -> float:
        """Get remaining epsilon budget."""
        return self.total_epsilon - self.spent_epsilon

    @property
    def remaining_delta(self) -> float:
        """Get remaining delta budget."""
        return self.total_delta - self.spent_delta

    @property
    def epsilon_fraction_used(self) -> float:
        """Get fraction of epsilon budget used."""
        return self.spent_epsilon / self.total_epsilon

    @property
    def delta_fraction_used(self) -> float:
        """Get fraction of delta budget used."""
        return self.spent_delta / self.total_delta

    def is_exhausted(self) -> bool:
        """Check if budget is exhausted."""
        return self.spent_epsilon >= self.total_epsilon or self.spent_delta >= self.total_delta

    def __str__(self) -> str:
        return (
            f"Budget: ε={self.spent_epsilon:.4f}/{self.total_epsilon:.4f}, "
            f"δ={self.spent_delta:.2e}/{self.total_delta:.2e} "
            f"({100*self.epsilon_fraction_used:.1f}% / {100*self.delta_fraction_used:.1f}%)"
        )
