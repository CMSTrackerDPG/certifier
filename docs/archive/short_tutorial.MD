 # High level overview

Django is the framework that is used to connect the relational database in the background to the various html sites.

The routing is done in the file <code>urls.py</code>. This defines which url leads to which html page. The loading of the html-site is done through views in <code>views.py</code>. These views are being called in <code>urls.py</code>.

## Models (models.py)
Models define the database table that will be used to store everything.
So for example: Among other things our database defines a **ReferenceRun**. Its fields are 

*  Run number
*  reconstruction mode
*  bfield
*  etc.

This means that the table with the name **ReferenceRun** has columns with the above listed names.
The rows in that table are therefore individual reference runs.

## Forms (forms.py)

Forms are a way to display/input data into the database. You define your Form which uses a Model that you previously defined. In combination with djangos generic views this lets you create display/input webpages very easily.

## Views (views.py)

## Small example

```python

# ---------- models.py ----------
class ReferenceRun(models.Model):
    reference_run         = models.IntegerField()
    reco                  = models.CharField(max_length=30, choices=RECO_CHOICES)
    runtype               = models.CharField(max_length=30, choices=RUNTYPE_CHOICES)
    bfield                = models.CharField(max_length=30, choices=BFIELD_CHOICES)
    beamtype              = models.CharField(max_length=30, choices=BEAMTYPE_CHOICES)
    beamenergy            = models.CharField(max_length=10, choices=BEAMENERGY_CHOICES)
    dataset               = models.CharField(max_length=150)

# ---------- tables.py ----------
class ReferenceRunTable(tables.Table):
    class Meta:
        model = ReferenceRun
        attrs = {'class': 'table table table-hover table-bordered'}

# ---------- forms.py ----------
class ReferenceRunForm(ModelForm):
    class Meta:
        model = ReferenceRun
        fields = '__all__'

# ---------- views.py ----------
class ListReferences(SingleTableView):  # SingleTableView is part of django-tables2
    model = ReferenceRun                # and implements generation of a simple table
    table_class = ReferenceRunTable

# ---------- urls.py ----------
url(r'^references/$', views.ListReferences.as_view(),  name='references')

```

This is everything that is needed to define the ReferneceRun table, and display its entries in a table. By looking at urls.py we can see that browsing [website]/refrences is going to call the ListReferences(SingleTableView) which uses the ReferenceRun model and the ReferenceRunTable class. All of which is going to be rendered in <code>referencerun_list.html</code>.

All of which is rendered with:
```javascript
---------- referencerun_list.html ----------
{% load static %}
{% load render_table from django_tables2 %}
{% render_table table %}
```

The .html code snippet also demonstrates a very powerful tool in django. It's called the Django Template Language. In simple terms; you can pass variables in the view to html files which you can then access using curly braces syntax

 <code>{{variable}} / {% inbuilt-function %}</code>