from datetime import date

from pydantic import BaseModel


class ContactDealflowFieldSerializer(BaseModel):
    name: str
    field_type: str


class ContactDealflowSerializerCreate(BaseModel):
    name: str
    email: str
    org_id: int = None
    position: list = []


class ContactDealflowSerializerUpdate(BaseModel):
    id: int
    name: str = ""
    email: str = ""
    org_id: int = None
    position: list = []


class ContactDealflowFieldSerializerUpdate(BaseModel):
    id: int


class OrganizationDealflowSerializerCreate(BaseModel):
    name: str
    source: list = []
    event: list = []
    deal_owner: list = []
    website: str = ""
    linkedin_url: str = ""
    address: str = ""
    female_c_level: list = []
    sector: list = []
    business_model: list = []
    stage: list = []
    impact: list = []
    arias_scope: list = []
    startup_competitors: str = ""
    tagline: str = ""
    # city: str = ""


class OrganizationDealflowSerializerUpdate(BaseModel):
    id: int
    name: str = ""
    Sources: list = []
    Event: list = []
    deal_owner: list = []
    Website: str = ""
    linkedin_url: str = ""
    address: str = ""
    female_c_level: list = []
    sector: list = []
    business_model: list = []
    stage: list = []
    impact: list = []
    arias_scope: list = []
    startup_competitors: str = ""
    tagline: str = ""


class NoteDealflowSerializerCreate(BaseModel):
    content: str
    person_id: int = None
    org_id: int = None


class NoteDealflowSerializerUpdate(BaseModel):
    id: int
    content: str = ""
    person_id: int = None
    org_id: int = None


class ActivityDealflowSerializerCreate(BaseModel):
    person_id: int = None
    org_id: int = None
    deal_id: int = None
    lead_id: int = None
    project_id: int = None
    participants: list = (
        []
    )  ### list of persons. e.g: [{"person_id":1,"primary_flag":true}]
    busy_flag: bool = None
    attendees: list = (
        []
    )  ### can be contacts or not. e.g if not contact: [{"email_address":"mail@example.org"}]. if contact: [{"person_id":1, "email_address":"mail@example.org"}]
    due_date: date = None
    due_time: date = None


class ActivityDealflowSerializerUpdate(BaseModel):
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


class ActivityTypeDealflowSerializerUpdate(BaseModel):
    id: int
    name: str = ""
    icon_key: str = ""
    color: str = ""


class ActivityTypeDealflowSerializerCreate(BaseModel):
    name: str
    icon_key: str
    color: str = ""


class LeadDealflowSerializerCreate(BaseModel):
    title: str
    # owner_id: int = None
    # label_ids: list = []
    # person_id: int = None
    organization_id: int = None
    # expected_close_date: str = "2023-01-01"  ### to be fixed


class LeadDealflowSerializerUpdate(BaseModel):
    id: str
    title: str = ""
    owner_id: int = None
    label_ids: list = []
    person_id: int = None
    organization_id: int = None
    expected_close_date: str = "2023-01-01"  ### to be fixed


class ActivityDealflowSerializerCreate(BaseModel):
    name: str = ""
    key: str = ""
    options: list = []
