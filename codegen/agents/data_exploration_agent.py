import pandas as pd
from pathlib import Path
from typing import Dict, Any

class DataExplorationAgent:
    """Automates basic EDA and suggests visuals."""

    def explore(self, csv_path: str) -> Dict[str, Any]:
        df = pd.read_csv(csv_path)
        summary = df.describe(include='all').to_dict()
        visuals = []
        if 'date' in df.columns or any('date' in c.lower() for c in df.columns):
            visuals.append({'type': 'line', 'x': 'date', 'y': df.columns[1]})
        if len(df.columns) >= 2:
            visuals.append({'type': 'bar', 'x': df.columns[0], 'y': df.columns[1]})
        return {'summary': summary, 'suggested_visuals': visuals}
