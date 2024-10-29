# create database
python scripts/setup_database.py --scale $scale
#generate data
./dsdgen -scale $scale -dir "../../generated_data/scale_$scale"
#generate queries
./dsqgen -directory "../query_templates/" -input "../query_templates/templates.lst" -dialect netezza -scale 1 -output_dir "../../generated_queries/"
#run load test
python scripts/load_test.py --scale $scale
#run power test
python scripts/power_test.py --scale $scale

# Generate query streams
./dsqgen -directory "../query_templates/" -input "../query_templates/templates.lst" -scale $scale -output_dir "../../generated_queries/stream_queries/scale_$scale" -streams 4 -dialect netezza
# run throughtput test 1
python scripts/throughtput_test.py --scale $scale --test 1
# run maintenance test 1
python scripts/maintenance_test.py --scale $scale --test 1
# run throughtput test 2
python scripts/throughtput_test.py --scale $scale --test 2
# run maintenance test 2
python scripts/maintenance_test.py --scale $scale --test 2