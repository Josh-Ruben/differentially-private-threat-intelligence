# Privacy Theory

## Differential Privacy Fundamentals

Differential privacy is a mathematical framework that guarantees privacy by ensuring that individual records cannot significantly influence query results.

## Definition

A mechanism M provides (ε, δ)-differential privacy if for any two adjacent datasets D and D' (differing by one record):

```
Pr[M(D) = O] ≤ e^ε × Pr[M(D') = O] + δ
```

Where:
- **ε (epsilon)**: Privacy loss parameter (lower = more privacy)
  - ε ≈ 0.1: Strong privacy
  - ε ≈ 1: Moderate privacy
  - ε ≈ 10: Weak privacy
- **δ (delta)**: Failure probability (typically 10^-6)

## Core Mechanisms

### Laplace Mechanism

For numerical queries, adds noise from Laplace distribution:

```
M(D) = f(D) + Laplace(0, Δf/ε)
```

Where Δf is the sensitivity (max change from removing one record).

**Pros**: Simple, fast, pure differential privacy
**Cons**: Works best for low-dimensional queries

### Gaussian Mechanism

For (ε, δ)-differential privacy:

```
M(D) = f(D) + N(0, σ²)
σ = Δf × ��(2 ln(1.25/δ)) / ε
```

**Pros**: Better composition properties, smaller noise for same privacy
**Cons**: Requires δ > 0

### Exponential Mechanism

For selecting from discrete options based on scores:

```
Pr[M(D) = o] ∝ exp(ε × score(o) / (2 × Δscore))
```

**Pros**: Utility-optimal for discrete problems
**Cons**: More complex, requires score normalization

## Composition

When running multiple queries, privacy budgets compose:

### Basic Composition
Running k queries with parameters (ε, δ):
- Total: (k×ε, k×δ)
- Loose bounds, rarely tight

### Advanced Composition (Dwork et al.)
Provides better bounds:
- Total: (k×ε²/ln(1/δ'), δ + k×δ')
- Much tighter for large k
- Requires additional δ'

### Parallel Composition
Queries on disjoint data subsets:
- Total: (ε, δ)
- Same privacy as single query!
- Not practical in many scenarios

## Key Concepts

### Sensitivity (Δf)

Maximum change in query output when one record is added/removed.

**Examples**:
- Count: Δf = 1 (changing one record changes count by ≤1)
- Sum of bounded values [0, V]: Δf = V
- Mean of [0, V] with n records: Δf = V/n

### Privacy Budget

Total privacy loss across all queries. Organization must:
1. Set total budget (ε, δ)
2. Allocate to queries
3. Track spending
4. Refuse queries when budget exhausted

### Utility-Privacy Tradeoff

- Lower ε = More privacy but more noise, less useful
- Higher ε = Less privacy but less noise, more useful
- Must balance requirements

## Privacy-Preserving Threat Intelligence

### Application to TI

1. **Data Sharing**: Organizations share threat data while protecting individual indicators
2. **Collaborative Analysis**: Multiple orgs analyze together without revealing specifics
3. **Statistics**: Compute aggregate threat statistics ("how many malware?")
4. **Detection**: Build models without access to raw sensitive data

### Specific Guarantees

- **Indicator Privacy**: Removing one malware sample shouldn't change results much
- **Organization Privacy**: One organization's data shouldn't significantly influence outputs
- **Temporal Privacy**: Time-series TI analysis maintains privacy across time

### Common Pitfalls

1. **Budget Exhaustion**: Using all privacy budget without planning
2. **Poor Sensitivity**: Underestimating max change leads to weak privacy
3. **Temporal Leakage**: Repeated queries on similar data over time
4. **Composition Neglect**: Forgetting that queries compose

## References

- Dwork, C. (2006). "Differential Privacy" - Foundational paper
- McSherry, F. (2009). "Privacy Integrated Queries" - Practical system design
- Vadhan, S. (2017). "The Complexity of Differential Privacy" - Comprehensive survey
- [OpenDP Project](https://opendp.org/) - Open source resources
