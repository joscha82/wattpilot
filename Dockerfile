ARG baseimage=python:3-slim
FROM ${baseimage}

WORKDIR /src

COPY . /src
COPY ./entrypoint.sh /

RUN pip install .

ENTRYPOINT [ "/entrypoint.sh" ]
