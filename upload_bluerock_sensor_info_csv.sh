#!/bin/bash

psql -d waterexp -c "DELETE FROM bluerock_sensor_info"
psql -d waterexp -c "\copy bluerock_sensor_info FROM './bluerock_sensor_info.csv' WITH (FORMAT csv, HEADER true)"