# base image
FROM python:3.8

# setup environment variable
ENV DockerHOME=/home/app/webapp

# expose port
EXPOSE 8000

# set work directory
RUN mkdir -p $DockerHOME
WORKDIR $DockerHOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

# copy only necessary files
COPY requirements.txt $DockerHOME/
RUN pip install -r requirements.txt
COPY . $DockerHOME/

RUN mkdir static

RUN cat /run/secrets/OAUTH2_REDIRECT_URI \
    /run/secrets/OAUTH2_SCOPES \
    /run/secrets/DB_NAME \
    /run/secrets/DB_USER \
    /run/secrets/DB_PASSWORD \
    /run/secrets/DB_HOST \
    /run/secrets/DB_PORT \
    /run/secrets/MASTER_DOCKER_URL > .env

# run entrypoint script
COPY entrypoint.sh $DockerHOME/
RUN chmod +x $DockerHOME/entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]