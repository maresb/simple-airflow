FROM apache/airflow:2.8.3

RUN pip install --no-cache-dir apache-airflow-providers-docker==3.9.2
