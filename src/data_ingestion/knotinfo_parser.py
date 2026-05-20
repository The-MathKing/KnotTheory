import pandas as pd
import requests
import os
import argparse
import sys

def download_knotinfo(output_path):
    """
    Downloads the KnotInfo complete database.
    """
    url = "https://knotinfo.org/knotinfo_data_complete.xls"
    print(f"Downloading KnotInfo database from {url}...")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"Successfully downloaded to {output_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download the database: {e}")
        sys.exit(1)

def process_invariants(input_path, output_path):
    """
    Reads the downloaded excel file and converts it into a clean, vectorized DataFrame.
    """
    print(f"Loading data from {input_path}...")
    try:
        # Knotinfo XLS files might require xlrd engine
        # Usually the first sheet contains the data
        df = pd.read_excel(input_path, engine='xlrd')
        print(f"Loaded {len(df)} rows and {len(df.columns)} columns.")
        
        # Save a clean CSV for our machine learning models to consume
        df.to_csv(output_path, index=False)
        print(f"Processed dataset saved to {output_path}")
        return df
    except Exception as e:
        print(f"Error processing the excel file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="KnotInfo Data Ingestion")
    parser.add_argument("--raw_output", type=str, default="../../data/raw/knotinfo_data_complete.xls")
    parser.add_argument("--processed_output", type=str, default="../../data/processed/knotinfo_invariants.csv")
    args = parser.parse_args()
    
    download_knotinfo(args.raw_output)
    process_invariants(args.raw_output, args.processed_output)
    
    print("\nData ingestion pipeline complete.")
