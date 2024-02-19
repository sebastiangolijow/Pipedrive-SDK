import json

import pytest

from core_management.models import Fundraising
from entities.investor.models.models import Investor
from pipedrive.app.utils.pipedrive_utils import return_deal_id
from pipedrive.sdk.investors.models.deal_model import PipedriveInvestorDeal
from pipedrive.sdk.investors.models.deal_model import PipedriveInvestorDealFields
from pipedrive.sdk.investors.models.organization_model import (
    PipedriveInvestorOrganization,
)


def test_PipedriveOrganization_get_fields():
    dealField: PipedriveInvestorDealFields = PipedriveInvestorDealFields()
    response = dealField.get_custom_fields()
    assert response["success"] == True


def test_PipedriveOrganization_model_update_custom_fields():
    data = {
        "fundraising": [16],
    }
    json_data = json.dumps(data)
    encoded_data = json_data.encode("utf-8")
    person: PipedriveInvestorDeal = PipedriveInvestorDeal(id=9523)
    response = person.update(encoded_data)
    assert response["data"]["b6923458151406bf97a3f694a051f063f6d3506b"] == "16"


# # Pipe
def test_deal_model_all():
    person: PipedriveInvestorDeal = PipedriveInvestorDeal()
    response = person.all()
    keys = response[0].keys()
    assert isinstance(response, list)
    assert "id" in keys
    assert "person_id" in keys
    assert "currency" in keys
    assert "b6923458151406bf97a3f694a051f063f6d3506b" in keys


# # #Pipe
@pytest.mark.skip(reason="Skip it to no create persons constantly on Pipedrive")
def test_deal_model_create():
    data: dict = {"title": "Motion Society Seed #1 (1938)", "currency": "EUR"}
    deal: PipedriveInvestorDeal = PipedriveInvestorDeal(**data)
    response = deal.create()
    data = response["data"]
    assert data["title"] == "Motion Society Seed #1 (1938)"


# # Pipe
def test_deal_model_get():
    person: PipedriveInvestorDeal = PipedriveInvestorDeal(id=9523)
    response = person.get()
    keys = response["data"].keys()
    assert "id" in keys
    assert "person_id" in keys
    assert "currency" in keys
    assert "b6923458151406bf97a3f694a051f063f6d3506b" in keys


@pytest.mark.skip(
    reason="Skip as exact_match not working on pipedrive and returning more than 1 object"
)
def test_deal_model_get_with_params():
    person: PipedriveInvestorDeal = PipedriveInvestorDeal()
    response = person.get(title="Keli Network Seed 2017 #3 (391)")
    keys = response["data"]["items"][0]["item"].keys()
    assert "id" in keys
    assert "title" in keys
    assert "currency" in keys


# # #Pipe
def test_deal_model_filter():
    person: PipedriveInvestorDeal = PipedriveInvestorDeal()
    response = person.filter(title="Keli Network Seed 2017 #3 (361)")
    data = response["data"]
    assert "Keli Network Seed 2017" in data["items"][0]["item"]["title"]


# # #Pipe
@pytest.mark.skip(reason="Skip it to no delete custom fields constantly on Pipedrive")
def test_deal_model_delete():
    person: PipedriveInvestorDeal = PipedriveInvestorDeal(id=1)
    response = person.get()
    assert response["success"] == True
    response = person.delete()
    assert response["success"] == True


@pytest.mark.skip(reason="Skip it to no delete custom fields constantly on Pipedrive")
def test_delete_custom_field():
    orgField: PipedriveInvestorDealFields = PipedriveInvestorDealFields(id=9082)
    response = orgField.delete()
    assert response["success"] == True


@pytest.mark.skip(reason="Skip it to no add custom fields constantly on Pipedrive")
def test_deal_add_field():
    data: dict = {"name": "test-field", "field_type": "text"}
    personField: PipedriveInvestorDealFields = PipedriveInvestorDealFields(**data)
    response = personField.add_custom_fields()
    assert response["success"] == True


def test_validation_fields():
    org: PipedriveInvestorDeal = PipedriveInvestorDeal()
    response = org.validate_fields()
    assert response == "all serializer fields has match"


def test_validation_keys():
    org: PipedriveInvestorDeal = PipedriveInvestorDeal()
    orgField: PipedriveInvestorDealFields = PipedriveInvestorDealFields()
    response = orgField.get_custom_fields()
    data = response["data"]
    res = org.validate_keys(data)
    assert res == "All keys are correct"


def test_validation_options():
    org: PipedriveInvestorDeal = PipedriveInvestorDeal()
    res = org.validate_options()
    assert res == "options are correct"


def test_return_deal_id():
    response = return_deal_id("Hive Series A 2023 #3", 2160)
    assert type(response) == int
