# TPC_DS_DUCKDB
Using TPC DS Benchmark

## Load test
TBA

## Power test
TBA

## Data maintenance test
For each scale, the number of refresh runs = the number of query streams used for the Throughput Test. Here, we choose the number to be $S = 4$. These streams are divided among the two Data Maintenance tests. For example, for scale 1:
- Data Maintenance test 1:
    - Refresh run 1: stream 1
    - Refresh run 2: stream 2
- Data Maintenance test 2:
    - Refresh run 1: stream 3
    - Refresh run 2: stream 4

So for each scale, we need to generate 4 sets of refresh data, each one corresponding to one refresh run.

### Generate refresh data
Use the <code>dsdgen</code> tool provided in the TPC-DS toolkit to generate the refresh data sets.

Assuming we have the following file structure:
```bash
.
├── databases
│   ├── sc_1.db
│   ├── sc_1.5.db
│   ├── sc_2.db
│   └── sc_3.db
├── refresh_data
│   ├── scale_1
│   │   ├── stream_1
│   │   ├── stream_2
│   │   ├── stream_3
│   │   └── stream_4
│   ├── scale_1.5
│   │   └── ...
│   ├── scale_2
│   │   └── ...
│   └── scale_3
│   │   └── ...
├── results
│   └── ...
├── scripts
│   ├── load_test.py
│   ├── maintenance_functions
│   │   └── ...
│   ├── maintenance_setup.py
│   ├── maintenance_test.py
│   ├── throughput_test.py
│   └── ...
├── tpcds-kit
│   └── ...
├── ...
```

For each scale, run the following commands to generate refresh data:

```bash
./dsdgen -scale [scale] -dir "../../refresh_data/scale_[scale]/stream_1" -update 1
./dsdgen -scale [scale] -dir "../../refresh_data/scale_[scale]/stream_2" -update 2
./dsdgen -scale [scale] -dir "../../refresh_data/scale_[scale]/stream_3" -update 3
./dsdgen -scale [scale] -dir "../../refresh_data/scale_[scale]/stream_4" -update 4
```

### Run the Data Maintenance test
From the <code>/scripts</code> directory, use the <code>maintenance_test.py</code> script to run the Data Maintenance test. This script requires two command line parameters:
- <code>--scale</code> or <code>-s</code>: the current scale factor, one value among the four: 1, 1.5, 2, 3.
- <code>--test</code> or <code>-t</code>: whether the test is the Data Maintenance Test 1 (conducted after the Throughput Test 1) or the Data Maintenance Test 2 (conducted after the Throughput Test 2). Choose one value between the two: 1 or 2.

For example, to run the Data Maintenance Test 1 for scale factor 1:
```bash
# In the /scripts directory
python maintenance_test.py --scale 1 --test 1
```

### Notes
If you are running the test for the same scale multiple times, run the <code>drop_mnt_tables.py</code> script to clear out the tables and views created in previous runs.