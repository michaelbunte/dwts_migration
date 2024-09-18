#!/bin/bash

rm -rf ./cluster || {}
pg_ctl -D ./cluster initdb 2>/dev/null | tail -n 2
echo "^ Run the above line to start the db"