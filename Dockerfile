FROM alpine:3.15 as builder

RUN apk add --no-cache \
        python3 \
        py3-pip

RUN pip install --no-cache-dir \
        pipenv \
        setuptools \
        wheel

WORKDIR "/etc/hashmaps"
COPY Pipfile ./
COPY Pipfile.lock ./

RUN pipenv install --clear \
                   --deploy \
                   --system \
                   --verbose

FROM alpine:3.15

RUN apk add --no-cache \
        bash \
        python3 \
        su-exec \
        uwsgi \
        uwsgi-python3 \
    \
 && ln -s /usr/bin/python3 /usr/local/bin/python \
 && adduser -h /var/www \
            -s /bin/bash \
            -u 82 \
            -G www-data \
            -D \
        \
        www-data

COPY --from=builder /usr/lib/python3.9/site-packages /usr/lib/python3.9/site-packages

ARG SOURCE_DIR="/opt/hashmaps"
ARG DATA_VOLUME="/var/lib/hashmaps"

WORKDIR "${SOURCE_DIR}"
COPY src/ ./
COPY entrypoint.sh /

ENV SOURCE_DIR="${SOURCE_DIR}"
ENV DATA_VOLUME="${DATA_VOLUME}"
ENV TMPDIR="${DATA_VOLUME}/tmp"

ENV DEBUG=""
ENV SECRET_KEY=""

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uwsgi"]

EXPOSE 8000
VOLUME ["${DATA_VOLUME}"]
