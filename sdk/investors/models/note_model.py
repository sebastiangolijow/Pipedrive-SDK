import json

from pipedrive.sdk.investors.models.abstract_model import BaseInvestorNoteModel
from pipedrive.sdk.investors.models.deal_model import PipedriveInvestorDeal
from pipedrive.sdk.investors.models.organization_model import (
    PipedriveInvestorOrganization,
)
from pipedrive.sdk.investors.models.person_model import PipedriveInvestorContact
from pipedrive.sdk.investors.serializers import NoteInvestorSerializerCreate
from pipedrive.sdk.investors.serializers import NoteInvestorSerializerUpdate


class PipedriveInvestorNote(BaseInvestorNoteModel):
    serializer_created = NoteInvestorSerializerCreate
    serializer_updated = NoteInvestorSerializerUpdate

    @classmethod
    def create_organization_note(cls, investor_name, content, org_id=None):
        try:
            if not org_id:
                org = PipedriveInvestorOrganization()
                org_id = org.filter(name=investor_name)["data"]["items"][0]["item"][
                    "id"
                ]
            data: dict = {
                "org_id": org_id,
                "content": content,
            }
            note = cls(**data)
            note.create()
        except:
            return "Org not found"

    @classmethod
    def create_deal_note(cls, deal_id, content):
        data: dict = {
            "deal_id": deal_id,
            "content": content,
        }
        note = cls(**data)
        return note.create()

    @classmethod
    def create_contact_note(cls, contact_id, content):
        data: dict = {
            "person_id": contact_id,
            "content": content,
        }
        note = cls(**data)
        note.create()
