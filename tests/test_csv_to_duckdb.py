import os
import sys
import shutil
import pandas as pd
import duckdb
import pytest
# Ensure project root is in sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dags.csv_to_duckdb import process_csv_files

def setup_module(module):
    # Prepare test directories
    os.makedirs('input', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    os.makedirs('output', exist_ok=True)

def teardown_module(module):
    # Clean up test directories
    for d in ['input', 'data', 'output']:
        if os.path.exists(d):
            shutil.rmtree(d)

def test_process_csv(tmp_path):
    # Setup paths
    input_dir = tmp_path / "input"
    data_dir = tmp_path / "data"
    output_dir = tmp_path / "output"
    os.makedirs(input_dir)
    os.makedirs(data_dir)
    os.makedirs(output_dir)
    # Create a sample CSV
    df = pd.DataFrame({
        'id': [1],
        'name': ['Test Name'],
        'addressline1': ['123 Main St'],
        'addressline2': ['Apt 4'],
        'city': ['Testville'],
        'state': ['TS'],
        'zipcode': ['12345'],
        'latitude': [12.34],
        'longitude': [56.78],
    })
    csv_path = input_dir / "test.csv"
    df.to_csv(csv_path, index=False)
    # Run the process_csv_files function
    result = process_csv_files(str(input_dir), str(data_dir), str(output_dir))
    # Check DuckDB file
    db_path = data_dir / "addresses.duckdb"
    con = duckdb.connect(str(db_path))
    out_df = con.execute("SELECT * FROM addresses").fetchdf()
    assert len(out_df) == 1
    assert out_df.iloc[0]['name'] == 'Test Name'
    # Check output summary
    summary_path = output_dir / "test.csv_summary.txt"
    assert summary_path.exists()
    with open(summary_path) as f:
        summary = f.read()
    assert "Processed 1 records" in summary
