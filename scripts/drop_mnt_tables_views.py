import duckdb

connection = duckdb.connect('../databases/sc_1.db')

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