#!/bin/bash

psql -d waterexp -c "\copy pryor_farms_plc_values FROM './pryor_farms_data.csv' WITH (FORMAT csv, HEADER true)"