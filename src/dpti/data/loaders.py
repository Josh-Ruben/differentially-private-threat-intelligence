"""Threat Intelligence data loaders and sources."""

from typing import List, Dict, Any
import pandas as pd


class ThreatIntelligenceFeed:
    """Loader for threat intelligence feeds."""

    def __init__(self, data_path: str):
        """Initialize threat intelligence feed loader.
        
        Args:
            data_path: Path to the threat intelligence data file.
        """
        self.data_path = data_path
        self.data: pd.DataFrame = pd.DataFrame()
        self.indicators: List[Dict[str, Any]] = []
        self._load_data()

    def _load_data(self) -> None:
        """Load data from file."""
        try:
            if self.data_path.endswith('.csv'):
                self.data = pd.read_csv(self.data_path)
            elif self.data_path.endswith('.json'):
                self.data = pd.read_json(self.data_path)
            else:
                raise ValueError(f"Unsupported file format: {self.data_path}")
            
            self.indicators = self.data.to_dict('records')
        except FileNotFoundError:
            raise FileNotFoundError(f"Data file not found: {self.data_path}")

    def __len__(self) -> int:
        """Get number of indicators."""
        return len(self.indicators)

    def __iter__(self):
        """Iterate over indicators."""
        return iter(self.indicators)
