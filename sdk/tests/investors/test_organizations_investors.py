import json

import pytest

from pipedrive.sdk.investors.models.organization_model import (
    PipedriveInvestorOrganization,
)
from pipedrive.sdk.investors.models.organization_model import (
    PipedriveInvestorOrganizationFields,
)


def test_organization_get_fields():
    organizationField: PipedriveInvestorOrganizationFields = (
        PipedriveInvestorOrganizationFields()
    )
    response = organizationField.get_custom_fields()
    assert response["success"] == True


def test_organization_model_update_custom_fields():
    data = {
        "type": [256],
        "qualification": [252],
        "name": "Sebas ORG",
    }
    json_data = json.dumps(data)
    encoded_data = json_data.encode("utf-8")
    person: PipedriveInvestorOrganization = PipedriveInvestorOrganization(id=24332)
    response = person.update(encoded_data)
    assert response["data"]["94c6c96cdaeccc3d6fd07ce455dcac4dc2291433"] == "256"
    assert response["data"]["6ea5013ed89a6eaa692836d30ba11c40ed8cd75a"] == "252"


# Pipe
def test_organization_model_all():
    person: PipedriveInvestorOrganization = PipedriveInvestorOrganization(id=1)
    response = person.all()
    keys = response[0].keys()
    assert isinstance(response, list)
    assert "name" in keys


# #Pipe
# @pytest.mark.skip(reason="Skip it to no create persons constantly on Pipedrive")
def test_organization_model_create():
    data: dict = {
        "name": "OneRagtest TESTING org",
    }
    person: PipedriveInvestorOrganization = PipedriveInvestorOrganization(**data)
    response = person.create()
    data = response["data"]
    assert data["name"] == "OneRagtest TESTING org"


@pytest.mark.skip(reason="Skip it to no get unexisting people")
def test_organization_model_get_org():
    person: PipedriveInvestorOrganization = PipedriveInvestorOrganization(id=1)
    response = person.get()
    keys = response["data"].keys()
    assert "id" in keys
    assert "name" in keys


@pytest.mark.skip(reason="Skip it to no get unexisting people")
def test_organization_model_get_with_params():
    person: PipedriveInvestorOrganization = PipedriveInvestorOrganization(id=1)
    response = person.get(name="sebas org")
    keys = response["data"]["items"][0]["item"].keys()
    assert "id" in keys
    assert "name" in keys


# #Pipe
def test_organization_model_filter():
    person: PipedriveInvestorOrganization = PipedriveInvestorOrganization()
    response = person.filter(name="Sebas")
    data = response["data"]
    assert data["items"][0]["item"]["name"] == "Sebas ORG"


# #Pipe
@pytest.mark.skip(reason="Skip it to no delete custom fields constantly on Pipedrive")
def test_organization_model_delete():
    person: PipedriveInvestorOrganization = PipedriveInvestorOrganization(id=4)
    response = person.get()
    assert response["success"] == True
    response = person.delete()
    assert response["success"] == True


@pytest.mark.skip(reason="Skip it to no delete custom fields constantly on Pipedrive")
def test_delete_custom_field():
    personField: PipedriveInvestorOrganizationFields = (
        PipedriveInvestorOrganizationFields(id=9082)
    )
    response = personField.delete()
    assert response["success"] == True


@pytest.mark.skip(reason="Skip it to no add custom fields constantly on Pipedrive")
def test_organization_add_field():
    data: dict = {"name": "test-field", "field_type": "text"}
    personField: PipedriveInvestorOrganizationFields = (
        PipedriveInvestorOrganizationFields(**data)
    )
    response = personField.add_custom_fields()
    assert response["success"] == True


def test_validation_fields():
    org: PipedriveInvestorOrganization = PipedriveInvestorOrganization()
    response = org.validate_fields()
    assert response == "all serializer fields has match"


def test_validation_keys():
    org: PipedriveInvestorOrganization = PipedriveInvestorOrganization()
    orgField: PipedriveInvestorOrganizationFields = (
        PipedriveInvestorOrganizationFields()
    )
    response = orgField.get_custom_fields()
    data = response["data"]
    res = org.validate_keys(data)
    assert res == "All keys are correct"


def test_validation_options():
    org: PipedriveInvestorOrganization = PipedriveInvestorOrganization()
    res = org.validate_options()
    assert res == "options are correct"
