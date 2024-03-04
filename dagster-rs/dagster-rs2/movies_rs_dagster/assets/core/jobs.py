""" """

from dagster import job
from dagster_airbyte import airbyte_sync_op

from movies_rs_dagster.resources import airbyte_instance

sync_movies = airbyte_sync_op.configured(
    {"connection_id": "53971324-cd07-4bc6-b9f7-d915d01e2e62"}, name="sync_movies"
)

sync_users = airbyte_sync_op.configured(
    {"connection_id": "7f7657ab-a371-48d8-904d-01dce4a8fd23"}, name="sync_users"
)

sync_scores = airbyte_sync_op.configured(
    {"connection_id": "ff92f38f-9d4f-4ce3-870e-4be0968e89e4"}, name="sync_scores"
)


@job(name="airbyte_sync_job", resource_defs={"airbyte": airbyte_instance})
def airbyte_job():
    sync_movies()
    sync_users()
    sync_scores()
