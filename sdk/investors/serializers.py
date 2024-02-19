from datetime import date
from typing import Any

from pydantic import BaseModel


class OrganizationInvestorSerializer(BaseModel):
    name: str
    address: str


class ContactInvestorSerializerCreate(BaseModel):
    name: str
    first_name: str = ""
    last_name: str = ""
    email: str
    phone: str = ""
    address: str = ""  # key for address: str
    country: list = []  # key for country
    language: list = []  # key for language
    linkedin: str = ""  # key for linkedin_url: str
    source: list = []  # key for source: str
    sub_source: list = []  # key for sub_source: str
    newsletter: list = []  # key for newsletter: str
    category: list = []
    tu_vous: list = []
    city: str = ""
    org_id: int = None
    core_url: str = ""


class ContactInvestorFieldSerializer(BaseModel):
    name: str
    field_type: str


class ContactInvestorSerializerUpdate(BaseModel):
    id: int
    name: str = ""
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: str = ""
    address: str = ""  # key for address: str
    country: list = []  # key for country
    language: list = []  # key for language
    linkedin_url: list = []  # key for linkedin_url: str
    source: list = []  # key for source: str
    sub_source: list = []  # key for sub_source: str
    newsletter: list = []  # key for newsletter: str
    core_url: str = ""


class ContactInvestorFieldSerializerUpdate(BaseModel):
    id: int


class OrganizationInvestorSerializerCreate(BaseModel):
    name: str
    type: list = []
    qualification: list = []
    category: list = []
    core_url: str = ""


class OrganizationInvestorSerializerUpdate(BaseModel):
    id: int
    name: str = ""
    type: list = []
    category: list = []
    qualification: list = []
    person_id: int = None
    core_url: str = ""


class NoteInvestorSerializerCreate(BaseModel):
    content: str
    person_id: int = None
    org_id: int = None
    deal_id: int = None
    lead_id: str = None


class NoteInvestorSerializerUpdate(BaseModel):
    id: int
    content: str = ""
    person_id: int = None
    org_id: int = None
    deal_id: int = None
    lead_id: int = None


class ActivityInvestorSerializerCreate(BaseModel):
    person_id: int = None
    org_id: int = None
    deal_id: int = None
    lead_id: str = None
    project_id: int = None
    participants: list = (
        []
    )  ### list of persons. e.g: [{"person_id":1,"primary_flag":true}]
    busy_flag: bool = None
    attendees: list = (
        []
    )  ### can be contacts or not. e.g if not contact: [{"email_address":"mail@example.org"}]. if contact: [{"person_id":1, "email_address":"mail@example.org"}]
    due_date: str = ""
    due_time: str = ""
    subject: str = ""
    public_description: str = None
    add_time: str = ""
    done: int = None
    reference_type: str = None
    duration: str = ""


class ActivityInvestorSerializerUpdate(BaseModel):
    id: int
    person_id: int = None
    org_id: int = None
    deal_id: int = None
    lead_id: int = None
    project_id: int = None
    participants: list = []
    busy_flag: bool = None
    attendees: list = []
    due_date: date = None
    due_time: date = None


class ActivityTypeInvestorSerializerUpdate(BaseModel):
    id: int
    name: str = ""
    icon_key: str = ""
    color: str = ""


class ActivityTypeInvestorSerializerCreate(BaseModel):
    name: str
    icon_key: str
    color: str = ""


class DealInvestorSerializerCreate(BaseModel):
    title: str
    value: str = ""
    fundraising: list = []
    currency: str = ""
    user_id: int = None
    person_id: int = None
    org_id: int = None
    status: str = ""
    add_time: str = ""
    fees_percentage: str = ""
    stage_id: int = None


class LeadInvestorSerializerCreate(BaseModel):
    title: str
    # owner_id: int = None
    # label_ids: list = []
    person_id: int = None
    organization_id: int = None
    # expected_close_date: str = "2023-01-01"  ### to be fixed


class LeadInvestorSerializerUpdate(BaseModel):
    id: str
    title: str = ""
    owner_id: int = None
    label_ids: list = []
    person_id: int = None
    organization_id: int = None
    expected_close_date: str = "2023-01-01"  ### to be fixed


class DealInvestorSerializerUpdate(BaseModel):
    id: int
    title: str = ""
    value: str = ""
    currency: str = ""
    user_id: int = None
    person_id: int = None
    org_id: int = None
    status: str = ""
    fees_percentage: str = ""
    stage_id: int = None


class DealFieldInvestorSerializerUpdate(BaseModel):
    id: int
    name: str = ""
    options: list = []


class DealFieldInvestorSerializerCreate(BaseModel):
    name: str
    field_type: str
    options: list = []


class DealFieldInvestorSerializerCreate(BaseModel):
    name: str
    field_type: str
    options: list = []


class ActivityFieldInvestorSerializerUpdate(BaseModel):
    name: str = ""
    key: str = ""
    options: list = []


class RecentInvestorSerializerCreate(BaseModel):
    since_timestamp: str
    id: int = None
    items: str = ""
    start: int = 0
    limit: int = None


class StageInvestorSerializerCreate(BaseModel):
    order_nr: int = None
    name: str = ""
    pipeline_id: int = None
    pipeline_name: str = ""
