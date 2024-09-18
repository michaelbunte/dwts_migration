import argparse
import psycopg2
from psycopg2 import sql

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

    def clip_values_group(self, plctime_str):
        sensors_string = ", ".join(self.sensors_to_clip)
        select_string = f"SELECT {sensors_string} FROM {self.dbname} WHERE plctime = '{plctime_str}' limit 1;"
        
        self.cursor.execute(sql.SQL(select_string))
        values = list(self.cursor.fetchall())[0]
        clipped_values = list(map(lambda x: max(0, x), values))
        update_strs_array = list(map(lambda x: f"{x[0]} = {x[1]}", zip(self.sensors_to_clip, clipped_values)))
        update_sensors_string = ", ".join(update_strs_array)
        self.cursor.execute(sql.SQL(f"UPDATE {self.dbname} SET {update_sensors_string} WHERE plctime = '{plctime_str}';"))
        

    def clean_array(self, plctime_str):
        try :
            self.clip_values_group(plctime_str)
            
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

    i = 0
    while True:
        try:
            clean_array.clean_array(datetime_to_string(current_time))
            current_time = get_next_time(current_time)
        except Exception as e:
            raise e
        if i% 100 == 0:
            print(i)
        i+=1

    local_conn.close()



parser = argparse.ArgumentParser()
parser.add_argument('table_to_clean', type=str)
args = parser.parse_args()
clean_data(args.table_to_clean)
