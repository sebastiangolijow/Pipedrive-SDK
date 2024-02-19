from datetime import datetime

from django.conf import settings
from rest_framework import status

from core_auth.factories import UserFactory
from core_auth.models.user import CustomUser
from core_management.factories.factory_kyc import KYCFromEmailFactory
from core_management.models import KYC
from entities.investor.choices import KYCStatusChoices
from entities.investor.factories import InvestorFromKYCFactory
from entities.investor.factories import UserInvestorRelationshipFactory
from entities.investor.models.models import Investor
from pipedrive.app.utils.pipedrive_utils import return_organization_name
from pipedrive.app.utils.pipedrive_utils import update_pipedrive_entities_with_core_url
from pipedrive.app.utils.utils import send_email_to_investor
from pipedrive.app.utils.utils import send_notification_investor_created
from pipedrive.app.utils.utils import send_notification_user_created
from pipedrive.app.views.pipedrive_webhook.base_trigger_check_execute_actions import (
    TriggerAndActionMixin,
)
from pipedrive.sdk.investors.models.note_model import PipedriveInvestorNote
from services.slack.choices import MessageChoices
from services.slack.main import InvestorSlackSender


class CreateUserAndInvestor(TriggerAndActionMixin):
    def check_trigger(self):
        return self.has_the_deal_been_updated_to_potential_deal()

    def execute_action(self):
        return self.a1_create_investor_and_user()

    def has_the_deal_been_updated_to_potential_deal(self):
        stage_pipedrive_potential_deal_id_sandbox: int = 5
        stage_pipedrive_potential_deal_id_prod: int = 3
        stage_pipedrive_potential_deal_id = (
            stage_pipedrive_potential_deal_id_sandbox
            if settings.ENVIRONMENT_NAME in ["local", "dev", "test", "staging"]
            or settings.TESTING_ENV == True
            else stage_pipedrive_potential_deal_id_prod
        )
        return (
            self.response["current"]["stage_id"] == stage_pipedrive_potential_deal_id
            and self.response["current"]["status"] == "open"
        )

    def get_or_create_user(self):
        return UserFactory(
            first_name=self.user_data["first_name"],
            last_name=self.user_data["last_name"],
            email=self.user_data["email"],
            onboarded_on=datetime.now(),
            is_active=True,
            phone_number=self.user_data["phone"],
        )

    def get_or_create_investor(self, kyc):
        return InvestorFromKYCFactory(
            name=return_organization_name(
                self.person_id,
                f"{self.user_data['first_name']} {self.user_data['last_name']}",
            ),
            kyc=kyc,
            status="on_trial",
        )

    def set_attributes(self):
        clubdeal_pipeline_id_prod: int = 1
        clubdeal_pipeline_id_sandbox: int = 2
        self.club_deal_pipeline_id = (
            clubdeal_pipeline_id_sandbox
            if settings.ENVIRONMENT_NAME in ["local", "dev", "test", "staging"]
            or settings.TESTING_ENV == True
            else clubdeal_pipeline_id_prod
        )
        self.user_existed_in_core = CustomUser.objects.filter(
            email=self.user_data["email"]
        ).exists()
        self.investor_exists_in_core = Investor.objects.filter(
            name=self.investor_data["name"]
        ).exists()
        self.user_count: int = CustomUser.objects.all().count()
        self.investor_count: int = Investor.objects.all().count()
        self.user: CustomUser = self.get_or_create_user()
        kyc: KYC = KYCFromEmailFactory(email=self.user_data["email"])
        self.investor: Investor = self.get_or_create_investor(kyc)
        self.person_name: str = (
            f"{self.user_data['first_name']} {self.user_data['last_name']}"
        )

    def check_if_user_was_created(self):
        return CustomUser.objects.all().count() == self.user_count + 1

    def check_if_investor_was_created(self):
        return Investor.objects.count() == self.investor_count + 1

    def check_investor_created_and_deal_club_deal_and_kyc_status(self):
        return (
            Investor.objects.count() == self.investor_count
            and self.response["current"]["pipeline_id"] == self.club_deal_pipeline_id
            and self.investor.kyc.status != KYCStatusChoices.validated.name
        )

    def a1_create_investor_and_user(self):
        self.set_attributes()
        if self.check_if_investor_was_created():
            send_notification_investor_created(self.investor.id, self.investor.name)
        if self.check_if_user_was_created():
            self.user.contact_info.first_name = self.user.first_name
            self.user.contact_info.last_name = self.user.last_name
            self.user.contact_info.phone_number = self.user_data["phone"]
            self.user.contact_info.signup_date = datetime.today()
            self.user.contact_info.save()
            self.user.settings.preferred_language = self.user_data["language"]
            if self.user.settings.preferred_language == []:
                self.user.settings.preferred_language = "EN"
            self.user.settings.save()
            send_notification_user_created(self.user.id, self.user.full_name)
        if self.check_if_investor_was_created() or self.check_if_user_was_created():
            relationship = UserInvestorRelationshipFactory(
                investor=self.investor,
                account=self.user,
            )
            self.user.acccount_management_relationship.relationship_id = relationship.id
            self.user.acccount_management_relationship.entity_type = "investor"
            self.user.acccount_management_relationship.save()
        send_email_to_investor(
            self.investor,
            self.user,
            self.investor_exists_in_core,
            self.user_data["email"],
            self.person_name,
        )
        if self.check_investor_created_and_deal_club_deal_and_kyc_status():
            slack_sender = InvestorSlackSender(
                investor_id=self.investor.id, investor_name=self.investor.name
            )
            slack_sender.send(MessageChoices.investor_kyc_is_not_validated.name)
            PipedriveInvestorNote.create_organization_note(
                self.investor.name,
                f"Investor: https://core.oneragtime.com/investors/{self.investor.id} has KYC but is not validated",
            )
            return f"[Pipedrive to Core error] <https://www.core.oneragtime.com/investors/{self.investor.id}|Investor> kyc is not validated"

        update_pipedrive_entities_with_core_url(
            self.user.id, self.investor.id, self.person_name, self.person_id
        )
        return "Entities successfully created"
