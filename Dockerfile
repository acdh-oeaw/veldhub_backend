FROM python:3.11.5
RUN apt update
RUN apt install -y git-lfs iputils-ping
RUN useradd -u 1000 docker_user
RUN mkdir "/home/docker_user"
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
USER docker_user
