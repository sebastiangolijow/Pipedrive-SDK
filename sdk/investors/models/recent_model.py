from pipedrive.sdk.investors.models.abstract_model import BaseInvestorRecentModel
from pipedrive.sdk.investors.serializers import RecentInvestorSerializerCreate


class PipedriveInvestorRecent(BaseInvestorRecentModel):
    serializer_created = RecentInvestorSerializerCreate
