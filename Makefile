PYTHON=/usr/bin/env python 

test:
	cd t/ && $(PYTHON) testconfig.py
#	cd t/ && $(PYTHON) testmpd.py
	[ -d share ] && git submodule init && git submodule update && cd share && for prj in *; do if [ -d "$$prj" ]; then cd "$$prj"; [ -f Makefile ] && make test; cd ..;  fi; done

