SHELL := /bin/bash

all: install

T=time
install:
	make clear
	python3 setup.py bdist_wheel ; pip install dist/online_text_flow-1.7.0-py3-none-any.whl
	make check

# the very first run after installation might be slower than the following, don't count it. Optimal is when the two options take the same time, around 300ms
check:
	$T echo 100 101 events. | online-text-flow events de
	$T echo 100 101 events. | python3 elitr/onlinetextflow/events.py de
	$T echo 100 101 events. | online-text-flow events de
	$T echo 100 101 events. | python3 elitr/onlinetextflow/events.py de

# for comparison only
editable:
	make clear
	pip install --editable .
	make check

# for comparison only
develop:
	make clear
	python3 setup.py develop
	make check

clear:
	rm -rf elitr/onlinetextflow/__pycache__ elitr/__pycache__ elitr/otf_server/__pycache__ build/ dist online_text_flow.egg-info/
	pip uninstall online-text-flow -y 
