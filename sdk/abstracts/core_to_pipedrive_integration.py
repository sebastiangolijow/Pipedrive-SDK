from rest_framework.serializers import Serializer

from core_auth.models.user import CustomUser
from entities.investor.models.models import Investor
from pipedrive.app.utils.pipedrive_utils import get_or_create_and_check_existing_org
from pipedrive.sdk.investors.models.organization_model import (
    PipedriveInvestorOrganization,
)
from pipedrive.sdk.investors.sdk_integration.serializers import InvestorDataSerializer
from pipedrive.sdk.investors.sdk_integration.serializers import UserToContactSerializer
from services.slack.choices import MessageChoices
from services.slack.main import InvestorSlackSender


class CoreToPipedriveIntegration:
    """
    This class mark the structure of how the Pipedrive integrations class should work.
    This class is inherit in the following classes that acts as Integrations between Core
    and Pipedrive: PipedriveInvestorIntegration, PipedriveUserJoinIntegration, PipedriveDealUpdateIntegration.
    """

    @classmethod
    def verify_data(cls, data, **kwargs):
        return True

    @classmethod
    def check_trigger(cls):
        return True

    @classmethod
    def perform_action(cls, data, **kwargs):
        pass

    @classmethod
    def sync(cls):
        try:
            if cls.verify_data() and cls.check_trigger():
                cls.perform_action()
        except BaseException as e:
            print("Pipedrive error: ", e)

    @classmethod
    def get_or_create_organization(cls, investor) -> None:
        serializer = InvestorDataSerializer(instance=investor)
        if serializer.is_valid():
            investor_data = serializer.validated_data
            organization: PipedriveInvestorOrganization = PipedriveInvestorOrganization(
                **investor_data
            )
            response, org_id = organization.get_or_create_org()
            if "CREATED" in response:
                slack_sender = InvestorSlackSender(
                    org_id=org_id,
                    person_name=investor_data["name"],
                )
                slack_sender.send(MessageChoices.organization_created_in_pipedrive.name)
            return response, org_id
        else:
            print("Validation errors:", serializer.errors)

    @classmethod
    def get_or_create_contact(cls, user, investor, org_id) -> None:
        data_to_serialize: dict = cls.return_user_data_to_serialize(
            investor, user, org_id
        )
        serializer = UserToContactSerializer(
            instance=user, data=data_to_serialize, partial=True
        )
        if serializer.is_valid():
            user_data = serializer.validated_data
            response, person_id = get_or_create_and_check_existing_org(user_data)
            if "CREATED" in response:
                slack_sender = InvestorSlackSender(
                    person_id=person_id,
                    person_name=user_data["name"],
                )
                slack_sender.send(MessageChoices.contact_created_in_pipedrive.name)
            return response, person_id
        else:
            print("Validation errors:", serializer.errors)

    @classmethod
    def return_user_data_to_serialize(
        cls, investor: Investor, user: CustomUser, org_id=None
    ) -> dict:
        country: str = (
            investor.kyc.country_of_residence.name
            if investor.kyc and investor.kyc.country_of_residence
            else ""
        )
        return {
            "id": investor.id,
            "city": (
                investor.kyc.representative_address.city
                if investor.kyc and investor.kyc.representative_address
                else user.contact_info.city
            ),
            "linkedin": (
                investor.links.linkedin
                if investor.links and investor.links.linkedin
                else " "
            ),
            "country": country,
            "address": (
                investor.kyc.representative_address.address_line_1
                if investor.kyc
                else ""
            ),
            "org_id": org_id,
        }
