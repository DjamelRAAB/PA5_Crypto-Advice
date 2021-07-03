#!/bin/bash
cd /

export project_id=pa5-crypto-advice2
export topic_id=metrics-flow
export GOOGLE_APPLICATION_CREDENTIALS=/conf/.key-file.json
export API_KEY=1sDGH1SMX74Z1deZFm32inPjYId
/usr/bin/python3.8 /app/indicateur_data.py
