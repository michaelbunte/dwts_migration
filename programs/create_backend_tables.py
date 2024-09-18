import psycopg2
from psycopg2 import sql
import subprocess
import create_plc_table_commands
from datetime import datetime, timedelta

'''
Connection Strings
psql -h localhost -p 5432 -U michaelbunte -d waterexp
'''


SPAS = {
    "shell": True,
    "capture_output": True,
    "text": True
}

def run(command, printout=False, printerr=True):
    res = subprocess.run(command, **SPAS)
    if(printout and res.stdout.strip() != ""):
        print(res.stdout)
    if(printerr and res.stderr.strip() != ""):
        print(res.stderr)
    return res

def main():
    # print("Removing previously downloaded database")
    # run('rm -rf ./data')

    # run('mkdir data')
    # print("Downloading remote historical postgres data")
    # run('pg_dump -U read_only -h postgres.svwaternet.org -p 5432 -t bluerock_plc_values -t pryor_farm_plc_values -t santa_teresa_plc_values tsdb > ./data/dump.sql', printerr=False)

    # print("PSQL Dump Size:")
    # run('cat ./data/dump.sql | wc -c', printout=True)

    # print("Killing any process running at port 5432")
    # run("kill -9 $(lsof -n -i :5432 | tail -n +2 | head -n 1 | awk '{print $2}')")

    # print("Removing any previous cluster data")
    # run("rm -rf ./cluster")

    # print("Initializing new database")
    # start_command = run("pg_ctl -D ./cluster initdb 2>/dev/null | tail -n 2").stdout
    # print(start_command)
    # print("Running new database")
    # run(start_command)

    # conn = psycopg2.connect(database="postgres")
    # conn.autocommit = True 
    # cursor = conn.cursor()
    # cursor.execute(sql.SQL("CREATE DATABASE waterexp;"))
    # cursor.close()
    # conn.close()

    run("dropdb waterexp || {}")
    run("createdb waterexp")

    conn = psycopg2.connect(database="waterexp")
    conn.autocommit = True 
    cursor = conn.cursor()
    cursor.execute(sql.SQL('CREATE TABLE site_table_names ('
            + 'site_name VARCHAR(63) PRIMARY KEY NOT NULL, '
            + 'data_sensor_table VARCHAR(63), '
            + 'low_res_table VARCHAR(63), '
            + 'sensor_info_table VARCHAR(63), '
            + 'alarm_table VARCHAR(63), '
            + 'unit_table VARCHAR(63), '
            + 'sensor_graph_table VARCHAR(63), '
            + 'pipe_graph_table VARCHAR(63), '
            + 'component_graph_table VARCHAR(63)'
        + ');'))

    print("Creating Bluerock Tables")
    createWaterSystemTable("bluerock", cursor)

    print("Creating Santa Teresa Tables")
    createWaterSystemTable("santa_teresa", cursor)

    print("Creating Pryor Farms Tables")
    createWaterSystemTable("pryor_farms", cursor)

    cursor.close()
    conn.close()


def create_plc_tables():
    conn = psycopg2.connect(database="waterexp")
    conn.autocommit = True 
    cursor = conn.cursor()
    cursor.execute(sql.SQL(create_plc_table_commands.createBluerock("bluerock_plc_values")))
    cursor.execute(sql.SQL(create_plc_table_commands.createBluerock("bluerock_plc_values_low_res")))
    cursor.execute(sql.SQL(create_plc_table_commands.createSantaTeresa("santa_teresa_plc_values")))
    cursor.execute(sql.SQL(create_plc_table_commands.createSantaTeresa("santa_teresa_plc_values_low_res")))
    cursor.execute(sql.SQL(create_plc_table_commands.createPryorFarms("pryor_farms_plc_values")))
    cursor.execute(sql.SQL(create_plc_table_commands.createPryorFarms("pryor_farms_plc_values_low_res")))
    conn.close()

    

# bluerock size: 20630192
def remote_connect(
        local_db_name,
        remote_db_name,
        db_row_count
):
    remote_conn = psycopg2.connect(
        dbname="tsdb",
        host="postgres.svwaternet.org",
        user="read_only"
    )
    local_conn = psycopg2.connect(database="waterexp")
    local_conn.autocommit = True 


    remote_cursor = remote_conn.cursor()
    local_cursor = local_conn.cursor()
    
    offset = 0
    limit = 10 ** 2
    while True:
        remote_cursor.execute(sql.SQL(f"SELECT * FROM " + remote_db_name + " ORDER BY plctime limit " + str(limit) + " offset " + str(offset) + ";"))
        items = list(remote_cursor.fetchall())
        if len(items) == 0:
            break
        s = "%s, " * (db_row_count - 1) + "%s"
        print(s)
        print("Data received, inserting")
        local_cursor.executemany("INSERT INTO " + local_db_name + " values (" + s + ")", items)
        offset += limit
        print(f"{offset} rows written")

    remote_conn.close()



# main()
# create_plc_tables()

# remote_connect(
#     "santa_teresa_plc_values",
#     "santa_teresa_plc_values",
#     58
# )`



# psql -d waterexp -c "\copy pryor_farms_plc_values FROM './out2.csv' WITH (FORMAT csv, HEADER true)"
# psql -h postgres.svwaternet.org -d tsdb -U read_only -c "COPY (SELECT * FROM santa_teresa_plc_values) TO STDOUT WITH CSV HEADER" > out4.csv
# psql -h postgres.svwaternet.org -d tsdb -U read_only -c "COPY (SELECT * FROM santa_teresa_plc_values) TO STDOUT WITH CSV HEADER" > out4.csv
# psql -d waterexp -c "\copy santa_teresa_plc_values FROM './out4.csv' WITH (FORMAT csv, HEADER true)"
