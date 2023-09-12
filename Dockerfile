FROM python:3.11.5
RUN apt update
RUN apt install git-lfs
RUN useradd -u 1000 docker_user
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
USER docker_user
