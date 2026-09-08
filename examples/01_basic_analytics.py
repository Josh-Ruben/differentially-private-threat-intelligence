"""Example: Basic Differential Privacy Analytics for Threat Intelligence."""

import numpy as np
from dpti.privacy import DPAnalytics
from dpti.privacy.composition import PrivacyBudget, PrivacyComposition
from dpti.analytics import CountQuery, SumQuery, MeanQuery, HistogramQuery


def example_basic_analytics():
    """Demonstrate basic differentially private analytics."""
    print("=" * 70)
    print("Example 1: Basic Differentially Private Analytics")
    print("=" * 70)
    
    # Initialize privacy-preserving analytics
    dp_analytics = DPAnalytics(epsilon=1.0, delta=1e-6)
    
    # Example threat intelligence data
    threat_counts = [5, 10, 8, 12, 15, 9, 11, 7, 14, 6]
    
    print(f"\nTrue threat count: {sum(threat_counts)}")
    print(f"Privacy parameters: epsilon={dp_analytics.total_epsilon}, delta={dp_analytics.total_delta}")
    
    # Perform count query
    dp_count = dp_analytics.count(len(threat_counts))
    print(f"Noisy threat count (DP): {dp_count:.2f}")
    print(f"Privacy budget used: ε={dp_analytics.epsilon_used:.4f}")
    print(f"Privacy budget remaining: ε={dp_analytics.budget_remaining():.4f}")


def example_multiple_queries():
    """Demonstrate privacy budget management with multiple queries."""
    print("\n" + "=" * 70)
    print("Example 2: Privacy Budget Management with Multiple Queries")
    print("=" * 70)
    
    from dpti.privacy.composition import PrivacyBudget
    
    # Initialize budget: total epsilon = 1.0, delta = 1e-5
    budget = PrivacyBudget(total_epsilon=1.0, total_delta=1e-5)
    print(f"\nInitial budget: {budget}")
    
    # Execute multiple queries
    queries = [
        {"name": "Count malware samples", "epsilon": 0.3, "delta": 3e-6},
        {"name": "Sum attack severity", "epsilon": 0.3, "delta": 3e-6},
        {"name": "Mean attack duration", "epsilon": 0.4, "delta": 4e-6},
    ]
    
    for query in queries:
        try:
            budget.spend(query["epsilon"], query["delta"], query["name"])
            print(f"\n✓ Query: {query['name']}")
            print(f"  Budget: {budget}")
        except RuntimeError as e:
            print(f"\n✗ Query failed: {query['name']}")
            print(f"  Error: {e}")


def example_aggregations():
    """Demonstrate differentially private aggregation functions."""
    print("\n" + "=" * 70)
    print("Example 3: Differentially Private Aggregations")
    print("=" * 70)
    
    # Simulated threat severity scores
    severity_scores = [8.5, 9.2, 7.3, 8.9, 9.5, 7.8, 8.1, 9.0, 8.3, 8.7]
    
    print(f"\nTrue data statistics:")
    print(f"  Count: {len(severity_scores)}")
    print(f"  Sum: {sum(severity_scores):.2f}")
    print(f"  Mean: {np.mean(severity_scores):.2f}")
    print(f"  Min: {min(severity_scores):.2f}, Max: {max(severity_scores):.2f}")
    
    # Set privacy parameters
    epsilon = 1.0
    delta = 1e-6
    max_value = 10.0  # Severity scores are 0-10
    
    # Run DP queries
    print(f"\nDifferentially private statistics (ε={epsilon}, δ={delta}):")
    
    count_query = CountQuery(epsilon=epsilon/3, delta=delta/3)
    dp_count = count_query.execute(severity_scores)
    print(f"  Noisy count: {dp_count:.2f}")
    
    sum_query = SumQuery(epsilon=epsilon/3, delta=delta/3, max_value=max_value)
    dp_sum = sum_query.execute(severity_scores)
    print(f"  Noisy sum: {dp_sum:.2f}")
    
    mean_query = MeanQuery(epsilon=epsilon/3, delta=delta/3, max_value=max_value)
    dp_mean = mean_query.execute(severity_scores)
    print(f"  Noisy mean: {dp_mean:.2f}")


def example_composition():
    """Demonstrate privacy composition theorems."""
    print("\n" + "=" * 70)
    print("Example 4: Privacy Composition Theorems")
    print("=" * 70)
    
    epsilon_per_query = 0.5
    delta_per_query = 1e-6
    num_queries = 5
    
    print(f"\nScenario: {num_queries} queries, each with ε={epsilon_per_query}, δ={delta_per_query}")
    
    # Basic composition
    basic = PrivacyComposition.basic_composition(epsilon_per_query, delta_per_query, num_queries)
    print(f"\nBasic composition: {basic}")
    
    # Advanced composition (better bounds)
    advanced = PrivacyComposition.advanced_composition(
        epsilon_per_query, delta_per_query, num_queries, delta_prime=1e-6
    )
    print(f"Advanced composition: {advanced}")
    
    # Parallel composition (no additional cost)
    parallel = PrivacyComposition.parallel_composition(
        epsilon_per_query, delta_per_query, num_queries
    )
    print(f"Parallel composition: {parallel}")


if __name__ == "__main__":
    print("\n" + "*" * 70)
    print("Differentially Private Threat Intelligence Analytics Examples")
    print("*" * 70)
    
    example_basic_analytics()
    example_multiple_queries()
    example_aggregations()
    example_composition()
    
    print("\n" + "*" * 70)
    print("Examples completed successfully!")
    print("*" * 70 + "\n")
