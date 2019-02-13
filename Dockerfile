FROM python:3.6.5-slim

WORKDIR /pawatt

ADD . /pawatt

RUN apt-get update \
  && apt-get upgrade -y \
  && apt-get install -y \
  build-essential \
  ca-certificates \
  gcc \
  git \
  libpq-dev \
  make \
  python-pip \
  ssh \
  && apt-get autoremove \
  && apt-get clean

RUN pip install --upgrade \ 
  pip shub python-dotenv scrapy \ 
  scrapinghub[msgpack] boto3 awscli
