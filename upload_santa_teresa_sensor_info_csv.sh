#!/bin/bash

psql -d waterexp -c "\copy santa_teresa_sensor_info FROM './pryor_teresa_sensor_info.csv' WITH (FORMAT csv, HEADER true)"