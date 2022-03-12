import pytest
from mixer.backend.django import mixer

from checklists.models import Checklist, ChecklistItem, ChecklistItemGroup

pytestmark = pytest.mark.django_db


def test_checklist():
    checklist = mixer.blend(Checklist, title="test")
    assert "test" == checklist.title


def test_checklistItemText():
    checklistItem = mixer.blend(ChecklistItem, text="test")
    assert "test" == checklistItem.text


def test_checklistItemLabel():
    checklistItem = mixer.blend(ChecklistItem, text="test")
    assert f"{checklistItem.checklistgroup.checklist.title}/{checklistItem.checklistgroup.name}/test" == str(
        checklistItem)
