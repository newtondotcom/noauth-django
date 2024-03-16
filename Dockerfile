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

RUN --mount=type=secret,id=OAUTH2_REDIRECT_URI \
    --mount=type=secret,id=OAUTH2_SCOPES \
    --mount=type=secret,id=DB_NAME \
    --mount=type=secret,id=DB_USER \
    --mount=type=secret,id=DB_PASSWORD \
    --mount=type=secret,id=DB_HOST \
    --mount=type=secret,id=DB_PORT \
    --mount=type=secret,id=MASTER_DOCKER_URL \
    export OAUTH2_REDIRECT_URI=$(cat /run/secrets/OAUTH2_REDIRECT_URI) && \
    export OAUTH2_SCOPES=$(cat /run/secrets/OAUTH2_SCOPES) && \
    export DB_NAME=$(cat /run/secrets/DB_NAME) && \
    export DB_USER=$(cat /run/secrets/DB_USER) && \
    export DB_PASSWORD=$(cat /run/secrets/DB_PASSWORD) && \
    export DB_HOST=$(cat /run/secrets/DB_HOST) && \
    export DB_PORT=$(cat /run/secrets/DB_PORT) && \
    export MASTER_DOCKER_URL=$(cat /run/secrets/MASTER_DOCKER_URL)

# run entrypoint script
COPY entrypoint.sh $DockerHOME/
RUN chmod +x $DockerHOME/entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]