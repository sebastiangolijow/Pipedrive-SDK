from pipedrive.sdk.dealflow.models.abstract_model import BaseDealflowNoteModel
from pipedrive.sdk.dealflow.serializers import NoteDealflowSerializerCreate
from pipedrive.sdk.dealflow.serializers import NoteDealflowSerializerUpdate


class PipedriveDealflowNote(BaseDealflowNoteModel):
    serializer_created = NoteDealflowSerializerCreate
    serializer_updated = NoteDealflowSerializerUpdate
