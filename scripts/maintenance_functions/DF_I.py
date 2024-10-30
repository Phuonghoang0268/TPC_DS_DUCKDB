from time import time

"""Execution of the DF_I function
Properties:
    Method: 3 - Inventory fact table delete
    Target table: inventory [I]

SQL query:
    DELETE FROM inventory
    WHERE inv_date_sk IN (
        SELECT d_date_sk
        FROM date_dim
        WHERE d_date BETWEEN [date_1] AND [date_2]);
"""
def execute(scale, test, run, connection):
    stream = (test - 1) * 2 + (run - 1) + 1
    print(f'\nExecuting function DF_I, test #{test}, run #{run}, stream #{stream}')
    flatfile = f'../refresh_data/scale_{scale}/stream_{stream}/inventory_delete_{stream}.dat'
    queries = []
    with open(flatfile, 'r') as file:
        for line in file:
            date_1, date_2, _ = line.strip().split('|')
            query = f'DELETE FROM inventory WHERE inv_date_sk IN (SELECT d_date_sk FROM date_dim WHERE d_date BETWEEN {date_1} AND {date_2});'
            queries.append(query)
        start_time = time()
    for query in queries:
        print(f'\tQuery: {query}')
        connection.sql(query)
    end_time = time()
    print(f'\n\tExecution time: {end_time - start_time} seconds')
    return end_time - start_time