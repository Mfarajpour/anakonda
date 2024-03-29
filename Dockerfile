FROM python:3.12-alpine

LABEL maintainer="mfarajpour"

ENV ANAKONDA_API_ENV=production
ENV ANAKONDA_API_DEBUG=0
ENV ANAKONDA_API_SECRET_KEY=secretkey
ENV ANAKONDA_API_JSON_PRETTYPRINT=0
ENV ANAKONDA_API_DATABASE_URI=None
ENV ANAKONDA_API_TIMEZONE=Europe/London

EXPOSE 8080

WORKDIR /opt/app

COPY requirements.txt .



RUN pip3 install -r requirements.txt

COPY . .

RUN adduser -DH -g anakonda anakonda

USER 1000

ENTRYPOINT ["gunicorn"]

CMD ["-c", "gunicorn.conf.py"]

ARG GIT_COMMIT=None
LABEL GIT_COMMIT=$GIT_COMMIT

ARG JENKINS_PIPELINE=None
LABEL JENKINS_PIPLINE=$JENKINS_PIPELINE

ARG BUILD_TAG=None
LABEL BUILD_TAG=$BUILD_TAG

ARG BUILD_ID=None
LABEL BUILD_ID=$BUILD_ID



