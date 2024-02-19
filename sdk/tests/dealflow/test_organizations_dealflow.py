import json

import pytest

from pipedrive.sdk.dealflow.models.organization_model import (
    PipedriveDealflowOrganization,
)
from pipedrive.sdk.dealflow.models.organization_model import (
    PipedriveDealflowOrganizationFields,
)


def test_PipedriveOrganization_get_fields():
    organizationField: PipedriveDealflowOrganizationFields = (
        PipedriveDealflowOrganizationFields()
    )
    response = organizationField.get_custom_fields()
    assert response["success"] == True


@pytest.mark.skip(reason="Skip it to not fail in master")
def test_PipedriveOrganization_model_update_custom_fields():
    data = {
        "type": [256],
        "qualification": [252],
        "name": "Sebas ORG",
    }
    json_data = json.dumps(data)
    encoded_data = json_data.encode("utf-8")
    person: PipedriveDealflowOrganization = PipedriveDealflowOrganization(id=2)
    response = person.update(encoded_data)
    assert response["data"]["94c6c96cdaeccc3d6fd07ce455dcac4dc2291433"] == "256"
    assert response["data"]["6ea5013ed89a6eaa692836d30ba11c40ed8cd75a"] == "252"


# Pipe
def test_PipedriveContact_model_all():
    org: PipedriveDealflowOrganization = PipedriveDealflowOrganization()
    response = org.all()
    keys = response[0].keys()
    assert isinstance(response, list)
    assert "name" in keys


# #Pipe
@pytest.mark.skip(reason="Skip it to no create persons constantly on Pipedrive")
def test_PipedriveContact_model_create():
    data: dict = {
        "name": "OneRagtest org",
    }
    person: PipedriveDealflowOrganization = PipedriveDealflowOrganization(**data)
    response = person.create()
    data = response["data"]
    assert data["name"] == "OneRagtest org"


# Pipe
def test_PipedriveContact_model_get():
    person: PipedriveDealflowOrganization = PipedriveDealflowOrganization(id=1)
    response = person.get()
    keys = response["data"].keys()
    assert "id" in keys
    assert "name" in keys


def test_PipedriveContact_model_get_with_params():
    person: PipedriveDealflowOrganization = PipedriveDealflowOrganization(id=1)
    response = person.get(name="sebas org")
    keys = response["data"]["items"][0]["item"].keys()
    assert "id" in keys
    assert "name" in keys


# #Pipe
def test_PipedriveContact_model_filter():
    person: PipedriveDealflowOrganization = PipedriveDealflowOrganization()
    response = person.filter(name="Sebas")
    data = response["data"]
    assert data["items"][0]["item"]["name"] == "Sebas ORG"


# #Pipe
@pytest.mark.skip(reason="Skip it to no delete custom fields constantly on Pipedrive")
def test_PipedriveContact_model_delete():
    person: PipedriveDealflowOrganization = PipedriveDealflowOrganization(id=4)
    response = person.get()
    assert response["success"] == True
    response = person.delete()
    assert response["success"] == True


@pytest.mark.skip(reason="Skip it to no delete custom fields constantly on Pipedrive")
def test_delete_custom_field():
    personField: PipedriveDealflowOrganizationFields = (
        PipedriveDealflowOrganizationFields(id=9082)
    )
    response = personField.delete()
    assert response["success"] == True


@pytest.mark.skip(reason="Skip it to no add custom fields constantly on Pipedrive")
def test_PipedriveContact_add_field():
    data: dict = {"name": "test-field", "field_type": "text"}
    personField: PipedriveDealflowOrganizationFields = (
        PipedriveDealflowOrganizationFields(**data)
    )
    response = personField.add_custom_fields()
    assert response["success"] == True


def test_validation_fields():
    org: PipedriveDealflowOrganization = PipedriveDealflowOrganization()
    response = org.validate_fields()
    assert response == "all serializer fields has match"


def test_validation_keys():
    org: PipedriveDealflowOrganization = PipedriveDealflowOrganization()
    orgField: PipedriveDealflowOrganizationFields = (
        PipedriveDealflowOrganizationFields()
    )
    response = orgField.get_custom_fields()
    data = response["data"]
    res = org.validate_keys(data)
    assert res == "All keys are correct"


def test_validation_options():
    org: PipedriveDealflowOrganization = PipedriveDealflowOrganization()
    res = org.validate_options()
    assert res == "options are correct"
