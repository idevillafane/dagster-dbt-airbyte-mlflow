from dagster import Definitions, define_asset_job, AssetSelection, ScheduleDefinition, FilesystemIOManager, asset, Output, String, AssetIn, FreshnessPolicy, MetadataValue
from dagster_airbyte import build_airbyte_assets
from dagster_dbt import load_assets_from_dbt_project

import pandas as pd

# from .constants import AIRBYTE_CONNECTION_ID, DBT_PROJECT_DIR


dbt_assets = load_assets_from_dbt_project(project_dir="/Users/nacho/Documents/Estudios/ITBA/dbt_mlops")

airbyte_assets = build_airbyte_assets(
    connection_id="5885933e-3c76-401c-85a8-358574ccb4f2",
    destination_tables=["Mlops"],
    asset_key_prefix=["airbyte_replica", "scores"]
)

from .assets import (
    core_assets, recommender_assets
)

all_assets = [*core_assets, *recommender_assets, *airbyte_assets, *dbt_assets]

mlflow_resources = {
    'mlflow': {
        'config': {
            'experiment_name': 'recommender_system',
        }            
    },
}
data_ops_config = {
    'movies': {
        'config': {
            'uri': 'https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/peliculas_0.csv'
            }
    }
}
users_ops_config = {
    'users': {
        'config': {
            'uri': 'https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/usuarios_0.csv'
            }
    }
}
scores_ops_config = {
    'scores': {
        'config': {
            'uri': 'https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/scores_0.csv'
            }
    },
}

training_config = {
    'keras_dot_product_model': {
        'config': {
            'batch_size': 128,
            'epochs': 10,
            'learning_rate': 1e-3,
            'embeddings_dim': 5
        }
    }
}

job_data_config = {
    'resources': {
        **mlflow_resources
    },
    'ops': {
        **data_ops_config,
    }
}

job_training_config = {
    'resources': {
        **mlflow_resources
    },
    'ops': {
        **training_config
    }
}

job_all_config = {
    'resources': {
        **mlflow_resources
    },
    'ops': {
        **data_ops_config,
        **users_ops_config,
        **scores_ops_config,
        **training_config
    }
}

get_data_job = define_asset_job(
    name='get_data',
    selection=['movies', 'users', 'scores', 'training_data'],
    config=job_data_config
)

get_data_schedule = ScheduleDefinition(
    job=get_data_job,
    cron_schedule="0 * * * *",  # every hour
)

io_manager = FilesystemIOManager(
    base_dir="data",  # Path is built relative to where `dagster dev` is run
)

defs = Definitions(
    assets=all_assets,
    jobs=[
        get_data_job,
        define_asset_job("full_process", config=job_all_config),
        define_asset_job(
            "only_training",
            # selection=['preprocessed_training_data', 'user2Idx', 'movie2Idx'],
            selection=AssetSelection.groups('recommender'),
            config=job_training_config
        )
    ],
    resources={
        'airbyte': airbyte_assets,
        'dbt': dbt_assets,
        "io_manager": io_manager,
    },
    schedules=[get_data_schedule],
    # sensors=all_sensors,
)

