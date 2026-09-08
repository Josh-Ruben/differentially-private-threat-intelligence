"""Example: Privacy-Preserving Threat Intelligence Sharing."""

import numpy as np
import pandas as pd
from dpti.analytics import CountQuery, MeanQuery, HistogramQuery
from dpti.privacy.composition import PrivacyBudget


def example_threat_sharing():
    """Demonstrate privacy-preserving threat sharing across organizations."""
    print("=" * 70)
    print("Example: Multi-Organization Threat Intelligence Sharing")
    print("=" * 70)
    
    # Simulate threat data from multiple organizations
    organizations = {
        "Org_A": {"malware_samples": [10, 15, 12, 18, 14],
                  "severity_scores": [7.5, 8.2, 6.9, 8.8, 7.1]},
        "Org_B": {"malware_samples": [8, 12, 11, 16, 13],
                  "severity_scores": [7.8, 8.1, 7.2, 8.5, 7.4]},
        "Org_C": {"malware_samples": [12, 18, 14, 20, 16],
                  "severity_scores": [8.1, 8.4, 7.5, 8.9, 7.6]},
    }
    
    # Create shared privacy budget
    shared_budget = PrivacyBudget(total_epsilon=2.0, total_delta=1e-5)
    
    print(f"\nShared privacy budget initialized: {shared_budget}")
    print(f"\nOrganizations participating: {', '.join(organizations.keys())}")
    
    # Aggregate data with privacy
    all_samples = []
    all_scores = []
    
    for org_name, org_data in organizations.items():
        all_samples.extend(org_data["malware_samples"])
        all_scores.extend(org_data["severity_scores"])
        print(f"\n{org_name}:")
        print(f"  Malware samples: {org_data['malware_samples']}")
        print(f"  Severity scores: {org_data['severity_scores']}")
    
    # Perform shared analytics with privacy
    print(f"\n" + "-" * 70)
    print("Shared Analytics Results (Differentially Private):")
    print("-" * 70)
    
    # Count query
    count_query = CountQuery(epsilon=0.5, delta=3e-6)
    dp_count = count_query.execute(all_samples)
    shared_budget.spend(0.5, 3e-6, "Total threat count")
    print(f"\nTotal threats detected (DP): {dp_count:.0f}")
    print(f"  Budget: {shared_budget}")
    
    # Mean severity query
    mean_query = MeanQuery(epsilon=0.5, delta=3e-6, max_value=10.0)
    dp_mean_severity = mean_query.execute(all_scores)
    shared_budget.spend(0.5, 3e-6, "Mean severity")
    print(f"\nMean threat severity (DP): {dp_mean_severity:.2f}")
    print(f"  Budget: {shared_budget}")
    
    # Histogram query
    histogram_query = HistogramQuery(
        epsilon=1.0, delta=4e-6, bins=5, range_tuple=(6, 9)
    )
    histogram_result = histogram_query.execute(all_scores)
    shared_budget.spend(1.0, 4e-6, "Severity histogram")
    print(f"\nSeverity score distribution (DP):")
    for center, count in zip(
        histogram_result["bin_centers"], histogram_result["noisy_counts"]
    ):
        print(f"  Score {center:.1f}: {count:.1f} threats")
    print(f"  Budget: {shared_budget}")
    
    if shared_budget.is_exhausted():
        print(f"\n⚠️  Privacy budget exhausted!")
    else:
        print(f"\n✓ Additional queries possible with remaining budget")


if __name__ == "__main__":
    print("\n" + "*" * 70)
    print("Differentially Private Threat Intelligence Sharing")
    print("*" * 70 + "\n")
    
    example_threat_sharing()
    
    print("\n" + "*" * 70)
    print("Example completed successfully!")
    print("*" * 70 + "\n")
