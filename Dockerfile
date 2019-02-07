FROM python:3.7.2-alpine3.8 as build
RUN apk add --no-cache \
        --virtual=.build-dependencies \
        g++ gfortran file binutils \
        musl-dev python3-dev openblas-dev && \
    apk add libstdc++ openblas && \
    \
    pip install numpy==1.16.1 && \
    pip install nltk==3.4 && \
    pip install scipy==1.2.0 && \
    pip install scikit-learn==0.20.2 && \
    pip install pycryptodome==3.7.3 && \
    python -m nltk.downloader punkt && \
    python -m nltk.downloader wordnet && \
    \
    rm -r /root/.cache && \
    find /usr/lib/python3.*/ -name 'tests' -exec rm -r '{}' + && \
    find /usr/lib/python3.*/site-packages/ -name '*.so' -print -exec sh -c 'file "{}" | grep -q "not stripped" && strip -s "{}"' \; && \
    \
    apk del .build-dependencies

ARG CACHEBUST=1
FROM build as app
RUN mkdir -p /var/www/talis
WORKDIR /var/www/talis
COPY ./requirements.txt .
RUN python -m pip install -r requirements.txt
COPY . .
