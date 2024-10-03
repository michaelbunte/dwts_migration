#!/bin/bash
node ./programs/create_low_res_tables.js -t "bluerock_plc_values" -e "_low_res" -g $((6 * 60 * 60 * 1000)) # 6 hours
node ./programs/create_low_res_tables.js -t "bluerock_plc_values" -e "_med_res" -g $((36 * 60 * 1000)) # 36 minutes