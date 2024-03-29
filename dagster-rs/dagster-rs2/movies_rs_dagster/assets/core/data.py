""" """
import os

import pandas as pd
import sqlalchemy as sa

postgres_conn = {
    "username": "postgres",
    "password": "mysecretpassword",
    "host": "localhost",
    "port": 5433,
    "database": "mlops",
}

POSTGRES_URL = "postgresql://{username}:{password}@{host}:{port}/{database}".format(
    **postgres_conn
)


def run_query(query: str) -> pd.DataFrame:
    """ """

    print(f"POSTGRES_URL -> {POSTGRES_URL}")

    engine = sa.create_engine(POSTGRES_URL)
    connection = engine.connect()

    result = connection.execute(sa.text(query))

    column_names = result.keys()
    data = result.fetchall()
    df = pd.DataFrame(data, columns=column_names)

    connection.close()
    engine.dispose()

    return df