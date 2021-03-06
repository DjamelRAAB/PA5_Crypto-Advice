CURRENT_PATH := $(shell pwd)
SHELL := /bin/bash
VENV := .venv
BIN=$(CURRENT_PATH)/$(VENV)/bin/
IMAGE := cryptoadvice-api
REL := 0.0.1
IMAGE_VERSION := 3.8.1
TAG := $(REL)
DOCKER_REGISTRY := localhost
PA5_REGISTRY := gcr.io/pa5-crypto-advice2
IMAGE_VERSION := latest
FROM_IMAGE := $(IMAGE):$(IMAGE_VERSION)
APPLICATION_NAME := cryptoadvice-api 
API_PATH := cryptoadvice/api 
PORT := 5000

.PHONY: venv activate install run

venv:
	python -m venv $(CURRENT_PATH)/$(VENV)

activate: venv
	source $(BIN)activate

install: activate
	- mkdir -p $(CURRENT_PATH)/logs
	$(BIN)pip install -r $(CURRENT_PATH)/webApi/requirements.txt

run : install
	$(BIN)uvicorn api:webApi --reload --app-dir webApi

build:
	docker build --rm=true -t $(DOCKER_REGISTRY)/$(IMAGE):$(TAG) .
	
run_container: build
	docker run -d --name $(APPLICATION_NAME) -p $(PORT):$(PORT) -v /home/raab/PA5/api/conf/:/conf --expose $(PORT) -ti  $(DOCKER_REGISTRY)/$(IMAGE):$(TAG)

tag: build
	docker tag $(DOCKER_REGISTRY)/$(IMAGE):$(TAG) $(PA5_REGISTRY)/$(IMAGE):$(IMAGE_VERSION)

push: tag
	gcloud docker -- push $(PA5_REGISTRY)/$(IMAGE):$(IMAGE_VERSION)

clean:
	docker rmi $(DOCKER_REGISTRY)/$(IMAGE):$(TAG)

auth:
	gcloud container clusters get-credentials cluster-pa5 --zone europe-west1-b
