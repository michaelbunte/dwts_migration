#!/bin/bash

psql -d waterexp -c "\copy santa_teresa_plc_values FROM './santa_teresa_data.csv' WITH (FORMAT csv, HEADER true)"