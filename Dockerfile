#Pull Python 3.6
FROM python:3.6-buster
#Set work dir
WORKDIR /usr/src/app
#Set env vars
ENV APP_SETTINGS config.DevelopmentConfig
ENV DATABASE_URL postgresql://postgres:root@localhost/covid
#Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
#Copy current directory to container work dir
COPY . /usr/src/app/
