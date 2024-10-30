import argparse
import os

parser = argparse.ArgumentParser(description="Helper script to modify .dat file encoding")
parser.add_argument('--scale', '-s', help="Scale factor (1, 1.5, 2, 3)", required=True, choices=['1', '1.5', '2', '3'])
scale = parser.parse_args().scale

filepath = f'../generated_data/scale_{scale}/customer.dat'
encoding = 'iso-8859-1'
output_filename = f'../generated_data/scale_{scale}/customer_new.dat'
output = open(output_filename, 'w')
with open(filepath, encoding=encoding) as input:
    for line in input:
        output.write(line + '\n')
output.close()
os.remove(filepath)
os.rename(output_filename, filepath)