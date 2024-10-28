import argparse
import duckdb
from time import time
import csv
import json

import maintenance_setup
from maintenance_functions import DF_CS, DF_I, DF_SS, DF_WS, LF_CR, LF_CS, LF_I, LF_SR, LF_SS, LF_WR, LF_WS

parser = argparse.ArgumentParser(description="TPC-DS Data Maintenance test")
parser.add_argument('--scale', '-s', help="Scale factor (1, 1.5, 2, 3)", required=True, choices=['1', '1.5', '2', '3'])
parser.add_argument('--test', '-t', help="Test (1 or 2)", required=True, type=int, choices=[1, 2])
args = parser.parse_args()

streams_no = 4
test = args.test
scale = args.scale
results = []

connection = duckdb.connect(f'../databases/sc_{args.scale}.db')
if test == 1:
    maintenance_setup.create_tables(connection)

functions = {'DF_CS': DF_CS, 'DF_I': DF_I, 'DF_SS': DF_SS,
            'DF_WS': DF_WS, 'LF_CR': LF_CR, 'LF_CS': LF_CS,
            'LF_I': LF_I, 'LF_SR': LF_SR, 'LF_SS': LF_SS,
            'LF_WR': LF_WR, 'LF_WS': LF_WS}

def make_result_obj(scale, test, run, func, result):
    obj = {
        'scale': scale,
        'test': test,
        'run': run,
        'function': func,
        'result': result
    }
    return obj

def execute_refresh_run(scale, test, run, connection):
    for name, func in functions.items():
        try:
            result = func.execute(scale, test, run, connection)
            results.append(make_result_obj(scale, test, run, name, result))
        except Exception as e:
            print(f'Cannot execute function {name}: {e}')

# Execute refresh run 1
run = 1
run_1_start = time()
maintenance_setup.clear_views(connection)
maintenance_setup.load_data(scale, test, run, connection)
setup_1_end = time()
execute_refresh_run(scale, test, run, connection)
run_1_end = time()

# Execute refresh run 2
run = 2
maintenance_setup.clear_views(connection)
maintenance_setup.load_data(scale, test, run, connection)
setup_2_end = time()
execute_refresh_run(scale, test, run, connection)
run_2_end = time()

# Write individual function elapsed times
outfile = open(f'../results/maintenance_s{scale}_t{test}.csv', 'w')
writer = csv.writer(outfile)
writer.writerow(['scale', 'test', 'run', 'function', 'result'])
for result in results:
    writer.writerow(result.values())
outfile.close()

# Write refresh run and test elapsed times
elapsed_times = {
    'setup_1': setup_1_end - run_1_start,
    'run_1': run_1_end - setup_1_end,
    'setup_2': setup_2_end - run_1_end,
    'run_2': run_2_end - setup_2_end,
    'test': run_2_end - setup_1_end
}

test_outfile = f'../results/test_s{scale}_t{test}.json'
with open(test_outfile, "w") as file: 
    json.dump(elapsed_times, file)

print(f'\nMaintenance test #{test} for scale {scale} completed.')
print(f'Function elapsed times are stored in ../results/maintenance_s{scale}_t{test}.csv')
print(f'Refresh runs and test elapsed times are stored in {test_outfile}')