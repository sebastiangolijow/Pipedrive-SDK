from pipedrive.sdk.dealflow.utils.pipe_choices import (
    PipedriveDealflowContactChoicesSandbox,
)
from pipedrive.sdk.dealflow.utils.pipe_choices import (
    PipedriveDealflowOrganizationChoicesSandbox,
)
from pipedrive.sdk.investors.utils.pipe_choices import (
    PipedriveInvestorContactChoicesSandbox,
)
from pipedrive.sdk.investors.utils.pipe_choices import (
    PipedriveInvestorDealChoicesSandbox,
)
from pipedrive.sdk.investors.utils.pipe_choices import (
    PipedriveInvestorOrganizationChoicesSandbox,
)
from pipedrive.settings.base import BaseSettings


class TestSettings(BaseSettings):
    ENVIRONMENT = "sandbox"
    PIPEDRIVE_BASE_URL = "https://oneragtimesas-sandbox.pipedrive.com/api/v1/"
    PIPEDRIVE_DEALFLOW_API_TOKEN = "00fced2c05909faef2abc17fdb5b484d758a35cf"
    PIPEDRIVE_INVESTORS_API_TOKEN = "b00025c105d750b9d5770f0976b63c2ff4bf5a9e"
    PIPEDRIVE_CONTACT_INVESTOR_CHOICES = PipedriveInvestorContactChoicesSandbox
    PIPEDRIVE_CONTACT_DEALFLOW_CHOICES = PipedriveDealflowContactChoicesSandbox
    PIPEDRIVE_ORGANIZATION_DEALFLOW_CHOICES = (
        PipedriveDealflowOrganizationChoicesSandbox
    )
    PIPEDRIVE_ORGANIZATION_INVESTOR_CHOICES = (
        PipedriveInvestorOrganizationChoicesSandbox
    )
    PIPEDRIVE_DEAL_INVESTOR_CHOICES = PipedriveInvestorDealChoicesSandbox
