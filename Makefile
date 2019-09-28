DB_HOST   ?= localhost
DB_PASSWD ?=
DB_USER   ?= root
DB_NAME   ?= bigrams


.PHONY: run
run:
	python ngram_cloud/run.py


.PHONY: build-run
build-run:
	pip install -r run-requirements.txt
	pip install -e .


kb.csv:
	gsutil cp gs://montenegrodr/kb.csv kb.csv


vocab.csv:
	gsutil cp gs://montenegrodr/vocab.csv vocab.csv
