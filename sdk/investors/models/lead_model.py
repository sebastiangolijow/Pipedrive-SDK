from pipedrive.sdk.investors.models.abstract_model import BaseInvestorLeadModel
from pipedrive.sdk.investors.serializers import LeadInvestorSerializerCreate
from pipedrive.sdk.investors.serializers import LeadInvestorSerializerUpdate


class PipedriveInvestorLead(BaseInvestorLeadModel):
    serializer_created = LeadInvestorSerializerCreate
    serializer_updated = LeadInvestorSerializerUpdate
