FROM    python:3.8.1

ARG     PYTHON_ROOT_DIR="/opt/python"
RUN		mkdir -p ${PYTHON_ROOT_DIR}/myvenv

WORKDIR /webApi

COPY webApi/ /webApi

RUN pip install -r /webApi/requirements.txt \
    && chmod -R 755 /webApi 

ENTRYPOINT ["/webApi/venv-entrypoint.sh"]

