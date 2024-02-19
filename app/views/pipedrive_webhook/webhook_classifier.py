from django.conf import settings
from rest_framework import status

from core_utils.choices import ChoiceCharEnum
from pipedrive.app.views.pipedrive_webhook.base_trigger_check_execute_actions import (
    NoActionNeeded,
)
from pipedrive.app.views.pipedrive_webhook.base_trigger_check_execute_actions import (
    TriggerAndActionMixin,
)
from pipedrive.app.views.pipedrive_webhook.create_user_and_investor_action import (
    CreateUserAndInvestor,
)
from pipedrive.app.views.pipedrive_webhook.investment_actions_in_view import (
    CreateInvestment,
)
from pipedrive.app.views.pipedrive_webhook.investment_actions_in_view import (
    RemoveInvestment,
)
from pipedrive.app.views.pipedrive_webhook.investment_actions_in_view import RevertDeal
from pipedrive.app.views.pipedrive_webhook.investment_actions_in_view import (
    UpdateInvestmentToWon,
)


stage_pipedrive_call_organized_id_sandbox: int = 4
stage_pipedrive_call_organized_id_prod: int = 2


class PipedriveCoreIntegration(ChoiceCharEnum):
    A0_BASE_CLASS = TriggerAndActionMixin
    A1_NO_ACTION_NEEDED = NoActionNeeded
    A2_REVERT_DEAL = RevertDeal
    A3_CREATE_USER_INVESTOR = CreateUserAndInvestor
    A4_CREATE_INVESTMENT = CreateInvestment
    A5_INVESTMENT_VALIDATED = UpdateInvestmentToWon
    A6_DELETE_INVESTMENT = RemoveInvestment


class PipedriveWebhookRouter:
    """
    This class will take as input the response of the webhook
    and classify it in the action it is supposed to do. Then it will perform the action in the core
    The actions are available here: https://www.notion.so/oneragtime/5d6cba28a408445b8838216b9ec3fca5?v=b1ca109f093a40a9b181e6e984f7ed4b&pvs=4
    """

    def __init__(
        self,
        response,
        user_data,
        investor_data,
        deal_id,
        investment_value,
        fundraising,
        missing_data,
        person_id,
        org_id,
    ) -> None:
        self.response = response
        self.user_data = user_data
        self.investor_data = investor_data
        self.deal_id = deal_id
        self.investment_value = investment_value
        self.fundraising = fundraising
        self.missing_data = missing_data
        self.action_on_core = PipedriveCoreIntegration.A0_BASE_CLASS.name
        self.stage_pipedrive_call_organized_id = (
            stage_pipedrive_call_organized_id_sandbox
            if settings.ENVIRONMENT_NAME in ["local", "dev", "test", "staging"]
            or settings.TESTING_ENV == True
            else stage_pipedrive_call_organized_id_prod
        )
        self.person_id = person_id
        self.org_id = org_id

    def evaluate_response_and_execute_action(self):
        for _, action in PipedriveCoreIntegration.choices():
            action_to_execute: TriggerAndActionMixin = action(
                self.response,
                self.user_data,
                self.investor_data,
                self.deal_id,
                self.investment_value,
                self.fundraising,
                self.missing_data,
                self.stage_pipedrive_call_organized_id,
                self.person_id,
                self.org_id,
            )
            if action_to_execute.check_trigger():
                response = action_to_execute.execute_action()
                return {
                    "response_data": response,
                    "status_code": status.HTTP_200_OK,
                }
