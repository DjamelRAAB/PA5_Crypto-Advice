FROM    python:3.8.1

ARG     PYTHON_ROOT_DIR="/opt/python"
RUN		mkdir -p ${PYTHON_ROOT_DIR}/myvenv

WORKDIR /app

COPY app/ /app

RUN pip install -r /app/requirements.txt \
    && chmod -R 755 /app 

ENTRYPOINT ["/app/venv-entrypoint.sh"]

