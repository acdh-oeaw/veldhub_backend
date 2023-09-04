FROM python:3.11.5
RUN useradd -u 1000 docker_user
COPY ./requirements.txt /tmp/requirements_veldhub.txt
COPY ./src/veld_registry/requirements.txt /tmp/requirements_registry.txt
COPY ./src/veld_repos/requirements.txt /tmp/requirements_repos.txt
RUN  ls -d /tmp/requirements* | xargs -i pip install -r {}
USER docker_user
