FROM python:3.7.2-alpine3.8

RUN mkdir -p /var/www/talis

WORKDIR /var/www/talis

COPY . .

RUN python3 -m pip install -r requirements.txt
