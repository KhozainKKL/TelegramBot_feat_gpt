FROM python:latest
MAINTAINER deimandar
RUN python -m pip install --upgrade pip &&  \
    pip install telebot &&  \
    pip install python-dotenv &&  \
    pip install pydantic &&  \
    pip install peewee &&  \
    pip install openai


WORKDIR /MyHelp_bot

COPY . /MyHelp_bot


