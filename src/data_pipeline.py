import pandas as pd
import os

def load_events_data(filepath="data/events.csv"):
    """
    Loads and validates the manually curated events dataset.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Error: Could not find {filepath}. Please ensure the file exists.")
    
    print(f"Loading event data from {filepath}...")
    df = pd.read_csv(filepath)
    
    # Standardize column names just in case of typos
    df.columns = df.columns.str.strip().str.title()
    
    # Ensure dates are actual datetime objects
    try:
        df['Event_Date'] = pd.to_datetime(df['Event_Date'])
    except Exception as e:
        raise ValueError(f"Error parsing dates in CSV. Ensure they are YYYY-MM-DD. Details: {e}")
        
    print(f"Successfully loaded {len(df)} events.")
    return df