from pipedrive.sdk.investors.models.abstract_model import BaseInvestorOrganizationModel
from pipedrive.sdk.investors.models.abstract_model import (
    BaseInvestorOrganizationModelField,
)
from pipedrive.sdk.investors.serializers import ContactInvestorFieldSerializer
from pipedrive.sdk.investors.serializers import ContactInvestorFieldSerializerUpdate
from pipedrive.sdk.investors.serializers import OrganizationInvestorSerializerCreate
from pipedrive.sdk.investors.serializers import OrganizationInvestorSerializerUpdate
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
from pipedrive.sdk.secrets import settings


class PipedriveInvestorOrganizationFields(BaseInvestorOrganizationModelField):
    serializer_created = ContactInvestorFieldSerializer
    serializer_updated = ContactInvestorFieldSerializerUpdate


class PipedriveInvestorOrganization(BaseInvestorOrganizationModel):
    serializer_created = OrganizationInvestorSerializerCreate
    serializer_updated = OrganizationInvestorSerializerUpdate
    choices = settings.PIPEDRIVE_ORGANIZATION_INVESTOR_CHOICES
    fields = PipedriveInvestorOrganizationFields
    options_to_validate = [
        organization_type_list_options_sandbox,
        organization_qualification_list_options_sandbox,
        organization_category_list_options_sandbox,
        organization_type_list_options_prod,
        organization_qualification_list_options_prod,
        organization_category_list_options_prod,
    ]

    def get_or_create_org(self):
        name: str = self.data.dict()["name"]
        found = self.filter(name=name)
        if len(found["data"]["items"]) > 0:
            return f"Organization GET: {name}", found["data"]["items"][0]["item"]["id"]
        else:
            response = self.create()
            return f"Organization CREATED: {name}", response["data"]["id"]
