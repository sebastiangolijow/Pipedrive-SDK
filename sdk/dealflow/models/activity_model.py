from pipedrive.sdk.dealflow.models.abstract_model import BaseDealflowActivityModel
from pipedrive.sdk.dealflow.models.abstract_model import BaseDealflowActivityTypeModel
from pipedrive.sdk.dealflow.models.abstract_model import BaseDealflowOActivityModelField
from pipedrive.sdk.dealflow.serializers import ActivityDealflowSerializerCreate
from pipedrive.sdk.dealflow.serializers import ActivityDealflowSerializerUpdate
from pipedrive.sdk.dealflow.serializers import ActivityTypeDealflowSerializerCreate
from pipedrive.sdk.dealflow.serializers import ActivityTypeDealflowSerializerUpdate


class PipedriveDealflowActivityFields(BaseDealflowOActivityModelField):
    serializer_created = ActivityDealflowSerializerCreate
    serializer_updated = ActivityDealflowSerializerCreate


class PipedriveDealflowActivity(BaseDealflowActivityModel):
    serializer_created = ActivityDealflowSerializerCreate
    serializer_updated = ActivityDealflowSerializerUpdate
    fields = PipedriveDealflowActivityFields


class PipedriveDealflowActivityType(BaseDealflowActivityTypeModel):
    serializer_created = ActivityTypeDealflowSerializerCreate
    serializer_updated = ActivityTypeDealflowSerializerUpdate
