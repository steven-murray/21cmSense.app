FROM python:3.8-slim-buster

RUN mkdir /21cmSense-server
WORKDIR /21cmSense-server
copy . . 

ENV REDIS_URL "redis"
ENV FLASK_APP "app"

RUN apt-get update -y
RUN apt-get install -qq -y build-essential gfortran python-pip python-dev redis-server
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /21cmSense-server

CMD ["flask", "run", "--cert=adhoc"]
