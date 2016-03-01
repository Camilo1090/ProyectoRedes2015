BEGIN;
/*
DROP TABLE IF EXISTS monitor;
CREATE TABLE monitor
(
 fecha     TIMESTAMP,
 who       VARCHAR,
 cpu_us    VARCHAR,
 cpu_sy    VARCHAR,
 cpu_id    VARCHAR,
 cpu_wa    VARCHAR,
 cpu_st    VARCHAR,
 mem_swpd  VARCHAR,
 mem_free  VARCHAR,
 mem_buff  VARCHAR,
 mem_cache VARCHAR,
 swap_si   VARCHAR,
 swap_so   VARCHAR,
 PRIMARY KEY (fecha)
);
*/
DROP TABLE IF EXISTS transmission;
CREATE TABLE transmission
(
 id		SERIAL,
 fecha_insert   TIMESTAMP,
 fecha_update	TIMESTAMP,
 magnet    	VARCHAR,
 estado    	VARCHAR,
 progreso  	VARCHAR,
 PRIMARY KEY (id)
);

COMMIT;
