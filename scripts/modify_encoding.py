filepath = '../generated_data/scale_3/customer.dat'
encoding = 'iso-8859-1'
output_filename = f'../generated_data/scale_3/customer_new.dat'
output = open(output_filename, 'w')
with open(filepath, encoding=encoding) as input:
    for line in input:
        output.write(line + '\n')
output.close()



# import argparse
#
# parser = argparse.ArgumentParser(description="TPC-DS Database Modify Customer")
# parser.add_argument('--scale', '-s', help="Scale factor (1, 1.5, 2, 3)", required=True, choices=['1', '1.5', '2', '3'])
# scale = parser.parse_args().scale
#
# filepath = f'../generated_data/scale_{scale}/customer.dat'
# encoding = 'iso-8859-1'
#
# list_line=[]
# # Read the original content
# with open(filepath, encoding=encoding) as input:
#     for line in input:
#         list_line.append(line)
#
# # Write back to the same file
# with open(filepath, 'w', encoding=encoding) as file:
#     for line in list_line:
#         file.write(line)
