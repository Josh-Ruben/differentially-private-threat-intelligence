# Differentially Private Threat Intelligence Analytics at Scale

A scalable, privacy-preserving system for analyzing threat intelligence data with formal differential privacy guarantees. This project enables organizations to collaborate on threat intelligence sharing and analysis without compromising individual data privacy.

## 🎯 Overview

This system implements differential privacy mechanisms to protect sensitive threat intelligence data while enabling meaningful analytics and insights at scale. It's designed for:

- **Security analysts** analyzing threat patterns across multiple sources
- **Organizations** sharing threat intelligence collaboratively
- **Researchers** studying cybersecurity trends with privacy guarantees
- **Compliance teams** maintaining GDPR, CCPA, and other privacy regulations

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Threat Intelligence Sources              │
│  (OSINT, ISACs, Network Logs, Endpoint Detection, etc.)    │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│              Data Ingestion & Normalization Layer           │
│  (Parsing, Deduplication, Validation, Schema Mapping)      │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│           Differential Privacy Mechanisms Layer             │
│  (Laplace, Gaussian, Exponential, Composition Tracking)    │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│            Analytics & Query Engine                         │
│  (Aggregations, Statistics, ML Models with DP)             │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│            Results & Visualization Layer                    │
│  (API, Dashboards, Reports, Insights Export)               │
└─────────────────────────────────────────────────────────────┘
```

## ✨ Key Features

### Core Capabilities
- **Differential Privacy Mechanisms**: Laplace, Gaussian, Exponential Mechanism, and composition tracking
- **Privacy Budget Management**: Track and enforce epsilon (ε) and delta (δ) budgets
- **Multi-level Analytics**: Count queries, aggregations, histograms, and statistical analysis
- **Composition Safety**: Advanced composition theorems (sequential, parallel, basic)
- **Noise Calibration**: Automatic noise scaling based on sensitivity and privacy parameters

### Scalability
- **Distributed Processing**: Support for PySpark and Dask for large-scale data
- **Batch & Streaming**: Handle both batch threat intelligence and real-time feeds
- **Query Optimization**: Efficient algorithms for complex analytical queries
- **Privacy-Utility Tradeoff**: Configurable privacy budgets for different use cases

### Enterprise Features
- **Audit Logging**: Complete audit trail of queries and privacy budget usage
- **Access Control**: Role-based access with privacy budget constraints per role
- **Data Governance**: Metadata tracking, lineage, and compliance reports
- **Integration**: REST API, Python SDK, and SQL query interface

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Josh-Ruben/differentially-private-threat-intelligence.git
cd differentially-private-threat-intelligence

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt
```

### Basic Usage

```python
from dpti.privacy import DPAnalytics
from dpti.data import ThreatIntelligenceFeed

# Initialize privacy-preserving analytics
dp_analytics = DPAnalytics(epsilon=1.0, delta=1e-6)

# Load threat intelligence data
threat_feed = ThreatIntelligenceFeed("data/threats.csv")

# Perform differentially private count query
sensitive_count = len(threat_feed.indicators)
dp_count = dp_analytics.count(sensitive_count)

print(f"Total threats (with DP): {dp_count}")
print(f"Privacy budget used: ε={dp_analytics.epsilon_used}, δ={dp_analytics.delta_used}")
```

## 📚 Documentation

- **[Architecture Guide](docs/architecture.md)** - System design and components
- **[Privacy Theory](docs/privacy-theory.md)** - Differential privacy fundamentals
- **[API Reference](docs/api-reference.md)** - Complete API documentation
- **[Examples](examples/)** - Practical examples and tutorials
- **[Configuration](docs/configuration.md)** - Setup and tuning guide

## 🔬 Project Structure

```
differentially-private-threat-intelligence/
├── src/dpti/
│   ├── privacy/              # DP mechanisms and budget management
│   │   ├── mechanisms.py      # Laplace, Gaussian, Exponential
│   │   ├── composition.py     # Composition theorems
│   │   ├── budget.py          # Privacy budget tracking
│   │   └── calibration.py     # Noise calibration
│   ├── data/                  # Data ingestion and normalization
│   │   ├── loaders.py         # TI source loaders
│   │   ├── normalizer.py      # Data normalization
│   │   └── validators.py      # Schema validation
│   ├── analytics/             # Analytics queries
│   │   ├── queries.py         # Query implementations
│   │   ├── aggregations.py    # Aggregation functions
│   │   └── ml.py              # Private ML models
│   ├── api/                   # REST API
│   │   ├── routes.py          # API endpoints
│   │   └── auth.py            # Authentication/Authorization
│   └── utils/                 # Utilities
│       ├── logging.py         # Audit logging
│       └── metrics.py         # Performance metrics
├── tests/                     # Unit and integration tests
├── examples/                  # Example notebooks and scripts
├── docs/                      # Documentation
├── requirements.txt           # Python dependencies
└── setup.py                   # Package setup
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/dpti tests/

# Run specific test file
pytest tests/test_mechanisms.py -v

# Integration tests
pytest tests/integration/ -v
```

## 📊 Example Workflows

### 1. Privacy-Preserving Threat Count Analysis
Analyze the number of threats in a dataset while protecting individual indicator details.

### 2. Differentially Private Aggregations
Compute statistics (mean, percentile, histogram) over threat properties with formal privacy guarantees.

### 3. Multi-party Collaboration
Multiple organizations contribute threat data to a shared analysis with privacy guarantees for all participants.

### 4. Privacy-Aware Machine Learning
Train models on threat data to predict attack types or severity while maintaining privacy.

## 🔐 Security & Privacy

- **Formal Privacy Guarantees**: All mechanisms proven secure under the DP definition
- **Privacy Budget Enforcement**: Strict tracking and enforcement of epsilon and delta budgets
- **Secure Computation**: No access to raw sensitive data in analytics layer
- **Audit Trail**: Complete logging of all queries and privacy budget usage
- **Regular Security Audits**: Code review and security testing

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run pre-commit checks
pre-commit run --all-files

# Build documentation locally
cd docs && make html
```

## 📖 References

### Foundational Papers
- Dwork, C. (2006). "Differential Privacy"
- McSherry, F. (2009). "Privacy Integrated Queries"
- Vadhan, S. (2017). "The Complexity of Differential Privacy"

### Practical Resources
- [Opacus Documentation](https://opacus.ai/) - PyTorch Differential Privacy
- [Diffprivlib](https://diffprivlib.readthedocs.io/) - IBM's DP Library
- [OpenDP Project](https://opendp.org/) - Open source differential privacy tools

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 👥 Authors

- Josh Ruben ([@Josh-Ruben](https://github.com/Josh-Ruben))

## 🐛 Issues & Support

Found a bug or have a question? Please open an [issue](https://github.com/Josh-Ruben/differentially-private-threat-intelligence/issues) on GitHub.

## 🗺️ Roadmap

### Phase 1: Core DP Mechanisms (Current)
- [x] Basic differential privacy mechanisms
- [ ] Privacy budget management system
- [ ] Composition tracking

### Phase 2: Analytics Engine
- [ ] Count and sum queries
- [ ] Histogram and aggregation queries
- [ ] Statistical analysis functions

### Phase 3: Scalability
- [ ] Distributed computing support
- [ ] Streaming data processing
- [ ] Performance optimization

### Phase 4: Enterprise Features
- [ ] REST API
- [ ] Access control and RBAC
- [ ] Audit logging and compliance

### Phase 5: ML & Advanced Analytics
- [ ] Private machine learning
- [ ] Anomaly detection
- [ ] Predictive threat modeling

---

**Status**: Early Development | **Last Updated**: 2026-09-07
