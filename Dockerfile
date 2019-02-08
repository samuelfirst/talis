ARG CACHEBUST=1
FROM 446783133405.dkr.ecr.us-west-2.amazonaws.com/talis:builder as app
RUN mkdir -p /var/www/talis
WORKDIR /var/www/talis
COPY ./requirements.txt ./run-tests ./
RUN python -m pip install -r requirements.txt && \
    chmod +x run-tests
COPY . .
