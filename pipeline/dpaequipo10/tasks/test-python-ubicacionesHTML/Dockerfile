FROM dpa/python:0.2

ENV PROJECT_NAME dpaequipo10

## Copiamos los scripts
ADD . /${PROJECT_NAME}/
WORKDIR /${PROJECT_NAME}

RUN mkdir /${PROJECT_NAME}/data
RUN pip install -r /dpaequipo10/requirements.txt

ENTRYPOINT [ "python", "/dpaequipo10/recomendacion.py" ]

