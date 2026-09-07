# Contributing to Differentially Private Threat Intelligence Analytics

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

This project adheres to the Contributor Covenant Code of Conduct. By participating, you are expected to uphold this code.

## How to Contribute

### Reporting Bugs

Before creating a bug report, please check the issue list to avoid duplicates. When reporting a bug, include:

- **Clear description** of the issue
- **Steps to reproduce** the behavior
- **Expected behavior** and actual behavior
- **Screenshots or logs** if applicable
- **Environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When suggesting an enhancement:

- Use a clear, descriptive title
- Provide a detailed description of the suggested enhancement
- Include examples of how it would be used
- Explain why this enhancement would be useful

### Pull Requests

1. **Fork the repository** and create a feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and commit with clear messages
   ```bash
   git commit -m "Add clear description of changes"
   ```

3. **Write tests** for new functionality
   ```bash
   pytest tests/test_your_feature.py
   ```

4. **Run code quality checks**
   ```bash
   black src/
   isort src/
   flake8 src/
   mypy src/
   ```

5. **Update documentation** if applicable

6. **Push to your fork** and submit a Pull Request
   ```bash
   git push origin feature/your-feature-name
   ```

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/differentially-private-threat-intelligence.git
cd differentially-private-threat-intelligence

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Setup pre-commit hooks
pre-commit install
```

## Coding Standards

- **Language**: Python 3.8+
- **Style**: PEP 8 (enforced by Black and Flake8)
- **Type hints**: Required for all public functions
- **Docstrings**: Google-style docstrings for all modules, classes, and functions
- **Tests**: Aim for >80% code coverage

### Example Function:

```python
def add_laplace_noise(value: float, sensitivity: float, epsilon: float) -> float:
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
    return value + noise
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src/dpti --cov-report=html tests/

# Run specific test file
pytest tests/test_mechanisms.py -v

# Run tests matching a pattern
pytest -k "test_laplace" -v
```

## Documentation

- Use clear, technical language
- Include examples for complex concepts
- Update README.md for major changes
- Use docstrings for code documentation

### Building Documentation Locally:

```bash
cd docs
make html
open _build/html/index.html
```

## Commit Messages

Follow these guidelines for commit messages:

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line
- Example:
  ```
  Add Laplace mechanism implementation
  
  Implement the Laplace mechanism for adding noise to numerical queries.
  Includes noise calibration based on sensitivity and epsilon.
  
  Fixes #42
  ```

## Review Process

1. **Code Review**: Your PR will be reviewed by maintainers
2. **Feedback**: Address any requested changes
3. **Approval**: Once approved, your PR will be merged
4. **Release**: Your contribution may be included in the next release

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.
