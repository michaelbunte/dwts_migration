#!/bin/bash
psql -d waterexp -c "DELETE FROM pryor_farms_sensor_info"
psql -d waterexp -c "\copy pryor_farms_sensor_info FROM './pryor_teresa_sensor_info.csv' WITH (FORMAT csv, HEADER true)"