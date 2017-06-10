FROM dpa/python:0.2

ENV PROJECT_NAME dpaequipo10

## Copiamos los scripts
ADD . /${PROJECT_NAME}/
WORKDIR /${PROJECT_NAME}

RUN mkdir /${PROJECT_NAME}/data

ENTRYPOINT [ "python", "/dpaequipo10/DBSCAN.py" ]

