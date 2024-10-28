import duckdb
import os
import fnmatch
import time
import threading
import argparse

parser=argparse.ArgumentParser

# Shared database connection
scale = 1
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

def execute_query(query, file_name):
    start_time = time.time()
    print(f"Executing query from thread ID: {threading.get_ident()} for file: {file_name}")

    cursor = con.cursor()
    cursor.execute(query)
    
    # Calculate the elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Total time is {elapsed_time} seconds') 
    print(f"Done executing query from thread ID: {threading.get_ident()} for file: {file_name}")
    
    
def main():
    outputfile = (f"../results/throughput_test_scale_{scale}_test_{test}.txt")
    
    TP_test_start_time_1 = time.time()

    queries = []
    threads = []
    
    for root, dirnames, filenames in os.walk('../generated_queries/scale_3'):
        print(root, filenames)
        for filename in fnmatch.filter(filenames, '*.sql'):
            print(filename)
            sql_file = open(os.path.join(root, filename), 'r')
            query = sql_file.read()
            queries.append((query, filename))  # Store query along with filename

    print(queries)
    
    
    # create threads and assign query stream to threads
    for query, file_name in queries:
        thread = threading.Thread(target=execute_query, args=(query, file_name))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # calculate the time for throughput test
    TP_test_end_time_1 = time.time()
    TP_test_time_1 = TP_test_end_time_1 - TP_test_start_time_1
    output = f'THROUGHPUT TEST TIME:\n\tThroughput test start time = {TP_test_start_time_1}\n\tThroughput test end time = {TP_test_end_time_1}\n\tThroughput test time = {TP_test_time_1}\n'
    print(output)

    if outputfile:
        with open(outputfile, 'w+') as f:
            f.write(output)

def test():
    for root, dirnames, filenames in os.walk('../generated_queries/scale_3'):
        print(root, filenames)
        for filename in fnmatch.filter(filenames, '*.sql'):
            print(filename)
            sql_file = open(os.path.join(root, filename), 'r')
            query = sql_file.read()
            execute_query(query, filename)  # Store query along with filename


if __name__ == "__main__":
    test()

