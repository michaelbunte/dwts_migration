#!/bin/bash
rm pryor_farms_data.csv || {}
psql -h postgres.svwaternet.org -d tsdb -U read_only -c "COPY (SELECT * FROM pryor_farm_plc_values) TO STDOUT WITH CSV HEADER" > pryor_farms_data.csv