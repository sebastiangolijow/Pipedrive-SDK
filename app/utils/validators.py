from rest_framework import status

from core_auth.models.user import CustomUser
from core_management.models import UserInvestorRelationship
from dealflow.fundraising.models.model_choices import FundraisingStatusChoices
from entities.investor.choices import KYCStatusChoices
from entities.investor.models.models import Investor
from pipedrive.sdk.investors.models.deal_model import PipedriveInvestorDeal


class CoreValidator:
    def __init__(self, user, investor, fundraising, deal_id):
        self.investor: Investor = investor
        self.user: CustomUser = user
        self.conditions: list = []
        self.fundraising = fundraising
        self.deal_id = deal_id

    def build_validators(self):
        pass

    def validate_conditions(self):
        self.build_validators()
        for option in self.conditions:
            if option["logic"]:
                return option
        return False


class ValidateCreateSubscriptionAgreement(CoreValidator):
    def build_validators(self):
        deal_ent = PipedriveInvestorDeal(id=self.deal_id)
        deal = deal_ent.get()
        fees_percentage = deal["data"][deal_ent.choices.fees_percentage.value]
        condition_1: dict = {
            "validator_name": "user_onboarded",
            "error_message": f"[Pipedrive to Core error] <https://www.core.oneragtime.com/users/{self.user.id}|{self.user.first_name} {self.user.last_name}> is not onboarded",
            "logic": self.user.onboarded_on == None,
        }
        condition_2: dict = {
            "validator_name": "user_investor_has_relation",
            "error_message": f"[Pipedrive to Core error] User Investor Relationship has no match",
            "logic": UserInvestorRelationship.objects.filter(
                account=self.user, investor=self.investor
            ).exists()
            == False,
        }
        condition_3: dict = {
            "validator_name": "investor_kyc_validated",
            "error_message": f"[Pipedrive to Core error] Investor kyc is not validated <https://www.core.oneragtime.com/investors/{self.investor.id}|{self.investor.name}>",
            "logic": self.investor.kyc.status != KYCStatusChoices.validated.name,
        }
        condition_4: dict = {
            "validator_name": "is_fundraising_open",
            "error_message": f"[Pipedrive to Core error] Fundraising is not 'Under Fundraising' <https://www.core.oneragtime.com/fundraisings/{self.fundraising.id}|{self.fundraising.name}>",
            "logic": self.fundraising.status != FundraisingStatusChoices.open.name,
        }
        condition_5: dict = {
            "validator_name": "deal_has_fees_percentage",
            "error_message": f"[Pipedrive to Core error] Deal is missing fees_percentage <https://oneragtimeinvestors-sandbox.pipedrive.com/deal/{self.deal_id}|Deal>",
            "logic": fees_percentage == None,
        }
        self.conditions = [
            condition_1,
            condition_2,
            condition_3,
            condition_4,
            condition_5,
        ]
