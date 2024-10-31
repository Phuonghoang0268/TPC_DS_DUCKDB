# TPC-DS Benchmark Using DuckDB
In this project, we implement the TPC-DS Benchmark on the DuckDB Database Management System to analyze database performance at different scales.

## Setup
1. Clone the repository
   ```bash
   git clone https://github.com/Phuonghoang0268/TPC_DS_DUCKDB.git
   cd TPC_DS_DUCKDB 
    ```
3. Install DuckDB
   ```bash
   pip install duckdb
   ```
5. Download TPC-DS Tools
   - Go to Go to [TPC-DS Official Site](https://www.tpc.org/tpc_documents_current_versions/current_specifications5.asp) and download `TPC-DS_Tools_v3.2.0.zip`.
   - Unzip the zip file to a folder named tpcds-kit

## Usage

### Data Generation 
- Go to  tpcds-kit/tools folder and run the command to generate data:
```bash
./dsdgen -scale 1 -dir "../../generated_data/scale_1" #SF 1
./dsdgen -scale 1.5 -dir "../../generated_data/scale_1.5" #SF 1.5
./dsdgen -scale 2 -dir "../../generated_data/scale_2" #SF 2
./dsdgen -scale 3 -dir "../../generated_data/scale_3" #SF 3
```
- Modify encoding problem for the customer.dat file: Go to folder TPC_DS_DUCKDB/scripts and run:
```bash
python modify_encoding.py --scale $scale
```

### Query Generation
- Go to  tpcds-kit/tools folder and run the command to generate query:
```bash
./dsqgen -directory "../query_templates/" -input "../query_templates/templates.lst" -dialect netezza -scale 1 -output_dir "../generated_queries/scale_1"
./dsqgen -directory "../query_templates/" -input "../query_templates/templates.lst" -dialect netezza -scale 1.5 -output_dir "../generated_queries/scale_1.5"
./dsqgen -directory "../query_templates/" -input "../query_templates/templates.lst" -dialect netezza -scale 2 -output_dir "../generated_queries/scale_2"
./dsqgen -directory "../query_templates/" -input "../query_templates/templates.lst" -dialect netezza -scale 3 -output_dir "../generated_queries/scale_3"
```
- Split queries using python scripts code/split.py
- Modify Queries
  
#### Note: In our repository, separated and modified queries for each scale are already available.

### Running the Benchmark
The execution.sh script, located in the scripts folder, automates all benchmark tests (load, power, throughput, and maintenance). Run it as follows:
```bash
bash scripts/execution.sh $scale
```
