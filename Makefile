build:
	pip3 install -r requirements.txt

dev:
	cd .. && pip3 uninstall -y sdx-common && pip3 install -I ./sdx-common
	pip3 install -r requirements.txt

test:
	pip3 install -r test_requirements.txt
	flake8 --exclude ./lib/*
	python -m pytest tests/test_rabbit_monitor.py

start:
	./startup.sh
