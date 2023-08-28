FROM python:3.10.12
RUN useradd -u 1000 docker_user
COPY ./requirements.txt /tmp/requirements_veldhub.txt
COPY ./src/veld_registry/requirements.txt /tmp/requirements_registry.txt
COPY ./src/veld_validator/requirements.txt /tmp/requirements_validator.txt
RUN  ls -d /tmp/* | xargs -i pip install -r {}
USER docker_user
