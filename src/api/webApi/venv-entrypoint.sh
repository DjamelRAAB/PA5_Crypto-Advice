#!/bin/bash
cd /
export GOOGLE_APPLICATION_CREDENTIALS=/conf/.key-file.json
uvicorn api:webApi --app-dir /app --host '0.0.0.0' --port 5000