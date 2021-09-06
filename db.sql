select pg_terminate_backend(pid) from pg_stat_activity where datname='sgp_db';

DROP DATABASE "sgp_db";

CREATE DATABASE sgp_db TEMPLATE template0 OWNER postgres;

