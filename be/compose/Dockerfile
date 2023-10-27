FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY /requirements /requirements

RUN apk update && apk upgrade \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev mysql-client \
    && apk add --virtual build-deps \
    && pip install --upgrade pip \
    && pip install -r /requirements/production.txt \
    && apk del build-deps

COPY compose/entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh
RUN ln -s /usr/local/bin/entrypoint.sh / # backwards compat

COPY compose/wait-for /usr/local/bin/
RUN chmod +x /usr/local/bin/wait-for
RUN ln -s /usr/local/bin/wait-for / # backwards compat


WORKDIR /src
ADD . /src/

ENTRYPOINT ["/entrypoint.sh"]
