#!/bin/bash

psql -d waterexp -c "\copy bluerock_plc_values FROM './bluerock_data.csv' WITH (FORMAT csv, HEADER true)"