FROM ubuntu
RUN mkdir /conf
WORKDIR /app
COPY app/ /app
RUN apt update && apt -y install openjdk-8-jre-headless && apt -y install python3-pip && pip install -r /app/requirements.txt && chmod -R 755 /app 
ARG     PYTHON_ROOT_DIR="/opt/python"
ENTRYPOINT ["/app/venv-entrypoint.sh"]
