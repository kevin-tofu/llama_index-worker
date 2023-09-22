FROM python:3.10-slim-buster

WORKDIR /myapp
COPY ./ ./

RUN apt-get update -y
RUN apt-get upgrade -y

ENV POETRY_HOME=/opt/poetry
RUN curl -sSL https://install.python-poetry.org/  | python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false


RUN poetry install --no-root
ENV http_proxy=
ENV https_proxy=

EXPOSE 80

CMD ["poetry", "run", "python", "-m", "llama_index_server"]