import pandas as pd
from sqlalchemy import create_engine

database_name = 'apple_store'
data_table = 'apple_data'
discount_table = 'discounts'

mysql_conn_str = f"mysql+mysqlconnector://root:root@localhost/{database_name}"

engine = create_engine(mysql_conn_str, echo=True)

data= pd.read_csv('data/apple data.csv')
discounts_data = pd.read_csv('data/discount_data.csv')

# Push DataFrame to MySQL database
data.to_sql(data_table, con=engine, index=False, if_exists='replace')
discounts_data.to_sql(discount_table, con=engine, index=False, if_exists='replace')