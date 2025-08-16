import os
import duckdb
import pandas as pd
from airflow import DAG
from airflow.decorators import task
from datetime import datetime, timedelta

def process_csv_files(input_dir, data_dir, output_dir):
    db_path = os.path.join(data_dir, "addresses.duckdb")
    table_name = "addresses"
    # Find CSV files in input directory
    csv_files = [f for f in os.listdir(input_dir) if f.endswith(".csv")]
    results = []
    for csv_file in csv_files:
        csv_path = os.path.join(input_dir, csv_file)
        df = pd.read_csv(csv_path)
        # Persist to DuckDB
        con = duckdb.connect(db_path)
        con.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER,
                name VARCHAR(300),
                addressline1 VARCHAR(250),
                addressline2 VARCHAR(250),
                city VARCHAR(250),
                state VARCHAR(50),
                zipcode VARCHAR(10),
                latitude DOUBLE,
                longitude DOUBLE
            );
        """
        )
        con.execute(f"INSERT INTO {table_name} SELECT * FROM df")
        # Optionally, write a summary to output
        summary_path = os.path.join(output_dir, f"{csv_file}_summary.txt")
        with open(summary_path, "w") as f:
            f.write(f"Processed {len(df)} records from {csv_file}\n")
        results.append(f"Processed {csv_file}")
        # Remove the file after processing
        os.remove(csv_path)
    return "\n".join(results)

with DAG(
    "csv_to_duckdb",
    description="Consume CSV and persist to DuckDB",
    schedule=timedelta(minutes=1),
    start_date=datetime(2025, 8, 16),
    catchup=False,
) as dag:

    @task
    def process_csv():
        input_dir = "/home/jim/development/python/airflow-vibe/input"
        data_dir = "/home/jim/development/python/airflow-vibe/data"
        output_dir = "/home/jim/development/python/airflow-vibe/output"
        return process_csv_files(input_dir, data_dir, output_dir)

    process_csv()
