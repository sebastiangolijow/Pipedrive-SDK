import pytest

from pipedrive.sdk.investors.models.note_model import PipedriveInvestorNote


# Pipe
@pytest.mark.skip(reason="Skip it to no update persons constantly on Pipedrive")
def test_PipedriveContact_model_update():
    person: PipedriveInvestorNote = PipedriveInvestorNote(id=1)

    payload_2: dict = {
        "id": 20,
        "content": "note updated",
    }
    response = person.update(payload_2)
    data = response["data"]
    assert data["content"] == "note updated"


# Pipe
def test_PipedriveContact_model_get():
    note: PipedriveInvestorNote = PipedriveInvestorNote(id=1)
    response = note.get(person_id=1)
    keys = response[0].keys()
    print(response[0]["id"])
    assert "id" in keys
    assert "content" in keys
    assert "person_id" in keys
    assert "org_id" in keys


# #Pipe
@pytest.mark.skip(reason="Skip it to no create persons constantly on Pipedrive")
def test_PipedriveContact_model_create():
    data: dict = {
        "person_id": 1,
        "content": "testing creation of a note",
    }
    person: PipedriveInvestorNote = PipedriveInvestorNote(**data)
    response = person.create()
    data = response["data"]
    assert response["success"] == True
    assert data["content"] == "testing creation of a note"
    assert data["person_id"] == 1


# #Pipe
@pytest.mark.skip(reason="Skip it to no delete custom fields constantly on Pipedrive")
def test_PipedriveContact_model_delete():
    note: PipedriveInvestorNote = PipedriveInvestorNote(id=17)
    response = note.delete()
    assert response["success"] == True
