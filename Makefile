build:
	pip3 install -r requirements.txt

test:
	flake8 --exclude ./lib/*
	python3 -m unittest tests/*.py

start:
	python3 -m rabbit_monitor
