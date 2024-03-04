""" """

from pathlib import Path

from dagster import EnvVar
from dagster_dbt import DbtCliResource
from dagster_airbyte import AirbyteResource

# AIRBYTE
airbyte_instance = AirbyteResource(
    host="localhost",
    port="8000",
    username="airbyte",
    password="password",
)

# DBT
project_dir = Path(__file__).joinpath("..", "..", "..", "..").resolve()
PROJECT_DIR = str(project_dir) + "/dbt_mlops"

dbt_resource = DbtCliResource(
    project_dir=PROJECT_DIR,
    target="default",
)
