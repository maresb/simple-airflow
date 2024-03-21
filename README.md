# Simple minimal Airflow setup

## Introduction

Here is a slim Airflow setup with the following conditions:

* Provision with Docker Compose.
* Replace `CeleryExecutor` by `LocalExecutor` and remove Redis/Flower.
* Enable the Docker provider.
* Provide a clean and concise Git history showing the individual alterations to the [standard configuration](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html).

Also, I want to be able to use Airflow in a project where it isn't installed in that project's environment, only running via Docker Compose. Towards this end, I created the [airflow-stubs](https://github.com/maresb/airflow-stubs) package.

## Running Airflow

To start Airflow,

```bash
git clone https://github.com/maresb/simple-airflow.git
cd simple-airflow
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker compose up airflow-init
docker compose up
```

Open <http://localhost:8080> with the credentials `airflow`/`airflow`.

For more details, refer to the [official instructions](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html).
