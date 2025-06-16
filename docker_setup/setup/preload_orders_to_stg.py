import os
os.environ["PREFECT_API_URL"] = "http://localhost:4200/api"

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from pathlib import Path

def preload_orders_to_stg(data_path: str = str(Path(__file__).parent / '../../data'),
               tips_public: str = 'tips_public.csv',
               order_products: str = 'order_products_denormalized.csv',
               orders: str = 'orders.parquet',
               cutoff = pd.to_datetime('2024-02-01'),
               number_of_drivers: int = 50):
    """
    Args:
        datapath: Path to the directory where the data files are stored (not in repository). No trailing slash.
        tips_public: Name of the CSV file containing public tips.
        order_products: Name of the CSV file containing order products.
        orders: Name of the Parquet file containing orders.
        cutoff: Date to filter orders, only orders before this date will be included.
                '2024-11-01' includes ~80% of the orders.
    """
    print('loading files')
    df_tips_public: pd.DataFrame = pd.read_csv(data_path + "/" + tips_public)
    df_order_products: pd.DataFrame = pd.read_csv(data_path + "/" + order_products)
    df_orders: pd.DataFrame = pd.read_parquet(data_path + "/" + orders)

    print('processing data')
    # orders
    df_tips_public.drop(['Unnamed: 0'], axis=1, inplace=True)
    table_orders = pd.merge(left=df_orders, right=df_tips_public, how='left', on='order_id').sort_values('order_date')
    random_drivers = np.random.randint(0, number_of_drivers, size=len(table_orders))
    table_orders['driver_id'] = random_drivers
    table_orders = table_orders[table_orders.order_date < cutoff]
    # order_products
    table_order_product = df_order_products[['order_id', 'product_id', 'add_to_cart_order']]
    table_order_product = pd.merge(left=table_orders[['order_date', 'order_id']], right=table_order_product, how='left', on='order_id').drop(columns=['order_date'])
    table_order_product = table_order_product[table_order_product['product_id'].notna()]


    print('writing data', end='\r')
    engine = create_engine("postgresql://admin:pass123@localhost:5432/data")  # Adjust the connection string as needed
    table_orders.to_sql('orders', schema='stg', con=engine, if_exists='append', index=False)
    print('writing data 1/2 (yes takes some time...)', end='\r')
    table_order_product.to_sql('order_product', schema='stg', con=engine, if_exists='append', index=False)
    print('writing data 2/2 done                    ')
    engine.dispose()
    
if __name__ == "__main__":
    preload_orders_to_stg()