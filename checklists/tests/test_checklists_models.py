import pytest
from mixer.backend.django import mixer

from checklists.models import *

pytestmark = pytest.mark.django_db

def test_checklist():
    checklist = mixer.blend(Checklist, title="test")
    assert "test" == str(checklist)

def test_checklistItem():
    checklistItem = mixer.blend(ChecklistItem, text="test")
    assert "test" == str(checklistItem)
