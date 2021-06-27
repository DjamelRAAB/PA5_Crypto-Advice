FROM python:3.7
RUN pip install --no-cache-dir --upgrade pip
COPY . /app
WORKDIR /app
ENV project_id=pa5-crypto-advice
ENV topic_id=trades-flow
ENV GOOGLE_APPLICATION_CREDENTIALS=./key-file.json
RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["python", "./price_getter.py"]