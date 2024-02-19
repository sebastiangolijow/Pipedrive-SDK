from pipedrive.sdk.investors.models.abstract_model import BaseInvestorContactModel
from pipedrive.sdk.investors.models.abstract_model import BaseInvestorContactModelField
from pipedrive.sdk.investors.serializers import ContactInvestorFieldSerializer
from pipedrive.sdk.investors.serializers import ContactInvestorFieldSerializerUpdate
from pipedrive.sdk.investors.serializers import ContactInvestorSerializerCreate
from pipedrive.sdk.investors.serializers import ContactInvestorSerializerUpdate
from pipedrive.sdk.investors.utils.lists import category_options_prod
from pipedrive.sdk.investors.utils.lists import category_options_sandbox
from pipedrive.sdk.investors.utils.lists import country_list_prod
from pipedrive.sdk.investors.utils.lists import country_list_sandbox
from pipedrive.sdk.investors.utils.lists import language_list_prod
from pipedrive.sdk.investors.utils.lists import language_list_sandbox
from pipedrive.sdk.investors.utils.lists import newsletter_options_prod
from pipedrive.sdk.investors.utils.lists import newsletter_options_sandbox
from pipedrive.sdk.investors.utils.lists import source_options_prod
from pipedrive.sdk.investors.utils.lists import source_options_sandbox
from pipedrive.sdk.investors.utils.lists import sub_source_options_prod
from pipedrive.sdk.investors.utils.lists import sub_source_options_sandbox
from pipedrive.sdk.investors.utils.lists import tu_vous_options_prod
from pipedrive.sdk.investors.utils.lists import tu_vous_options_sandbox
from pipedrive.sdk.secrets import settings


class PipedriveInvestorContactFields(BaseInvestorContactModelField):
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

    serializer_created = ContactInvestorFieldSerializer
    serializer_updated = ContactInvestorFieldSerializerUpdate


class PipedriveInvestorContact(BaseInvestorContactModel):
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

    serializer_created = ContactInvestorSerializerCreate
    serializer_updated = ContactInvestorSerializerUpdate
    fields = PipedriveInvestorContactFields
    choices = settings.PIPEDRIVE_CONTACT_INVESTOR_CHOICES
    options_to_validate = [
        country_list_sandbox,
        country_list_prod,
        language_list_sandbox,
        language_list_prod,
        source_options_sandbox,
        source_options_prod,
        sub_source_options_sandbox,
        sub_source_options_prod,
        newsletter_options_sandbox,
        newsletter_options_prod,
        category_options_sandbox,
        category_options_prod,
        tu_vous_options_prod,
        tu_vous_options_sandbox,
    ]
