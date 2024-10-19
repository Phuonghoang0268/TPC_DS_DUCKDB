filepath = '../generated_data/customer.dat'
encoding = 'iso-8859-1'
output_filename = f'../generated_data/scale_1_new/customer.dat'
output = open(output_filename, 'w')
with open(filepath, encoding=encoding) as input:
    for line in input:
        output.write(line + '\n')
output.close()