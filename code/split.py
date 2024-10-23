import re

input_file_path = '../generated_queries/stream_queries/query_2.sql'

with open(input_file_path, 'r') as f:
    sql_content = f.read()

queries = sql_content.split('\n\n\n')

for i, query in enumerate(queries, start=1):    
    query = query.strip()
    
    if query:
        output_file_path = f'../generated_queries/stream_queries/split_stream2/query_{i}.sql'
        with open(output_file_path, 'w') as f:
            f.write(query)  
        print(f"Query {i} saved to {output_file_path}")

print("All queries have been successfully split into separate files.")
