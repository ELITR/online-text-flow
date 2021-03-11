SHELL := /bin/bash

all: install

#T='/usr/bin/time --format="took %E"'
T=time
install:
	make clear
	pip uninstall online-text-flow -y ; python3 setup.py bdist_wheel ; pip install dist/online_text_flow-1.7.0-py3-none-any.whl
	make check


check:
	$T echo 100 101 events. | online-text-flow events de
	$T echo 100 101 events. | python3 elitr/onlinetextflow/events.py
	$T echo 100 101 events. | online-text-flow events de
	$T echo 100 101 events. | python3 elitr/onlinetextflow/events.py

editable:
	make clear
	pip install --editable .

develop:
	make clear
	python3 setup.py develop

clear:
	rm -rf elitr/onlinetextflow/__pycache__ elitr/__pycache__ elitr/otf_server/__pycache__ build/ dist online_text_flow.egg-info/ 
