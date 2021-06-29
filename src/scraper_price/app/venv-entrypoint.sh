#!/bin/bash
cd /

export project_id=pa5-crypto-advice2
export topic_id=trades-flow
export GOOGLE_APPLICATION_CREDENTIALS=/conf/key-file.json

python /app/price_getter.py