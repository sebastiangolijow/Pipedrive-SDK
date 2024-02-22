from django.conf import settings
from pydantic import ValidationError

from core_auth.models.user import CustomUser
from core_management.models import Fundraising
from core_management.utils import RequestTypeChoices
from dealflow.investment.models.models import Investment
from dealflow.investment.models.models_choices import InvestmentStatusChoices
from entities.investor.models.models import Investor
from pipedrive.app.utils.pipedrive_utils import check_deal_existence
from pipedrive.app.utils.pipedrive_utils import get_or_create_and_check_existing_org
from pipedrive.app.utils.pipedrive_utils import return_deal_id
from pipedrive.app.utils.pipedrive_utils import update_deal_with_core_url
from pipedrive.sdk.abstracts.core_to_pipedrive_integration import (
    CoreToPipedriveIntegration,
)
from pipedrive.sdk.investors.models.deal_model import PipedriveInvestorDeal
from pipedrive.sdk.investors.models.lead_model import PipedriveInvestorLead
from pipedrive.sdk.investors.models.note_model import PipedriveInvestorNote
from pipedrive.sdk.investors.sdk_integration.serializers import (
    InvestmentToDealSerializer,
)
from pipedrive.sdk.investors.sdk_integration.serializers import InvestorDataSerializer
from pipedrive.sdk.investors.sdk_integration.serializers import UserToContactSerializer
from services.slack.choices import MessageChoices
from services.slack.main import InvestorSlackSender


stage_pipedrive_potential_deal_id_sandbox: int = 5
stage_pipedrive_potential_deal_id_prod: int = 3
stage_pipedrive_potential_deal_id = (
    stage_pipedrive_potential_deal_id_sandbox
    if settings.ENVIRONMENT_NAME in ["local", "dev", "test", "staging"]
    or settings.TESTING_ENV == True
    else stage_pipedrive_potential_deal_id_prod
)

stage_pipedrive_commited_sa_sent_id_sandbox: int = 6
stage_pipedrive_commited_sa_sent_id_prod: int = 27
stage_pipedrive_commited_sa_sent_id = (
    stage_pipedrive_commited_sa_sent_id_sandbox
    if settings.ENVIRONMENT_NAME in ["local", "dev", "test", "staging"]
    or settings.TESTING_ENV == True
    else stage_pipedrive_commited_sa_sent_id_prod
)

stage_pipedrive_done_id_sandbox: int = 22
stage_pipedrive_done_id_prod: int = 26
stage_pipedrive_done_id = (
    stage_pipedrive_done_id_sandbox
    if settings.ENVIRONMENT_NAME in ["local", "dev", "test", "staging"]
    or settings.TESTING_ENV == True
    else stage_pipedrive_done_id_prod
)


class PipedriveDealUpdateIntegration(CoreToPipedriveIntegration):
    """Class to create / update Pipedrive deal when updating or creating investments in core"""

    @classmethod
    def sync(
        cls,
        investment_data: dict,
        request_type: str,
        prev_instance_data: dict or None = None,
    ):
        """Main entry for the class. It will receive investment_id, request_type and optional prev_instance_data dict from investment Signal"""
        try:
            if cls.verify_data(investment_data):
                deal_exists_in_pipedrive: bool = cls.check_trigger(investment_data)
                cls.perform_action(
                    investment_data,
                    deal_exists_in_pipedrive,
                    prev_instance_data,
                    request_type,
                )
        except BaseException as e:
            print("Pipedrive error: ", e)

    @classmethod
    def verify_data(cls, investment_data) -> bool:
        """Verify if data is correct in serializer"""
        serializer = InvestmentToDealSerializer(data=investment_data)
        return serializer.is_valid()

    @classmethod
    def check_trigger(cls, investment_data: dict) -> bool:
        """Check if investment already exists in Pipedrive as deal.
        If it exists we will proceed to update it or delete it according the request_type received
        """
        deal_exists_in_pipedrive = check_deal_existence(investment_data)
        return deal_exists_in_pipedrive

    @classmethod
    def return_pipedrive_deal(cls, investment_data: dict):
        """This method will receive an instance of an investment and return the corresponding deal in Pipedrive"""

        response = return_deal_id(
            investment_data["fundraising_name"], investment_data["id"]
        )
        deal_id: int = response
        found_deal = PipedriveInvestorDeal(id=deal_id)
        return found_deal

    @classmethod
    def perform_action(
        cls,
        investment_data: dict,
        deal_exists_in_pipedrive,
        prev_instance_dict,
        request_type,
    ) -> None or str:
        """If data is valid we will create or update deal depending on the check_trigger response"""
        if request_type == RequestTypeChoices.CREATE.name:
            return cls.create_deal(investment_data)
        if request_type == RequestTypeChoices.DELETE.name and deal_exists_in_pipedrive:
            return cls.delete_deal(investment_data)
        if request_type == RequestTypeChoices.UPDATE.name and deal_exists_in_pipedrive:
            return cls.update_deal(prev_instance_dict, investment_data)

    @classmethod
    def update_deal(cls, prev_instance_dict: dict, investment_data: dict):
        """Main class method to update deal, it will return the correct update function execute: update_status/update_sa/update_committed_amount"""
        deal_id: int = return_deal_id(
            investment_data["fundraising_name"], investment_data["id"]
        )
        deal_to_update = PipedriveInvestorDeal(id=deal_id)
        data_dict: dict = {
            "status": cls.update_status,
            "committed_amount": cls.update_committed_amount,
            "document_subscription_agreement": cls.update_sa,
        }
        for key, value in prev_instance_dict.items():
            if key == "status" and value != investment_data["status"]:
                data_dict["status"](deal_to_update, investment_data, deal_id)
            elif (
                key == "committed_amount"
                and value != investment_data["committed_amount"]
            ):
                data_dict["committed_amount"](deal_to_update, investment_data, deal_id)
            elif (
                investment_data["bill_count"] > 0
                and investment_data["document_subscription_agreement"]
                and investment_data["status"] == InvestmentStatusChoices.transfered.name
            ):
                data_dict["document_subscription_agreement"](
                    deal_to_update, investment_data, deal_id
                )
        return True

    @classmethod
    def update_status(
        cls, deal_to_update, investment_data: dict, deal_id: int
    ) -> str or None:
        if investment_data["status"] not in [
            InvestmentStatusChoices.transfered.name,
        ]:
            data: dict = {"status": investment_data["status"]}
            if data["status"] == "sa_sent" or data["status"] == "sa_signed":
                data["stage_id"] = stage_pipedrive_commited_sa_sent_id
            response = deal_to_update.update(data)
            if response["success"]:
                slack_sender = InvestorSlackSender(
                    investment_id=investment_data["id"],
                    investor_id=investment_data["investor_id"],
                    investor_name=investment_data["investor_name"],
                    old_value=investment_data["status"],
                    field_modified="status",
                    field_modified_value=investment_data["status"],
                    deal_id=deal_id,
                )
                slack_sender.send(MessageChoices.investment_update_succeed.name)
                note_content: str = (
                    f"[Core] Modified investment status from Core. Change made by https://core.oneragtime.com/users/{investment_data['user_id']}"
                )
                PipedriveInvestorNote.create_deal_note(deal_id, note_content)
                return "Investment update succeed"
            return "Update Investment fail", cls.return_slack_error_message(
                investment_data
            )
        cls.return_slack_error_message(investment_data)

    @classmethod
    def update_committed_amount(
        cls, deal_to_update, investment_data: dict, deal_id
    ) -> str or None:
        if (
            investment_data["status"]
            not in [
                InvestmentStatusChoices.sa_signed.name,
                InvestmentStatusChoices.transfered.name,
            ]
            and investment_data["document_subscription_agreement"]
        ):
            data: dict = {"value": investment_data["committed_amount"]}
            response = deal_to_update.update(data)
            if response["success"]:
                slack_sender = InvestorSlackSender(
                    investment_id=investment_data["id"],
                    investor_id=investment_data["investor_id"],
                    investor_name=investment_data["investor_name"],
                    old_value=investment_data["committed_amount"],
                    field_modified="committed amount",
                    field_modified_value=investment_data["committed_amount"],
                    deal_id=deal_id,
                )
                slack_sender.send(MessageChoices.investment_update_succeed.name)
                note_content: str = (
                    f"[Core] Modified investment value from Core. Change made by https://core.oneragtime.com/users/{investment_data['user_id']}"
                )
                PipedriveInvestorNote.create_deal_note(deal_id, note_content)
                return "Investment update succeed"
            return "Update Investment fail", cls.return_slack_error_message(
                investment_data
            )
        else:
            cls.return_slack_error_message(investment_data)

    @classmethod
    def update_sa(cls, deal_to_update, investment_data: dict, deal_id):
        data: dict = {
            "status": "transferred",
            "status_won": "won",
            "stage_id": stage_pipedrive_done_id,
        }
        response = deal_to_update.update(data)
        fundraising: Fundraising = Fundraising.objects.get(
            name=investment_data["fundraising_name"]
        )
        if response["success"]:
            slack_sender = InvestorSlackSender(
                investment_id=investment_data["id"],
                investor_id=investment_data["investor_id"],
                investor_name=investment_data["investor_name"],
                fundraising_id=fundraising.id,
                fundraising_name=fundraising.name,
                deal_id=deal_id,
            )
            slack_sender.send(MessageChoices.investment_update_deal_to_won.name)
            note_content: str = (
                f"[Core] Deal moved to won automatically due Core to Pipedrive automation"
            )
            PipedriveInvestorNote.create_deal_note(deal_id, note_content)
            return "Investment update succeed"
        return "Update Investment fail", cls.return_slack_error_message(investment_data)

    @classmethod
    def return_slack_error_message(self, investment_data):
        slack_sender = InvestorSlackSender(
            investment_id=investment_data["id"],
            investor_id=investment_data["investor_id"],
            investor_name=investment_data["investor_name"],
        )
        slack_sender.send(MessageChoices.investment_update_error.name)

    @classmethod
    def create_deal(cls, investment_data: dict) -> None:
        """Create deal in pipedrive on stage potential deal when creating investment from core"""
        try:
            investor: Investor = Investor.objects.get(id=investment_data["investor_id"])
            user: CustomUser = CustomUser.objects.get(id=investment_data["user_id"])
            _, org_id = cls.get_or_create_organization(investor)

            data_to_serialize: dict = cls.return_user_data_to_serialize(
                investor, user, org_id
            )
            user_serializer = UserToContactSerializer(
                instance=user, data=data_to_serialize, partial=True
            )
            if user_serializer.is_valid():
                _, person_id = get_or_create_and_check_existing_org(
                    user_serializer.data
                )
            else:
                slack_sender = InvestorSlackSender(
                    error=str(user_serializer.errors),
                    investment_id=investment_data["id"],
                )
                slack_sender.send(MessageChoices.error_on_deal_creation.name)
            investment_data["person_id"] = person_id
            investment_data["org_id"] = org_id
            serializer = InvestmentToDealSerializer(data=investment_data)
            if serializer.is_valid():
                deal_data = serializer.validated_data
                deal_data["fees_percentage"] = f"{deal_data['fees_percentage']}%"
                deal: PipedriveInvestorDeal = PipedriveInvestorDeal(**deal_data)
                deal_response = deal.create()
                cls.add_core_url_and_send_notifications(deal_response, investment_data)
        except ValidationError as e:
            error: str = e.errors()[0]["loc"][0]
            slack_sender = InvestorSlackSender(
                error=error,
                investment_id=investment_data["id"],
            )
            slack_sender.send(MessageChoices.error_on_deal_creation.name)
        except BaseException as e:
            pass

    @classmethod
    def add_core_url_and_send_notifications(
        cls, deal_response, investment_data: dict
    ) -> None:
        update_deal_with_core_url(deal_response["data"]["id"], investment_data["id"])
        slack_sender = InvestorSlackSender(
            deal_id=deal_response["data"]["id"],
            investment_id=investment_data["id"],
        )
        slack_sender.send(MessageChoices.investment_created_in_core.name)
        note_content: str = (
            f"Deal created due an Investment creation in Core. Investment: https://core.oneragtime.com/investments/{investment_data['id']}"
        )
        PipedriveInvestorNote.create_deal_note(
            deal_response["data"]["id"], note_content
        )

    @classmethod
    def delete_deal(cls, investment_data: dict):
        deal_to_delete = cls.return_pipedrive_deal(investment_data)
        return deal_to_delete.delete()


class PipedriveInvestorIntegration(CoreToPipedriveIntegration):
    """Integration to integrate Investor and Investment views with Pipedrive"""

    @classmethod
    def sync(cls, investor: Investor, user: CustomUser):
        """Main entry for the class, it will receive investor and user instances from
        InvestorInvite view and create corresponding entities in Pipedrive"""
        try:
            if cls.verify_data(investor, user) and cls.check_trigger():
                cls.perform_action(investor, user)
        except BaseException as e:
            print("Pipedrive error: ", e)

    @classmethod
    def verify_data(cls, investor: Investor, user: CustomUser) -> bool:
        """Verify if data is correct in serializer"""
        investor_serializer = InvestorDataSerializer(instance=investor)
        data_to_serialize: dict = cls.return_user_data_to_serialize(investor, user)
        user_serializer = UserToContactSerializer(
            instance=user, data=data_to_serialize, partial=True
        )
        return investor_serializer.is_valid() and user_serializer.is_valid()

    @classmethod
    def check_trigger(cls):
        return True

    @classmethod
    def perform_action(cls, investor: Investor, user: CustomUser) -> None:
        """Create entities Organization from investor and contact from User"""
        response, org_id = cls.get_or_create_organization(investor)
        _, person_id = cls.get_or_create_contact(user, investor, org_id)
        if "CREATED" in response:
            cls.create_lead(investor, org_id, person_id)

    @classmethod
    def create_lead(cls, investor: Investor, org_id, person_id) -> None:
        """Create pipedrive lead and link it with contact and organization"""
        title: str = f"{investor.name} lead"
        data: dict = {
            "title": title,
            "organization_id": org_id,
            "person_id": person_id,
        }
        lead_ent: PipedriveInvestorLead = PipedriveInvestorLead()
        lead_exists: bool = len(lead_ent.filter(title=title)["data"]["items"]) > 0
        if not lead_exists:
            lead: PipedriveInvestorLead = PipedriveInvestorLead(**data)
            lead.create()
