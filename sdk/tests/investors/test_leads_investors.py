import json

import pytest
from tqdm import tqdm

from pipedrive.sdk.investors.models.activity_model import PipedriveInvestorActivity
from pipedrive.sdk.investors.models.lead_model import PipedriveInvestorLead
from pipedrive.sdk.investors.models.organization_model import (
    PipedriveInvestorOrganization,
)
from pipedrive.sdk.investors.models.person_model import PipedriveInvestorContact


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
    lead: PipedriveInvestorLead = PipedriveInvestorLead(
        id="737c17e0-3822-11ee-aaa4-4dbe33d9b869"
    )
    response = lead.get()
    keys = response["data"].keys()
    assert response["success"] == True
    assert "id" in keys
    assert "organization_id" in keys
    assert "title" in keys


# # #Pipe
@pytest.mark.skip(reason="Skip it to no create activitys constantly on Pipedrive")
def test_PipedriveContact_model_create():
    data: dict = {"title": "test", "organization_id": 1}
    lead: PipedriveInvestorLead = PipedriveInvestorLead(**data)
    response = lead.create()
    data = response["data"]
    assert response["success"] == True


# # #Pipe
@pytest.mark.skip(reason="Skip it to no delete custom fields constantly on Pipedrive")
def test_PipedriveContact_model_delete():
    lead: PipedriveInvestorLead = PipedriveInvestorLead(id=1)
    response = lead.delete()
    assert response["success"] == True


def test_PipedriveContact_model_all():
    lead: PipedriveInvestorLead = PipedriveInvestorLead()
    response = lead.all()
    keys = response[0].keys()
    assert "title" in keys
    assert "id" in keys
    assert "person_id" in keys
