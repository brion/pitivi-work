
# Don't try to use wildcards to replace the list of tests below.
# http://www.gnu.org/software/automake/manual/automake.html#Wildcards
# Keep this list sorted!
tests =	test_basic.py \
	test_common.py \
	test_log.py \
	test_misc.py \
	test_prefs.py \
	test_preset.py \
	test_project.py \
	test_projectmanager.py \
	test_projectsettings.py \
	test_signallable.py \
	test_system_gnome.py \
	test_system.py \
	test_timeline_undo.py \
	test_undo.py \
	test_utils.py \
	test_widgets.py
# Keep the list sorted!

EXTRA_DIST = \
	__init__.py \
	common.py \
	runtests.py \
	$(tests)

clean-local:
	rm -rf *.pyc *.pyo

check-local:
	@PYTHONPATH=$(top_srcdir):$(PYTHONPATH) $(PYTHON) $(srcdir)/runtests.py \
		$(tests)

%.check: %
	@PYTHONPATH=$(top_srcdir):$(PYTHONPATH) $(PYTHON) $(srcdir)/runtests.py $*
