select pg_terminate_backend(pid) from pg_stat_activity where datname='sgp_db_produccion';

DROP DATABASE "sgp_db_produccion";

CREATE DATABASE sgp_db_produccion TEMPLATE template0 OWNER postgres;

