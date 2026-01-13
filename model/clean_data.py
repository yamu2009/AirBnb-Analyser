import pandas as pd
import numpy as np
import os

def clean_data(input_path, output_path):
    print(f"Loading data from {input_path}...")
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: File not found at {input_path}")
        return

    # Columns we can actually use based on the file inspection
    # Note: 'accommodates' and 'amenities' were requested for frontend but are missing in this CSV.
    # We will use what is available.
    relevant_cols = [
        'neighbourhood', 
        'room_type', 
        'minimum_nights', 
        'availability_365', 
        'price'
    ]
    
    # Check if columns exist
    missing_cols = [c for c in relevant_cols if c not in df.columns]
    if missing_cols:
        print(f"Warning: Missing columns in CSV: {missing_cols}")
        # Proceed with what we have
        relevant_cols = [c for c in relevant_cols if c in df.columns]

    df = df[relevant_cols].copy()

    # 1. Clean Price
    # It seems price is already numeric in the head sample, but good to be safe
    if df['price'].dtype == 'object':
        df['price'] = df['price'].replace('[\$,]', '', regex=True)
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
    
    # Drop rows where price is missing or 0
    df = df.dropna(subset=['price'])
    df = df[df['price'] > 0]

    # 2. Handle Missing Values
    # For numerical cols, fill with median
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        df[col] = df[col].fillna(df[col].median())

    # For categorical cols, fill with mode (most common value)
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        if not df[col].mode().empty:
            df[col] = df[col].fillna(df[col].mode()[0])
        else:
            df[col] = df[col].fillna('Unknown')

    # 3. Save
    print(f"Data cleaned. Shape: {df.shape}")
    print(f"Saving to {output_path}...")
    df.to_csv(output_path, index=False)
    print("Done.")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_csv = os.path.join(base_dir, 'data', 'listings.csv')
    output_csv = os.path.join(base_dir, 'data', 'listings_cleaned.csv')
    
    clean_data(input_csv, output_csv)
