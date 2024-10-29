import duckdb
import os
import fnmatch
import time
import threading
import argparse
import csv

parser = argparse.ArgumentParser(description="TPC-DS Database Throughput test")
parser.add_argument('--scale', '-s', help="Scale factor (1,1.5,2,3)", required=True, choices=['1', '1.5', '2', '3'])
parser.add_argument('--test', '-t', help="Test (1 or 2)", required=True, type=int, choices=[1, 2])
args = parser.parse_args()

test = args.test
scale = args.scale
streams_no = 4

# Connect to the database
db_path = f'../databases/sc_{scale}.db'
try:
    con = duckdb.connect(db_path)
    print(f'Connected to database at {db_path}')
except Exception as e:
    print(f"Failed to connect to database: {e}")
    exit()

# Store query execution times for each thread
query_times = []


def execute_query(query, file_name, thread_id):
    start_time = time.time()
    print(f"Executing query from thread ID: {thread_id} for file: {file_name}")

    cursor = con.cursor()
    cursor.execute(query)

    # Calculate the elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total time is {elapsed_time} seconds")
    print(f"Done executing query from thread ID: {thread_id} for file: {file_name}")

    # Append times for CSV
    query_times.append({
        "thread_id": f"Thread {thread_id}",
        "start_time": start_time,
        "end_time": end_time,
        "execution_time": elapsed_time
    })


# Set up output paths
outputfile = f"../results/throughput_test_scale_{scale}_test_{test}.txt"
csv_file = f"../results/throughput_test_scale_{scale}_test_{test}.csv"

# Start time for throughput test
TP_test_start_time_1 = time.time()

queries = []
threads = []

# Gather queries
for root, dirnames, filenames in os.walk(f'../generated_queries/stream_queries/scale_{scale}'):
    for filename in fnmatch.filter(filenames, '*.sql'):
        with open(os.path.join(root, filename), 'r') as sql_file:
            query = sql_file.read()
            queries.append((query, filename))  # Store query along with filename

# Create and start threads
for i, (query, file_name) in enumerate(queries):
    thread = threading.Thread(target=execute_query, args=(query, file_name, i + 1))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

# Calculate the total throughput time
TP_test_end_time_1 = time.time()
TP_test_time_1 = TP_test_end_time_1 - TP_test_start_time_1
output = (
    f'THROUGHPUT TEST TIME:\n'
    f'\tThroughput test start time = {TP_test_start_time_1}\n'
    f'\tThroughput test end time = {TP_test_end_time_1}\n'
    f'\tThroughput test time = {TP_test_time_1}\n'
)
print(output)

# Write to output text file
with open(outputfile, 'w') as f:
    f.write(output)

# Append total time as a row in query_times for CSV
query_times.append({
    "thread_id": "Total",
    "start_time": TP_test_start_time_1,
    "end_time": TP_test_end_time_1,
    "execution_time": TP_test_time_1
})

# Write execution times to CSV
with open(csv_file, 'w', newline='') as csvfile:
    fieldnames = ['thread_id', 'start_time', 'end_time', 'execution_time']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for entry in query_times:
        writer.writerow(entry)

print(f"Execution times written to {csv_file}")
