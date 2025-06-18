import os

import prefect.types
import prefect.types.entrypoint
os.environ["PREFECT_API_URL"] = "http://localhost:4200/api"

from prefect import flow, task
from prefect.client import get_client
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from prefect.docker import DockerImage
from pathlib import Path

@task(log_prints=True)
def choose_driver(order_id):
    """
    Chooses a driver for the order based on some criteria.
    For simplicity, this function returns a random driver ID.
    """

    engine = create_engine("postgresql://admin:pass123@data-db:5432/data")
    #engine = create_engine("postgresql://admin:pass123@localhost:5432/data")  # for local testing
    with engine.connect() as conn:
        # change logic for driver_id with ML model (and request needed data from the database)
        # ↓
        driver_id =  np.random.randint(1, 50)
        # ↑
        conn.execute(text("UPDATE stg.orders SET driver_id = :driver_id WHERE order_id = :order_id;"),
                     {"driver_id": driver_id, "order_id": order_id})
        conn.commit()

@task(log_prints=True)
def search_for_unassigned_orders():
    """
    """
    engine = create_engine("postgresql://admin:pass123@data-db:5432/data")
    #engine = create_engine("postgresql://admin:pass123@localhost:5432/data")  # for local testing
    with engine.connect() as conn:
        result = conn.execute(text("SELECT order_id FROM stg.orders WHERE driver_id IS NULL;"))
        orders = [order[0] for order in result.fetchall()]
        #for order_id in orders:
        #    choose_driver(order_id)
        choose_driver(orders[0])
    print(f'undassigned: {len(orders)}, actual: {orders[0]}')

@flow(log_prints=True, name='process_orders')
def process_orders():
    """
    Main flow to process orders.
    """
    search_for_unassigned_orders()


if __name__ == "__main__":
    process_orders.deploy(
        name="process-orders-deployment",
        work_pool_name="general-work-pool",
        image="localhost:6500/dabi_2025-worker:latest",
        push=True,
        build=False
    )

#from_source(
#        source="flows",
#        entrypoint="process_orders.py:process_orders",
#    ).

#if __name__ == "__main__":
#    process_orders.deploy(
#        name="process-orders-deployment",
#        work_pool_name="general-work-pool",
#        image=DockerImage(
#            name="dabi_2025-cli",
#            tag='v1.0',
#            dockerfile="./Dockerfile",
#            rm=True
#        ),
#        push=False,
#        build=False
#    )