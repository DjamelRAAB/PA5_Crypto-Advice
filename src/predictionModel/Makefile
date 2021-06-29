CURRENT_PATH := $(shell pwd)
SHELL := /bin/bash
VENV := .venv
BIN=$(CURRENT_PATH)/$(VENV)/bin/
IMAGE := cryptoadvice-prediction
REL := 0.0.1
IMAGE_VERSION := 3.8.1
TAG := $(REL)
DOCKER_REGISTRY := localhost
PA5_REGISTRY := gcr.io/pa5-crypto-advice2
IMAGE_VERSION := latest
FROM_IMAGE := $(IMAGE):$(IMAGE_VERSION)
APPLICATION_NAME := cryptoadvice-prediction
PORT := 5000

.PHONY: venv activate install run

venv:
	python -m venv $(CURRENT_PATH)/$(VENV)

activate: venv
	source $(BIN)activate

install: activate
	- mkdir -p $(CURRENT_PATH)/logs
	$(BIN)pip install -r $(CURRENT_PATH)/app/requirements.txt

run : install
	$(BIN)python app/main.py

build:
	docker build --rm=true -t $(DOCKER_REGISTRY)/$(IMAGE):$(TAG) .
	
run_container: build
	docker run -d --name $(APPLICATION_NAME) -p $(PORT):$(PORT) -v /home/raab/PA5/model/conf/:/conf -v /home/raab/PA5/model/models:/volume --expose $(PORT) -ti $(DOCKER_REGISTRY)/$(IMAGE):$(TAG)

tag: build
	docker tag $(DOCKER_REGISTRY)/$(IMAGE):$(TAG) $(PA5_REGISTRY)/$(IMAGE):$(IMAGE_VERSION)

push: tag
	gcloud docker -- push $(PA5_REGISTRY)/$(IMAGE):$(IMAGE_VERSION)

clean:
	docker rmi $(DOCKER_REGISTRY)/$(IMAGE):$(TAG)

auth:
	gcloud container clusters get-credentials cluster-pa5 --zone europe-west1-b
