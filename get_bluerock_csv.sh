#!/bin/bash


rm bluerock_data.csv|| {}
psql -h postgres.svwaternet.org -d tsdb -U read_only -c "COPY (SELECT * FROM bluerock_plc_values) TO STDOUT WITH CSV HEADER" > bluerock_data.csv