"""Automatic sensitivity and noise calibration."""

import numpy as np
from typing import Tuple


class NoiseCalibratorGaussian:
    """Calibrates Gaussian noise parameters for differential privacy."""

    @staticmethod
    def calibrate(
        sensitivity: float, epsilon: float, delta: float
    ) -> float:
        """Calculate standard deviation for Gaussian mechanism.
        
        Args:
            sensitivity: Sensitivity of the query (max change from one record).
            epsilon: Privacy parameter (lower = more privacy).
            delta: Failure probability (typically 1e-6).
        
        Returns:
            Standard deviation for Gaussian noise.
        """
        if sensitivity < 0:
            raise ValueError(f"sensitivity must be non-negative, got {sensitivity}")
        if epsilon <= 0:
            raise ValueError(f"epsilon must be positive, got {epsilon}")
        if delta <= 0 or delta >= 1:
            raise ValueError(f"delta must be in (0, 1), got {delta}")
        
        # Formula: sigma = sensitivity * sqrt(2 * ln(1.25/delta)) / epsilon
        sigma = sensitivity * np.sqrt(2 * np.log(1.25 / delta)) / epsilon
        return sigma


class NoiseCalibrationLaplace:
    """Calibrates Laplace noise parameters for differential privacy."""

    @staticmethod
    def calibrate(sensitivity: float, epsilon: float) -> float:
        """Calculate scale parameter for Laplace mechanism.
        
        Args:
            sensitivity: Sensitivity of the query (max change from one record).
            epsilon: Privacy parameter (lower = more privacy).
        
        Returns:
            Scale parameter for Laplace noise.
        """
        if sensitivity < 0:
            raise ValueError(f"sensitivity must be non-negative, got {sensitivity}")
        if epsilon <= 0:
            raise ValueError(f"epsilon must be positive, got {epsilon}")
        
        # Laplace scale: b = sensitivity / epsilon
        return sensitivity / epsilon


class SensitivityCalculator:
    """Calculates query sensitivity for different operations."""

    @staticmethod
    def count_sensitivity() -> float:
        """Calculate sensitivity for count queries.
        
        Removing one record changes count by at most 1.
        
        Returns:
            Sensitivity value of 1.0.
        """
        return 1.0

    @staticmethod
    def sum_sensitivity(max_value: float) -> float:
        """Calculate sensitivity for sum queries.
        
        Args:
            max_value: Maximum absolute value any record can have.
        
        Returns:
            Sensitivity equal to max_value.
        """
        if max_value < 0:
            raise ValueError(f"max_value must be non-negative, got {max_value}")
        return max_value

    @staticmethod
    def mean_sensitivity(max_value: float, n: int) -> float:
        """Calculate sensitivity for mean queries.
        
        Args:
            max_value: Maximum absolute value any record can have.
            n: Total number of records.
        
        Returns:
            Sensitivity for mean computation.
        """
        if max_value < 0:
            raise ValueError(f"max_value must be non-negative, got {max_value}")
        if n <= 0:
            raise ValueError(f"n must be positive, got {n}")
        
        # Sensitivity of mean is max_value / n (adding/removing one record)
        return max_value / n

    @staticmethod
    def histogram_sensitivity(num_bins: int = 1) -> float:
        """Calculate sensitivity for histogram queries.
        
        Args:
            num_bins: Number of histogram bins (default: 1 for single bin).
        
        Returns:
            Sensitivity for histogram (1 per bin).
        """
        if num_bins <= 0:
            raise ValueError(f"num_bins must be positive, got {num_bins}")
        return 1.0

    @staticmethod
    def percentile_sensitivity(
        percentile: float, max_value: float, n: int
    ) -> float:
        """Estimate sensitivity for approximate percentile.
        
        Note: Exact percentile sensitivity is complex; this gives approximation.
        
        Args:
            percentile: Percentile value (0-100).
            max_value: Maximum absolute value any record can have.
            n: Total number of records.
        
        Returns:
            Approximate sensitivity for percentile.
        """
        if not 0 <= percentile <= 100:
            raise ValueError(f"percentile must be in [0, 100], got {percentile}")
        if max_value < 0:
            raise ValueError(f"max_value must be non-negative, got {max_value}")
        if n <= 0:
            raise ValueError(f"n must be positive, got {n}")
        
        # Rough approximation: max_value / sqrt(n)
        return max_value / np.sqrt(n)
