FROM postgres:15.4
RUN usermod -u 1000 postgres
RUN groupmod -g 1000 postgres
COPY ./sql/db_init.sql /docker-entrypoint-initdb.d/
