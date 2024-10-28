import argparse
import duckdb
from time import time
import os

parser = argparse.ArgumentParser(description="TPC-DS Database Load test")
parser.add_argument('--scale', '-s', help="Scale factor (1, 1.5, 2, 3)", required=True, choices=['1', '1.5', '2', '3'])
scale = parser.parse_args().scale

connection = duckdb.connect(f'../databases/sc_{scale}.db')
data_path = f'../generated_data/scale_{scale}'
data_files = os.listdir(data_path)

print(f'Executing the Database Load Test for scale {scale}')
start = time()
for file in data_files:
    if file.endswith('.dat'):
        table = file[:-4]
        query = f"COPY {table} FROM '{data_path}/{file}'"
        print(f'\tQuery: {query}')
        connection.sql(query)
end = time()

outfile = f'../results/load_test_s{scale}.txt'
output = open(outfile, 'w')
output.write(str(end - start))
output.close()
print(f'\nDatabase load test for scale {scale} completed. Elapsed time: {end - start} seconds')
print(f'Results are stored in ../results/load_test_s{scale}.txt')