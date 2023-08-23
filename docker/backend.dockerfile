FROM python:3.10.12
RUN pip install psycopg2==2.9.7
RUN useradd -u 1000 docker_user
USER docker_user
WORKDIR /src
