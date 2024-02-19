import requests
from pydantic import BaseModel

from pipedrive.sdk.secrets import settings
from pipedrive.sdk.utils.choices import ChoiceCharEnum


class PipeFieldModel:
    """
    Base class for interacting with custom fields in Pipedrive.

    In Pipedrive apart the actual entities, each entity has each own fields, Pipedrive
    has native fields as name, first_name, last_name, etc. But we can add our owns custom
    fields, this is the base model for the custom fields, each entity has it own model for
    custom fields treatment (e.g: class PipedriveContact --> PersonField, PipeOrganization --> OrganizationField)

    """

    url: str = settings.PIPEDRIVE_BASE_URL
    url_custom_field: str = ""
    api_token = settings.PIPEDRIVE_INVESTORS_API_TOKEN
    serializer_created = BaseModel
    serializer_updated = BaseModel
    choices = ChoiceCharEnum
    params: str = ""

    def __init__(self, **kwargs):
        """
        Initializes a new instance of the PipeFieldModel class.

        Args:
            **kwargs: The keyword arguments used to create or update the custom field.
            If the 'id' key is present, an update operation is performed;
            otherwise, a create operation is performed.
        """
        if not self.api_token:
            raise TypeError("not api key provided")
        else:
            self.params = {"api_token": self.api_token}
        if kwargs:
            if "id" in kwargs:
                self.data = self.serializer_updated(**kwargs)
            else:
                self.data = self.serializer_created(**kwargs)

    def get_custom_fields(self):
        """
        Retrieve all custom fields for the entity.

        Returns:
            dict: The custom fields data retrieved from the Pipedrive API.

        Raises:
            requests.exceptions.RequestException: If an error occurs while making the API request.
            KeyError: If the response does not contain the expected data field.
        """
        response = requests.get(self.url, params=self.params)
        return response.json()

    def add_custom_fields(self):
        """
        Add new custom fields for the entity.

        Returns:
            dict: The response data confirming the addition of custom fields from the Pipedrive API.

        Raises:
            requests.exceptions.RequestException: If an error occurs while making the API request.
            KeyError: If the response does not contain the expected data field.
        """
        response = requests.post(self.url, json=self.data.dict(), params=self.params)
        return response.json()

    def delete_custom_fields(self):
        """
        Delete existing custom fields for the entity.

        Returns:
            dict: The response data confirming the deletion of custom fields from the Pipedrive API.

        Raises:
            requests.exceptions.RequestException: If an error occurs while making the API request.
            KeyError: If the response does not contain the expected data field.
        """
        response = requests.post(f"{self.url}/{self.id}", params=self.params)
        return response.json()


class PipedriveContactFieldsAbstract(PipeFieldModel):
    url = settings.PIPEDRIVE_BASE_URL + "personFields"


class PipedriveOrganizationFieldAbstract(PipeFieldModel):
    url = settings.PIPEDRIVE_BASE_URL + "organizationFields"


class PipedriveDealFieldAbstract(PipeFieldModel):
    url: str = f"{settings.PIPEDRIVE_BASE_URL}dealFields"


class PipedriveActivityFieldAbstract(PipeFieldModel):
    url: str = f"{settings.PIPEDRIVE_BASE_URL}activityFields"
