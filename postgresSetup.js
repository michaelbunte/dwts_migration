const { Client } = require('pg');



// Order of function calls:
// setupFromBlank() -> createWaterSystemTables() -> linkSensorDataTables()
// -> createSantaTeresaPLCTables()

//     console.log('Query result:', result.rows);

// Initializes the database to be ready to start adding systems.
function setupFromBlank(client){
    const create_site_table_names = 
        'CREATE TABLE site_table_names ('
            + 'site_name VARCHAR(63) PRIMARY KEY NOT NULL, '
            + 'data_sensor_table VARCHAR(63), '
            + 'low_res_table VARCHAR(63), '
            + 'sensor_info_table VARCHAR(63), '
            + 'alarm_table VARCHAR(63), '
            + 'unit_table VARCHAR(63), '
            + 'sensor_graph_table VARCHAR(63), '
            + 'pipe_graph_table VARCHAR(63), '
            + 'component_graph_table VARCHAR(63)'
        + ');';

    client.query(create_site_table_names, (err, result) => {
        if (err) {
            console.error('Error creating table: ', err);
        } else {
            console.log("site_table_names created");
        }
    });

    const create_minmax = "CREATE TYPE minmax AS ENUM ('min', 'max');"
    client.query(create_minmax, (err, result) => {
        if (err) {
            console.error('Error creating minmax enum: ', err);
        } else {
            console.log("minmax enum created");
        }
    });
}

// Initializes the unit_table, sensor_info_table, and the alarm_table for a 
// given system. 
function createWaterSystemTables(client, systemName) {
    const unit_table_name = `${systemName}_unit_table`;
    const sensor_info_table_name = `${systemName}_sensor_info`;
    const alarm_table_name = `${systemName}_alarm_table`;

    const create_site_unit_table = 
    `CREATE TABLE ${unit_table_name} (`
        + 'unit VARCHAR(63) NOT NULL,'
        + 'id SERIAL PRIMARY KEY,'
        + 'primary_unit VARCHAR(63) NOT NULL,'
        + 'conversion_factor DOUBLE PRECISION NOT NULL'
    +'); ';

    const create_site_sensor_info_table = 
    `CREATE TABLE ${sensor_info_table_name} (`
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
    + ');';

    const create_site_alarm_table = 
    `CREATE TABLE ${alarm_table_name} (`
        + 'id SERIAL PRIMARY KEY,'
        + 'value DOUBLE PRECISION NOT NULL,'
        + 'duration INTERVAL NOT NULL,'
        + 'sensor minmax NOT NULL'
    + ');';

    const insert_system_into_site_table_names = 
    `INSERT INTO site_table_names
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
        '${systemName}',
        NULL,
        NULL,
        '${sensor_info_table_name}',
        '${alarm_table_name}',
        '${unit_table_name}',
        NULL,
        NULL,
        NULL
    )`;
    
    client.query(create_site_unit_table, (err, result) => {
        if (err) {
            console.error('Error creating table: ', err);
        } else {
            console.log("site_unit_table created");
        }
    });

    client.query(create_site_sensor_info_table, (err, result) => {
        if (err) {
            console.error('Error creating table: ', err);
        } else {
            console.log("site_sensor_info_table created");
        }
    });

    client.query(create_site_alarm_table, (err, result) => {
        if (err) {
            console.error('Error creating table: ', err);
        } else {
            console.log("site_alarm_table created");
        }
    });

    client.query(insert_system_into_site_table_names, (err, result) => {
        if (err) {
            console.error('Error adding to site table', err);
        } else {
            console.log("site_table_names updated");
        }
    });
}

/*
These tables were created using
pg_dump -t 'schema-name.table-name' --schema-only database-name

Except for otherwise noted changes ("-- Added After Dump")
*/

function createBluerockHelper(
    tableName
) {
    const createBluerock = `
    --
    -- PostgreSQL database dump
    --

    -- Dumped from database version 14.8 (Ubuntu 14.8-0ubuntu0.22.04.1)
    -- Dumped by pg_dump version 14.9 (Homebrew)

    SET statement_timeout = 0;
    SET lock_timeout = 0;
    SET idle_in_transaction_session_timeout = 0;
    SET client_encoding = 'UTF8';
    SET standard_conforming_strings = on;
    SELECT pg_catalog.set_config('search_path', '', false);
    SET check_function_bodies = false;
    SET xmloption = content;
    SET client_min_messages = warning;
    SET row_security = off;

    SET default_tablespace = '';

    SET default_table_access_method = heap;

    --
    -- Name: ${tableName}; Type: TABLE; Schema: public; Owner: postgres
    --

    CREATE TABLE public.${tableName} (
        location text NOT NULL,
        totalroflow double precision,
        totalfeedflow double precision,
        totalrecycleflow double precision,
        totaldelflow double precision,
        dumpproduct boolean,
        wellpumprun boolean,
        wellpumpauto boolean,
        feedpumprun boolean,
        ropumprun boolean,
        deliveryrun boolean,
        deliveryauto boolean,
        inletrun boolean,
        concbypassrun boolean,
        proddiversionrun boolean,
        plctime timestamp with time zone NOT NULL,
        permeateflow double precision,
        deliveryflow double precision,
        feedflow double precision,
        concentrateflow double precision,
        recycleflow double precision,
        feedtanklevel double precision,
        dailypermflow double precision,
        alarm boolean,
        alarmword integer,
        rostandby boolean,
        state integer,
        lockout boolean,
        runflush boolean,
        warnword0 integer,
        warnword1 integer,
        totalhrs double precision,
        permtds double precision,
        feedtds double precision,
        permnitrate double precision,
        permtemp double precision,
        prodtanklevel double precision,
        prodtankdisable boolean,
        prodtankdepth double precision,
        feedtankdepth double precision,
        residualtankdepth double precision,
        inletpressure double precision,
        concentratepressure double precision,
        permeatepressure double precision,
        ropressure double precision,
        deliverypressure double precision,
        feedpressure double precision,
        recyclevalveposition double precision,
        ropressctrlvalveposition double precision,
        ropumpspeed double precision,
        powermeter double precision,
        flushduret double precision,
        producttds double precision,
        chlorinepumprun boolean,
        residtankvalverun boolean,
        residualtanklevel double precision,
        recordtime timestamp with time zone,
        schema_version text,
        extras jsonb,
        flushrun boolean,
        inletflow double precision -- Added after dump
    );


    -- [REMOVED] ALTER TABLE public.${tableName} OWNER TO postgres;

    --
    -- Name: ${tableName}_plctime_idx; Type: INDEX; Schema: public; Owner: postgres
    --

    CREATE INDEX ${tableName}_plctime_idx ON public.${tableName} USING btree (plctime DESC);


    --
    -- Name: ${tableName} ts_insert_blocker; Type: TRIGGER; Schema: public; Owner: postgres
    --

    -- [REMOVED] CREATE TRIGGER ts_insert_blocker BEFORE INSERT ON public.${tableName} FOR EACH ROW EXECUTE FUNCTION _timescaledb_internal.insert_blocker();


    --
    -- Name: TABLE ${tableName}; Type: ACL; Schema: public; Owner: postgres
    --

    -- [REMOVED] GRANT SELECT ON TABLE public.${tableName} TO read_only;


    --
    -- PostgreSQL database dump complete
    --
    `;
    return createBluerock;
}

function createSantaTeresaHelper(
    tableName
) {
    const createSantaTeresa = `
    --
    -- PostgreSQL database dump
    --
    
    -- Dumped from database version 14.8 (Ubuntu 14.8-0ubuntu0.22.04.1)
    -- Dumped by pg_dump version 14.9 (Homebrew)
    
    SET statement_timeout = 0;
    SET lock_timeout = 0;
    SET idle_in_transaction_session_timeout = 0;
    SET client_encoding = 'UTF8';
    SET standard_conforming_strings = on;
    SELECT pg_catalog.set_config('search_path', '', false);
    SET check_function_bodies = false;
    SET xmloption = content;
    SET client_min_messages = warning;
    SET row_security = off;
    
    SET default_tablespace = '';
    
    SET default_table_access_method = heap;
    
    --
    -- Name: ${tableName}; Type: TABLE; Schema: public; Owner: postgres
    --
    
    CREATE TABLE public.${tableName} (
        location text NOT NULL,
        totalroflow double precision,
        totalinletflow double precision,
        totalconcflow double precision,
        totaldelflow double precision,
        dumpproduct boolean,
        wellpumprun boolean,
        wellpumpauto boolean,
        feedpumprun boolean,
        ropumprun boolean,
        deliveryrun boolean,
        deliveryauto boolean,
        inletrun boolean,
        flushrun boolean,
        concbypassrun boolean,
        proddiversionrun boolean,
        flushdiversionrun boolean,
        plctime timestamp with time zone NOT NULL,
        permeateflow double precision,
        deliveryflow double precision,
        inletflow double precision,
        concentrateflow double precision,
        recycleflow double precision,
        feedtanklevel double precision,
        dailypermflow double precision,
        dailyinletflow double precision,
        alarm boolean,
        alarmword integer,
        rostandby boolean,
        state integer,
        lockout boolean,
        runflush boolean,
        warnword0 integer,
        warnword1 integer,
        totalhrs double precision,
        permtds double precision,
        feedtds double precision,
        permnitrate double precision,
        permtemp double precision,
        prodtanklevel double precision,
        prodtankdisable boolean,
        prodtankdepth double precision,
        feedtankdepth double precision,
        flushtanklevel double precision,
        flushtankdepth double precision,
        flushtankfull boolean,
        inletpressure double precision,
        concentratepressure double precision,
        permeatepressure double precision,
        ropressure double precision,
        deliverypressure double precision,
        feedpressure double precision,
        recyclevalveposition double precision,
        ropressctrlvalveposition double precision,
        ropumpspeed double precision,
        powermeter double precision,
        flushduret double precision,
        producttds double precision
    );
    
    
    -- [REMOVED] ALTER TABLE public.${tableName} OWNER TO postgres;
    
    --
    -- Name: ${tableName} ${tableName}_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
    --
    
    ALTER TABLE ONLY public.${tableName}
        ADD CONSTRAINT ${tableName}_pkey PRIMARY KEY (location, plctime);
    
    
    --
    -- Name: ${tableName}_plctime_idx; Type: INDEX; Schema: public; Owner: postgres
    --
    
    CREATE INDEX ${tableName}_plctime_idx ON public.${tableName} USING btree (plctime DESC);
    
    
    --
    -- Name: ${tableName} ts_insert_blocker; Type: TRIGGER; Schema: public; Owner: postgres
    --
    
    -- [REMOVED] CREATE TRIGGER ts_insert_blocker BEFORE INSERT ON public.${tableName} FOR EACH ROW EXECUTE FUNCTION _timescaledb_internal.insert_blocker();
    
    
    --
    -- Name: TABLE ${tableName}; Type: ACL; Schema: public; Owner: postgres
    --
    
    -- [REMOVED] GRANT SELECT ON TABLE public.${tableName} TO read_only;
    
    
    --
    -- PostgreSQL database dump complete
    --
    `;
    return createSantaTeresa;
}

function createSantaTeresaPLCTables(
    client,
    mainDataTableName,
    lowResDataTableName
){
    if (mainDataTableName != null ) {
        let createSantaTeresaSetupString 
            = createSantaTeresaHelper(mainDataTableName);

        client.query(createSantaTeresaSetupString, (err, result) => {
            if (err) {
                console.error('Error creating table: ', err);
            } else {
                console.log(`${mainDataTableName} created`);
            }
        });
    }

    if (lowResDataTableName != null) {
        let createSantaTeresaLowResSetupString 
        = createSantaTeresaHelper(lowResDataTableName);
        
        client.query(createSantaTeresaLowResSetupString, (err, result) => {
            if (err) {
                console.error('Error creating table: ', err);
            } else {
                console.log(`${lowResDataTableName} created`);
            }
        });
    }
}


function createBluerockPLCTables(
    client,
    mainDataTableName,
    lowResDataTableName
){
    if (mainDataTableName != null ) {
        let createBluerockSetupString 
            = createBluerockHelper(mainDataTableName);

        client.query(createBluerockSetupString, (err, result) => {
            if (err) {
                console.error('Error creating table: ', err);
            } else {
                console.log(`${mainDataTableName} created`);
            }
        });
    }

    if (lowResDataTableName != null) {
        let createBluerockSetupString 
        = createBluerockHelper(lowResDataTableName);
        
        client.query(createBluerockSetupString, (err, result) => {
            if (err) {
                console.error('Error creating table: ', err);
            } else {
                console.log(`${lowResDataTableName} created`);
            }
        });
    }
}



// Since the "PLC data" and the "low resolution PLC data" are initialized 
// separately, this function adds "PLC data table" and "low resolution PLC data
// table" names to the site_name sensors.
function linkSensorDataTables(
    client,
    systemName, 
    mainDataTableName = null, 
    lowResDataTableName = null
) {
    if (mainDataTableName === null && lowResDataTableName === null) { return; }
    
    if (mainDataTableName != null) {
        const site_table_names_update = 
            `UPDATE site_table_names
             SET data_sensor_table = '${mainDataTableName}'
             WHERE site_name = '${systemName}';
            `;
        client.query(site_table_names_update, (err, result) => {
            if (err) {
                console.error('Failed to update data_sensor_table name', err);
            } else {
                console.log("site_table_names updated with 'main data' table");
            }
        });
    }

    if (lowResDataTableName != null) {
        const site_table_names_update = 
        `UPDATE site_table_names
         SET low_res_table = '${lowResDataTableName}'
         WHERE site_name = '${systemName}';
        `;

        client.query(site_table_names_update, (err, result) => {
            if (err) {
                console.error('Failed to update low_res_table name', err);
            } else {
                console.log("site_table_names updated with 'low res data' table");
            }
        });
    }
}

function deleteAllTables(client) {
    const deleteAllTablesQuery = 'DROP SCHEMA public CASCADE; CREATE SCHEMA public;';

    client.query(deleteAllTablesQuery, (err, result) => {
        if (err) {
            console.error('Error deleting tables: ', err);
        } else {
            console.log("All tables deleted");
        }
    });
}

module.exports = {
    setupFromBlank, 
    createWaterSystemTables, 
    linkSensorDataTables,
    createSantaTeresaPLCTables,
    createBluerockPLCTables,
    deleteAllTables
};