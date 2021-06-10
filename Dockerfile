FROM python:3.8-slim-buster
ADD . /flask-ml
WORKDIR /flask-ml
RUN pip3 install -r requirements.txt