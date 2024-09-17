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

def createWaterSystemTable(systemName, cursor):
    unit_table_name = f'{systemName}_unit_table'
    sensor_info_table_name = f'{systemName}_sensor_info'
    alarm_table_name = f'{systemName}_alarm_table'
    data_table_name = f'{systemName}_plc_data'

    create_site_unit_table = (
        f'CREATE TABLE {unit_table_name} ('
        + 'unit VARCHAR(63) NOT NULL,'
        + 'id SERIAL PRIMARY KEY,'
        + 'primary_unit VARCHAR(63) NOT NULL,'
        + 'conversion_factor DOUBLE PRECISION NOT NULL'
        +'); '
    )

    create_site_sensor_info_table = (
        f'CREATE TABLE {sensor_info_table_name} ('
        + 'internal_data_name VARCHAR(63) NOT NULL,'
        + 'human_readible_name VARCHAR(63),'
        + 'abbreviated_name VARCHAR(63),'
        + 'date_installed TIMESTAMP,'
        + 'date_removed TIMESTAMP,'
        + 'serial_code VARCHAR(63),'
        + 'sensor_stream_name VARCHAR(63),'
        + 'id SERIAL PRIMARY KEY,'
        + 'units VARCHAR(63),'
        + 'description TEXT'
        + ');'
    )

    create_site_alarm_table = (
        f'CREATE TABLE {alarm_table_name} ('
        + 'id SERIAL PRIMARY KEY,'
        + 'value DOUBLE PRECISION NOT NULL,'
        + 'duration INTERVAL NOT NULL,'
        + 'sensor VARCHAR(63) NOT NULL'
        + ');'
    )

    insert_system_into_site_table_names = f"""
        INSERT INTO site_table_names
        (
            site_name,
            data_sensor_table,
            low_res_table,
            sensor_info_table,
            alarm_table,
            unit_table,
            sensor_graph_table,
            pipe_graph_table,
            component_graph_table
        ) VALUES (
            '{systemName}',
            '{data_table_name}',
            NULL,
            '{sensor_info_table_name}',
            '{alarm_table_name}',
            '{unit_table_name}',
            NULL,
            NULL,
            NULL
        );
    """

    cursor.execute(sql.SQL(create_site_unit_table))
    cursor.execute(sql.SQL(create_site_sensor_info_table))
    cursor.execute(sql.SQL(create_site_alarm_table))
    cursor.execute(sql.SQL(insert_system_into_site_table_names))


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
    cursor.execute(sql.SQL(create_plc_table_commands.createSantaTeresa("santa_teresa_plc_values")))
    cursor.execute(sql.SQL(create_plc_table_commands.createPryorFarms("pryor_farms_plc_values")))
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

class CleanArray:
    def __init__(self, cursor, dbname):
        self.cursor = cursor
        self.dbname = dbname
        self.sensors_to_clip = [ 
            "feedpressure", 
            "permeatepressure",
            "feedtds",
            "permtds",

            "totalroflow",
            "totaldelflow",
            "permeateflow",
            "deliveryflow",
            "concentrateflow",
            "recycleflow",
            "dailypermflow",
            "inletflow"
        ]

        self.ro_states = {
            0: "off",
            1: "stopped",
            2: "production",
            3: "standby",
            4: "feed_flush",
            5: "permeate_flush",
            8: "permeate_flush"
        }

        self.cached_values = {
            "feedtds": 0,
            "permtds": 0
        }


    def clip_value_at_zero(self, plctime_str, value_name):
        self.cursor.execute(sql.SQL(f"SELECT {value_name} FROM {self.dbname} where plctime = '{plctime_str}' limit 1;"))
        value = list(self.cursor.fetchall())[0][0]
        new_value = max(0, value)
        self.cursor.execute(sql.SQL(f"UPDATE {self.dbname} SET {value_name} = {new_value} WHERE plctime = '{plctime_str}';"))

    def cache_if_flusing_or_restore_cache_if_standby(self, plctime_str, value_name):
        self.cursor.execute(sql.SQL(f"SELECT state FROM {self.dbname} where plctime = '{plctime_str}' limit 1;"))
        ro_state = list(self.cursor.fetchall())[0][0]
        ro_state_string = self.ro_states[ro_state]
        if "flush" in ro_state_string:
            self.cursor.execute(sql.SQL(f"SELECT {value_name} FROM {self.dbname} where plctime = '{plctime_str}' limit 1;"))
            sensor_value = list(self.cursor.fetchall())[0][0]
            self.cached_values[value_name] = sensor_value
        elif ro_state_string == "standby":
            self.cursor.execute(sql.SQL(f"UPDATE {self.dbname} SET {value_name} = {self.cached_values[value_name]} WHERE plctime = '{plctime_str}';"))
            

    def clean_array(self, plctime_str):
        try :
            for sensor in self.sensors_to_clip:
                self.clip_value_at_zero(plctime_str, sensor)
            
            for sensor in self.cached_values.keys():
                self.cache_if_flusing_or_restore_cache_if_standby(plctime_str, sensor)
        except:
            raise Exception('no more values')

def clean_data(
    local_db_name,
):
    local_conn = psycopg2.connect(database="waterexp")
    local_conn.autocommit = True 
    local_cursor = local_conn.cursor()
    
    def get_first_plctime():
        local_cursor.execute(sql.SQL(f"SELECT plctime FROM {local_db_name} ORDER BY plctime asc limit 1;"))
        times = list(local_cursor.fetchall())
        return times[0][0]
    
    def datetime_to_string(timestamp):
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')

    current_time = get_first_plctime()

    def get_next_time(timestamp):
        local_cursor.execute(sql.SQL(f"SELECT plctime FROM {local_db_name} where plctime > '{datetime_to_string(timestamp)}' ORDER BY plctime asc limit 1;"))
        times = list(local_cursor.fetchall())
        return times[0][0]
    
    clean_array = CleanArray(local_cursor, local_db_name)

    while True:
        try:
            clean_array.clean_array(datetime_to_string(current_time))
            current_time = get_next_time(current_time)
        except Exception as e:
            raise e

    local_conn.close()


clean_data("santa_teresa_plc_values")


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
