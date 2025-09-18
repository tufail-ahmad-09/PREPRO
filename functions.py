import pandas as pd
from sklearn.model_selection import train_test_split

# Optional profiling import
try:
    from ydata_profiling import ProfileReport
    PROFILING_AVAILABLE = True
except ImportError:
    PROFILING_AVAILABLE = False

def missing_data_summary(df):
    """Return a summary DataFrame of missing data counts and percentages for each column."""
    missing_count = df.isnull().sum()
    missing_percent = 100 * missing_count / len(df)
    summary_df = pd.DataFrame({
        'missing_count': missing_count,
        'missing_percent': missing_percent
    })
    return summary_df

def handle_missing_data(df, method='drop_rows', fill_value=None):
    """
    Handle missing data in the DataFrame using specified method.

    Args:
    - df: pandas DataFrame
    - method: str, one of ['drop_rows', 'drop_columns', 'fill_mean', 'fill_median', 'fill_mode', 'fill_value']
    - fill_value: value to fill if method is 'fill_value'

    Returns:
    - DataFrame after missing data handling
    """
    if method == 'drop_rows':
        return df.dropna()
    elif method == 'drop_columns':
        return df.dropna(axis=1)
    elif method == 'fill_mean':
        return df.fillna(df.mean(numeric_only=True))
    elif method == 'fill_median':
        return df.fillna(df.median(numeric_only=True))
    elif method == 'fill_mode':
        mode_vals = df.mode().iloc[0]
        return df.fillna(mode_vals)
    elif method == 'fill_value':
        if fill_value is None:
            raise ValueError("fill_value must be provided when method='fill_value'")
        return df.fillna(fill_value)
    else:
        raise ValueError("Invalid method specified")
    
def duplicate_summary(df):
    """
    Returns the number of duplicate rows and optionally the duplicate rows themselves.
    """
    duplicate_count = df.duplicated().sum()
    duplicates = df[df.duplicated(keep=False)]
    return duplicate_count, duplicates

def remove_duplicates(df):
    """
    Removes duplicate rows from the DataFrame and returns the cleaned DataFrame.
    """
    return df.drop_duplicates()

def generate_profile_report(df, output_path="profile_report.html"):
    """
    Generates an automated profiling HTML report for a given DataFrame.
    Saves the report to the specified output_path.
    """
    if not PROFILING_AVAILABLE:
        # Create a simple HTML report if ydata-profiling is not available
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Data Profile Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .stats {{ margin: 20px 0; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>Data Profile Report</h1>
            <div class="stats">
                <h2>Dataset Overview</h2>
                <p><strong>Rows:</strong> {len(df)}</p>
                <p><strong>Columns:</strong> {len(df.columns)}</p>
                <p><strong>Memory Usage:</strong> {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB</p>
            </div>
            
            <div class="stats">
                <h2>Column Information</h2>
                <table>
                    <tr><th>Column</th><th>Type</th><th>Non-Null Count</th><th>Missing %</th></tr>
                    {''.join([f"<tr><td>{col}</td><td>{df[col].dtype}</td><td>{df[col].count()}</td><td>{(df[col].isnull().sum()/len(df)*100):.1f}%</td></tr>" for col in df.columns])}
                </table>
            </div>
            
            <div class="stats">
                <h2>Statistical Summary</h2>
                {df.describe().to_html()}
            </div>
        </body>
        </html>
        """
        with open(output_path, 'w') as f:
            f.write(html_content)
        return output_path
    else:
        # Use ydata-profiling if available
        profile = ProfileReport(df, title="Automated Profiling Report", explorative=True)
        profile.to_file(output_path)
        return output_path
"""function to train,test and split the dataset"""
from sklearn.model_selection import train_test_split

def split_train_test(df, target_col, test_size=0.2, stratify=True):
    """
    Splits the dataframe into train and test sets.
    
    Args:
        df (pd.DataFrame): The input dataframe.
        target_col (str): The name of the target column.
        test_size (float): Fraction of data to use as test set (default 0.2).
        stratify (bool): Whether to stratify by target for classification (default True).
        
    Returns:
        tuple: (train_df, test_df) split dataframes including target column.
    """
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in dataframe.")

    X = df.drop(columns=[target_col])
    y = df[target_col]

    stratify_data = y if stratify else None

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=stratify_data, random_state=42
    )

    train_df = X_train.copy()
    train_df[target_col] = y_train

    test_df = X_test.copy()
    test_df[target_col] = y_test

    return train_df, test_df


"""function to detect outliers in Data"""
def detect_outliers_iqr(df):
    """
    Detect outliers in numeric columns using the IQR method.
    Returns a DataFrame with boolean flags for outliers per column and an outlier summary.
    """
    outlier_flags = pd.DataFrame(False, index=df.index, columns=df.columns)
    outlier_summary = {}

    for col in df.select_dtypes(include=['number']).columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Flag outliers
        outliers = (df[col] < lower_bound) | (df[col] > upper_bound)
        outlier_flags[col] = outliers

        # Summarize
        outlier_summary[col] = outliers.sum()

    return outlier_flags, outlier_summary
"""remove outliers"""
def remove_outliers_iqr(df):
    """
    Remove rows containing outliers in any numeric column based on IQR.
    Returns the cleaned DataFrame.
    """
    flags, _ = detect_outliers_iqr(df)
    # Drop any row that has an outlier in any column
    df_cleaned = df[~flags.any(axis=1)].copy()
    return df_cleaned

