# pytest
## Links

 * https://docs.pytest.org/en/latest/
 * https://pytest-django.readthedocs.io/en/latest/
 * https://speakerdeck.com/mbrochh/the-django-tdd-cookbook

## Installation

```bash
pip install pytest-django
pip install pytest-cov
```

## Configuration

*dqmsite/test_settings.py*
```
from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
```

*pytest.ini*
```
[pytest]
DJANGO_SETTINGS_MODULE = dqmsite.test_settings
python_files = tests.py test_*.py *_tests.py
addopts = --nomigrations --cov=. --cov-report=html
```

*.coveragerc*
```
[run]
omit =
    *apps.py,
    *migrations/*,
    *settings*,
    *tests/*,
    *wsgi.py,
    manage.py,
    venv/*
```

## Run the tests

```bash
pytest
```
or 

```bash
pytest --cov-report=html
```

view html report in the browser

```bash
firefox htmlcov/index.html 
```

alternatively in console

```bash
pytest --cov-report=term
```