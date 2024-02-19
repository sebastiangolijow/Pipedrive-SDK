from pipedrive.sdk.investors.models.abstract_model import BaseInvestorActivityModel
from pipedrive.sdk.investors.models.abstract_model import BaseInvestorActivityModelField
from pipedrive.sdk.investors.models.abstract_model import BaseInvestorActivityTypeModel
from pipedrive.sdk.investors.serializers import ActivityFieldInvestorSerializerUpdate
from pipedrive.sdk.investors.serializers import ActivityInvestorSerializerCreate
from pipedrive.sdk.investors.serializers import ActivityInvestorSerializerUpdate
from pipedrive.sdk.investors.serializers import ActivityTypeInvestorSerializerCreate
from pipedrive.sdk.investors.serializers import ActivityTypeInvestorSerializerUpdate


class PipedriveInvestorActivityFields(BaseInvestorActivityModelField):
    serializer_created = ActivityFieldInvestorSerializerUpdate
    serializer_updated = ActivityFieldInvestorSerializerUpdate


class PipedriveInvestorActivity(BaseInvestorActivityModel):
    serializer_created = ActivityInvestorSerializerCreate
    serializer_updated = ActivityInvestorSerializerUpdate


class PipedriveInvestorActivityType(BaseInvestorActivityTypeModel):
    serializer_created = ActivityTypeInvestorSerializerCreate
    serializer_updated = ActivityTypeInvestorSerializerUpdate
    fields = PipedriveInvestorActivityFields
