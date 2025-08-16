# Airflow + Nginx with Docker Compose & Podman

This setup runs the Airflow web interface behind an Nginx reverse proxy using Docker Compose or Podman Compose.

## Usage

1. Ensure you have Docker or Podman installed.

2. From the `docker` directory, run:

   - With Docker Compose:

     ```bash
     docker compose up --build
     ```

   - With Podman Compose:

     ```bash
     podman-compose up
     ```

3. Access the Airflow web interface at [http://localhost](http://localhost)

## Airflow 3.x Migration Step (Podman)

Before starting all services, you must manually initialize the Airflow database:

```bash
podman-compose run airflow-init bash -c "airflow db migrate"
```

Then start the services:

```bash
podman-compose up
```

## Airflow 3.x Database Persistence & Migration (Podman)

To ensure the Airflow SQLite database is persistent and shared between containers, add the following volume to your `docker-compose.yml`:

```yaml
    volumes:
      - ../dags:/opt/airflow/dags
      - airflow-logs:/opt/airflow/logs
      - ../airflow-db:/opt/airflow
```

Create the database directory:

```bash
mkdir ../airflow-db
```

Run the migration using the same configuration as your containers:

```bash
podman run --rm \
  -e AIRFLOW__CORE__EXECUTOR=LocalExecutor \
  -e AIRFLOW__CORE__FERNET_KEY=your_fernet_key \
  -e AIRFLOW__CORE__DAGS_FOLDER=/opt/airflow/dags \
  -e AIRFLOW__CORE__LOAD_EXAMPLES=False \
  -v $(pwd)/../dags:/opt/airflow/dags \
  -v docker_airflow-logs:/opt/airflow/logs \
  -v $(pwd)/../airflow-db:/opt/airflow \
  docker.io/apache/airflow:3.0.0 bash -c "airflow db migrate"
```

Then start your services:

```bash
podman-compose up
```

This ensures your Airflow database is initialized and persistent for all future runs.

## Notes

- The default Airflow admin user is `admin` / `admin`.
- Airflow DAGs are mounted from the main project's `dags` directory.
- Nginx proxies requests to the Airflow webserver.
- You can customize `nginx.conf` and the Airflow image as needed.
