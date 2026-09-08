"""Aggregation functions with differential privacy."""

import numpy as np
from typing import List, Tuple, Optional
from .mechanisms import LaplaceNoise, GaussianNoise
from .calibration import SensitivityCalculator, NoiseCalibratorGaussian, NoiseCalibrationLaplace


class DPAggregations:
    """Differentially private aggregation functions."""

    @staticmethod
    def dp_sum(
        values: List[float],
        max_value: float,
        epsilon: float,
        delta: Optional[float] = None,
    ) -> float:
        """Compute differentially private sum.
        
        Args:
            values: List of values to sum.
            max_value: Maximum absolute value any record can have (for sensitivity).
            epsilon: Privacy parameter.
            delta: Failure probability (optional, uses Gaussian if provided).
        
        Returns:
            Noisy sum value.
        """
        true_sum = sum(values)
        sensitivity = SensitivityCalculator.sum_sensitivity(max_value)
        
        if delta is not None:
            sigma = NoiseCalibratorGaussian.calibrate(sensitivity, epsilon, delta)
            noise = np.random.normal(0, sigma)
        else:
            scale = NoiseCalibrationLaplace.calibrate(sensitivity, epsilon)
            noise = np.random.laplace(0, scale)
        
        return true_sum + noise

    @staticmethod
    def dp_mean(
        values: List[float],
        max_value: float,
        epsilon: float,
        delta: Optional[float] = None,
    ) -> float:
        """Compute differentially private mean.
        
        Args:
            values: List of values to average.
            max_value: Maximum absolute value any record can have.
            epsilon: Privacy parameter.
            delta: Failure probability (optional).
        
        Returns:
            Noisy mean value.
        """
        n = len(values)
        if n == 0:
            raise ValueError("values list cannot be empty")
        
        true_sum = sum(values)
        sensitivity = SensitivityCalculator.mean_sensitivity(max_value, n)
        
        if delta is not None:
            sigma = NoiseCalibratorGaussian.calibrate(sensitivity, epsilon, delta)
            noise = np.random.normal(0, sigma)
        else:
            scale = NoiseCalibrationLaplace.calibrate(sensitivity, epsilon)
            noise = np.random.laplace(0, scale)
        
        return (true_sum + noise) / n

    @staticmethod
    def dp_count(
        count: int,
        epsilon: float,
        delta: Optional[float] = None,
    ) -> float:
        """Compute differentially private count.
        
        Args:
            count: True count value.
            epsilon: Privacy parameter.
            delta: Failure probability (optional).
        
        Returns:
            Noisy count.
        """
        sensitivity = SensitivityCalculator.count_sensitivity()
        
        if delta is not None:
            sigma = NoiseCalibratorGaussian.calibrate(sensitivity, epsilon, delta)
            noise = np.random.normal(0, sigma)
        else:
            scale = NoiseCalibrationLaplace.calibrate(sensitivity, epsilon)
            noise = np.random.laplace(0, scale)
        
        return count + noise

    @staticmethod
    def dp_histogram(
        values: List[float],
        bins: np.ndarray,
        epsilon: float,
        delta: Optional[float] = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Compute differentially private histogram.
        
        Args:
            values: List of values to bin.
            bins: Bin edges for histogram.
            epsilon: Privacy parameter.
            delta: Failure probability (optional).
        
        Returns:
            Tuple of (bin_centers, noisy_counts).
        """
        # Compute true histogram
        true_counts, bin_edges = np.histogram(values, bins=bins)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        # Add noise to each bin count
        sensitivity = SensitivityCalculator.histogram_sensitivity(len(true_counts))
        
        if delta is not None:
            sigma = NoiseCalibratorGaussian.calibrate(sensitivity, epsilon, delta)
            noise = np.random.normal(0, sigma, size=len(true_counts))
        else:
            scale = NoiseCalibrationLaplace.calibrate(sensitivity, epsilon)
            noise = np.random.laplace(0, scale, size=len(true_counts))
        
        noisy_counts = np.maximum(0, true_counts + noise)  # Clip to non-negative
        return bin_centers, noisy_counts

    @staticmethod
    def dp_quantile(
        values: List[float],
        q: float,
        epsilon: float,
        delta: Optional[float] = None,
    ) -> float:
        """Compute approximate differentially private quantile.
        
        Args:
            values: List of values.
            q: Quantile to compute (0-1).
            epsilon: Privacy parameter.
            delta: Failure probability (optional).
        
        Returns:
            Noisy quantile value.
        """
        if not 0 <= q <= 1:
            raise ValueError(f"q must be in [0, 1], got {q}")
        
        true_quantile = np.quantile(values, q)
        
        # Approximate sensitivity (this is a rough estimate)
        value_range = max(values) - min(values)
        sensitivity = value_range / np.sqrt(len(values))
        
        if delta is not None:
            sigma = NoiseCalibratorGaussian.calibrate(sensitivity, epsilon, delta)
            noise = np.random.normal(0, sigma)
        else:
            scale = NoiseCalibrationLaplace.calibrate(sensitivity, epsilon)
            noise = np.random.laplace(0, scale)
        
        return true_quantile + noise
