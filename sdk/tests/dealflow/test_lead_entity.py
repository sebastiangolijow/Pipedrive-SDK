import json

import pytest
from tqdm import tqdm

from pipedrive.sdk.dealflow.models.activity_model import PipedriveDealflowActivity
from pipedrive.sdk.dealflow.models.lead_model import PipedriveDealflowLead
from pipedrive.sdk.dealflow.models.organization_model import (
    PipedriveDealflowOrganization,
)
from pipedrive.sdk.dealflow.models.person_model import PipedriveDealflowContact


# Pipe
# @pytest.mark.skip(reason="Skip it to no update activitys constantly on Pipedrive")
# def test_PipedriveContact_model_update():
#
#         activity: PipedriveDealflowActivity = PipedriveDealflowActivity(id=1)

#         payload_2: dict = {"id": 59, "type": "task", "person_id": 1}
#         response = activity.update(payload_2)
#         assert response["success"] == True


# # Pipe
# @pytest.mark.skip(reason="Skip it to no delete custom fields constantly on Pipedrive")
def test_PipedriveContact_model_get():
    lead: PipedriveDealflowLead = PipedriveDealflowLead(
        id="9cd1d850-3755-11ee-ae4e-ad98f3210546"
    )
    response = lead.get()
    keys = response["data"].keys()
    assert response["success"] == True
    assert "id" in keys
    assert "title" in keys
    assert "person_id" in keys


# # #Pipe
@pytest.mark.skip(reason="Skip it to no create activitys constantly on Pipedrive")
def test_PipedriveContact_model_create():
    data: dict = {"title": "test", "organization_id": 1}
    lead: PipedriveDealflowLead = PipedriveDealflowLead(**data)
    response = lead.create()
    data = response["data"]
    assert response["success"] == True


# # #Pipe
@pytest.mark.skip(reason="Skip it to no delete custom fields constantly on Pipedrive")
def test_PipedriveContact_model_delete():
    note: PipedriveDealflowLead = PipedriveDealflowLead(id=1)
    response = note.delete()
    assert response["success"] == True


def test_PipedriveContact_model_all():
    lead: PipedriveDealflowLead = PipedriveDealflowLead()
    response = lead.all()
    keys = response[0].keys()
    assert "title" in keys
    assert "id" in keys
    assert "person_id" in keys
