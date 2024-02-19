import json

from django.conf import settings

from core_auth.models.user import CustomUser
from core_management.models import Fundraising
from dealflow.investment.models.models import Investment
from dealflow.investment.models.models_choices import InvestmentStatusChoices
from entities.investor.choices import KYCStatusChoices
from entities.investor.factories import InvestmentFactory
from pipedrive.app.utils.pipedrive_utils import (
    check_if_deal_pipeline_is_clubdeal_and_return_core_url,
)
from pipedrive.app.utils.pipedrive_utils import update_deal_with_core_url
from pipedrive.sdk.investors.models.deal_model import PipedriveInvestorDeal
from pipedrive.sdk.investors.models.note_model import PipedriveInvestorNote
from pipedrive.sdk.investors.utils.lists import category_options_prod
from pipedrive.sdk.investors.utils.lists import category_options_sandbox
from pipedrive.sdk.investors.utils.lists import country_list_prod
from pipedrive.sdk.investors.utils.lists import country_list_sandbox
from pipedrive.sdk.investors.utils.lists import fundraising_list_choices_prod
from pipedrive.sdk.investors.utils.lists import fundraising_list_choices_sandbox
from pipedrive.sdk.investors.utils.lists import language_list_prod
from pipedrive.sdk.investors.utils.lists import language_list_sandbox
from pipedrive.sdk.investors.utils.lists import newsletter_options_prod
from pipedrive.sdk.investors.utils.lists import newsletter_options_sandbox
from pipedrive.sdk.investors.utils.lists import organization_category_list_options_prod
from pipedrive.sdk.investors.utils.lists import (
    organization_category_list_options_sandbox,
)
from pipedrive.sdk.investors.utils.lists import (
    organization_qualification_list_options_prod,
)
from pipedrive.sdk.investors.utils.lists import (
    organization_qualification_list_options_sandbox,
)
from pipedrive.sdk.investors.utils.lists import organization_type_list_options_prod
from pipedrive.sdk.investors.utils.lists import organization_type_list_options_sandbox
from pipedrive.sdk.investors.utils.lists import source_options_prod
from pipedrive.sdk.investors.utils.lists import source_options_sandbox
from pipedrive.sdk.investors.utils.lists import sub_source_options_prod
from pipedrive.sdk.investors.utils.lists import sub_source_options_sandbox
from pipedrive.sdk.secrets import settings as pipedrive_settings
from pipedrive.settings.master import PipedriveInvestorDealChoicesProd
from pipedrive.settings.test import PipedriveInvestorDealChoicesSandbox
from services.email.interface import EmailService
from services.slack.choices import MessageChoices
from services.slack.choices import OriginChoices
from services.slack.main import InvestorSlackSender


options_mapping: dict = {
    "country_list": {"prod": country_list_prod, "sandbox": country_list_sandbox},
    "category_list": {
        "prod": category_options_prod,
        "sandbox": category_options_sandbox,
    },
    "language_list": {"prod": language_list_prod, "sandbox": language_list_sandbox},
    "newsletter_list": {
        "prod": newsletter_options_prod,
        "sandbox": newsletter_options_sandbox,
    },
    "qualification_list": {
        "prod": organization_qualification_list_options_prod,
        "sandbox": organization_qualification_list_options_sandbox,
    },
    "type_list": {
        "prod": organization_type_list_options_prod,
        "sandbox": organization_type_list_options_sandbox,
    },
    "source_list": {"prod": source_options_prod, "sandbox": source_options_sandbox},
    "sub_source_list": {
        "prod": sub_source_options_prod,
        "sandbox": sub_source_options_sandbox,
    },
    "fundraising_list": {
        "prod": fundraising_list_choices_prod,
        "sandbox": fundraising_list_choices_sandbox,
    },
    "organization_category_list": {
        "prod": organization_category_list_options_prod,
        "sandbox": organization_category_list_options_sandbox,
    },
}


def return_correct_option(option):
    env_name = pipedrive_settings.ENVIRONMENT
    return options_mapping[f"{option}_list"][env_name]


def map_option_id(instance, options):
    for option in options:
        if option["id"] == int(instance):
            return [option["label"]]
    return []


def map_option(instance, options):
    if not instance:
        return []
    if instance == False:
        instance = "no"
    if instance == True:
        instance = "yes"
    for option in options:
        if option["label"] == instance.capitalize() or option["label"] == instance:
            return [option["id"]]
    return []


def return_env_choices(env):
    if "sandbox" in env["meta"]["host"]:
        return PipedriveInvestorDealChoicesSandbox.fundraising.value
    else:
        return PipedriveInvestorDealChoicesProd.fundraising.value


def return_fundraising(request_data) -> Fundraising:
    fundraising = request_data["current"][return_env_choices(request_data)]
    if fundraising:
        fundraising_name: str = map_option_id(
            fundraising,
            return_correct_option("fundraising"),
        )[0]
        return Fundraising.objects.get(name=fundraising_name)
    return None


def investment_exisits_in_core(investor, fundraising):
    return Investment.objects.filter(
        investor=investor, fundraising=fundraising
    ).exists()


def create_or_update_investment_and_send_slack_message(
    investor, investment_value, fundraising, deal_id, fees_percentage
):
    (
        investment_is_club_deal,
        core_url,
    ) = check_if_deal_pipeline_is_clubdeal_and_return_core_url(deal_id)
    if investment_is_club_deal:
        if investment_exisits_in_core(investor, fundraising):
            investment: Investment = Investment.objects.get(
                investor=investor, fundraising=fundraising
            )
            fundraising: Fundraising = Fundraising.objects.get(name=fundraising)
            send_slack_message_on_missing_field_and_update_deal_core_url_if_needed(
                investment.id,
                core_url,
                deal_id,
                investment_value,
                investor.id,
                fundraising.id,
                investor.name,
            )
            return investment
    return create_investment_and_update_core_url_in_pipedrive(
        investor, investment_value, fundraising, deal_id, fees_percentage
    )


def add_core_url(deal_id, investment_id):
    deal: PipedriveInvestorDeal = PipedriveInvestorDeal(id=deal_id)
    data = {
        "core_url": f"https://core.oneragtime.com/investments/{investment_id}",
    }
    json_data = json.dumps(data)
    encoded_data = json_data.encode("utf-8")
    deal.update(encoded_data)


def send_slack_message_on_missing_field_and_update_deal_core_url_if_needed(
    investment_id,
    core_url,
    deal_id,
    investment_value,
    investor_id,
    fundraising_id,
    investor_name,
):
    if str(investment_id) in core_url:
        slack_sender = InvestorSlackSender(deal_id=deal_id, investment_id=investment_id)
        slack_sender.send(MessageChoices.update_deal_error_existing_in_core.name)
        revert_deal_to_potential_deal_stage(deal_id)
        response_text = (
            f"[Pipedrive] This Deal was moved to Commited. However, there is no  SA signed document in core, so the Deal has been moved back to potential deal",
        )
        PipedriveInvestorNote.create_deal_note(deal_id, response_text)
        add_core_url(deal_id, investment_id)
    else:
        deal: PipedriveInvestorDeal = PipedriveInvestorDeal(id=deal_id)
        payload: dict = {
            "core_url": f"https://core.oneragtime.com/investments/{investment_id}"
        }
        deal.update(payload)
        slack_sender = InvestorSlackSender(
            deal_id=deal_id,
            investment_id=investment_id,
            investor_id=investor_id,
            fundraising_id=fundraising_id,
            investment_value=investment_value,
            investor_name=investor_name,
        )
        slack_sender.send(MessageChoices.link_investment.name)


def create_investment_and_update_core_url_in_pipedrive(
    investor, investment_value, fundraising, deal_id, fees_percentage
):
    investment: Investment = InvestmentFactory(
        investor=investor,
        committed_amount=investment_value,
        status=InvestmentStatusChoices.intentional.name,
        fundraising=fundraising,
        fees_percentage=fees_percentage,
    )
    investment.send_slack_message_on_create(origin=OriginChoices.Pipedrive.name)
    update_deal_with_core_url(deal_id, investment.id)
    return investment


def send_email_to_investor(
    investor, user, investor_existed_in_core, email, person_name
):
    investor_has_completed_kyc = investor.kyc.status in [
        KYCStatusChoices.validated.name,
        KYCStatusChoices.refused.name,
    ]
    if not investor_existed_in_core:
        EmailService.send_reset_password_email(user)

    elif not investor_has_completed_kyc:
        EmailService.send_update_your_kyc_to_investor(
            email,
            investor,
            user,
        )


def send_notification_investor_created(investor_id, investor_name):
    note_text: str = (
        f"Investor created: https://core.oneragtime.com/investors/{investor_id}. Investor KYC not validated"
    )
    PipedriveInvestorNote.create_organization_note(investor_name, note_text)
    slack_sender = InvestorSlackSender(
        investor_id=investor_id, investor_name=investor_name
    )
    slack_sender.send(MessageChoices.investor_created.name)


def send_notification_user_created(user_id, user_name):
    slack_sender = InvestorSlackSender(user_id=user_id, user_name=user_name)
    slack_sender.send(MessageChoices.user_created.name)


def revert_deal_to_potential_deal_stage(deal_id):
    stage_pipedrive_potential_deal_id_sandbox: int = 5
    stage_pipedrive_potential_deal_id_prod: int = 3
    stage_pipedrive_potential_deal_id = (
        stage_pipedrive_potential_deal_id_sandbox
        if settings.ENVIRONMENT_NAME in ["local", "dev", "test", "staging"]
        or settings.TESTING_ENV == True
        else stage_pipedrive_potential_deal_id_prod
    )
    deal = PipedriveInvestorDeal(id=deal_id)
    deal.update({"stage_id": stage_pipedrive_potential_deal_id})


def revert_deal_to_committed_sa_sent_stage(deal_id):
    stage_pipedrive_commited_sa_sent_id_sandbox: int = 6
    stage_pipedrive_commited_sa_sent_id_prod: int = 27
    stage_pipedrive_commited_sa_sent_id = (
        stage_pipedrive_commited_sa_sent_id_sandbox
        if settings.ENVIRONMENT_NAME in ["local", "dev", "test", "staging"]
        or settings.TESTING_ENV == True
        else stage_pipedrive_commited_sa_sent_id_prod
    )
    deal = PipedriveInvestorDeal(id=deal_id)
    deal.update({"stage_id": stage_pipedrive_commited_sa_sent_id, "status": "open"})
    data: dict = {
        "deal_id": deal_id,
        "content": f"[Pipedrive] This Deal was moved to Commited. However, there is no  SA signed document in core, so the Deal has been moved back to sent",
    }
    note = PipedriveInvestorNote(**data)
    note.create()


def revert_deal_to_call_organized_stage_and_add_note(deal_id, error_keys):
    stage_pipedrive_call_organized_id_sandbox: int = 4
    stage_pipedrive_call_organized_id_prod: int = 2
    stage_pipedrive_call_organized_id = (
        stage_pipedrive_call_organized_id_sandbox
        if settings.ENVIRONMENT_NAME in ["local", "dev", "test", "staging"]
        or settings.TESTING_ENV == True
        else stage_pipedrive_call_organized_id_prod
    )
    deal = PipedriveInvestorDeal(id=deal_id)
    deal.update({"stage_id": stage_pipedrive_call_organized_id})
    data: dict = {
        "deal_id": deal_id,
        "content": f"[Pipedrive] This Deal was moved to Potential deal, but there is missing data: {error_keys}. It has been moved back to Stage Call Organized",
    }
    note = PipedriveInvestorNote(**data)
    note.create()


def get_phone_number(user: CustomUser):
    if user.contact_info != None:
        if type(user.contact_info.phone_number) == str:
            return user.contact_info.phone_number
        if (
            type(user.contact_info.phone_number) != str
            and user.contact_info.phone_number != None
        ):
            return f"{user.contact_info.phone_number.country_code} {user.contact_info.phone_number.national_number}"
        if user.contact_info.phone_number == None:
            return "not found"
        return user.phone_number
