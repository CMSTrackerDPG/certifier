from decimal import Decimal

import pytest
from django.test import TestCase
import numpy as np

from analysis.analyse import *

pytestmark = pytest.mark.django_db

# Create your tests here.

class TestAnalyse:
    def test_run_principal_component_analysis(self):
        run_principal_component_analysis(np.array([1,2,3]))
        assert True

    def test_run_tsne(self):
        run_tsne(np.array([1,2,3]))
        assert True
