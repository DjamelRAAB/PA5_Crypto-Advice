FROM    python:3.8.1

ARG     PYTHON_ROOT_DIR="/opt/python"
RUN		mkdir -p ${PYTHON_ROOT_DIR}/myvenv
RUN mkdir /conf
RUN mkdir /data

WORKDIR /webApp

COPY ./webApp/ /webApp
COPY ./data/ /data
COPY ./conf/ /conf
COPY venv-entrypoint.sh /venv-entrypoint.sh

RUN pip install -r /webApp/requirements.txt \
    && chmod -R 755 /webApp \
    && chmod -R 755 /venv-entrypoint.sh\
    && chmod -R 755 /conf 

RUN mkdir /logs \
    && chmod -R 755 /logs 


ENTRYPOINT ["/venv-entrypoint.sh"]

