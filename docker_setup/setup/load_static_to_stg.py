import os
os.environ["PREFECT_API_URL"] = "http://localhost:4200/api"

import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path


def load_static_to_stg(data_path: str = str(Path(__file__).parent / '../../data'),
               order_products: str = 'order_products_denormalized.csv'
               )-> None:
    """
    Args:
        datapath: Path to the directory where the data files are stored (not in repository). No trailing slash.
        order_products: Name of the CSV file containing order products.
    """
    print('loading files')
    #df_tips_public: pd.DataFrame = pd.read_csv(data_path + "/" + tips_public)
    df_order_products: pd.DataFrame = pd.read_csv(data_path + "/" + order_products)
    #df_orders: pd.DataFrame = pd.read_parquet(data_path + "/" + orders)
    print('processing data')
    df_poducts_star = df_order_products.drop(['order_id', 'add_to_cart_order'], axis=1).drop_duplicates()

    table_departments = df_poducts_star[['department_id', 'department']].drop_duplicates().sort_values('department_id')
    table_aisles = df_poducts_star[['aisle_id', 'aisle', 'department_id']].drop_duplicates().sort_values('aisle_id')
    table_products = df_poducts_star[['product_id', 'product_name', 'aisle_id']].drop_duplicates().sort_values('product_id')
    #table_orders = pd.merge(left=df_orders, right=df_tips_public, how='left', on='order_id').drop('Unnamed: 0', axis=1)
    print('writing data', end='\r')
    engine = create_engine("postgresql://admin:pass123@localhost:5432/data")  # Adjust the connection string as needed
    table_departments.to_sql('department', schema='stg', con=engine, if_exists='append', index=False)
    print('writing data 1/3', end='\r')
    table_aisles.to_sql('aisle', schema='stg', con=engine, if_exists='append', index=False)
    print('writing data 2/3', end='\r')
    table_products.to_sql('product', schema='stg', con=engine, if_exists='append', index=False)
    print('writing data 3/3 done')
    engine.dispose()

if __name__ == "__main__":
    load_static_to_stg()