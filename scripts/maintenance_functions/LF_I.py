from time import time

"""Execution of the LF_I function
Properties:
    Method: 1 - Fact table load
    Target table: inventory
"""

def create_view(connection):
    print('\tCreating view iv')
    query = '''CREATE view iv AS
SELECT
	d_date_sk inv_date_sk,
	i_item_sk inv_item_sk,
	w_warehouse_sk inv_warehouse_sk,
	invn_qty_on_hand inv_quantity_on_hand
FROM
	s_inventory
	LEFT OUTER JOIN warehouse ON (invn_warehouse_id = w_warehouse_id)
	LEFT OUTER JOIN item ON (
		invn_item_id = i_item_id
		AND i_rec_end_date IS NULL
	)
	LEFT OUTER JOIN date_dim ON (d_date = invn_date);'''

    connection.sql(query)

def insert_from_view(connection):
    query = 'INSERT OR IGNORE INTO inventory SELECT DISTINCT(*) FROM iv'
    print(f'\tQuery: {query}')
    connection.sql(query)

def execute(scale, test, run, connection):
    stream = (test - 1) * 2 + (run - 1) + 1
    print(f'\nExecuting function LF_I, test #{test}, run #{run}, stream #{stream}')
    start_time = time()
    create_view(connection)
    insert_from_view(connection)
    end_time = time()
    print(f'\n\tExecution time: {end_time - start_time} seconds')
    return end_time - start_time