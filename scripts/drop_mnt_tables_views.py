import argparse
import duckdb

parser = argparse.ArgumentParser(description="Helper script to clear database for Data Maintenance test")
parser.add_argument('--scale', '-s', help="Scale factor (1, 1.5, 2, 3)", required=True, choices=['1', '1.5', '2', '3'])
scale = parser.parse_args().scale

connection = duckdb.connect(f'../databases/sc_{scale}.db')

tables = ['s_catalog_order',
            's_catalog_order_lineitem',
            's_catalog_returns',
            's_inventory',
            's_purchase',
            's_purchase_lineitem',
            's_store_returns',
            's_web_order',
            's_web_order_lineitem',
            's_web_returns']

for table in tables:
    print(f'Dropping table {table}')
    connection.sql(f'DROP TABLE {table}')

views = ['crv', 'csv', 'iv', 'srv', 'ssv', 'wrv', 'wsv']

for view in views:
    print(f'Dropping view {view}')
    connection.sql(f'DROP VIEW IF EXISTS {view}')