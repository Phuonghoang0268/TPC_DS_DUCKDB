from time import time

"""Execution of the DF_CS function
Properties:
    Method: 2 - sales and returns fact table delete
    Target tables: catalog_sales [S], catalog_returns [R]

SQL query:
    DELETE FROM catalog_returns
    WHERE cr_order_number IN (
            SELECT cs_order_number
            FROM catalog_sales
            WHERE cs_sold_date_sk IN (
                SELECT d_date_sk
                FROM date_dim
                WHERE d_date BETWEEN [date_1] AND [date_2]
            )
    );

    DELETE FROM catalog_sales
    WHERE cs_sold_date_sk IN (
        SELECT d_date_sk
        FROM date_dim
        WHERE d_date BETWEEN [date_1] AND [date_2]);
"""
def execute(scale, test, run, connection):
    stream = (test - 1) * 2 + (run - 1) + 1
    print(f'\nExecuting function DF_CS, test #{test}, run #{run}, stream #{stream}')
    flatfile = f'../refresh_data/scale_{scale}/stream_{stream}/delete_{stream}.dat'
    queries = []
    with open(flatfile, 'r') as file:
        for line in file:
            date_1, date_2, _ = line.strip().split('|')
            query_1 = f"DELETE FROM catalog_returns WHERE cr_order_number IN (SELECT cs_order_number FROM catalog_sales WHERE cs_sold_date_sk IN (SELECT d_date_sk FROM date_dim WHERE d_date BETWEEN CAST('{date_1}' AS DATE) AND CAST('{date_2}' AS DATE)));"
            query_2 = f"DELETE FROM catalog_sales WHERE cs_sold_date_sk IN (SELECT d_date_sk FROM date_dim WHERE d_date BETWEEN CAST('{date_1}' AS DATE) AND CAST('{date_2}' AS DATE));"
            queries.append(query_1)
            queries.append(query_2)
    start_time = time()
    for query in queries:
        print(f'\tQuery: {query}')
        connection.sql(query)
    end_time = time()
    print(f'\n\tExecution time: {end_time - start_time} seconds')
    return end_time - start_time