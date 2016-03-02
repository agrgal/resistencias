## Process this file with automake to produce Makefile.in
## Created by Anjuta


uidir = $(pkgdatadir)/ui
ui_DATA = resistencias.ui


## The main script
bin_SCRIPTS = resistencias.py

## Directory where .class files will be installed
resistenciasdir = $(pythondir)/resistencias


resistencias_PYTHON = \
	resistencias.py


EXTRA_DIST = $(ui_DATA)


# Remove ui directory on uninstall
uninstall-local:

	-rm -r $(uidir)

	-rm -r $(pkgdatadir)
