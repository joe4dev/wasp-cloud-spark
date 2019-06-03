all: run

install:
	pip install -r requirements.txt

run: compute

run_cloud:
	python run_cloud.py

run_cloud_log:
	python run_cloud.py | tee run_cloud.log

compute:
	python compute.py
