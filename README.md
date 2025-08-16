
# Airflow Vibe

This project is an Apache Airflow application that processes CSV files containing address data, persists the data to a DuckDB database, and writes job results to an output directory. The job runs every minute.

## Features

- Consumes CSV files from the `input` directory with columns:
  - `id` (int)
  - `name` (varchar(300))
  - `addressline1` (varchar(250))
  - `addressline2` (varchar(250))
  - `city` (varchar(250))
  - `state` (varchar(50))
  - `zipcode` (varchar(10))
  - `latitude` (float)
  - `longitude` (float)
- Persists data to DuckDB in the `data` directory
- Writes job summaries to the `output` directory
- Uses Airflow 3.x TaskFlow API for modern DAG authoring
- Includes development tools: bumpver, isort, autoflake, black
- Includes pytest tests for core logic

## Setup

1. **Install dependencies**

   ```bash
   pip install .[development]
   ```

2. **Initialize Airflow**

   ```bash
   export AIRFLOW_HOME=$(pwd)
   airflow db init
   airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
   ```

3. **Start Airflow Scheduler and Webserver**

   ```bash
   airflow scheduler &
   airflow webserver &
   ```

4. **Access the Airflow Web Interface**

   By default, the Airflow webserver runs on [http://localhost:8080](http://localhost:8080). Open this URL in your browser to monitor DAGs, job execution, and task status.

5. **Place CSV files in the `input` directory**

## Development

- Format code: `python setup.py black`
- Sort imports: `python setup.py isort`
- Remove unused imports: `python setup.py autoflake`
- Bump version: `python setup.py bumpver`
- Run tests: `pytest tests`

## License

Apache License 2.0
