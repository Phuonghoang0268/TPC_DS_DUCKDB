import argparse
import duckdb
import os
import fnmatch
from time import time
import csv

parser = argparse.ArgumentParser(description="TPC-DS Database Power test")
parser.add_argument('--scale', '-s', help="Scale factor (1, 1.5, 2, 3)", required=True, choices=['1', '1.5', '2', '3'])
scale = parser.parse_args().scale

# Connect to the database
db_path = f'../databases/sc_{scale}.db'
try:
    con = duckdb.connect(db_path)
    print(f'Connected to database at {db_path}')
except Exception as e:
    print(f"Failed to connect to database: {e}")
    exit()

# Dictionary to store query execution times
query_times = {}

print(f'Executing the Powet Test for scale {scale}')
start_time = time()

# Read and execute all the queries
for root, dirnames, filenames in os.walk(f'../generated_queries/scale_{scale}'):
    for filename in fnmatch.filter(filenames, '*.sql'):        
        query_start_time = time()
        
        query_file_path = os.path.join(root, filename)
        
        # Read the SQL query
        with open(query_file_path, 'r') as file:
            sql = file.read()
        
        try:
            # Run the query
            result = con.execute(sql)
            query_end_time = time()
            execution_time = query_end_time - query_start_time
            print(f"\tSuccessfully executed {filename} in {execution_time:.4f} seconds")
            
            # Store the result and execution time
            query_times[filename] = execution_time
            
        except Exception as e:
            print(f"\tError executing {filename}: {e}")
            query_times[filename] = 'ERROR'

# Calculate and print the total elapsed time
end_time = time()
elapsed_time = end_time - start_time
print(f'\n\tTotal execution time: {elapsed_time:.4f} seconds')

# Save query execution times to a csv file
outfile = open(f'../results/power_s{scale}.csv', 'w')
writer = csv.writer(outfile)
writer.writerow(['Query', 'Execution Time'])
for query, t in query_times.items():
    writer.writerow([query, t])
outfile.close()

print(f'\nPower test for scale {scale} completed')
print(f'Query execution times are stored in ../results/power_s{scale}.csv')

# Close the database connection
con.close()
print('Closed database connection')