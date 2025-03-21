from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class Analysis(BaseModel):
    title: str
    date_start: str
    date_end: str

class Table(BaseModel):
    n: int
    n_var: int
    memory_size: int
    record_size: float
    n_cells_missing: int
    n_vars_with_missing: int
    n_vars_all_missing: int
    p_cells_missing: float
    types: Dict[str, int]
    n_duplicates: int
    p_duplicates: float

class Variable(BaseModel):
    type: str
    n_distinct: int
    p_distinct: float
    is_unique: bool
    n_unique: Optional[int] = None
    p_unique: Optional[float] = None
    hashable: bool
    n_missing: int
    n: int
    p_missing: float
    count: int
    memory_size: int
    value_counts_without_nan: Optional[Dict[str, int]] = None
    value_counts_index_sorted: Optional[Dict[str, int]] = None
    ordering: Optional[bool] = None
    imbalance: Optional[float] = None
    first_rows: Optional[Dict[str, str]] = None
    chi_squared: Optional[Dict[str, float]] = None
    max_length: Optional[int] = None
    mean_length: Optional[float] = None
    median_length: Optional[int] = None
    min_length: Optional[int] = None
    length_histogram: Optional[Dict[str, int]] = None
    histogram_length: Optional[Dict[str, List[float]]] = None
    n_characters_distinct: Optional[int] = None
    n_characters: Optional[int] = None
    character_counts: Optional[Dict[str, int]] = None
    category_alias_values: Optional[Dict[str, str]] = None
    block_alias_values: Optional[Dict[str, str]] = None
    block_alias_counts: Optional[Dict[str, int]] = None
    n_block_alias: Optional[int] = None
    block_alias_char_counts: Optional[Dict[str, Dict[str, int]]] = None
    script_counts: Optional[Dict[str, int]] = None
    n_scripts: Optional[int] = None
    script_char_counts: Optional[Dict[str, Dict[str, int]]] = None
    category_alias_counts: Optional[Dict[str, int]] = None
    n_category: Optional[int] = None
    category_alias_char_counts: Optional[Dict[str, Dict[str, int]]] = None
    word_counts: Optional[Dict[str, int]] = None
    cast_type: Optional[str] = None
    min: Optional[str] = None
    max: Optional[str] = None
    range: Optional[str] = None
    histogram: Optional[Dict[str, List[float]]] = None
    invalid_dates: Optional[int] = None
    n_invalid_dates: Optional[int] = None
    p_invalid_dates: Optional[float] = None



class DatasetProfile(BaseModel):
    analysis: Analysis
    time_index_analysis: Optional[str] = None
    table: Table
    variables: Dict[str, Variable]
    alerts: List[str]
