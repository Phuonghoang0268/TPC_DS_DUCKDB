#!/bin/bash
# execution.sh

# Check if the scale argument is provided
if [ -z "$1" ]; then
    echo "Error: Scale argument is required."
    echo "Usage: bash execution.sh <scale>"
    exit 1
fi

# Parse argument
scale=$1

# Validate scale values
case $scale in
    0|1|1.5|2|3) 
        echo "Using scale: $scale"
        ;;
    *)
        echo "Error: Scale must be one of the following values: 0, 1, 1.5, 2, 3."
        exit 1
        ;;
esac

# Create database
python setup_database.py --scale $scale
# Run load test
python load_test.py --scale $scale
# Run power test
python power_test.py --scale $scale
# Run throughput test 1
python throughput_test.py --scale $scale --test 1
# Run maintenance test 1
python maintenance_test.py --scale $scale --test 1
# Run throughput test 2
python throughput_test.py --scale $scale --test 2
# Run maintenance test 2
python maintenance_test.py --scale $scale --test 2
