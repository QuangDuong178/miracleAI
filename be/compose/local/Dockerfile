FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY /requirements /requirements

#RUN apk update && apk upgrade \
#    && apk add --virtual build-deps gcc python3-dev musl-dev libffi-dev libpq-dev g++ \
#    && apk add --no-cache mariadb-dev mysql-client \
#    && python -m pip install --upgrade pip \
#    && pip install -r /requirements/local.txt \
#    && apk del build-deps

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # mysql dependencies
  && apt-get install -y default-libmysqlclient-dev libmariadb-dev pkg-config netcat \
  && python -m pip install --upgrade pip \
  && pip install -r /requirements/local.txt \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*


COPY compose/entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh
RUN ln -s /usr/local/bin/entrypoint.sh / # backwards compat

COPY compose/wait-for /usr/local/bin/
RUN chmod +x /usr/local/bin/wait-for
RUN ln -s /usr/local/bin/wait-for / # backwards compat


WORKDIR /src
ADD . /src/

ENTRYPOINT ["/entrypoint.sh"]
