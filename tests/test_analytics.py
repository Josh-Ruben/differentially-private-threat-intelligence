"""Tests for aggregation functions."""

import pytest
import numpy as np
from src.dpti.analytics import (
    CountQuery,
    SumQuery,
    MeanQuery,
    HistogramQuery,
)


class TestCountQuery:
    """Test CountQuery class."""

    def test_count_query_basic(self):
        """Test basic count query."""
        query = CountQuery(epsilon=1.0, delta=1e-6)
        data = [1, 2, 3, 4, 5]
        result = query.execute(data)
        assert isinstance(result, float)
        # Result should be close to true count (5) with some noise
        assert 0 <= result <= 10  # Reasonable bounds

    def test_count_query_empty(self):
        """Test count query on empty data."""
        query = CountQuery(epsilon=1.0, delta=1e-6)
        result = query.execute([])
        assert isinstance(result, float)
        # Should add noise to 0


class TestSumQuery:
    """Test SumQuery class."""

    def test_sum_query_basic(self):
        """Test basic sum query."""
        query = SumQuery(epsilon=1.0, delta=1e-6, max_value=10.0)
        data = [1.0, 2.0, 3.0, 4.0, 5.0]
        result = query.execute(data)
        assert isinstance(result, float)
        # True sum is 15, result should be somewhat close
        assert 0 <= result <= 30

    def test_sum_query_max_value(self):
        """Test that max_value affects sensitivity."""
        data = [1.0, 2.0, 3.0]
        
        query1 = SumQuery(epsilon=1.0, delta=1e-6, max_value=10.0)
        query2 = SumQuery(epsilon=1.0, delta=1e-6, max_value=100.0)
        
        # Run multiple times to see variance
        results1 = [query1.execute(data) for _ in range(100)]
        results2 = [query2.execute(data) for _ in range(100)]
        
        # Higher max_value should lead to more noise
        std1 = np.std(results1)
        std2 = np.std(results2)
        assert std2 > std1


class TestMeanQuery:
    """Test MeanQuery class."""

    def test_mean_query_basic(self):
        """Test basic mean query."""
        query = MeanQuery(epsilon=1.0, delta=1e-6, max_value=10.0)
        data = [2.0, 4.0, 6.0, 8.0, 10.0]
        result = query.execute(data)
        assert isinstance(result, float)
        # True mean is 6, result should be in reasonable range
        assert 0 <= result <= 10


class TestHistogramQuery:
    """Test HistogramQuery class."""

    def test_histogram_query_basic(self):
        """Test basic histogram query."""
        query = HistogramQuery(
            epsilon=1.0, delta=1e-6, bins=5, range_tuple=(0, 10)
        )
        data = [1.0, 2.5, 3.0, 5.5, 7.0, 8.5, 9.0]
        result = query.execute(data)
        
        assert "bin_centers" in result
        assert "noisy_counts" in result
        assert len(result["bin_centers"]) == 5
        assert len(result["noisy_counts"]) == 5
        # All counts should be non-negative
        assert all(c >= 0 for c in result["noisy_counts"])
