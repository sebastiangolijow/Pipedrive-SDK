from pipedrive.sdk.dealflow.models.abstract_model import BaseDealflowOrganizationModel
from pipedrive.sdk.dealflow.models.abstract_model import (
    BaseDealflowOrganizationModelField,
)
from pipedrive.sdk.dealflow.serializers import ContactDealflowFieldSerializerUpdate
from pipedrive.sdk.dealflow.serializers import OrganizationDealflowSerializerCreate
from pipedrive.sdk.dealflow.serializers import OrganizationDealflowSerializerUpdate
from pipedrive.sdk.dealflow.utils.lists import arias_scope_dealflow_options_prod
from pipedrive.sdk.dealflow.utils.lists import arias_scope_dealflow_options_sandbox
from pipedrive.sdk.dealflow.utils.lists import business_model_dealflow_options_prod
from pipedrive.sdk.dealflow.utils.lists import business_model_dealflow_options_sandbox
from pipedrive.sdk.dealflow.utils.lists import deal_owner_dealflow_options_prod
from pipedrive.sdk.dealflow.utils.lists import deal_owner_dealflow_options_sandbox
from pipedrive.sdk.dealflow.utils.lists import event_dealflow_options_prod
from pipedrive.sdk.dealflow.utils.lists import event_dealflow_options_sandbox
from pipedrive.sdk.dealflow.utils.lists import female_c_level_dealflow_options_prod
from pipedrive.sdk.dealflow.utils.lists import female_c_level_dealflow_options_sandbox
from pipedrive.sdk.dealflow.utils.lists import sector_dealflow_options_prod
from pipedrive.sdk.dealflow.utils.lists import sector_dealflow_options_sandbox
from pipedrive.sdk.dealflow.utils.lists import source_dealflow_options_prod
from pipedrive.sdk.dealflow.utils.lists import source_dealflow_options_sandbox
from pipedrive.sdk.dealflow.utils.lists import stage_dealflow_options_prod
from pipedrive.sdk.dealflow.utils.lists import stage_dealflow_options_sandbox
from pipedrive.sdk.secrets import settings


class PipedriveDealflowOrganizationFields(BaseDealflowOrganizationModelField):
    serializer_created = OrganizationDealflowSerializerCreate
    serializer_updated = ContactDealflowFieldSerializerUpdate


class PipedriveDealflowOrganization(BaseDealflowOrganizationModel):
    serializer_created = OrganizationDealflowSerializerCreate
    serializer_updated = OrganizationDealflowSerializerUpdate
    choices = settings.PIPEDRIVE_ORGANIZATION_DEALFLOW_CHOICES
    fields = PipedriveDealflowOrganizationFields
    options_to_validate = [
        source_dealflow_options_sandbox,
        source_dealflow_options_prod,
        event_dealflow_options_sandbox,
        event_dealflow_options_prod,
        deal_owner_dealflow_options_sandbox,
        deal_owner_dealflow_options_prod,
        female_c_level_dealflow_options_sandbox,
        female_c_level_dealflow_options_prod,
        sector_dealflow_options_sandbox,
        sector_dealflow_options_prod,
        business_model_dealflow_options_sandbox,
        business_model_dealflow_options_prod,
        stage_dealflow_options_sandbox,
        stage_dealflow_options_prod,
        arias_scope_dealflow_options_sandbox,
        arias_scope_dealflow_options_prod,
    ]
