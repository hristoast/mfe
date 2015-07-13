BUILD = ./setup.py build --force
BDIST = ./setup.py bdist
CLEAN1 = ./setup.py clean
CLEAN2 = find . -name "*~" -exec /bin/rm -f {} \;
CLEAN3 = find . -name "*pyc" -exec /bin/rm -f {} \;
CLEAN4 = /bin/rm -fr build build-stamp dist mfe.egg-info debian/files \
	debian/mednafenfe debian/mednafenfe.debhelper.log debian/mednafenfe.substvars
DEB = fakeroot debian/rules binary
INSTALL = ./setup.py install --force --optimize 2
SDIST = ./setup.py sdist
UNINSTALL = /bin/rm -f /usr/local/lib/python2.7/dist-packages/mfe-*.egg \
	/usr/local/bin/mfe

.DEFAULT_GOAL := build
.PHONY: all

all: bdist build clean deb i install sdist uninstall

bdist:
	$(BDIST)

build:
	$(BUILD)

clean:
	$(CLEAN1) && $(CLEAN2) && $(CLEAN3) && $(CLEAN4)

deb:
	$(DEB)

i:
	$(INSTALL) && $(CLEAN1) && $(CLEAN2) && $(CLEAN3) && $(CLEAN4)

install:
	$(INSTALL)

sdist:
	$(SDIST)

uninstall:
	$(UNINSTALL)
