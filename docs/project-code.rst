Project Structure
=================

Basically, the project has the following folder structure:

::

    certifier
    │   manage.py
    │   pytest.ini
    │   requirements.txt
    │   testing-requirements.txt
    │
    ├───addrefrun
    │   │   admin.py
    │   │   apps.py
    │   │   urls.py
    │   │   views.py
    │   │
    │   ├───migrations
    │   ├───templates
    │   └───tests
    │
    ├───analysis
    │   │   admin.py
    │   │   analyse.py
    │   │   apps.py
    │   │   models.py
    │   │   urls.py
    │   │   views.py
    │   │
    │   ├───migrations
    │   ├───templates
    │   ├───tests
    │   └───jobs
    │
    ├───certifier
    │   │   admin.py
    │   │   apps.py
    │   │   forms.py
    │   │   manager.py
    │   │   models.py
    │   │   urls.py
    │   │   views.py
    │   │
    │   ├───migrations
    │   ├───static
    │   ├───templates
    │   ├───templatetags
    │   ├───tests
    │   └───utilities
    │
    ├───checklists
    │   │   admin.py
    │   │   apps.py
    │   │   forms.py
    │   │   models.py
    │   │   urls.py
    │   │   views.py
    │   │
    │   ├───migrations
    │   ├───static
    │   ├───templates
    │   ├───templatetags
    │   └───tests
    │
    ├───delete
    │   │   admin.py
    │   │   apps.py
    │   │   manager.py
    │   │   models.py
    │   │   query.py
    │   │   urls.py
    │   │   views.py
    │   │
    │   ├───migrations
    │   ├───templates
    │   └───tests
    │
    ├───dqmgui
    │   │   apps.py
    │   │   models.py
    │   │   tests.py
    │   │
    │   └───migrations
    │
    ├───dqmhelper
    │       asgi.py
    │       routing.py
    │       settings.py
    │       urls.py
    │       wsgi.py
    │
    ├───home
    │   │   admin.py
    │   │   apps.py
    │   │   models.py
    │   │   tests.py
    │   │   urls.py
    │   │   views.py
    │   │
    │   ├───migrations
    │   ├───static
    │   └───templates
    │
    ├───listruns
    │   │   admin.py
    │   │   apps.py
    │   │   filters.py
    │   │   urls.py
    │   │   views.py
    │   │
    │   ├───migrations
    │   ├───static
    │   ├───templates
    │   ├───tests
    │   └───utilities
    │
    ├───oms
    │   │   admin.py
    │   │   apps.py
    │   │   models.py
    │   │   utils.py
    │   │
    │   ├───migrations
    │   └───tests
    │
    ├───openruns
    │   │   admin.py
    │   │   apps.py
    │   │   models.py
    │   │   tests.py
    │   │   urls.py
    │   │   utilities.py
    │   │   views.py
    │   │
    │   ├───migrations
    │   └───templates
    │
    ├───plot
    │   │   admin.py
    │   │   apps.py
    │   │   models.py
    │   │   urls.py
    │   │   views.py
    │   │
    │   ├───migrations
    │   ├───templates
    │   └───tests
    │
    ├───restore
    │   │   admin.py
    │   │   apps.py
    │   │   models.py
    │   │   urls.py
    │   │   views.py
    │   │
    │   ├───migrations
    │   ├───templates
    │   └───tests
    │
    ├───runregistryapp
    │   │   apps.py
    │   │   client.py
    │   │   utilities.py
    │   │
    │   ├───migrations
    │   └───tests
    │
    ├───shiftleader
    │   │   apps.py
    │   │   filters.py
    │   │   query.py
    │   │   urls.py
    │   │   views.py
    │   │
    │   ├───migrations
    │   ├───static
    │   ├───templates
    │   ├───templatetags
    │   ├───tests
    │   └───utilities
    │
    ├───summary
    │   │   admin.py
    │   │   apps.py
    │   │   models.py
    │   │   urls.py
    │   │   views.py
    │   │
    │   ├───migrations
    │   ├───templates
    │   ├───tests
    │   └───utilities
    │
    ├───tables
    │   │   apps.py
    │   │   tables.py
    │   │
    │   ├───migrations
    │   └───utilities
    │
    ├───templates
    │   └───dqmhelper
    │
    ├───trackermaps
    │   │   admin.py
    │   │   apps.py
    │   │   models.py
    │   │   output_socket.py
    │   │   routing.py
    │   │   tests.py
    │   │   urls.py
    │   │   views.py
    │   │
    │   ├───migrations
    │   └───templates
    │
    └───users
        │   admin.py
        │   apps.py
        │   models.py
        │   signals.py
        │   urls.py
        │   views.py
        │
        ├───migrations
        ├───static
        ├───templates
        ├───tests
        └───utilities

addrefrun
---------

``addrefrun`` is Django application used for adding a new reference run. Only the shiftleader has access to it.

analysis
--------

The ``analysis`` application is used for everything from retrieving data to applying a couple of machine learning algorithms and showing it on a series of charts. Still under development.

certifier
---------

In the ``certifier`` application is where the whole process of filling in the data for the certification is happening. It consists of a form that is mostly self filled. It still requires a couple of entries from the user, but they are kept at a minimum.

checklists
----------

The ``checklists`` application contains all the checklists the shifters have to go over and tick to be sure they cover the whole process of certification and not forget anything while certifying the run.

delete
------

The ``delete`` application is meant to hold the delete strategy of the tool, therefore anything related to deleteing an entry in a table is found here.

dqmhelper
---------

``dqmhelper`` could be seen as the "main" of the Certhelper. Here lies all the settings needed to run the tool. This is where all the applications are linked together.

home
----

The ``home`` application is as the name implies, the one responsible for the home page, what the user first sees when he/she accessed the tool. It consists of tiles that take you to the functionalities of the site.

listruns
--------

``listruns`` is where the shifter or shiftleader can see a table that contains his/her certified runs. This is showing by default the runs from the current day.

oms
---

The ``oms`` application is the one responsible with getting the data for the runs from the CMS OMS. This is further used for automatically filling the certification form.

openruns
--------

``openruns`` is the application where the shifter will first access for certifying a run. Here the shifter can either collect all the openruns he/she has to certify or choose a run number and a type to directly certify that run.

restore
-------

The shifter is able to delete certification, but those are not fully deleted, the shiftleader is the only one capable of fully deleting the certifications. That is the purpose of the ``restore`` application, if for example a certification is deleted by mistake by the shifter or for some reason it shouldn't have been deleted, the shiftleader can restore it. Here lies all the code related to this process.

runregistryapp
--------------

The ``runregistryapp`` is used for getting the data from the runregistry and comparing it with the one in the certification helper.

shiftleader
-----------

The ``shiftleader`` application contains the shiftleader tools, it's the code behind what can be seen in the Shift Leader Report page.

summary
-------

This application is responsible for the creation of the Daily Shift Report, needed by the shifter.

tables
------

There are a couple of tables across the site and all of them can be found here.

templates
---------

This contains the main templates of the site, on which every page is based on.

trackermaps
-----------

The ``trackermaps`` application is where the shiftleader can generate new trackermaps to be used in the certification process.

users
-----

In order to limit access to only the authorized user, the ``users`` application is responsible for categorizing the users accouring to they belonging to different cern groups.

tests
-----

The ``tests`` module in each application is dedicated to unit tests. They can be executed
locally via ``pytest`` or automatically via Travis CI when pushing a
branch to GitHub. A detailed description about testing can be found in
chapter Testing.

static
------

The ``static`` folder consists of static files like javascript files,
css files and images. This folder together with static files from other
applications will be
`collected <https://docs.djangoproject.com/en/1.11/ref/contrib/staticfiles/>`__
and then served by the
`WhiteNoise <http://whitenoise.evans.io/en/stable/>`__ middleware when
deploying to production.

urls.py
~~~~~~~

https://docs.djangoproject.com/en/1.11/topics/http/urls/

Every time a new page is added or the path of an existing page updated,
changes to ``urls.py`` have to be made. An excerpt of this file from the
website looks like this:

.. code:: python

    urlpatterns = [
        url(r'^$', views.listruns, name='list'),
        url(r'^shiftleader/$', views.shiftleader_view, name='shiftleader'),
        url(r'^summary/$', views.summaryView, name='summary'),
        url(r'^create/$', views.CreateRun.as_view(), name='create'),

        url(r'^(?P<pk>[0-9]+)/update/$', views.UpdateRun.as_view(), name='update'),
        url(r'^(?P<pk>[0-9]+)/delete/$', views.DeleteRun.as_view(), name='delete'),
        # ...
    ]

``urlpatterns`` is a list of URLs which consist of the URL path
expressed in regular expressions, the view function which is called when
visiting the URL and a unique name for easy referral.

The views are implemented in ``views.py`` and can be either function
based views or class-based views. In the example above the view
``shiftleader_view`` is a function based view and
\`\`\`CreateRun\`\`\`\`is a class-based view which can be easily found
out by the python naming convention. Function names should always be
lowercase with an underscore as word separator and class names should
always start with a capital letter with the CamelCase naming convention.

If the view is a class-based view then additionally the ``.as_view()``
method of that class has to be called in the second url parameter.

The first view that is called when a user visits
https://certhelper.web.cern.ch/ is ``home.views.home`` as it is the only
pattern in the urlpatterns list that matches the url: ``/``

views.py
~~~~~~~~

https://docs.djangoproject.com/en/1.11/topics/http/views/

This ``views.py`` file consists of all the views that exist in the app.
A view function takes a Web request and returns a Web response. In most
cases the response consists of the HTML content of a web page, that will
be displayed when a user tries to visit a page. It can also be a 404
error, a JSON file, an image, etc.

A view has to be mapped to a URL in the urls.py file with an unambiguous
url path.

Most commonly a view uses a *template* to generate HTML code. In order
to specify which data should be used in the template the *context*
dictionary has to be filled accordingly

::

    context["mydata""] = "Hello World"

models.py
~~~~~~~~~

https://docs.djangoproject.com/en/1.11/topics/db/models/

This file contains classes which inherit from *django.db.models.Model*.
Each model maps to a single database table and each instance of the
python class represents a line in that table.

The most important model is the *TrackerCertification* model. It represents a
certified run that will be created when a shifter submits the certification
form.

.. code:: python

    class TrackerCertification(SoftDeletionModel):
        # ...
        user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
        runreconstruction = models.OneToOneField(
            RunReconstruction, on_delete=models.CASCADE, primary_key=True
        )
        dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
        reference_runreconstruction = models.ForeignKey(
            RunReconstruction, on_delete=models.CASCADE, related_name="ref", limit_choices_to={'is_reference': True}
        )
        # ...

manager.py
~~~~~~~~~~

https://docs.djangoproject.com/en/1.11/topics/db/managers/

Managers are responsible for accessing the database for certain Django
models. Custom managers for a particular model extend the functionality
of the base Manager. This extra functionality, for example, could be to
only show runs that were certified as "Good". Every Django model has at
least one manager, most commonly the *objects* manager.

query.py
~~~~~~~~

https://docs.djangoproject.com/en/1.11/ref/models/querysets/

When a manager accesses the database a QuerySet object will be returned
containing the desired entity. The QuerySet object itself has methods
which can be used to further tailor the database query.

For example, the ``cosmics`` method filter the QuerySet to only
"Cosmics" runs that were certified, rather than "Collisions".

.. code:: python

    def cosmics(self):
        return self.filter(type__runtype="Cosmics")

tables.py
~~~~~~~~~

https://django-tables2.readthedocs.io/en/latest/

When data should be presented on the website it can often be done in a
simple HTML table. The tables.py describe how these tables should look
like and what attributes of what model should be used.

signals.py
~~~~~~~~~~

https://docs.djangoproject.com/en/1.11/topics/signals/
https://django-allauth.readthedocs.io/en/latest/signals.html

Signals provide a way of notifying an application when a certain event
happens. One signal could, for example, be to automatically update the
privileges (like shift leader or admin status) when a user performs a
login into the website.

admin.py
~~~~~~~~

https://docs.djangoproject.com/en/1.11/ref/contrib/admin/

Django provides an automatic admin interface which manages all the
models. This admin interface can be customized in the admin.py file.

apps.py
~~~~~~~

https://docs.djangoproject.com/en/1.11/ref/applications/

Before an application can be used it has to be configured in a registry
called *django.apps* which is done in *apps.py*

filters.py
~~~~~~~~~~

https://django-filter.readthedocs.io/en/master/index.html

It is often desired to only show a small portion of a database table.
Filters provide an easy way of filtering this data based on specific
criteria. One example of a filter is the run filter in the shifter view.

The way the filter should behave is specified in filters.py

forms.py
~~~~~~~~

https://docs.djangoproject.com/en/1.11/topics/forms/

When certifying a new run or updating an existing run the data has to be
entered in a form. *forms.py* specifies which attributes and which model
should be used and also how the valid form data should look like. Form
validation is performed with one of the *clean* methods of a form class.

.. code:: python

    class TrackerCertificationForm(ModelForm):
      # ...
      def clean(self):
        cleaned_data = super(TrackerCertificationForm, self).clean()

        is_sistrip_bad = cleaned_data.get('sistrip') == 'Bad'
        is_tracking_good = cleaned_data.get('tracking') == 'Good'

        if is_sistrip_bad and is_tracking_good:
        self.add_error(None, ValidationError(
            "Tracking can not be GOOD if SiStrip is BAD. Please correct."))

      # ...

templates
~~~~~~~~~

https://docs.djangoproject.com/en/1.11/ref/templates/language/

A template is a text document which can generate HTML code. Templates
have a close relationship with views, which take care of retrieving the
actual data that needs to be displayed. The data that should be
displayed in the template are defined in the *context* dictionary of the
view.

It can then be accessed directly like this:

::

    {{ mydata }}
