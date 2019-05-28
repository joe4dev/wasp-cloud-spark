all: run

install:
	pip install -r requirements.txt

run: multiply

multiply:
	python multiply.py

import:
	python import.py