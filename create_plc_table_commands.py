

createSantaTeresaFull = '''
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
-- Name: santa_teresa_plc_values; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.santa_teresa_plc_values (
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


ALTER TABLE public.santa_teresa_plc_values OWNER TO postgres;

--
-- Name: santa_teresa_plc_values santa_teresa_plc_values_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.santa_teresa_plc_values
    ADD CONSTRAINT santa_teresa_plc_values_pkey PRIMARY KEY (location, plctime);


--
-- Name: santa_teresa_plc_values_plctime_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX santa_teresa_plc_values_plctime_idx ON public.santa_teresa_plc_values USING btree (plctime DESC);


--
-- Name: santa_teresa_plc_values ts_insert_blocker; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER ts_insert_blocker BEFORE INSERT ON public.santa_teresa_plc_values FOR EACH ROW EXECUTE FUNCTION _timescaledb_internal.insert_blocker();


--
-- Name: TABLE santa_teresa_plc_values; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.santa_teresa_plc_values TO read_only;


--
-- PostgreSQL database dump complete
--
'''




createBluerockFull = '''
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
-- Name: bluerock_plc_values; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bluerock_plc_values (
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
    flushrun boolean
);


ALTER TABLE public.bluerock_plc_values OWNER TO postgres;

--
-- Name: bluerock_plc_values_plctime_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX bluerock_plc_values_plctime_idx ON public.bluerock_plc_values USING btree (plctime DESC);


--
-- Name: bluerock_plc_values ts_insert_blocker; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER ts_insert_blocker BEFORE INSERT ON public.bluerock_plc_values FOR EACH ROW EXECUTE FUNCTION _timescaledb_internal.insert_blocker();


--
-- Name: TABLE bluerock_plc_values; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.bluerock_plc_values TO read_only;


--
-- PostgreSQL database dump complete
--
'''



def createBluerock(system_name):
    return  f'''
    CREATE TABLE {system_name} (
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
        flushrun boolean
    );

    CREATE INDEX idx_time ON {system_name} (plctime);
    '''


def createSantaTeresa(system_name):
    return  f'''
    CREATE TABLE {system_name} (
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

    CREATE INDEX idx_time ON {system_name} (plctime);
    '''