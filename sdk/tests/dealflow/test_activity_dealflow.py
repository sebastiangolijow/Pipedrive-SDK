import pytest

from pipedrive.sdk.dealflow.models.activity_model import PipedriveDealflowActivity
from pipedrive.sdk.dealflow.models.activity_model import PipedriveDealflowActivityType


# Pipe
@pytest.mark.skip(reason="Skip it to no update activitys constantly on Pipedrive")
def test_PipedriveContact_model_update():
    activity: PipedriveDealflowActivity = PipedriveDealflowActivity(id=1)

    payload_2: dict = {"id": 59, "type": "task", "person_id": 1}
    response = activity.update(payload_2)
    assert response["success"] == True


# Pipe
def test_PipedriveContact_model_get():
    activity: PipedriveDealflowActivity = PipedriveDealflowActivity(id=2)
    response = activity.get()
    keys = response["data"].keys()
    assert response["success"] == True
    assert "id" in keys
    assert "org_id" in keys
    assert "person_id" in keys
    assert "company_id" in keys
    assert "type" in keys
    assert "attendees" in keys


# #Pipe
@pytest.mark.skip(reason="Skip it to no create activitys constantly on Pipedrive")
def test_PipedriveContact_model_create():
    data: dict = {
        "person_id": 1,
        "type": "task",
        "participants": [{"person_id": 1, "primary_flag": True}],
    }
    activity: PipedriveDealflowActivity = PipedriveDealflowActivity(**data)
    response = activity.create()
    data = response["data"]
    assert response["success"] == True


# #Pipe
@pytest.mark.skip(reason="Skip it to no delete custom fields constantly on Pipedrive")
def test_PipedriveContact_model_delete():
    note: PipedriveDealflowActivity = PipedriveDealflowActivity(id=1)
    response = note.delete()
    assert response["success"] == True


def test_PipedriveContact_model_all():
    activity: PipedriveDealflowActivity = PipedriveDealflowActivity(id=1)
    response = activity.all()
    keys = response["data"][0].keys()
    assert "id" in keys
    assert "org_id" in keys
    assert "person_id" in keys
    assert "company_id" in keys
    assert "type" in keys
    assert "attendees" in keys


def test_PipedriveContact_model_all_activity_type():
    activity: PipedriveDealflowActivityType = PipedriveDealflowActivityType(id=1)
    response = activity.all()
    keys = response[0].keys()
    assert "name" in keys
    assert "key_string" in keys
    assert "id" in keys
