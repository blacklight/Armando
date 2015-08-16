PYTHON=/usr/bin/env python 

test:
	cd t/ && $(PYTHON) testconfig.py
	cd t/ && $(PYTHON) testmpd.py

