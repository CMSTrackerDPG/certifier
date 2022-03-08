Testing
=======

Run unit tests
--------------

The unit tests (without selenium/ functional tests) can be run using
``pytest``:

::

    pytest --ignore tests/selenium

::

    ============================= test session starts =============================
    platform win32 -- Python 3.6.5, pytest-3.7.1, py-1.5.4, pluggy-0.7.1
    Django settings: dqmsite.test_settings (from ini file)
    rootdir: C:\Users\keepingitsecret\workspace\CERN\certifier, inifile: pytest.ini
    plugins: mock-1.10.0, django-3.3.3, cov-2.5.1
    collected 118 items                                                            

    runregistry\tests.py ....                                                [  3%]
    tests\certhelper\test_dynamic_preferences.py .                           [  4%]
    tests\certhelper\test_forms.py .                                         [  5%]
    tests\certhelper\test_manager.py .......                                 [ 11%]
    tests\certhelper\test_models.py ..................                       [ 26%]
    tests\certhelper\test_myfilters.py ......                                [ 31%]
    tests\certhelper\test_query.py ........................                  [ 51%]
    tests\certhelper\test_shiftleaderreport.py ......                        [ 56%]
    tests\certhelper\test_signals.py ....                                    [ 60%]
    tests\certhelper\test_summaryreport.py .                                 [ 61%]
    tests\certhelper\test_utilities.py ..................                    [ 76%]
    tests\certhelper\test_views.py ..................                        [ 91%]
    tests\certhelper\client\test_login.py ..                                 [ 93%]
    tests\certhelper\client\test_urls.py ........                            [100%]

    ========================= 118 passed in 14.16 seconds =========================.p

Selenium
~~~~~~~~

If the selenium tests should also be run one needs at least FireFox ESR
and has to download the geckodriver which can be found on the *mozilla*
GitHub repository: https://github.com/mozilla/geckodriver/releases

It should be kept in mind that selenium tests require a lot more time to
execute since they run actual instances of FireFox.

Geckodriver
^^^^^^^^^^^

**Linux**:

::

    wget https://github.com/mozilla/geckodriver/releases/download/v0.21.0/geckodriver-v0.21.0-linux64.tar
    .gz
    mkdir geckodriver
    tar -xzf geckodriver-v0.21.0-linux64.tar.gz -C geckodriver
    export PATH=$PATH:$PWD/geckodriver

**Windows**:

Download and extract

https://github.com/mozilla/geckodriver/releases/download/v0.21.0/geckodriver-v0.21.0-win64.zip

and export geckodriver.exe to the PATH environment variable

**Arch Linux**

On Arch Linux all that has to be done is:

::

    sudo pacman -S geckodriver

Run Selenium tests
^^^^^^^^^^^^^^^^^^

After installing the geckodriver it should be possible to run the
selenium tests as well:

::

    pytest tests/selenium

To see what is happening during the tests the ``--headless`` parameter
in ``conftest.py`` can be commented out temporarily.

Write unit tests
----------------

https://docs.pytest.org/en/latest/

Whenever functionality is added a corresponding unit test should be
written to ensure correctness and robustness against future changes.

A test function should be defined anywhere in the *tests* module for
example *tests/certhelper/test\_utilities.py* Any function in that file
that starts with *test\_* is considered as a test function.

::

    def test_my_new_function():
      assert "My expected output" == my_new_function()

pytest automatically detects *test\_my\_new\_function* and includes it
in the testing procedure.

Configure Travis CI
-------------------

Travis CI sets up a testing environment according to the ``.travis.yml``
file. This file contains the python version, the Django version and the
test commands.

.. code:: yaml

	addons: 
	  apt: 
	    packages: 
	      - postgresql-12
	      - postgresql-client-12
	  firefox: latest
	  postgresql: "12"
	after_success: 
	  - codecov
	before_install: 
	  - "wget https://github.com/mozilla/geckodriver/releases/download/v0.21.0/geckodriver-v0.21.0-linux64.tar.gz"
	  - "mkdir geckodriver"
	  - "tar -xzf geckodriver-v0.21.0-linux64.tar.gz -C geckodriver"
	  - "export PATH=$PATH:$PWD/geckodriver"
	before_script: 
	  - "psql -c \"create database testdb;\" -U travis"
	env: 
	  global: 
	    - PGUSER=travis
	    - PGVER=12
	    - PGPORT=5433
	install: 
	  - "pip install --upgrade -r requirements.txt"
	  - "pip install --upgrade pytest pytest-django pytest-cov codecov mixer selenium"
	language: python
	python: 
	  - "3.8"
	script: 
	  - "PYTHONWARNINGS=all travis_retry pytest --ds=dqmhelper.test_ci_settings --cov=. --ignore certifier/tests/test_certifier_views.py --ignore oms/tests/test_oms_utils.py"
	

.. note::

   Certifier views tests and OMS utils tests have been disabled due to OMS being unreachable from outside CERN.
		
In Travis CI following environment variables have to be set:

.. code:: bash

		  DJANGO_DATABASE_ENGINE django.db.backends.postgresql_psycopg2
		  DJANGO_DATABASE_HOST localhost
		  DJANGO_DATABASE_NAME testdb
		  DJANGO_DATABASE_USER postgres
		  DJANGO_DEBUG True
		  DJANGO_SECRET_KEY dbwqabxpc2denpefq4hgfhijkl0usxi6d3tm4jk609zo85dqrw
		  OMS_CLIENT_ID <secret>
		  OMS_CLIENT_SECRET <secret>
		  PGPORT 5543
		  POSTGRES_DB test_postgres_db
		  POSTGRES_USER travis

Coverage Reports
----------------

If the all tests pass a coverage report is automatically uploaded to
codecov and can be viewed on:

-  https://codecov.io/gh/CMSTrackerDPG/certifier

The Report shows which files need further testing and how good the
overall test coverage is.
