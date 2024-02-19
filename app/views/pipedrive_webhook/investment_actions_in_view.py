from django.conf import settings

from core_auth.models.user import CustomUser
from core_management.models import Fundraising
from dealflow.investment.models.models import Investment
from dealflow.investment.models.models_choices import InvestmentStatusChoices
from dealflow.investment.utils.investments_utils import (
    create_investment_subscription_agreement,
)
from dealflow.investment.utils.investments_utils import (
    send_investment_subscription_agreement,
)
from entities.investor.models.models import Investor
from pipedrive.app.utils.pipedrive_utils import (
    check_if_deal_pipeline_is_clubdeal_and_return_core_url,
)
from pipedrive.app.utils.utils import add_core_url
from pipedrive.app.utils.utils import create_or_update_investment_and_send_slack_message
from pipedrive.app.utils.utils import revert_deal_to_call_organized_stage_and_add_note
from pipedrive.app.utils.utils import revert_deal_to_committed_sa_sent_stage
from pipedrive.app.utils.utils import revert_deal_to_potential_deal_stage
from pipedrive.app.utils.validators import ValidateCreateSubscriptionAgreement
from pipedrive.app.views.pipedrive_webhook.base_trigger_check_execute_actions import (
    TriggerAndActionMixin,
)
from pipedrive.sdk.investors.models.deal_model import PipedriveInvestorDeal
from pipedrive.sdk.investors.models.note_model import PipedriveInvestorNote
from pipedrive.sdk.investors.models.organization_model import (
    PipedriveInvestorOrganization,
)
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


class CreateInvestment(TriggerAndActionMixin):
    def check_trigger(self):
        return self.has_the_deal_been_updated_to_committed()

    def execute_action(self):
        return self.a2_create_investment_and_send_sa_if_needed()

    def has_the_deal_been_updated_to_committed(self):
        stage_pipedrive_commited_sa_sent_id_sandbox: int = 6
        stage_pipedrive_commited_sa_sent_id_prod: int = 27
        stage_pipedrive_commited_sa_sent_id = (
            stage_pipedrive_commited_sa_sent_id_sandbox
            if settings.ENVIRONMENT_NAME in ["local", "dev", "test", "staging"]
            or settings.TESTING_ENV == True
            else stage_pipedrive_commited_sa_sent_id_prod
        )
        return (
            self.response["current"]["stage_id"] == stage_pipedrive_commited_sa_sent_id
            and self.response["current"]["status"] == "open"
            and self.response["previous"]["stage_id"]
            == stage_pipedrive_potential_deal_id
        )

    def a2_create_investment_and_send_sa_if_needed(self):
        investor: Investor = self.return_core_investor_from_pipedrive_deal()
        if Investment.objects.filter(
            investor=investor, fundraising=self.fundraising
        ).exists():
            slack_sender = InvestorSlackSender(
                investor_id=investor.id,
                investor_name=investor.name,
                fundraising_name=self.fundraising.name,
                fundraising_id=self.fundraising.id,
            )
            slack_sender.send(MessageChoices.investment_already_exists.name)
            revert_deal_to_potential_deal_stage(self.deal_id)
            return f"Investment with Investor: {investor.name} and Fundraising: {self.fundraising.name} already exists."
        self.user = CustomUser.objects.get(email=self.user_data["email"])
        validator: ValidateCreateSubscriptionAgreement = (
            ValidateCreateSubscriptionAgreement(
                self.user, investor, self.fundraising, self.deal_id
            )
        )
        validation_error = validator.validate_conditions()
        if not validation_error:
            deal = PipedriveInvestorDeal()
            fees_percentage = self.response["previous"][
                deal.choices.fees_percentage.value
            ]
            self.investment = create_or_update_investment_and_send_slack_message(
                investor,
                self.investment_value,
                self.fundraising,
                self.deal_id,
                fees_percentage,
            )
            if self.investment.document_subscription_agreement == None:
                response = create_investment_subscription_agreement(
                    self.investment, self.user
                )
                if response:
                    slack_sender = InvestorSlackSender(
                        investor_id=investor.id,
                        investor_name=investor.name,
                    )
                    slack_sender.send(MessageChoices.kyc_missing_data.name)
                    return response
                send_investment_subscription_agreement(self.investment.id, self.user)
            return f"[Pipedrive Update] Investment successfully created:  core.oneragtime.com/investments/{self.investment.id}"
        else:
            revert_deal_to_potential_deal_stage(self.deal_id)
            slack_sender = InvestorSlackSender(
                deal_id=self.deal_id,
                validation_error=validation_error["error_message"],
            )
            slack_sender.send(MessageChoices.global_error_message.name)
            response_text = f"[Pipedrive] This Deal was moved to Commited. However, there is an error: {validation_error['error_message']}, so the Deal has been moved back to potential deal"
            PipedriveInvestorNote.create_deal_note(self.deal_id, response_text)
            return response_text

    def return_core_investor_from_pipedrive_deal(self):
        try:
            org_e: PipedriveInvestorOrganization = PipedriveInvestorOrganization(
                id=self.org_id
            )
            org: PipedriveInvestorOrganization = org_e.get()
            if org["data"][org_e.choices.core_url.value]:
                investor_id: int = int(
                    org["data"][org_e.choices.core_url.value].split("/")[-1]
                )
                investor: Investor = Investor.objects.get(id=investor_id)
            else:
                investor: Investor = Investor.objects.get(name=org["data"]["name"])
        except:
            investor: Investor = Investor.objects.get(
                kyc__email=self.user_data["email"]
            )
        return investor


class UpdateInvestmentToWon(TriggerAndActionMixin):
    def check_trigger(self):
        return self.has_the_deal_been_updated_to_won()

    def execute_action(self):
        return self.a3_investment_validated()

    def has_the_deal_been_updated_to_won(self):
        return (
            self.response["previous"]["status"] != "won"
            and self.response["current"]["status"] == "won"
        )

    def a3_investment_validated(self):
        _, core_url = check_if_deal_pipeline_is_clubdeal_and_return_core_url(
            self.deal_id
        )
        investment_id: int = int(core_url.split("/")[-1])
        investment: Investment = Investment.objects.get(id=investment_id)
        self.fundraising: Fundraising
        if investment.document_subscription_agreement:
            investment.status = InvestmentStatusChoices.sa_signed.name
            investment.save()
            slack_choice: MessageChoices = MessageChoices.deal_to_won_message.name
            response_text: str = (
                f"[Pipedrive Update] Investment: https://core.oneragtime.com/investments/{investment.id} updated status to SA Signed as Deal: https://oneragtimeinvestors.pipedrive.com/deal/{self.deal_id} has been moved to Won"
            )
        else:
            slack_choice: MessageChoices = MessageChoices.deal_to_won_error_message.name
            response_text: str = (
                f"[Pipedrive Update Error] https://oneragtimeinvestors.pipedrive.com/deal/{self.deal_id} from https://core.oneragtime.com/investors/{investment.investor.id} {self.investor_data['name']} in https://core.oneragtime.com/fundraisings/{self.fundraising.id}|{self.fundraising.name} has been moved to stage Won. However, there is no  SA signed document in core."
            )
            revert_deal_to_committed_sa_sent_stage(self.deal_id)
        slack_sender = InvestorSlackSender(
            deal_id=self.deal_id,
            investor_id=investment.investor.id,
            investment_id=investment_id,
            investor_name=self.investor_data["name"],
            fundraising_id=self.fundraising.id,
            fundraising_name=self.fundraising.name,
        )
        slack_sender.send(slack_choice)
        PipedriveInvestorNote.create_deal_note(self.deal_id, response_text)
        add_core_url(self.deal_id, investment_id)
        return response_text


class RemoveInvestment(TriggerAndActionMixin):
    def check_trigger(self):
        return self.has_the_deal_been_updated_to_lost()

    def execute_action(self):
        return self.a4_delete_investment()

    def has_the_deal_been_updated_to_lost(self):
        return (
            self.response["previous"]["status"] != "lost"
            and self.response["current"]["status"] == "lost"
        )

    def a4_delete_investment(self):
        _, core_url = check_if_deal_pipeline_is_clubdeal_and_return_core_url(
            self.deal_id
        )
        investment_id = None
        if core_url:
            investment_id: int = int(core_url.split("/")[-1])
            investment: Investment = Investment.objects.get(id=investment_id)
            investment.delete()
        slack_sender = InvestorSlackSender(deal_id=self.deal_id)
        slack_sender.send(MessageChoices.deal_to_lost_message.name)
        return f"[Pipedrive Update] Investment with id: {investment_id} successfully deleted"


class RevertDeal(TriggerAndActionMixin):
    def check_trigger(self):
        return self.should_deal_be_revert_to_prev_stage()

    def execute_action(self):
        return self.revert_deal_and_send_slack_message()

    def deal_updated_from_call_organized_to_potential_deal(self):
        original_state: int = (
            self.response["previous"]["stage_id"] if self.response["previous"] else None
        )
        next_state: int = self.response["current"]["stage_id"]
        return (
            original_state == self.stage_pipedrive_call_organized_id
            and next_state == stage_pipedrive_potential_deal_id
        )

    def should_deal_be_revert_to_prev_stage(self):
        return (
            self.missing_data
            and self.deal_updated_from_call_organized_to_potential_deal()
        )

    def revert_deal_and_send_slack_message(self):
        slack_sender = InvestorSlackSender(
            user_id=self.person_id,
            missing_field=self.missing_data,
        )
        slack_sender.send(MessageChoices.pipedrive_user_missing_fields.name)
        revert_deal_to_call_organized_stage_and_add_note(
            self.response["current"]["id"], self.missing_data
        )
        return f"[Pipedrive to Core Error] Missing deal {self.missing_data} in pipedrive deal: https://oneragtimeinvestors.pipedrive.com/deal/{self.response['current']['id']}"
