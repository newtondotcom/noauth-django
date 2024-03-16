FROM python:3.8
ENV DockerHOME=/home/app/webapp
EXPOSE 8000
RUN mkdir -p $DockerHOME
WORKDIR $DockerHOME


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install --upgrade pip


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
    --mount=type=secret,id=ALLOWED_API_KEYS \
    echo "OAUTH2_REDIRECT_URI=$(cat /run/secrets/OAUTH2_REDIRECT_URI)" >> $DockerHOME/.env && \
    echo "OAUTH2_SCOPES=$(cat /run/secrets/OAUTH2_SCOPES)" >> $DockerHOME/.env && \
    echo "DB_NAME=$(cat /run/secrets/DB_NAME)" >> $DockerHOME/.env && \
    echo "DB_USER=$(cat /run/secrets/DB_USER)" >> $DockerHOME/.env && \
    echo "DB_PASSWORD=$(cat /run/secrets/DB_PASSWORD)" >> $DockerHOME/.env && \
    echo "DB_HOST=$(cat /run/secrets/DB_HOST)" >> $DockerHOME/.env && \
    echo "DB_PORT=$(cat /run/secrets/DB_PORT)" >> $DockerHOME/.env && \
    echo "MASTER_DOCKER_URL=$(cat /run/secrets/MASTER_DOCKER_URL)" >> $DockerHOME/.env && \
    echo "ALLOWED_API_KEYS=$(cat /run/secrets/ALLOWED_API_KEYS)" >> $DockerHOME/.env

COPY entrypoint.sh $DockerHOME/
RUN chmod +x $DockerHOME/entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]