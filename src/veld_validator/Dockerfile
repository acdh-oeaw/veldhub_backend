FROM python:3.10.12
RUN useradd -u 1000 docker_user
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
USER docker_user
