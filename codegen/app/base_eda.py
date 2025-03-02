import pandas as pd
import numpy as np
from typing import Dict, List, Union
from collections import defaultdict
import json
from pandas.api.types import is_datetime64_any_dtype, is_numeric_dtype, is_object_dtype

class DataFrameJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        if isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if pd.isna(obj):
            return None
        if isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        return super().default(obj)

def load_data(file_path: str) -> pd.DataFrame:
    """ Load data (supports CSV for now, can be extended). """
    return pd.read_csv(file_path)

def infer_column_types(df: pd.DataFrame) -> Dict[str, List[str]]:
    """ Classify columns into comprehensive categories. """
    types = defaultdict(list)

    for col in df.columns:
        unique_count = df[col].nunique()

        if is_datetime64_any_dtype(df[col]):
            types['datetime'].append(col)
        elif is_numeric_dtype(df[col]):
            types['numeric'].append(col)
        elif is_object_dtype(df[col]):
            if unique_count < 50:
                types['categorical_low_cardinality'].append(col)
            else:
                types['categorical_high_cardinality'].append(col)

    return types

def column_missingness(df: pd.DataFrame) -> Dict[str, float]:
    """ Compute percentage of missing values per column. """
    return {col: df[col].isnull().mean() * 100 for col in df.columns}

def column_cardinality(df: pd.DataFrame) -> Dict[str, int]:
    """ Count unique values per column. """
    return {col: df[col].nunique() for col in df.columns}

def detect_primary_key_candidates(df: pd.DataFrame) -> List[str]:
    """ Columns where number of unique values ≈ number of rows. """
    candidates = []
    row_count = len(df)
    for col in df.columns:
        if df[col].nunique() >= row_count * 0.95:
            candidates.append(col)
    return candidates

def detect_outliers(df: pd.DataFrame) -> Dict[str, Dict[str, Union[int, float]]]:
    """ Identify outliers in numeric columns using IQR method. """
    outlier_report = {}

    for col in df.columns:
        if is_numeric_dtype(df[col]):
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()

            outlier_report[col] = {
                'outlier_count': int(outliers),
                'lower_bound': lower_bound,
                'upper_bound': upper_bound
            }
    return outlier_report

def suggest_filters(df: pd.DataFrame) -> List[str]:
    """ Suggest columns as filters if they are low-cardinality categorical or datetime. """
    filters = []
    for col in df.columns:
        unique_count = df[col].nunique()

        if is_datetime64_any_dtype(df[col]):
            filters.append(f"Date filter on '{col}'")
        elif is_object_dtype(df[col]) and unique_count < 50:
            filters.append(f"Category filter on '{col}'")

    return filters

def detect_date_frequency(df: pd.DataFrame) -> Dict[str, str]:
    """ Detect frequency for datetime columns using inferred gaps. """
    frequencies = {}
    for col in df.columns:
        if is_datetime64_any_dtype(df[col]):
            date_series = pd.to_datetime(df[col]).dropna().sort_values()
            inferred_freq = pd.infer_freq(date_series)
            frequencies[col] = inferred_freq if inferred_freq else "Irregular"
    return frequencies

def basic_distribution_summary(df: pd.DataFrame) -> Dict[str, Dict[str, Union[float, int, str]]]:
    """ For numeric and categorical columns, produce basic distribution summaries. """
    summaries = {}

    for col in df.columns:
        if is_numeric_dtype(df[col]):
            summaries[col] = {
                'mean': df[col].mean(),
                'median': df[col].median(),
                'min': df[col].min(),
                'max': df[col].max(),
                'std_dev': df[col].std()
            }
        elif is_object_dtype(df[col]) and df[col].nunique() < 50:
            summaries[col] = {
                'top_values': df[col].value_counts().head(5).to_dict()
            }
    return summaries

def assess_data_quality(df: pd.DataFrame) -> Dict[str, Union[int, float]]:
    """ Dataset-level quality check. """
    return {
        "row_count": len(df),
        "column_count": len(df.columns),
        "missing_value_percentage": df.isnull().mean().mean() * 100,
        "duplicate_row_count": df.duplicated().sum()
    }

def process_file(file_path: str, output_file: str = None) -> Dict:
    """ Full pipeline for non-NLP inference over a dataset. """
    df = load_data(file_path)

    inferred_context = {
        "column_types": infer_column_types(df),
        "column_missingness": column_missingness(df),
        "column_cardinality": column_cardinality(df),
        "primary_key_candidates": detect_primary_key_candidates(df),
        "outlier_report": detect_outliers(df),
        "suggested_filters": suggest_filters(df),
        "date_frequencies": detect_date_frequency(df),
        "basic_distribution_summary": basic_distribution_summary(df),
        "data_quality": assess_data_quality(df)
    }

    if output_file:
        with open(output_file, 'w') as f:
            json.dump(inferred_context, f, cls=DataFrameJSONEncoder, indent=2)

    return inferred_context

# Example Run
if __name__ == "__main__":
    file_path = "example_data.csv"
    output_file = "eda_results.json"
    context = process_file(file_path, output_file)
    print(json.dumps(context, cls=DataFrameJSONEncoder, indent=2))
