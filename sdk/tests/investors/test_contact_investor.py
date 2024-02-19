import json

import pytest

from pipedrive.sdk.investors.models.person_model import PipedriveInvestorContact
from pipedrive.sdk.investors.models.person_model import PipedriveInvestorContactFields


# Pipe
@pytest.mark.skip(reason="Pipedrive put request not working for the moment")
def test_contact_model_update():
    person: PipedriveInvestorContact = PipedriveInvestorContact(id=23060)
    response = person.get()
    assert response["data"]["name"] == "Test Person"
    payload: dict = {
        "name": "test",
        "email": "test@updated.com",
        "first_name": "test",
        "last_name": "Golijow",
        "phone": "111111",
    }
    response = person.update(payload)
    data = response["data"]
    assert data["name"] == "test Golijow"
    assert data["email"][0]["value"] == "test@updated.com"

    payload_2: dict = {
        "name": "Test Person",
        "email": "usertest@testing.com",
        "first_name": "Test",
        "last_name": "Person",
    }
    person.update(payload_2)


# Pipe
def test_contact_model_all():
    person: PipedriveInvestorContact = PipedriveInvestorContact(id=1)
    response = person.all(start=0, limit=5)
    keys = response[0].keys()
    assert "id" in keys
    assert "first_name" in keys
    assert "last_name" in keys
    assert "email" in keys


# #Pipe
@pytest.mark.skip(reason="Skip it to no create persons constantly on Pipedrive")
def test_contact_model_create():
    data: dict = {
        "name": "sebastian",
        "first_name": "sebastian",
        "last_name": "person",
        "email": "testingtheemail@email.com",
    }
    person: PipedriveInvestorContact = PipedriveInvestorContact(**data)
    response = person.create()
    data = response["data"]
    assert data["name"] == "sebastian"
    assert data["email"][0]["value"] == "testingtheemail@email.com"


# Pipe
def test_contact_model_get():
    person: PipedriveInvestorContact = PipedriveInvestorContact(id=23058)
    response = person.get()
    data = response["data"]
    assert data["name"] == "Sebastian Testing"
    assert data["email"][0]["value"] == "sebas@testing.com"


@pytest.mark.skip(reason="Skip it to no create persons constantly on Pipedrive")
def test_contact_model_get_with_params():
    person: PipedriveInvestorContact = PipedriveInvestorContact(id=1)
    response = person.get(name="Sebas Golijow")
    assert response["data"]["items"][0]["item"]["name"] == "Sebas Golijow"
    assert len(response["data"]["items"]) == 1


def test_contact_model_get_with_params_fails_more_than_1_object():
    try:
        person: PipedriveInvestorContact = PipedriveInvestorContact()
        person.get(name="sebas")
    except TypeError as e:
        assert str(e) == "Error: method get return more than 1 object"


def test_contact_model_get_with_params_fails_no_object():
    try:
        person: PipedriveInvestorContact = PipedriveInvestorContact()
        person.get(name="asdsdffsd")
    except TypeError as e:
        assert str(e) == "['Error: no result found for name=asdsdffsd']"


# #Pipe
def test_contact_model_filter():
    person: PipedriveInvestorContact = PipedriveInvestorContact()
    response = person.filter(name="Test Validation")
    data = response["data"]
    assert data["items"][0]["item"]["name"] == "Test Validation"
    assert data["items"][0]["item"]["primary_email"] == None


# #Pipe
@pytest.mark.skip(reason="Skip it to no delete custom fields constantly on Pipedrive")
def test_contact_model_delete():
    person: PipedriveInvestorContact = PipedriveInvestorContact(id=5)
    response = person.get()
    assert response["success"] == True
    response = person.delete()
    assert response["success"] == True


@pytest.mark.skip(reason="Skip it to no delete custom fields constantly on Pipedrive")
def test_delete_custom_field():
    personField: PipedriveInvestorContactFields = PipedriveInvestorContactFields(
        id=9082
    )
    response = personField.delete()
    assert response["success"] == True


@pytest.mark.skip(reason="Skip it to no add custom fields constantly on Pipedrive")
def test_contact_add_field():
    data: dict = {"name": "test-field", "field_type": "text"}
    personField: PipedriveInvestorContactFields = PipedriveInvestorContactFields(**data)
    response = personField.add_custom_fields()
    assert response["success"] == True


def test_contact_get_fields():
    personField: PipedriveInvestorContactFields = PipedriveInvestorContactFields()
    response = personField.get_custom_fields()
    assert response["success"] == True


@pytest.mark.skip(reason="Pipedrive put request not working for the moment")
def test_contact_model_update_custom_fields():
    data = {
        "country": [30],
        "language": [20],
        "name": "Test Person",
        "first_name": "Test",
        "last_name": "Person",
        "email": "usertest@testing.com",
    }
    json_data = json.dumps(data)
    encoded_data = json_data.encode("utf-8")
    person: PipedriveInvestorContact = PipedriveInvestorContact(id=23060)
    response = person.update(encoded_data)
    assert response["data"]["2b6b5a83998d702748130c6d90621dcd8d39606e"] == "30"
    assert response["data"]["1316bee71be0e3a090c1f58ad36827e96be756e3"] == "20"


def test_validation_fields():
    person: PipedriveInvestorContact = PipedriveInvestorContact()
    response = person.validate_fields()
    assert response == "all serializer fields has match"


def test_validation_keys():
    person: PipedriveInvestorContact = PipedriveInvestorContact()
    personField: PipedriveInvestorContactFields = PipedriveInvestorContactFields()
    response = personField.get_custom_fields()
    data = response["data"]
    res = person.validate_keys(data)
    assert res == "All keys are correct"


def test_validation_options():
    person: PipedriveInvestorContact = PipedriveInvestorContact()
    res = person.validate_options()
    assert res == "options are correct"


def test_get_contact_activities():
    person: PipedriveInvestorContact = PipedriveInvestorContact(id=23058)
    response = person.get_activities(start=0, limit=5)
    assert len(response["data"]) == 2
    assert response["success"] == True


def test_investor_get_or_create_return_existing_user():
    person: PipedriveInvestorContact = PipedriveInvestorContact(id=1)
    data: dict = {
        "name": "sebastian",
        "first_name": "sebastian",
        "last_name": "person",
        "email": "testingtheemail@email.com",
    }
    person: PipedriveInvestorContact = PipedriveInvestorContact(**data)
    _, data = person.get_or_create()
    assert data["items"][0]["item"]["emails"][0] == "testingtheemail@email.com"
    assert data["items"][0]["item"]["name"] == "sebastian"


def test_investor_get_or_create_user_created():
    person: PipedriveInvestorContact = PipedriveInvestorContact(id=1)
    data: dict = {
        "name": "Sebas Golijow",
        "first_name": "Sebas",
        "last_name": "Golijow",
        "email": "test@updated.com",
    }
    person: PipedriveInvestorContact = PipedriveInvestorContact(**data)
    _, response = person.get_or_create()
    assert response["items"][0]["item"]["name"] == "Sebas Golijow"


def test_add_picture():
    person: PipedriveInvestorContact = PipedriveInvestorContact(id=1)
    link = "http://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
    name = "imagename.png"
    response = person.add_picture(link=link, name=name)
    assert response["success"] == True
