import json

import pytest

from pipedrive.sdk.dealflow.models.person_model import PipedriveDealflowContact
from pipedrive.sdk.dealflow.models.person_model import PipedriveDealflowContactFields


# Pipe
@pytest.mark.skip(reason="Skip it to no update people on master")
def test_PipedriveContact_model_update():
    person: PipedriveDealflowContact = PipedriveDealflowContact(id=1)
    response = person.get()
    assert response["data"]["name"] == "Sebas Golijow"
    payload: dict = {
        "name": "test",
        "email": "test@updated.com",
        "first_name": "test",
        "last_name": "Golijow",
    }
    response = person.update(payload)
    data = response["data"]
    assert data["name"] == "test Golijow"
    assert data["email"][0]["value"] == "test@updated.com"

    payload_2: dict = {
        "name": "Sebas Golijow",
        "email": "test@updated.com",
        "first_name": "Sebas",
        "last_name": "Golijow",
    }
    person.update(payload_2)


# Pipe
def test_PipedriveContact_model_all():
    person: PipedriveDealflowContact = PipedriveDealflowContact(id=1)
    response = person.all(start=0, limit=5)
    keys = response[0].keys()

    payload_2: dict = {
        "name": "Sebas Golijow",
        "email": "test@updated.com",
        "first_name": "Sebas",
        "last_name": "Golijow",
    }
    person.update(payload_2)
    assert "id" in keys
    assert "first_name" in keys
    assert "last_name" in keys
    assert "email" in keys


# #Pipe
@pytest.mark.skip(reason="Skip it to no create persons constantly on Pipedrive")
def test_PipedriveContact_model_create():
    data: dict = {
        "name": "sebastian",
        "first_name": "sebastian",
        "last_name": "person",
        "email": "testingtheemail@email.com",
    }
    person: PipedriveDealflowContact = PipedriveDealflowContact(**data)
    response = person.create()
    data = response["data"]
    assert data["name"] == "sebastian"
    assert data["email"][0]["value"] == "testingtheemail@email.com"


# Pipe
@pytest.mark.skip(reason="Skip it as this test is not consistent")
def test_PipedriveContact_model_get():
    person: PipedriveDealflowContact = PipedriveDealflowContact(id=2)
    response = person.get()
    data = response["data"]
    assert data["name"] == "Alvaro"


def test_PipedriveContact_model_get_with_params():
    person: PipedriveDealflowContact = PipedriveDealflowContact()
    response = person.get(name="Alvaro")
    assert response["data"]["items"][0]["item"]["name"] == "Alvaro"
    assert len(response["data"]["items"]) == 1


def test_PipedriveContact_model_get_with_params_fails_more_than_1_object():
    try:
        person: PipedriveDealflowContact = PipedriveDealflowContact()
        person.get(name="sebas")
    except TypeError as e:
        assert str(e) == "Error: method get return more than 1 object"


def test_PipedriveContact_model_get_with_params_fails_no_object():
    try:
        person: PipedriveDealflowContact = PipedriveDealflowContact()
        person.get(name="asdsdffsd")
    except TypeError as e:
        assert str(e) == "['Error: no result found for name=asdsdffsd']"


# #Pipe
def test_PipedriveContact_model_filter():
    person: PipedriveDealflowContact = PipedriveDealflowContact()
    response = person.filter(name="testing")
    data = response["data"]
    assert data["items"][0]["item"]["name"] == "testing"


# #Pipe
@pytest.mark.skip(reason="Skip it to no delete custom fields constantly on Pipedrive")
def test_PipedriveContact_model_delete():
    person: PipedriveDealflowContact = PipedriveDealflowContact(id=5)
    response = person.get()
    assert response["success"] == True
    response = person.delete()
    assert response["success"] == True


@pytest.mark.skip(reason="Skip it to no delete custom fields constantly on Pipedrive")
def test_delete_custom_field():
    personField: PipedriveDealflowContactFields = PipedriveDealflowContactFields(
        id=9082
    )
    response = personField.delete()
    assert response["success"] == True


@pytest.mark.skip(reason="Skip it to no add custom fields constantly on Pipedrive")
def test_PipedriveContact_add_field():
    data: dict = {"name": "test-field", "field_type": "text"}
    personField: PipedriveDealflowContactFields = PipedriveDealflowContactFields(**data)
    response = personField.add_custom_fields()
    assert response["success"] == True


def test_PipedriveContact_get_fields():
    personField: PipedriveDealflowContactFields = PipedriveDealflowContactFields()
    response = personField.get_custom_fields()
    assert response["success"] == True


@pytest.mark.skip(reason="We didnt cerate custom fields in dealflow sandbox")
def test_PipedriveContact_model_update_custom_fields():
    data = {
        "country": [30],
        "language": [21],
        "name": "Sebas Golijow 2",
        "first_name": "Sebas",
        "last_name": "Golijow",
        "email": "test@updated.com",
    }
    json_data = json.dumps(data)
    encoded_data = json_data.encode("utf-8")
    person: PipedriveDealflowContact = PipedriveDealflowContact(id=338)
    response = person.update(encoded_data)
    assert "e1a4d001c24b9de43adaa3630578f3a66bb710e0" == response["data"]


def test_validation_fields():
    person: PipedriveDealflowContact = PipedriveDealflowContact()
    response = person.validate_fields()
    assert response == "all serializer fields has match"


def test_validation_keys():
    person: PipedriveDealflowContact = PipedriveDealflowContact()
    personField: PipedriveDealflowContactFields = PipedriveDealflowContactFields()
    response = personField.get_custom_fields()
    data = response["data"]
    res = person.validate_keys(data)
    assert res == "All keys are correct"


@pytest.mark.skip(reason="Dont have dealflow sandbox options")
def test_validation_options():
    person: PipedriveDealflowContact = PipedriveDealflowContact()
    res = person.validate_options()
    assert res == "options are correct"


def test_get_contact_activities():
    person: PipedriveDealflowContact = PipedriveDealflowContact(id=338)
    response = person.get_activities(start=0, limit=5)
    assert len(response["data"]) == 1
    assert response["success"] == True


def test_investor_get_or_create_return_existing_user():
    person: PipedriveDealflowContact = PipedriveDealflowContact(id=1)
    data: dict = {
        "name": "sebastian",
        "first_name": "sebastian",
        "last_name": "person",
        "email": "testingtheemail@email.com",
    }
    person: PipedriveDealflowContact = PipedriveDealflowContact(**data)
    response = person.get_or_create()
    assert response["emails"][0] == "testingtheemail@email.com"
    assert response["name"] == "sebastian"


def test_investor_get_or_create_user_created():
    person: PipedriveDealflowContact = PipedriveDealflowContact(id=1)
    data: dict = {
        "name": "sebastian_new",
        "first_name": "sebastian",
        "last_name": "person",
        "email": "testemaildontexisit@email.com",
    }
    person: PipedriveDealflowContact = PipedriveDealflowContact(**data)
    response = person.get_or_create()
    assert response["name"] == "sebastian_new"
