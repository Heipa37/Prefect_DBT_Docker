"""
Import raw data and provides the DataFrames for the project.
Variables:

df_tips_public (pandas.DataFrame):
   - Tips for analysis. One line for each order. Columns: ["order_id", "tip"]
df_tip_testdaten (pandas.DataFrame):
   - Testset with tips for ML training. One line for each order. Columns: ["order_id", "tip"]
df_order_products (pandas.DataFrame):
   - Ordered products, one line for each order item. Columns: ['order_id', 'product_id', 
        'add_to_cart_order', 'product_name', 'department', 'aisle']
df_orders (pandas.DataFrame):
   - One line for each order: Columns: ['order_id', 'user_id', 'order_date']

"""


import pandas as pd

df_tips_public: pd.DataFrame = pd.read_csv("data/tips_public.csv")[["order_id", "tip"]]
df_tip_testdaten: pd.DataFrame = pd.read_csv("data/tip_testdaten_template.csv")[["order_id", "tip"]]
df_order_products: pd.DataFrame = pd.read_csv("data/order_products_denormalized.csv")\
    .drop(["aisle_id", "department_id"], axis=1)
df_orders: pd.DataFrame = pd.read_parquet("data/orders.parquet")

def create_sample(sample_size: float, random_state: None | int=None)-> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    create a sample with sample_size between 0 and 1 (decimal fraction) of the total data set.

    Returnvalue:
       df_orders_sample, df_tips_public_sample, df_order_products_sample
    """
    if not 0 < sample_size <= 1:
        raise ValueError("sample_size has to be be between 0 and 1")
    df_users = pd.DataFrame(df_orders["user_id"]).drop_duplicates()
    df_user_sample = df_users.sample(frac=sample_size, random_state=random_state)
    df_orders_sample = pd.merge(left=df_user_sample, right=df_orders, how="left")
    _df_orders = pd.DataFrame(df_orders_sample["order_id"]).drop_duplicates()
    df_tips_public_sample = pd.merge(left=_df_orders, right=df_tips_public, how="left")
    df_order_products_sample = pd.merge(left=_df_orders, right=df_order_products, how="left")
    return df_orders_sample, df_tips_public_sample, df_order_products_sample

