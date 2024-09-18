#!/bin/bash

rm santa_teresa_data.csv || {}
psql -h postgres.svwaternet.org -d tsdb -U read_only -c "COPY (SELECT * FROM santa_teresa_plc_values) TO STDOUT WITH CSV HEADER" > santa_teresa_data.csv