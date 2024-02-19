import json
from typing import Union

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from core_management.factories.factory_kyc import KYCFromEmailFactory
from core_management.models import KYC
from core_management.models import Fundraising
from entities.investor.models.models import Investor
from pipedrive.app.serializers.webhook_serializer import DealSerializer
from pipedrive.app.utils.pipedrive_utils import (
    get_phone_number_and_email_from_pipedrive_user_name,
)
from pipedrive.app.utils.pipedrive_utils import is_human_action
from pipedrive.app.utils.pipedrive_utils import return_organization_name
from pipedrive.app.utils.utils import map_option_id
from pipedrive.app.utils.utils import return_correct_option
from pipedrive.app.utils.utils import return_fundraising
from pipedrive.app.views.pipedrive_webhook.webhook_classifier import (
    PipedriveWebhookRouter,
)
from pipedrive.sdk.investors.models.person_model import PipedriveInvestorContact


class PipedriveWebhookInitialValidatorMixin:
    """
    Description:
    This mixin is used in the following view (PipedriveInvestorWebhook) to validate the data and set it as attributes so we can use it in the router (PipedriveWebhookRouter).

    Data flow:
    From Pipedrive to Core.

    Methods:
    We have two methods:
    - validate_and_assign_serializer_data to validate the data and serialize it.
    All the data is validated through the serializer except the email as it is not coming in the first request. We are getting it with the method: get_phone_number_and_email_from_pipedrive_user_name
    If data is invalid or we have missing data, it will set it as attribute and use it in the router.
    - return_user_and_investor_data it return the data that we need to create the user and investor in the following class inside the router: CreateUserAndInvestor
    """

    email: Union[str, bool] = False
    phone: Union[str, bool] = False
    person_name: Union[str, bool] = False
    fundraising: Union[Fundraising, bool] = False
    investment_value: Union[float, bool] = False
    deal_id: Union[int, bool] = False
    org_id: Union[int, bool] = False
    user_data: Union[dict, bool] = False
    investor_data: Union[dict, bool] = False
    response: dict = False
    missing_data: Union[list, bool] = False

    def return_user_and_investor_data(self):
        split: list = self.person_name.split(" ")
        person = PipedriveInvestorContact(id=self.response["current"]["person_id"])
        person_f = person.get()
        language = (
            person_f["data"][person.choices.language.value]
            if person_f["data"][person.choices.language.value] != None
            else 0
        )
        language_f = map_option_id(
            language,
            return_correct_option("language"),
        )
        user_data: dict = {
            "first_name": split[0],
            "last_name": split[-1],
            "email": self.email,
            "phone": self.phone,
            "language": language_f[0] if language_f != [] else [],
        }
        try:
            kyc = Investor.objects.get(
                name=return_organization_name(self.person_id, self.person_name)
            ).kyc
        except:
            kyc = KYC.get_by_email_or_company_name(
                self.email, return_organization_name(self.person_id, self.person_name)
            )
        if not kyc:
            kyc = KYCFromEmailFactory(email=self.email) if self.email else None

        investor_data: dict = {
            "name": return_organization_name(self.person_id, self.person_name),
            "kyc": kyc,
        }
        return investor_data, user_data

    def validate_and_assign_serializer_data(self, serializer):
        self.fundraising: Fundraising = return_fundraising(self.response)
        if serializer.is_valid():
            serialized_data = serializer.validated_data
            self.person_name: str = serialized_data["person_name"]
            self.deal_id: int = serialized_data["id"]
            self.investment_value: float = serialized_data["value"]
            self.stage_id: int = serialized_data["stage_id"]
            self.person_id: int = serialized_data["person_id"]
            self.org_id: int = serialized_data["org_id"]
            (
                self.email,
                self.phone,
            ) = get_phone_number_and_email_from_pipedrive_user_name(self.person_name)
            self.investor_data, self.user_data = self.return_user_and_investor_data()
            self.missing_data = (
                ["email", "fundraising"]
                if not self.email and not self.fundraising
                else (
                    ["email"]
                    if not self.email
                    else ["fundraising"] if not self.fundraising else None
                )
            )
        else:
            error_keys = list(serializer.errors.keys())
            self.missing_data = error_keys


class PipedriveInvestorWebhook(
    generics.CreateAPIView, PipedriveWebhookInitialValidatorMixin
):
    def post(self, request, *args, **kwargs):
        try:
            decode_body = request.body.decode("utf8").replace("'", '"')
            self.response = json.loads(decode_body)
            serializer = DealSerializer(data=self.response["current"])
            if is_human_action(self.response):
                self.validate_and_assign_serializer_data(serializer)
                router = PipedriveWebhookRouter(
                    response=self.response,
                    user_data=self.user_data,
                    investor_data=self.investor_data,
                    deal_id=self.deal_id,
                    investment_value=self.investment_value,
                    fundraising=self.fundraising,
                    missing_data=self.missing_data,
                    person_id=self.response["current"]["person_id"],
                    org_id=self.org_id,
                )
                response = router.evaluate_response_and_execute_action()
            else:
                response: dict = {
                    "response_data": "No action needed",
                    "status_code": 200,
                }
            return Response(
                response["response_data"],
                status=response["status_code"],
            )
        except Exception as e:
            return Response(
                str(e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
