from pipedrive.sdk.investors.models.abstract_model import BaseInvestorStageModel
from pipedrive.sdk.investors.serializers import StageInvestorSerializerCreate


class PipedriveInvestorStage(BaseInvestorStageModel):
    serializer_created = StageInvestorSerializerCreate
