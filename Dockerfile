FROM python:3.11

COPY requirements.txt /temp/requirements.txt

COPY core /core

WORKDIR /core

RUN pip install --upgrade pip

RUN pip install --upgrade setuptools

RUN pip install -r /temp/requirements.txt

RUN chmod 755 .