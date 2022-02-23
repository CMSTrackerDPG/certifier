Development
===========

Prerequisites
-------------

-  git
-  python3
-  Django Tutorial

In case one wants to improve the Certhelper project, the following
steps are necessary:

-  Install Python version 3.7 or 3.8 (recommended 3.8)
-  Setup a virtual environment
-  Install requirements packages

Installing Python
~~~~~~~~~~~~~~~~~

Python can be downloaded on https://www.python.org/ or via package
managers on a linux distribution. Python (3.4+) should come bundled with
pip and virtualenv, so everything necessary should be ready to use.

**Windows**:

https://www.python.org/downloads/windows/

**Ubuntu or Ubuntu based distributions**:

.. code:: bash

    sudo apt install python3

**Arch Linux or Arch based distributions:**

Use an `AUR helper`_ like `yay`_ and install `python36`_

.. code:: bash

   yay -S python/pacman -S python

If you do not want to use an AUR helper you can install Python 3.6
`manually`_ with:

.. code:: bash

   git clone https://aur.archlinux.org/packages/python-git/
   cd python-git
   makepkg -si

.. _AUR helper: https://wiki.archlinux.org/index.php/AUR_helpers
.. _yay: https://github.com/Jguer/yay
.. _python36: https://aur.archlinux.org/packages/python36/
.. _manually: https://wiki.archlinux.org/index.php/Arch_User_Repository#Installing_packages

Checking Python Version
^^^^^^^^^^^^^^^^^^^^^^^

The project requires the python version 3.7 or 3.8. To ensure that the
correct python version is configured the ``python3 --version`` command
be used.

.. code:: bash

    python3 --version

.. code:: bash

    Python 3.8.1

Cloning the Project
~~~~~~~~~~~~~~~~~~~

.. code:: bash

    git clone https://github.com/CMSTrackerDPG/certifier
    cd certifier

Setup Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~

It is recommended to develop in a isolated virtual environment to ensure
the correct package versions and avoid conflicts with other projects.

.. code:: bash

    python -m venv venv
    source venv/bin/activate

After executing these commands a ``(venv)`` should precede the command
line.

Installing Requirements
~~~~~~~~~~~~~~~~~~~~~~~

The requirements files contain every python package that is necessary in
order to deploy the website. Each line consists of one single python
package which can be a link to a GitHub repository or the package name
and version which are registered in the `pypi <https://pypi.org/>`__
repository. Since there are additional packages used exclusively for
testing, which are not necessary in the production environment an
additional testing-requirements.txt file exists.

.. code:: bash

    pip install -r requirements.txt
    pip install -r testing-requirements.txt

Configure database connection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The credentials are read from environment variables which have to be set
accordingly.

In case one wants to work with a local SQLDatabase while developing then
following environment variables should be exported.

.. code:: bash

    DJANGO_DATABASE_ENGINE=django.db.backends.sqlite3
    DJANGO_DEBUG=True
    DJANGO_DATABASE_NAME=db.sqlite3
    DJANGO_SECRET_KEY=(%g65bg+&9rbnt+h&txlxw$+lkq=g=yrp!6@v+7@&$a%9^yt-!

In case one wants to work with the development database (used in
dev-certhelper.web.cern.ch) following environment variables have to be
exported:

.. code:: bash

    DJANGO_DATABASE_ENGINE=django.db.backends.postgresql_psycopg2
    DJANGO_DATABASE_NAME=<your database name>
    DJANGO_DATABASE_USER=<your username>
    DJANGO_DATABASE_PASSWORD=<your password>
    DJANGO_DATABASE_HOST=<your database host name>
    DJANGO_DATABASE_PORT=6600
    DJANGO_DEBUG=True
    DJANGO_SECRET_KEY=p*3y)jem=g8gj)6g_qy_6opfrwg2px^+((56y02l^pqz#!gitz

Alternatively a ``.env`` file with the content above can be created.

The DJANGO\_SECRET\_KEY key stated here serve just as examples and
should not be used anywhere outside of the local development. For a
production environment, the secret key should never be visible to the
outside world and can be generated with tools like:
https://www.miniwebtool.com/django-secret-key-generator/

These environment variables are read in the settings.py module which
configures the database.

Load sample data
~~~~~~~~~~~~~~~~
When running the project from a development database as was setup above, you will probably
need some data to play with. This is done via `Django fixtures <https://docs.djangoproject.com/en/4.0/howto/initial-data/>`__,
which are written by hand in the ``certifier.yaml`` file in ``certifier/fixtures``. 

To load them, activate the virtual environment and run:

.. code:: bash
		  
   python manage.py loaddata certifier.yaml

Alternatively, ``factory_boy`` can be used, by calling the custom management command ``fake_data``.
For example, to populate the database with a default superuser and some
fake data, run the following:

.. code:: bash

		  python manage.py fake_data


		  
Packages
--------

The website uses following python packages which are automatically
installed on deployment:

-  **django**: The most important package. The whole website is built
   with it.
-  **django-allauth**: Implements the CERN OAuth2 SSO Provider
-  **django-bootstrap3**: Easy Integration of the bootstrap frontend
-  **django-categories**: Easy creation of Categories (and
   Subcategories)
-  **django-ckeditor**: HTML Text editor to edit Checklist items
-  **django-dynamic-preferences**: Easily create preferences in the
   Admin Settings. Used to configure the shift leader popup message.
-  **django-filter**: Filter the certified runs
-  **django-nested-admin**: Makes it possible to inline multiple
   hierarchies in the admin panel. Used to inline checklist items in
   checklist groups in checklists
-  **django-tables2**: Display Tables
-  **djangorestframework**: Toolkit for building Web APIs
-  **django-widget-tweaks**: Convenient Template Tags
-  **django-extensions**: Collection of custom extensions for the Django Framework.
-  **terminaltables**: Used to generate the shifters daily summary
   report
-  **whitenoise**: static files provider. Necessary for deploying the
   website without debug mode enabled.
-  **asgiref**: This package includes the ASGI base libraries
-  **cernrequests**: Enables easy requests to cern APIs (https://pypi.org/project/cernrequests/)
-  **certifi**: Collection of Root Certificates
-  **channels_redis**: An ASGI channel layer that uses Redis as its backing store.
-  **psycopg2-binary**: PostgreSQL database adapter for the Python.
-  **python-decouple**: Used to sepparate config settings from code
-  **requests**: Enables requests to the web
-  **daphne**: Daphne is a HTTP, HTTP2 and WebSocket protocol server for ASGI and ASGI-HTTP, developed to power Django Channels.
-  **numpy**: Used for analisys of data
-  **runregcrawlr**: Tool used to crawl a few runs from the CERN CMS Run Registry.
-  **dqmcrawlr**: Tool used to crawl a few plots from the CMS Data Quality Monitor web tool.
-  **wbmcrawlr**: Retrieve data from the CMS Online Monitoring System and CMS Web Based Monitoring
-  **pandas**: Data analysis and manipulation tool used for generating the charts
-  **paramiko**: Tools used for sshing into the VM
-  **seaborn**: Data visualization library based on matplotlib.
-  **scipy**: Library used for processing data
-  **scikit-learn**: Machine learning library for Python
-  **umap-learn**: Uniform Manifold Aproximation and Projection Algorithm used for clustering the runs
-  **runregitry**: Tool for using the runregistry API
-  **apscheduler**: Scheduling library for Python code


The *requirements.txt* should always be updated when adding new
packages.

Testing Packages
~~~~~~~~~~~~~~~~

-  **pytest-cov**: Create coverage reports when running pytest
-  **pytest-django**: Easy Django integration for pytest
-  **mixer**: Fast and convenient way of creating model instances for
   unit tests
-  **selenium**: Necessary to run functional tests (with firefox)
- **codecov**: Generate code test coverage raport

All packages that are used in a testing environment should be stated in
the *testing-requirements.txt* file.

Branches
--------

Master
~~~~~~

The master branch is the production branch. It is used to deploy to
certhelper.web.cern.ch via OpenShift. This branch should only contain
stable and tested code. Changes should never be made directly in the
master branch.

Develop
~~~~~~~

Development branch to test new features before deploying it to the
production website. Commits in the development branch are automatically
deployed to dev-certhelper.web.cern.ch every time changes are pushed to
GitHub.

.. code:: bash

    git push origin develop

When a develop branch is thoroughly tested and ready for production then
it can be merged into the master branch:

.. code:: bash

    git checkout master
    git merge develop
    git push origin master

Feature branches
~~~~~~~~~~~~~~~~

When developing new features, a new feature branch should be created.

.. code:: bash

    git checkout -b feature-mynewfeature develop

After the new changes have been committed, they can be merged back into
the develop branch.

.. code:: bash

    git checkout develop
    git merge my-new-feature
    git branch -d my-new-feature
    git push origin develop

The push to the development branch automatically triggers the unit tests
at Travis CI.

Django Tutorial
---------------

It is recommended to the finish the Django tutorial at
https://docs.djangoproject.com/en/1.11/intro/tutorial01/ before doing
any changes at the website. The tutorial is beneficial and gives a big
overview of how Django works.

Style Guide
-----------

To improve readability of the source code, a consistent style guide
should be used. The python files are all formatted with the Black Code
Formatter

The black code formatter can be installed on the local machine via

.. code:: bash

    pip install black

The project files can then be reformated with

.. code:: bash

    black [FILES...]


Run the website locally
-----------------------

.. code:: bash

    python manage.py migrate
    python manage.py collectstatic


.. code:: bash

    python manage.py runserver


Migrations
----------

Whenever you make changes to ``models.py`` you should run the ``makemigrations`` command.

.. code:: bash

    python manage.py makemigrations

The migrations can then be applied with:

.. code:: bash

    python manage.py migrate


Documentation
-------------

If you want to contribute to the documentation that is hosted at
`readthedocs`_ you should get familiar with Spinx and reStructedText

-  https://docs.readthedocs.io/en/latest/intro/getting-started-with-sphinx.html
-  http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html

To generate a local documentation these commands have to be run:

.. code:: bash

   pip install sphinx
   cd docs
   make html

After that you can open the ``index.html`` file that is located at
``docs/_build/html``.

.. _readthedocs: https://tkdqmdoctor.readthedocs.io/en/latest/
