build:
	pip3 install --require-hashes -r requirements.txt

test:
	pip3 install -r test_requirements.txt
	flake8 --exclude ./lib/*
	python -m pytest tests/test_rabbit_monitor.py

start:
	./startup.sh

