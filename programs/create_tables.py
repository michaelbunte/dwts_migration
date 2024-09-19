import psycopg2
from psycopg2 import sql
import create_plc_table_commands

def createWaterSystemTable(systemName, cursor):
    unit_table_name = f'{systemName}_unit_table'
    sensor_info_table_name = f'{systemName}_sensor_info'
    alarm_table_name = f'{systemName}_alarm_table'
    data_table_name = f'{systemName}_plc_values'
    low_res_data_table_name = f'{systemName}_plc_values_low_res'

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
            '{low_res_data_table_name}',
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

def create_metadata_tables():
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

create_metadata_tables()
create_plc_tables()