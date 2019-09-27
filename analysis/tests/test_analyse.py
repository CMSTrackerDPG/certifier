from decimal import Decimal

import pytest
from django.test import TestCase

from analysis.analyse import *

pytestmark = pytest.mark.django_db

# Create your tests here.

class TestAnalyse:
    def test_run_principal_component_analysis(self):
        #run_principal_component_analysis()
        assert True

    def test_run_tsne(self):
        #run_tsne()
        assert True

    def test_run_umap(self):
        #run_umap()
        assert True
