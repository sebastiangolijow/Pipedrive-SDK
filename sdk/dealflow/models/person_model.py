from pipedrive.sdk.dealflow.models.abstract_model import BaseDealflowContactModel
from pipedrive.sdk.dealflow.models.abstract_model import BaseDealflowContactModelField
from pipedrive.sdk.dealflow.serializers import ContactDealflowFieldSerializer
from pipedrive.sdk.dealflow.serializers import ContactDealflowFieldSerializerUpdate
from pipedrive.sdk.dealflow.serializers import ContactDealflowSerializerCreate
from pipedrive.sdk.dealflow.serializers import ContactDealflowSerializerUpdate
from pipedrive.sdk.secrets import settings


class PipedriveDealflowContactFields(BaseDealflowContactModelField):
    """
    Represents the 'Person Fields' entity in Pipedrive and provides methods to manage person fields.

    Attributes:
        url (str): The API endpoint URL for the 'Person Fields' entity in Pipedrive.
        serializer_created (Type[BaseModel]): The serializer class used for creating new person fields.
        serializer_updated (Type[BaseModel]): The serializer class used for updating existing person fields.

    Methods:
        all(self) -> List[Dict[str, Any]]: Retrieve all person fields.
        create(self) -> Dict[str, Any]: Create a new person field.
        get(self, field_id: int) -> Dict[str, Any]: Retrieve a specific person field.
        update(self, field_id: int, data: Dict[str, Any]) -> Dict[str, Any]: Update an existing person field.
        delete(self, field_id: int) -> Dict[str, Any]: Delete an existing person field.

    Raises:
        requests.exceptions.RequestException: If an error occurs while making the API request.
        KeyError: If the response does not contain the expected data field.
    """

    serializer_created = ContactDealflowFieldSerializer
    serializer_updated = ContactDealflowFieldSerializerUpdate


class PipedriveDealflowContact(BaseDealflowContactModel):
    """
    Represents the 'Person' entity in Pipedrive and provides methods to manage person records.

    Attributes:
        url (str): The API endpoint URL for the 'Person' entity in Pipedrive.
        serializer_created (Type[BaseModel]): The serializer class used for creating new person records.
        serializer_updated (Type[BaseModel]): The serializer class used for updating existing person records.
        choices (Enum): The enumeration class representing the available choices for person fields.

    Methods:
        all(self) -> List[Dict[str, Any]]: Retrieve all person records.
        create(self) -> Dict[str, Any]: Create a new person record.
        get(self) -> Dict[str, Any]: Retrieve a specific person record.
        filter(self, search_term: str) -> List[Dict[str, Any]]: Filter person records based on a search term.
        update(self, data: Union[Dict[str, Any], bytes]) -> Dict[str, Any]: Update an existing person record.
        delete(self) -> Dict[str, Any]: Delete an existing person record.
        get_custom_fields(self) -> Dict[str, Any]: Retrieve all custom fields for person entity.
        add_custom_fields(self) -> Dict[str, Any]: Add new custom fields for person entity.
        delete_custom_fields(self) -> Dict[str, Any]: Delete existing custom fields for person entity.

    Raises:
        requests.exceptions.RequestException: If an error occurs while making the API request.
        KeyError: If the response does not contain the expected data field.
    """

    serializer_created = ContactDealflowSerializerCreate
    serializer_updated = ContactDealflowSerializerUpdate
    fields = PipedriveDealflowContactFields
    choices = settings.PIPEDRIVE_CONTACT_DEALFLOW_CHOICES
