# System Architecture

## Overview

The Differentially Private Threat Intelligence (DPTI) system is built as a modular, layered architecture to support scalable privacy-preserving analytics.

## Component Architecture

### 1. Data Ingestion Layer

**Purpose**: Load and normalize threat intelligence from various sources.

**Components**:
- `loaders.py`: Data source connectors (CSV, JSON, APIs)
- `normalizer.py`: Schema normalization and standardization
- `validators.py`: Data validation and quality checks

**Key Features**:
- Multi-format support (CSV, JSON, STIX, etc.)
- Deduplication and conflict resolution
- Schema mapping and transformation

### 2. Privacy Mechanisms Layer

**Purpose**: Implement and manage differential privacy mechanisms.

**Components**:
- `mechanisms.py`: Core DP algorithms (Laplace, Gaussian, Exponential)
- `composition.py`: Composition theorems for budget management
- `budget.py`: Privacy budget tracking and enforcement
- `calibration.py`: Automatic noise calibration

**Key Features**:
- Multiple DP mechanisms
- Automatic sensitivity calculation
- Privacy budget accounting
- Composition safety guarantees

### 3. Analytics Engine

**Purpose**: Execute queries on protected data.

**Components**:
- `queries.py`: Query implementations
- `aggregations.py`: Aggregation functions with DP
- `ml.py`: Machine learning with differential privacy

**Key Features**:
- Count and sum queries
- Aggregations (mean, percentile, histogram)
- Statistical analysis
- Private model training

### 4. API & Integration Layer

**Purpose**: Provide external interfaces.

**Components**:
- `routes.py`: REST API endpoints
- `auth.py`: Authentication and authorization

**Key Features**:
- REST API for query submission
- Python SDK
- SQL query interface (future)

### 5. Utilities & Infrastructure

**Components**:
- `logging.py`: Audit logging
- `metrics.py`: Performance monitoring
- `config.py`: Configuration management

## Data Flow

```
Threat Intelligence Sources
    ↓
[Data Ingestion & Normalization]
    ↓
Standardized TI Dataset
    ↓
[User Query]
    ↓
[Privacy Budget Allocation]
    ↓
[Query Execution with DP Mechanisms]
    ↓
[Result Sanitization]
    ↓
Differentially Private Results
```

## Deployment Architecture

### Single Machine
- Suitable for prototyping and small datasets
- All components in single process

### Distributed (PySpark)
- Distributed query execution
- Privacy budget management across nodes
- Large-scale threat intelligence processing

### Cloud-Native
- Containerized components (Docker)
- Kubernetes orchestration
- Managed privacy budget service
- Audit logging to persistent storage

## Privacy Guarantees

The system provides:
- **Epsilon-differential privacy**: Controlled data leakage
- **Delta parameter support**: Failure probability bound
- **Composition safety**: Multiple query privacy guarantees
- **Budget enforcement**: Strict epsilon/delta tracking

## Scalability Considerations

1. **Data Volume**: Distributed processing with PySpark
2. **Query Throughput**: Caching and query optimization
3. **Privacy Budget**: Privacy broker service for coordination
4. **Audit Trail**: Time-series database for logging
