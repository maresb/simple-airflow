import json
from datetime import datetime
from os import environ
from typing import Dict

from airflow.decorators import dag, task
from airflow.providers.docker.operators.docker import DockerOperator

# This is necessary until <https://github.com/apache/airflow/pull/38387>
# is released in `apache-airflow-providers-docker>3.9.2`.
# <https://pypi.org/project/apache-airflow-providers-docker/>
docker_url: str = environ.get("DOCKER_HOST", "unix://var/run/docker.sock")


@task(multiple_outputs=True)
def parse_json(docker_hello_output: str) -> Dict:
    """Parse JSON output, splitting top-level key-value pairs into separate XComs."""
    json_output = json.loads(docker_hello_output)
    return json_output


@dag(schedule=None, start_date=datetime(2024, 1, 1), catchup=False)
def example_dag():
    # Use a classical DockerOperator where the last line of stdout becomes
    # the output of the task with the single XCom
    # `return_value={"greeting": "Hello", "greeted": "world"}`.
    docker_hello = DockerOperator(
        task_id="docker_hello_mix",
        image="python:3.12-slim-bookworm",
        auto_remove="force",
        force_pull=True,
        docker_url=docker_url,
        command=["echo", '{"greeting": "Hello", "greeted": "world"}'],
    )
    # Assign a particular ID to the general-purpose reusable parse_json task.
    parse_docker_hello_json = parse_json.override(task_id="parse_docker_hello_json")
    # Now `parsed` will have two XComs: `greeting="Hello"` and `greeted="world"`.
    parsed = parse_docker_hello_json(docker_hello.output)

    # Execute the `assemble_greeting` Python function in a Docker container.
    @task.docker(
        image="python:3.12-slim-bookworm",
        multiple_outputs=True,
        auto_remove="force",
        docker_url=docker_url,
    )
    def assemble_greeting(greeting: str, greeted: str) -> Dict[str, str]:
        return dict(assembled_greeting=f"{greeting}, {greeted}!")

    # Now assemble_greeting has one XCom: `assembled_greeting="Hello, world!"`.
    assembled_greeting = assemble_greeting(parsed["greeting"], parsed["greeted"])

    # Print it out.
    @task()
    def show_greeting(greeting: str) -> None:
        print(greeting)

    show_greeting(assembled_greeting["assembled_greeting"])


# Create the DAG.
example_dag()
