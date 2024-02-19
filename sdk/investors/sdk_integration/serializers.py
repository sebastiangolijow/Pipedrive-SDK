from django.conf import settings as django_settings
from rest_framework import serializers

from core_auth.choices import PreferredNotificationsChoices
from core_auth.models import CustomUser
from pipedrive.app.utils.pipedrive_utils import map_fundraisings
from pipedrive.sdk.dealflow.utils.lists import business_model_dealflow_options_prod
from pipedrive.sdk.dealflow.utils.lists import business_model_dealflow_options_sandbox
from pipedrive.sdk.dealflow.utils.lists import stage_dealflow_options_prod
from pipedrive.sdk.dealflow.utils.lists import stage_dealflow_options_sandbox
from pipedrive.sdk.investors.utils.lists import category_options_prod
from pipedrive.sdk.investors.utils.lists import category_options_sandbox
from pipedrive.sdk.investors.utils.lists import country_list_prod
from pipedrive.sdk.investors.utils.lists import country_list_sandbox
from pipedrive.sdk.investors.utils.lists import language_list_prod
from pipedrive.sdk.investors.utils.lists import language_list_sandbox
from pipedrive.sdk.investors.utils.lists import newsletter_options_prod
from pipedrive.sdk.investors.utils.lists import newsletter_options_sandbox
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
from pipedrive.sdk.secrets import settings


stage_pipedrive_potential_deal_id_sandbox: int = 5
stage_pipedrive_potential_deal_id_prod: int = 3
stage_pipedrive_potential_deal_id = (
    stage_pipedrive_potential_deal_id_sandbox
    if django_settings.ENVIRONMENT_NAME in ["local", "dev", "test", "staging"]
    or django_settings.TESTING_ENV == True
    else stage_pipedrive_potential_deal_id_prod
)

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
    "business_models_list": {
        "prod": business_model_dealflow_options_prod,
        "sandbox": business_model_dealflow_options_sandbox,
    },
    "stage_list": {
        "prod": stage_dealflow_options_prod,
        "sandbox": stage_dealflow_options_sandbox,
    },
}


def return_correct_option(option) -> list:
    env_name = settings.ENVIRONMENT
    return options_mapping[f"{option}_list"][env_name]


def return_notification(option_list: list) -> str:
    if option_list:
        for instance in option_list:
            if instance in [PreferredNotificationsChoices.global_newsletter.name]:
                return "no"
    return "yes"


class InvestorDataSerializer(serializers.Serializer):
    """Serializer to create dict from instance of class Investor or data and Organization entity in pipedrive"""

    def __init__(self, instance=None, data=None, **kwargs):
        if data:
            data = {
                "name": f"{data['first_name']} {data['last_name']}",
                "qualification": map_option(
                    "private", return_correct_option("qualification")
                ),
                "type": map_option("investor", return_correct_option("type")),
            }
        if instance:
            data = {
                "name": instance.name,
                "investor_id": instance.id,
                "category": map_option(
                    instance.type, return_correct_option("category")
                ),
                "qualification": map_option(
                    "private", return_correct_option("qualification")
                ),
                "type": map_option("investor", return_correct_option("type")),
                "core_url": f"core.oneragtime.com/investors/{instance.id}",
            }
        super().__init__(data=data, **kwargs)

    name = serializers.CharField()
    investor_id = serializers.IntegerField(required=False, allow_null=True)
    type = serializers.ListField()
    qualification = serializers.ListField()
    core_url = serializers.CharField(required=False, allow_blank=True, allow_null=True)


def map_option(instance, options):
    if instance == False:
        instance = "no"
    if instance == True:
        instance = "yes"
    for option in options:
        if option["label"] == instance.capitalize() or option["label"] == instance:
            return [option["id"]]
    return []


class UserToContactSerializer(serializers.Serializer):
    """Serializer to create dict from instance of class CustomUser or data and create Contact entity in pipedrive"""

    def __init__(self, instance=None, data=None, **kwargs):
        if data:
            data = {
                "name": (
                    f"{data['first_name']} {data['last_name']}"
                    if "first_name" in data.keys()
                    else ""
                ),
                "first_name": data["first_name"] if "first_name" in data.keys() else "",
                "last_name": data["last_name"] if "last_name" in data.keys() else "",
                "type": "user",
                "email": data["email"] if "email" in data.keys() else "",
                "core_url": f"core.oneragtime.com/investors/{data['id']}",
                "org_id": data["org_id"] if "org_id" in data.keys() else None,
            }
        if instance:
            data = {
                "name": f"{instance.first_name} {instance.last_name}",
                "first_name": instance.first_name,
                "last_name": instance.last_name,
                "type": "user",
                "email": instance.email,
                "phone": self.get_phone(instance),
                "language": self.get_language(instance),
                "linkedin": (
                    instance.contact_info.links.linkedin
                    if instance.contact_info and instance.contact_info.links
                    else ""
                ),
                "newsletter": self.get_newsletter(instance),
                "category": self.get_category(),
                "source": self.get_source(),
                "sub_source": [],  ### ask loui
                "tu_vous": [],  ### ask loui
                "country": self.get_country(),
                "address": self.get_address(),
                "core_url": f"core.oneragtime.com/investors/{instance.id}",
                "org_id": self.get_org_id(),
            }
        super().__init__(data=data, **kwargs)

    name = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    type = serializers.CharField(default="user")
    email = serializers.EmailField()
    phone = serializers.CharField(allow_blank=True, allow_null=True)
    language = serializers.ListField()
    linkedin = serializers.CharField(allow_blank=True, allow_null=True)
    newsletter = serializers.ListField()
    category = serializers.ListField()
    source = serializers.ListField()
    sub_source = serializers.ListField()
    tu_vous = serializers.ListField()
    address = serializers.CharField(default="")
    core_url = serializers.CharField(required=False)
    country = serializers.ListField(required=False)
    org_id = serializers.IntegerField(required=False, allow_null=True)
    address = serializers.CharField(allow_blank=True, allow_null=True)

    def get_phone(self, obj: CustomUser):
        if obj.phone_number is not None:
            return f"{obj.phone_number}"
        if obj.contact_info is not None:
            if isinstance(obj.contact_info.phone_number, str):
                return f"{obj.contact_info.phone_number}"
            if (
                isinstance(obj.contact_info.phone_number, str)
                and obj.contact_info.phone_number is not None
            ):
                return f"{obj.contact_info.phone_number.national_number}"
            return ""

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_country(self):
        return map_option(
            self.__dict__["_kwargs"]["data"]["country"],
            return_correct_option("country"),
        )

    def get_language(self, obj):
        return map_option(
            obj.settings.preferred_language, return_correct_option("language")
        )

    def get_newsletter(self, obj):
        return map_option(
            return_notification(obj.settings.preferred_notifications),
            return_correct_option("newsletter"),
        )

    def get_category(self):
        return map_option("Main(s) contact(s)", return_correct_option("category"))

    def get_source(self):
        return map_option("core", return_correct_option("source"))

    def get_address(self):
        return self.__dict__["_kwargs"]["data"]["address"]

    def get_org_id(self):
        return self.__dict__["_kwargs"]["data"]["org_id"]


class InvestmentToDealSerializer(serializers.Serializer):
    """Serializer to validate data coming from investment to create deal in pipedrive"""

    def __init__(self, data=None, **kwargs):
        if data:
            data = {
                "title": f"{data.get('fundraising_name')} Deal",
                "status": data.get("status"),
                "currency": "EUR",
                "value": str(data.get("committed_amount")),
                "stage_id": stage_pipedrive_potential_deal_id,
                "fundraising": map_fundraisings(data.get("fundraising_name")),
                "fees_percentage": data.get("fees_percentage"),
                "core_url": f"https://core.oneragtime.com/investments/{data.get('id')}",
                "person_id": data.get("person_id"),
                "org_id": data.get("org_id"),
            }
        super().__init__(data=data, **kwargs)

    title = serializers.CharField()
    status = serializers.CharField()
    currency = serializers.CharField(default="user")
    value = serializers.CharField()
    stage_id = serializers.IntegerField()
    fundraising = serializers.ListField()
    fees_percentage = serializers.IntegerField()
    core_url = serializers.CharField()
    org_id = serializers.IntegerField(required=False, allow_null=True)
    person_id = serializers.IntegerField(required=False, allow_null=True)
