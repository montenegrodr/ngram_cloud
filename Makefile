DB_HOST     ?= 127.0.0.1
DB_PASSWD   ?=
DB_USER     ?= root
DB_NAME     ?= bigrams
REGISTRY    ?= montenegrodr
VERSION     ?= 0.1
REPOSITORY  ?= ngram_cloud

.PHONY: run
run:
	python ngram_cloud/run.py


.PHONY: build-run
build-run:
	pip install -r run-requirements.txt
	pip install -e .


.PHONY: build-image
build-image:
	docker build . -t $(REGISTRY)/$(REPOSITORY):${VERSION} \
	               -t $(REGISTRY)/$(REPOSITORY):latest


.PHONY: push-image
push-image:
	docker push $(REGISTRY)/$(REPOSITORY):${VERSION}
	docker push $(REGISTRY)/$(REPOSITORY):latest


kb.csv:
	gsutil cp gs://montenegrodr/kb.csv kb.csv


vocab.csv:
	gsutil cp gs://montenegrodr/vocab.csv vocab.csv
