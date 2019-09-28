FROM czentye/matplotlib-minimal:3.1.1

RUN apk update
RUN apk add --no-cache make mariadb-dev gcc g++ automake python3-dev


WORKDIR /srv

COPY ngram_cloud ./ngram_cloud
COPY setup.py Makefile run-requirements.txt ./

RUN make build-run

ENTRYPOINT ["make", "run"]