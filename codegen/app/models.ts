// Interface for the Analysis section
interface Analysis {
    title: string;        // Title of the analysis
    date_start: string;   // Start date of the analysis (ISO format)
    date_end: string;     // End date of the analysis (ISO format)
}

// Interface for the Table section
interface Table {
    n: number;                    // Number of rows
    n_var: number;                // Number of variables
    memory_size: number;          // Memory usage in bytes
    record_size: number;          // Average record size in bytes
    n_cells_missing: number;      // Total number of missing cells
    n_vars_with_missing: number;  // Number of variables with missing values
    n_vars_all_missing: number;   // Number of variables entirely missing
    p_cells_missing: number;      // Proportion of missing cells (0 to 1)
    types: { [key: string]: number };  // Count of each variable type (e.g., {"Categorical": 5})
    n_duplicates: number;         // Number of duplicate rows
    p_duplicates: number;         // Proportion of duplicate rows (0 to 1)
}

// Interface for the Variable section
// Includes common fields and optional type-specific fields
interface Variable {
    type: string;           // Variable type (e.g., "Categorical", "DateTime", "Text")
    n_distinct: number;     // Number of distinct values
    p_distinct: number;     // Proportion of distinct values (0 to 1)
    is_unique: boolean;     // Whether all values are unique
    n_unique?: number;      // Number of unique values (optional)
    p_unique?: number;      // Proportion of unique values (optional)
    hashable: boolean;      // Whether the variable is hashable
    n_missing: number;      // Number of missing values
    n: number;              // Total number of observations
    p_missing: number;      // Proportion of missing values (0 to 1)
    count: number;          // Number of non-missing values
    memory_size: number;    // Memory usage in bytes

    // Optional fields for Categorical variables
    value_counts_without_nan?: { [key: string]: number };  // Value counts excluding NaN
    value_counts_index_sorted?: { [key: string]: number }; // Sorted value counts
    ordering?: boolean;         // Whether values are ordered
    imbalance?: number;         // Imbalance measure
    chi_squared?: { statistic: number; pvalue: number };  // Chi-squared test results

    // Optional fields for Text variables
    max_length?: number;        // Maximum length of text
    mean_length?: number;       // Mean length of text
    median_length?: number;     // Median length of text
    min_length?: number;        // Minimum length of text
    length_histogram?: { [key: string]: number };  // Histogram of lengths
    histogram_length?: { counts: number[]; bin_edges: number[] };  // Histogram bins
    n_characters_distinct?: number;  // Number of distinct characters
    n_characters?: number;     // Total number of characters
    character_counts?: { [key: string]: number };  // Frequency of each character
    category_alias_values?: { [key: string]: string };  // Category aliases
    block_alias_values?: { [key: string]: string };  // Block aliases
    block_alias_counts?: { [key: string]: number };  // Block alias frequencies
    n_block_alias?: number;    // Number of block aliases
    block_alias_char_counts?: { [key: string]: { [char: string]: number } };  // Char counts per block
    script_counts?: { [key: string]: number };  // Frequency of scripts (e.g., Latin)
    n_scripts?: number;        // Number of scripts
    script_char_counts?: { [key: string]: { [char: string]: number } };  // Char counts per script
    category_alias_counts?: { [key: string]: number };  // Category alias frequencies
    n_category?: number;       // Number of categories
    category_alias_char_counts?: { [key: string]: { [char: string]: number } };  // Char counts per category
    word_counts?: { [key: string]: number };  // Word frequency

    // Optional fields for DateTime variables
    cast_type?: string;        // Type cast applied (if any)
    min?: string;              // Minimum value (ISO format)
    max?: string;              // Maximum value (ISO format)
    range?: string;            // Range of values
    histogram?: { counts: number[]; bin_edges: number[] };  // Histogram bins
    invalid_dates?: number;    // Number of invalid dates
    n_invalid_dates?: number;  // Duplicate field for invalid dates
    p_invalid_dates?: number;  // Proportion of invalid dates (0 to 1)

    // General optional field for sample values
    first_rows?: { [key: string]: string };  // Sample of initial values
}

// Interface for the Correlation section
interface Correlation {
    auto: Array<{ [key: string]: number }>;  // List of correlation dictionaries (e.g., variable pairs)
}

// Interface for bar chart data
interface BarChartData {
    counts: number[];
    labels: string[];
    percentages: number[];
}

// Interface for matrix data
interface MatrixData {
    values: number[][];
    labels: string[];
    colorScale: string[];
}

// Interface for the Missing section
interface Missing {
    bar: BarChartData;    // Bar chart data for missing values
    matrix: MatrixData;   // Matrix data for missing values
}

// Interface for the Package section
interface Package {
    ydata_profiling_version: string;  // Version of the profiling package
    ydata_profiling_config: string;   // Configuration used (stringified JSON)
}

// Interface for sample row data
interface SampleRowData {
    [key: string]: string | number | boolean | null;
}

// Interface for the Sample section
interface Sample {
    id: string;              // Identifier (e.g., "head", "tail")
    data: SampleRowData[];   // Sample rows as key-value pairs
    name: string;            // Name of the sample (e.g., "First rows")
    caption?: string;        // Optional caption for the sample
}

// Interface for scatter plot data
interface ScatterPlotData {
    x: number[];
    y: number[];
    labels: string[];
    correlations: number[];
}

// Interface for duplicate data
interface DuplicateData {
    index: number[];
    count: number;
    percentage: number;
}

// Interface for transformations
interface Transformation {
    description: string;  // Description of the transformation
    timestamp: string;    // When the transformation was applied
    version: string;      // Version number of the transformation
}

// Root interface for the entire profiling output
export interface DatasetProfile {
    analysis: Analysis;                        // Analysis metadata
    time_index_analysis?: string | null;       // Time index analysis (often null)
    table: Table;                              // Table statistics
    variables: { [key: string]: Variable };    // Dictionary of variables by name
    scatter: ScatterPlotData;                  // Scatter plot data
    correlations: Correlation;                 // Correlation data
    missing: Missing;                          // Missing value visualizations
    alerts: string[];                          // List of warnings or alerts
    package: Package;                          // Package metadata
    sample: Sample[];                          // List of sample sections
    duplicates: DuplicateData[];              // List of duplicate rows or related data
    transformations: Transformation[];         // List of transformations applied to the dataset
}