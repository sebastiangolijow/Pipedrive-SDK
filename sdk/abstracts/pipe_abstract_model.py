import json

import pandas as pd
import requests
from pydantic import BaseModel

from pipedrive.sdk.secrets import settings
from pipedrive.sdk.utils.choices import ChoiceCharEnum


def check_dict_values(data):
    for value in data.values():
        if isinstance(value, (list, dict)):
            return True
    return False


def replace_keys_if_choices(data, input_dict):
    new_dict: dict = {}
    choice_keys = list(data.__members__.keys())
    if not isinstance(input_dict, dict):
        data_decoded = input_dict.decode("utf-8")
        data_dict = json.loads(data_decoded)
    else:
        data_dict = input_dict
    for key in data_dict.keys():
        if key in choice_keys:
            value = data[key].value
            new_dict[value] = data_dict[key]
        else:
            new_dict[key] = data_dict[key]
    return new_dict


def validate_filter_fields(data):
    if len(data.keys()) > 1:
        raise TypeError("Error: use only one field to search by")


class PipedriveAbstractModel:
    """
    Base class for interacting with entities in Pipedrive.

    This class will act as abstract and will be inherit in every model that will represent an entity in Pipedrive.
    """

    url: str = settings.PIPEDRIVE_BASE_URL
    url_custom_field: str = ""
    api_token = ""
    serializer_created = BaseModel
    serializer_updated = BaseModel
    choices = ChoiceCharEnum
    params: dict = {}

    def __init__(self, **kwargs):
        if not self.api_token:
            raise TypeError("not api key provided")
        else:
            self.params = {"api_token": self.api_token}
        if kwargs:
            if "id" in kwargs:
                self.data = self.serializer_updated(**kwargs)
            else:
                self.data = self.serializer_created(**kwargs)

    def all(self, **kwargs):
        """
        Retrieve all records.

        Returns:
            list: A list of records retrieved from the Pipedrive API.

        Raises:
            requests.exceptions.RequestException: If an error occurs while making the API request.
            KeyError: If the response does not contain the expected data field.
        """
        if kwargs:
            self.url = f"{self.url}?start={kwargs.get('start')}&limit={kwargs.get('limit')}&archived_status=not_archived"
            response = requests.get(self.url, params=self.params)
            return response.json()["data"]
        response = requests.get(self.url, params=self.params)
        return response.json()["data"]

    def create(self):
        """
        Create a new record.

        Returns:
            dict: The newly created record data retrieved from the Pipedrive API.

        Raises:
            requests.exceptions.RequestException: If an error occurs while making the API request.
            KeyError: If the response does not contain the expected data field.
        """
        data = replace_keys_if_choices(self.choices, self.data.dict())
        response = requests.post(self.url, json=data, params=self.params)
        return response.json()

    def get(self, **kwargs):
        """
        Retrieve a specific record.

        Returns:
            dict: The retrieved record data from the Pipedrive API.

        Raises:
            requests.exceptions.RequestException: If an error occurs while making the API request.
            KeyError: If the response does not contain the expected data field.
        """
        if kwargs:
            validate_filter_fields(kwargs)
            search_params = "&".join(
                [f"term={value}&fields={key}" for key, value in kwargs.items()]
            )
            url = f"{self.url}/search?{search_params}"
            response = requests.get(url, params=self.params)
            if len(response.json()["data"]["items"]) > 1:
                raise TypeError("Error: method get return more than 1 object")
            if len(response.json()["data"]["items"]) == 0:
                raise TypeError(
                    [
                        f"Error: no result found for {key}={value}"
                        for key, value in kwargs.items()
                    ]
                )
            else:
                return response.json()
        response = requests.get(f"{self.url}/{self.data.id}", params=self.params)
        return response.json()

    def filter(self, **kwargs):
        """
        Filter records based on search terms.

        Args:
            **kwargs: Keyword arguments representing the search fields and terms.

        Returns:
            dict: The filtered records data retrieved from the Pipedrive API.

        Raises:
            requests.exceptions.RequestException: If an error occurs while making the API request.
            KeyError: If the response does not contain the expected data field.
        """
        validate_filter_fields(kwargs)
        search_params = "&".join(
            [f"term={value}&fields={key}" for key, value in kwargs.items()]
        )
        url = f"{self.url}/search?{search_params}"
        response = requests.get(url, params=self.params)
        return response.json()

    def update(self, data):
        """
        Update an existing record.

        Args:
            data (dict or bytes): A dictionary or bytes object containing the data for updating the record.

        Returns:
            dict: The updated record data retrieved from the Pipedrive API.

        Raises:
            requests.exceptions.RequestException: If an error occurs while making the API request.
            KeyError: If the response does not contain the expected data field.
        """
        if not isinstance(data, dict):
            json_string = data.decode("utf-8")
            data_dict = json.loads(json_string)
            data = data_dict
        data["id"] = self.data.id
        self.serializer_updated(**data)
        if self.choices != ChoiceCharEnum:
            result = replace_keys_if_choices(self.choices, data)
            data = result
        response = requests.put(
            f"{self.url}/{self.data.id}", data=data, params=self.params
        )
        return response.json()

    def delete(self):
        """
        Delete an existing record.

        Returns:
            dict: The response data confirming the deletion from the Pipedrive API.

        Raises:
            requests.exceptions.RequestException: If an error occurs while making the API request.
            KeyError: If the response does not contain the expected data field.
        """
        response = requests.delete(f"{self.url}/{self.data.id}", params=self.params)
        return response.json()

    def validate_fields(self):
        keys = list(self.serializer_created.__annotations__.keys())
        instance = self.fields()
        pipeFields = instance.get_custom_fields()
        data = pipeFields["data"]
        names = self.extract_names(data)
        lowercase_strings = [s.lower() for s in names]
        for key in keys:
            if key not in lowercase_strings:
                print(f"{key} not found")
                raise TypeError(f"{key} not found")
        print("all serializer fields has match")
        return "all serializer fields has match"

    def validate_keys(self, data):
        for obj in data:
            for e in self.choices:
                if e.name == obj["name"] and e.value != obj["key"]:
                    raise TypeError("keys doesn't match")
        print("All keys are correct")
        return "All keys are correct"

    def validate_options(self):
        instance = self.fields()
        pipeFields = instance.get_custom_fields()
        data = pipeFields["data"]
        for obj in data:
            for e in self.choices:
                if (
                    "options" in obj.keys()
                    and e.name == obj["name"]
                    and obj["options"] not in self.options_to_validate
                ):
                    raise TypeError("options mismatched")
        print("options are correct")
        return "options are correct"

    def extract_names(self, obj_list):
        names = []
        for obj in obj_list:
            names.append(obj["name"])
            names.append(obj["key"])
        return names


class PipedriveContactAbstract(PipedriveAbstractModel):
    url: str = f"{settings.PIPEDRIVE_BASE_URL}persons"


class PipedriveOrganizationAbstract(PipedriveAbstractModel):
    url: str = f"{settings.PIPEDRIVE_BASE_URL}organizations"


class PipedriveNoteAbstract(PipedriveAbstractModel):
    url: str = f"{settings.PIPEDRIVE_BASE_URL}notes"

    def get(self, **kwargs):
        if kwargs:
            if "person_id" in kwargs:
                self.url = f"{self.url}?person_id={kwargs.get('person_id')}"
            if "org_id" in kwargs:
                self.url = f"{self.url}?org_id={kwargs.get('org_id')}"
            if "org_id" not in kwargs and "person_id" not in kwargs:
                raise TypeError("Error: missing id")
            response = requests.get(self.url, params=self.params)
            return response.json()["data"]

    def create(self, **kwargs):
        if kwargs:
            if "person_id" in kwargs:
                self.url = f"{self.url}?person_id={kwargs.get('person_id')}"
            if "org_id" in kwargs:
                self.url = f"{self.url}?org_id={kwargs.get('org_id')}"
            else:
                raise TypeError("Error: missing id")
        response = requests.post(self.url, json=self.data.dict(), params=self.params)
        return response.json()

    def update(self, **kwargs):
        response = requests.put(
            f"{self.url}/{kwargs.get('id')}",
            json={"add_time": kwargs.get("add_time")},
            params=self.params,
        )
        return response.json()

    def all(self, **kwargs):
        response = requests.get(
            f"{self.url}?{kwargs.get('id_type')}={kwargs.get('id')}", params=self.params
        )
        return response.json()


### should move the all method to an abstract model and update the create methods of the activity
class PipedriveActivitiesAbstract(PipedriveAbstractModel):
    url: str = f"{settings.PIPEDRIVE_BASE_URL}activities"

    def all(self, **kwargs):
        response = requests.get(
            f"{self.url}?{kwargs.get('id_type')}={kwargs.get('id')}", params=self.params
        )
        return response.json()

    def create(self, **kwargs):
        if kwargs:
            if "person_id" in kwargs:
                self.url = f"{self.url}?person_id={kwargs.get('person_id')}"
            if "org_id" in kwargs:
                self.url = f"{self.url}?org_id={kwargs.get('org_id')}"
            else:
                raise TypeError("Error: missing id")
        response = requests.post(self.url, json=self.data.dict(), params=self.params)
        return response.json()


class PipedriveActivitiesTypesAbstract(PipedriveAbstractModel):
    url: str = f"{settings.PIPEDRIVE_BASE_URL}activityTypes"


class PipedriveDealsAbstract(PipedriveAbstractModel):
    url: str = f"{settings.PIPEDRIVE_BASE_URL}deals"


class PipedriveLeadsAbstract(PipedriveAbstractModel):
    url: str = f"{settings.PIPEDRIVE_BASE_URL}leads"


class PipedriveRecentAbstract(PipedriveAbstractModel):
    url: str = f"{settings.PIPEDRIVE_BASE_URL}recents"

    def get(self, **kwargs):
        response = requests.get(
            f"{self.url}?since_timestamp={self.data.dict()['since_timestamp']}&items={self.data.dict()['items']}",
            params=self.params,
        )
        return response.json()


class PipedriveFileAbstract(PipedriveAbstractModel):
    url: str = f"{settings.PIPEDRIVE_BASE_URL}files"


class PipedriveStageAbstract(PipedriveAbstractModel):
    url: str = f"{settings.PIPEDRIVE_BASE_URL}stages"
