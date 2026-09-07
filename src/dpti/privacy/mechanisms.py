"""Differential Privacy mechanisms for noise addition and query answering."""

import numpy as np
from typing import Union, List


class LaplaceNoise:
    """Laplace mechanism for adding noise to numerical queries."""

    @staticmethod
    def add_noise(value: float, sensitivity: float, epsilon: float) -> float:
        """Add Laplace noise to a value for differential privacy.
        
        Args:
            value: The original value to add noise to.
            sensitivity: The sensitivity of the query (max absolute change from one record).
            epsilon: Privacy parameter controlling noise magnitude (lower = more privacy).
        
        Returns:
            The value with Laplace noise added.
        
        Raises:
            ValueError: If epsilon <= 0 or sensitivity < 0.
        """
        if epsilon <= 0:
            raise ValueError(f"epsilon must be positive, got {epsilon}")
        if sensitivity < 0:
            raise ValueError(f"sensitivity must be non-negative, got {sensitivity}")
        
        scale = sensitivity / epsilon
        noise = np.random.laplace(0, scale)
        return float(value + noise)


class GaussianNoise:
    """Gaussian mechanism for adding noise to numerical queries."""

    @staticmethod
    def add_noise(
        value: float, sensitivity: float, epsilon: float, delta: float
    ) -> float:
        """Add Gaussian noise to a value for differential privacy.
        
        Args:
            value: The original value to add noise to.
            sensitivity: The sensitivity of the query (max absolute change from one record).
            epsilon: Privacy parameter (lower = more privacy).
            delta: Failure probability parameter (usually 1e-6).
        
        Returns:
            The value with Gaussian noise added.
        
        Raises:
            ValueError: If parameters are invalid.
        """
        if epsilon <= 0:
            raise ValueError(f"epsilon must be positive, got {epsilon}")
        if delta <= 0 or delta >= 1:
            raise ValueError(f"delta must be in (0, 1), got {delta}")
        if sensitivity < 0:
            raise ValueError(f"sensitivity must be non-negative, got {sensitivity}")
        
        # Standard deviation for Gaussian mechanism
        sigma = sensitivity * np.sqrt(2 * np.log(1.25 / delta)) / epsilon
        noise = np.random.normal(0, sigma)
        return float(value + noise)


class ExponentialMechanism:
    """Exponential mechanism for selecting from a set of options."""

    @staticmethod
    def select(
        options: List[Union[int, str]],
        scores: List[float],
        sensitivity: float,
        epsilon: float,
    ) -> Union[int, str]:
        """Select an option with probability proportional to its score.
        
        Args:
            options: The set of options to choose from.
            scores: The scores for each option (higher is better).
            sensitivity: The sensitivity of the scoring function.
            epsilon: Privacy parameter (lower = more privacy).
        
        Returns:
            The selected option.
        
        Raises:
            ValueError: If parameters are invalid.
        """
        if len(options) != len(scores):
            raise ValueError("options and scores must have same length")
        if epsilon <= 0:
            raise ValueError(f"epsilon must be positive, got {epsilon}")
        if sensitivity < 0:
            raise ValueError(f"sensitivity must be non-negative, got {sensitivity}")
        
        scores_array = np.array(scores, dtype=float)
        
        # Compute probabilities proportional to exp(epsilon * score / (2 * sensitivity))
        scaled_scores = epsilon * scores_array / (2 * sensitivity)
        scaled_scores = scaled_scores - np.max(scaled_scores)  # For numerical stability
        probabilities = np.exp(scaled_scores)
        probabilities = probabilities / np.sum(probabilities)
        
        # Select option according to probabilities
        selected_idx = np.random.choice(len(options), p=probabilities)
        return options[selected_idx]
