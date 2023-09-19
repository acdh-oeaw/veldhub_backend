FROM debian:12.1
RUN apt update
RUN apt install -y git-lfs iputils-ping python3.11=3.11.2-6 python3-pip
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --break-system-packages -r /tmp/requirements.txt
RUN useradd -u 1000 docker_user
RUN mkdir "/home/docker_user"
USER docker_user
