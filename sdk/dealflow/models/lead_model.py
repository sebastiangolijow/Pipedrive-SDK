from pipedrive.sdk.dealflow.models.abstract_model import BaseDealflowLeadModel
from pipedrive.sdk.dealflow.serializers import LeadDealflowSerializerCreate
from pipedrive.sdk.dealflow.serializers import LeadDealflowSerializerUpdate


class PipedriveDealflowLead(BaseDealflowLeadModel):
    serializer_created = LeadDealflowSerializerCreate
    serializer_updated = LeadDealflowSerializerUpdate
