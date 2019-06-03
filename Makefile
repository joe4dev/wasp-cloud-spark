all: run

install:
	pip install -r requirements.txt

run: compute

run_cloud:
	python run_cloud.py

compute:
	python compute.py
