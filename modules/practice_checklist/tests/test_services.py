import pytest
from unittest.mock import Mock
from modules.practice_checklist.services.checklist import PracticeChecklistService, PracticeChecklistItemService
from modules.practice_checklist.models import PracticeChecklist, PracticeChecklistItem

def test_close_checklist():
    service = PracticeChecklistService()
    mock_session = Mock()
    service.repo = Mock()
    service.repo.session = mock_session

    checklist = PracticeChecklist(id=1, name="Test", status="open")
    mock_session.get.return_value = checklist

    result = service.close(1, "Test close")

    assert checklist.status == "closed"
    assert checklist.closed_at is not None
    assert "[Cierre] Test close" in checklist.description

def test_set_done_item():
    service = PracticeChecklistItemService()
    mock_session = Mock()
    service.repo = Mock()
    service.repo.session = mock_session

    item = PracticeChecklistItem(id=1, title="Test item", is_done=False)
    mock_session.get.return_value = item

    result = service.set_done(1, True, "Done note")

    assert item.is_done == True
    assert item.done_at is not None
    assert "[Estado] Done note" in item.note
