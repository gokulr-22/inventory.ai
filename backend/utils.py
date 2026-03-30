import pandas as pd # type: ignore

def process_file(file):
    """Process uploaded CSV file, auto-detecting format.
    
    Supports two formats:
      1. Long format:  month, product, sales
      2. Wide format:  date-index, Stock_1, Stock_2, ... (stock price columns)
    
    Both are normalized into the long format (month, product, sales) that
    the ML model expects.
    """
    df = pd.read_csv(file)

    # --- Format 1: already has required columns ---
    required = ['month', 'product', 'sales']
    if all(col in df.columns for col in required):
        return df

    # --- Format 2: wide table (date index + numeric stock columns) ---
    # The first column is typically a date (possibly unnamed or 'Unnamed: 0')
    # and the remaining columns are stock/product values.

    # Identify the date column
    date_col = None
    for col in df.columns:
        if 'unnamed' in col.lower() or 'date' in col.lower():
            date_col = col
            break

    # If no explicit date column, check if the first column looks like dates
    if date_col is None:
        first_col = df.columns[0]
        try:
            pd.to_datetime(df[first_col].head())
            date_col = first_col
        except Exception:
            pass

    if date_col is not None:
        # Parse dates and derive a numeric month index
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df = df.dropna(subset=[date_col])

        # Value columns = everything except the date column
        value_cols = [c for c in df.columns if c != date_col]

        if not value_cols:
            raise Exception("No value columns found in the uploaded CSV")

        # Melt wide → long
        melted = df.melt(id_vars=[date_col], value_vars=value_cols,
                         var_name='product', value_name='sales')

        # Create a sequential month index per product (1-based)
        melted = melted.sort_values([date_col, 'product']).reset_index(drop=True)
        melted['month'] = melted.groupby('product').cumcount() + 1

        # Keep only the columns the model needs
        melted = melted[['month', 'product', 'sales']]

        # Ensure numeric sales
        melted['sales'] = pd.to_numeric(melted['sales'], errors='coerce')
        melted = melted.dropna(subset=['sales'])

        return melted

    # --- Fallback: try treating all numeric columns as products ---
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if numeric_cols:
        df['month'] = range(1, len(df) + 1)
        melted = df.melt(id_vars=['month'], value_vars=numeric_cols,
                         var_name='product', value_name='sales')
        melted['sales'] = pd.to_numeric(melted['sales'], errors='coerce')
        melted = melted.dropna(subset=['sales'])
        return melted

    raise Exception(
        "Could not parse CSV. Expected either columns [month, product, sales] "
        "or a date-indexed table with numeric value columns."
    )