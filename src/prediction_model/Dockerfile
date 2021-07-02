FROM python:3.8
WORKDIR /app
COPY app/ /app

RUN pip install -r /app/requirements.txt \
    && chmod -R 755 /app 
RUN mkdir /volume \
    && mkdir /volume/models \
    && chmod -R 755 /volume
EXPOSE 8080
CMD ["/app/venv-entrypoint.sh"]