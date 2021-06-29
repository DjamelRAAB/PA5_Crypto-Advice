FROM python:3.7
ARG     PYTHON_ROOT_DIR="/opt/python"

WORKDIR /app
COPY app/ /app

RUN pip install --no-cache-dir --upgrade pip \
    && pip install -r /app/requirements.txt \
    && chmod -R 755 /app 

