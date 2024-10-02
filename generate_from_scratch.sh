echo "initializing empty database"
./create_local_db.sh
./create_empty_tables.sh

echo "downloading bluerock csv"
./get_bluerock_csv.sh
echo "downloading santa teresa csv"
./get_santa_teresa_csv.sh
echo "downloading pryor farms csv"
./get_pryor_farms_csv.sh

echo "uploading bluerock csv to local db"
./upload_bluerock_csv.sh
echo "uploading santa teresa csv to local db"
./upload_santa_teresa_csv.sh
echo "uploading pryor farms csv to local db"
./upload_pryor_farms_csv.sh

echo "uploading bluerock sensor meta data"
./upload_bluerock_sensor_info_csv.sh
echo "uploading santa teresa sensor meta data"
./upload_santa_teresa_sensor_info_csv.sh
echo "uploading pryor farms sensor meta data"
./upload_pryor_farms_sensor_info_csv.sh

echo "cleaning bluerock sensor data"
./clean_bluerock_table.sh
echo "cleaning pryor farms data"
./clean_pryor_farms_table.sh
echo "cleaning santa teresa farms data"
./clean_santa_teresa_table.sh

echo "creating low res bluerock table"
./create_low_res_bluerock.sh
echo "creating low res pryor farms table"
./create_low_res_pryor_farms.sh
echo "creating low res santa teresa table"
./create_low_res_santa_teresa.sh

echo "transfer complete"