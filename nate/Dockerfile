FROM python:3.7-slim-buster

MAINTAINER Hansun Lee

ADD . /flask-ml
WORKDIR /flask-ml
RUN pip3 install -r requirements.txt

CMD flask run --host=0.0.0.0 --port:5000