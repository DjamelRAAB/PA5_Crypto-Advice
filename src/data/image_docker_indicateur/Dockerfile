FROM ubuntu
COPY . /app
WORKDIR /app
ENV project_id=pa5-crypto-advice
ENV topic_id=trades-flow
ENV API_KEY=1sDGH1SMX74Z1deZFm32inPjYId
ENV GOOGLE_APPLICATION_CREDENTIALS=./key-file.json
RUN apt update && apt -y install openjdk-8-jre-headless && apt -y install python3-pip && pip install -r requirements.txt
CMD python3 ./indicateur_data.py