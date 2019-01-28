FROM python:3.7.2-alpine3.8

RUN mkdir -p /var/www/talis

WORKDIR /var/www/talis

COPY . .

RUN python3 -m pip install -r requirements.txt

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

CMD ["/wait && python twitch_message_producer.py"]
