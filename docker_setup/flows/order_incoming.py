import os
os.environ["PREFECT_API_URL"] = "http://localhost:4200/api"

from prefect import flow, task
from prefect.client import get_client
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from pathlib import Path
import datetime as dt
import asyncio

def get_last_order_date() -> dt.datetime | None:
    """
    Fetches the latest order date from the 'stg.orders' table.
    Returns:
        The latest order date as a datetime object.
    """
    engine = create_engine("postgresql://admin:pass123@localhost:5432/data")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT MAX(order_date) FROM stg.orders;"))
        latest_date = result.scalar()
    return latest_date

@task(log_prints=True)
def load_data(data_path: str = str(Path(__file__).parent / '../../data'),
               order_products: str = 'order_products_denormalized.csv',
               orders: str = 'orders.parquet') -> tuple[pd.DataFrame, pd.DataFrame]:
    """Loads data from CSV and Parquet files into Pandas DataFrames, processes them and returns them.
    Args:
        datapath: Path to the directory where the data files are stored (not in repository). No trailing slash.
        order_products: Name of the CSV file containing order products.
        orders: Name of the Parquet file containing orders.
    Returns:
        returns a tuple of DataFrames (orders, order_products).
    """
    print('loading files')
    df_order_products: pd.DataFrame = pd.read_csv(data_path + "/" + order_products)
    df_orders: pd.DataFrame = pd.read_parquet(data_path + "/" + orders)
    
    latest_date = get_last_order_date()
    if latest_date is None:
        latest_date = dt.datetime(1900, 1, 1)
    latest_date = latest_date.date()

    print('processing data')
    # orders
    table_orders = df_orders.sort_values('order_date')
    table_orders['driver_id'] = np.nan
    table_orders['tip'] = np.nan
    table_orders['order_date'] = pd.to_datetime(table_orders['order_date'])
    
    newer_orders = table_orders[table_orders['order_date'].dt.date > latest_date]
    next_day = newer_orders['order_date'].dt.date.min()
    next_day_orders = newer_orders[newer_orders['order_date'].dt.date == next_day]

    # order_products
    table_order_product = df_order_products[['order_id', 'product_id', 'add_to_cart_order']]
    next_day_order_product = pd.merge(left=next_day_orders[['order_date', 'order_id']], right=table_order_product, how='left', on='order_id').drop(columns=['order_date'])
    next_day_order_product = next_day_order_product[next_day_order_product['product_id'].notna()]

    print(next_day_orders.head(3))
    print(next_day_order_product.head(3))
    return next_day_orders, next_day_order_product

@task(name='write todays orders to DB' ,log_prints=True)
def write_tables(next_day_orders: pd.DataFrame, next_day_order_product)-> None:
    """Writes the processed DataFrames to the PostgreSQL database.
    Args:
        next_day_orders: DataFrame containing orders for the next day.
        next_day_order_product: DataFrame containing order products for the next day.
    """
    print('writing data', end='\r')
    engine = create_engine("postgresql://admin:pass123@localhost:5432/data")  # Adjust the connection string as needed
    next_day_orders.to_sql('orders', schema='stg', con=engine, if_exists='append', index=False)
    print('writing data 1/2', end='\r')
    next_day_order_product.to_sql('order_product', schema='stg', con=engine, if_exists='append', index=False)
    print('writing data 2/2')
    engine.dispose()

@flow(name="order_incoming")
def main_flow()-> None:
    """Orders from todays orders are collected and written to the database."""
    table_orders, table_order_products = load_data()
    write_tables(table_orders, table_order_products)

if __name__ == "__main__":
    main_flow()