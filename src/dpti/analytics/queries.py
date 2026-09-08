"""Differentially private queries."""

from typing import List, Optional, Dict, Any
import numpy as np
from .aggregations import DPAggregations


class DPQuery:
    """Base class for differentially private queries."""

    def __init__(self, epsilon: float, delta: Optional[float] = None):
        """Initialize query with privacy parameters.
        
        Args:
            epsilon: Privacy parameter.
            delta: Failure probability (optional).
        """
        if epsilon <= 0:
            raise ValueError(f"epsilon must be positive, got {epsilon}")
        if delta is not None and (delta <= 0 or delta >= 1):
            raise ValueError(f"delta must be in (0, 1), got {delta}")
        
        self.epsilon = epsilon
        self.delta = delta

    def execute(self, data: Any) -> Any:
        """Execute the query on data.
        
        Args:
            data: Input data.
        
        Returns:
            Query result.
        """
        raise NotImplementedError("Subclasses must implement execute()")


class CountQuery(DPQuery):
    """Differentially private count query."""

    def execute(self, data: List[Any]) -> float:
        """Execute count query.
        
        Args:
            data: List of items to count.
        
        Returns:
            Noisy count.
        """
        true_count = len(data)
        return DPAggregations.dp_count(true_count, self.epsilon, self.delta)


class SumQuery(DPQuery):
    """Differentially private sum query."""

    def __init__(
        self, epsilon: float, delta: Optional[float] = None, max_value: float = 1.0
    ):
        """Initialize sum query.
        
        Args:
            epsilon: Privacy parameter.
            delta: Failure probability (optional).
            max_value: Maximum absolute value any record can have.
        """
        super().__init__(epsilon, delta)
        self.max_value = max_value

    def execute(self, data: List[float]) -> float:
        """Execute sum query.
        
        Args:
            data: List of numerical values.
        
        Returns:
            Noisy sum.
        """
        return DPAggregations.dp_sum(data, self.max_value, self.epsilon, self.delta)


class MeanQuery(DPQuery):
    """Differentially private mean query."""

    def __init__(
        self, epsilon: float, delta: Optional[float] = None, max_value: float = 1.0
    ):
        """Initialize mean query.
        
        Args:
            epsilon: Privacy parameter.
            delta: Failure probability (optional).
            max_value: Maximum absolute value any record can have.
        """
        super().__init__(epsilon, delta)
        self.max_value = max_value

    def execute(self, data: List[float]) -> float:
        """Execute mean query.
        
        Args:
            data: List of numerical values.
        
        Returns:
            Noisy mean.
        """
        return DPAggregations.dp_mean(data, self.max_value, self.epsilon, self.delta)


class HistogramQuery(DPQuery):
    """Differentially private histogram query."""

    def __init__(
        self,
        epsilon: float,
        delta: Optional[float] = None,
        bins: int = 10,
        range_tuple: Optional[tuple] = None,
    ):
        """Initialize histogram query.
        
        Args:
            epsilon: Privacy parameter.
            delta: Failure probability (optional).
            bins: Number of histogram bins.
            range_tuple: (min, max) range for binning.
        """
        super().__init__(epsilon, delta)
        self.bins = bins
        self.range_tuple = range_tuple

    def execute(self, data: List[float]) -> Dict[str, Any]:
        """Execute histogram query.
        
        Args:
            data: List of values to bin.
        
        Returns:
            Dictionary with bin_centers and noisy_counts.
        """
        if self.range_tuple:
            bin_edges = np.linspace(self.range_tuple[0], self.range_tuple[1], self.bins + 1)
        else:
            bin_edges = self.bins
        
        bin_centers, noisy_counts = DPAggregations.dp_histogram(
            data, bin_edges, self.epsilon, self.delta
        )
        
        return {"bin_centers": bin_centers, "noisy_counts": noisy_counts}
