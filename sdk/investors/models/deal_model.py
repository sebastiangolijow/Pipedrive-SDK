import json

import requests

from core_utils.choices import ChoiceCharEnum
from pipedrive.sdk.abstracts.pipe_abstract_model import replace_keys_if_choices
from pipedrive.sdk.investors.models.abstract_model import BaseInvestorDealModel
from pipedrive.sdk.investors.models.abstract_model import BaseInvestorDealModelField
from pipedrive.sdk.investors.serializers import DealFieldInvestorSerializerCreate
from pipedrive.sdk.investors.serializers import DealFieldInvestorSerializerUpdate
from pipedrive.sdk.investors.serializers import DealInvestorSerializerCreate
from pipedrive.sdk.investors.serializers import DealInvestorSerializerUpdate
from pipedrive.sdk.investors.utils.lists import fundraising_list_choices_prod
from pipedrive.sdk.investors.utils.lists import fundraising_list_choices_sandbox
from pipedrive.sdk.secrets import settings


class PipedriveInvestorDealFields(BaseInvestorDealModelField):
    serializer_created = DealFieldInvestorSerializerCreate
    serializer_updated = DealFieldInvestorSerializerUpdate


class PipedriveInvestorDeal(BaseInvestorDealModel):
    serializer_created = DealInvestorSerializerCreate
    serializer_updated = DealInvestorSerializerUpdate
    choices = settings.PIPEDRIVE_DEAL_INVESTOR_CHOICES
    fields = PipedriveInvestorDealFields
    options_to_validate = [
        fundraising_list_choices_prod,
        fundraising_list_choices_sandbox,
    ]

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
        if "status_won" in data.keys():
            data["status"] = data["status_won"]
        response = requests.put(
            f"{self.url}/{self.data.id}", data=data, params=self.params
        )
        return response.json()
