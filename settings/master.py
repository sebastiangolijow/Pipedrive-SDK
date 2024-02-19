from pipedrive.sdk.dealflow.utils.pipe_choices import (
    PipedriveDealflowContactChoicesProd,
)
from pipedrive.sdk.dealflow.utils.pipe_choices import (
    PipedriveDealflowOrganizationChoicesProd,
)
from pipedrive.sdk.investors.utils.pipe_choices import (
    PipedriveInvestorContactChoicesProd,
)
from pipedrive.sdk.investors.utils.pipe_choices import PipedriveInvestorDealChoicesProd
from pipedrive.sdk.investors.utils.pipe_choices import (
    PipedriveInvestorOrganizationChoicesProd,
)
from pipedrive.settings.base import BaseSettings


class MasterSettings(BaseSettings):
    ENVIRONMENT = "prod"
    PIPEDRIVE_BASE_URL = "https://oneragtimesas.pipedrive.com/api/v1/"
    PIPEDRIVE_INVESTORS_API_TOKEN = "ef864e8ea35d5554caf4667ef8564368a7c01b77"
    PIPEDRIVE_DEALFLOW_API_TOKEN = "4b9a5a4c5aea9063ccbf7deedf65c9482b20d9eb"
    PIPEDRIVE_CONTACT_INVESTOR_CHOICES = PipedriveInvestorContactChoicesProd
    PIPEDRIVE_ORGANIZATION_INVESTOR_CHOICES = PipedriveInvestorOrganizationChoicesProd
    PIPEDRIVE_ORGANIZATION_DEALFLOW_CHOICES = PipedriveDealflowOrganizationChoicesProd
    PIPEDRIVE_CONTACT_DEALFLOW_CHOICES = PipedriveDealflowContactChoicesProd
    PIPEDRIVE_DEAL_INVESTOR_CHOICES = PipedriveInvestorDealChoicesProd
