from typing import Tuple

from django.conf import settings

from dealflow.investment.models.models import Investment
from pipedrive.sdk.investors.models.activity_model import PipedriveInvestorActivity
from pipedrive.sdk.investors.models.deal_model import PipedriveInvestorDeal
from pipedrive.sdk.investors.models.lead_model import PipedriveInvestorLead
from pipedrive.sdk.investors.models.note_model import PipedriveInvestorNote
from pipedrive.sdk.investors.models.organization_model import (
    PipedriveInvestorOrganization,
)
from pipedrive.sdk.investors.models.person_model import PipedriveInvestorContact


def add_activity(entity, id, entity_id):
    if entity["activities"] != None:
        for activity in entity["activities"]:
            data: dict = {
                entity_id: id,
                "type": activity["type"],
                "attendees": activity["attendees"] if activity["attendees"] else [],
                "due_time": activity["due_time"] if activity["due_time"] else "",
                "due_date": activity["due_date"],
                "participants": (
                    activity["participants"] if activity["participants"] else []
                ),
                "subject": activity["subject"] if activity["subject"] else "",
                "public_description": (
                    activity["public_description"]
                    if activity["public_description"]
                    else ""
                ),
                "add_time": activity["add_time"],
                "done": 0 if activity["done"] == False else 1,
                "reference_type": (
                    activity["reference_type"]
                    if activity["reference_type"] != None
                    else ""
                ),
                "duration": activity["duration"],
                "add_time": activity["add_time"],
            }
            new_activity: PipedriveInvestorActivity = PipedriveInvestorActivity(**data)
            new_activity.create()
    else:
        print(f"User {entity['name']} found but doesn't has any activities")


def update_contact_with_core_url(person_name, user_id):
    person: PipedriveInvestorContact = PipedriveInvestorContact()
    person_found: dict = person.get(name=person_name)
    person_to_update: PipedriveInvestorContact = PipedriveInvestorContact(
        id=person_found["data"]["items"][0]["item"]["id"]
    )
    payload: dict = {
        "core_url": f"https://core.oneragtime.com/users/{user_id}",
    }
    person_to_update.update(payload)


def return_organization_name(person_id, person_name):
    try:
        person: PipedriveInvestorContact = PipedriveInvestorContact(id=person_id)
        person_found: dict = person.get()
        if person_found["data"]["org_name"] != None:
            return person_found["data"]["org_name"]
        return person_name
    except:
        return person_name


def update_org_with_core_url(org_name, investor_id):
    org: PipedriveInvestorOrganization = PipedriveInvestorOrganization()
    org_found = org.get(name=org_name)
    org_to_update = PipedriveInvestorOrganization(
        id=org_found["data"]["items"][0]["item"]["id"]
    )
    org_payload: dict = {
        "core_url": f"https://core.oneragtime.com/investors/{investor_id}",
    }
    org_to_update.update(org_payload)


def return_activity_data(person_data, entity):
    entity_found = entity(id=person_data["id"])
    activities: list = entity_found.get_activities()
    if activities["data"] != None:
        activities_list = []
        for activity in activities["data"]:
            activities_list.append(activity)
        return activities_list
    else:
        print(f"User with {person_data['name']} doesn't has any activities")


def update_pipedrive_entities_with_core_url(
    user_id, investor_id, person_name, person_id
):
    update_contact_with_core_url(person_name, user_id)
    update_org_with_core_url(
        return_organization_name(person_id, person_name), investor_id
    )


def update_deal_with_core_url(deal_id, investment_id):
    deal: PipedriveInvestorDeal = PipedriveInvestorDeal(id=deal_id)
    deal_payload: dict = {
        "core_url": f"https://core.oneragtime.com/investments/{investment_id}",
    }
    deal.update(deal_payload)


def check_if_deal_pipeline_is_clubdeal_and_return_core_url(deal_id):
    clubdeal_pipeline_id_prod: int = 1
    clubdeal_pipeline_id_sandbox: int = 2
    club_deal_pipeline_id = (
        clubdeal_pipeline_id_sandbox
        if settings.ENVIRONMENT_NAME in ["local", "dev", "test", "staging"]
        or settings.TESTING_ENV == True
        else clubdeal_pipeline_id_prod
    )
    deal: PipedriveInvestorDeal = PipedriveInvestorDeal(id=deal_id)
    deal_found = deal.get()
    return deal_found["data"].get("pipeline_id") == club_deal_pipeline_id, deal_found[
        "data"
    ].get(deal.choices.core_url.value)


def get_phone_number_and_email_from_pipedrive_user_name(person_name):
    person: PipedriveInvestorContact = PipedriveInvestorContact()
    try:
        person_found: dict = person.get(name=person_name)
    except:
        person_found: dict = person.filter(name=person_name)
    email: str = None
    phone: str = ""
    if person_found["data"]["items"][0]["item"]["emails"] != []:
        email = person_found["data"]["items"][0]["item"]["emails"][0]
    if person_found["data"]["items"][0]["item"]["phones"] != []:
        phone = person_found["data"]["items"][0]["item"]["phones"][0]
    return email, phone


def create_lead(first_name, last_name, org_id, person_id):
    data: dict = {
        "title": f"{first_name} {last_name} Lead",
        "organization_id": org_id,
        "person_id": person_id,
    }
    lead: PipedriveInvestorLead = PipedriveInvestorLead(**data)
    response = lead.create()
    return response


def map_fundraisings(fundraising):
    options_to_validate: list = PipedriveInvestorDeal.options_to_validate[
        (
            1
            if settings.ENVIRONMENT_NAME in ["local", "dev", "test", "staging"]
            or settings.TESTING_ENV == True
            else 0
        )
    ]
    for option in options_to_validate:
        if fundraising == option["label"]:
            return [option["id"]]


def check_custom_fields(array, string) -> dict or bool:
    for obj in array:
        if "custom_fields" in obj["item"]:
            if string in obj["item"]["custom_fields"]:
                return obj["item"]
    return False


def return_deal_id(fundraising_name: str, investment_id: int) -> int or str:
    deal_e = PipedriveInvestorDeal()
    deal = deal_e.filter(name=fundraising_name)
    core_url: str = f"https://core.oneragtime.com/investments/{investment_id}"
    pipedrive_deal = check_custom_fields(deal["data"]["items"], core_url)
    if pipedrive_deal:
        deal_id = pipedrive_deal["id"]
        return deal_id
    return "Deal not found"


def check_deal_existence(investment_data: dict) -> bool:
    response: bool = return_deal_id(
        investment_data["fundraising_name"], investment_data["id"]
    )
    if response == "Deal not found":
        return False
    return True


def get_or_create_and_check_existing_org(data) -> Tuple[str, int]:
    person: PipedriveInvestorContact = PipedriveInvestorContact(**data)
    email: str = data["email"]
    found = person.filter(email=email)
    if len(found["data"]["items"]) == 1:
        if not found["data"]["items"][0]["item"]["organization"]:
            update_person_organization(
                found["data"]["items"][0]["item"]["id"],
                data.get("org_id"),
                email,
                data.get("name"),
            )
        else:
            add_notes_to_created_entities(
                data.get("org_id"), found["data"]["items"][0]["item"]["id"]
            )
        return f"GET contact: {email}", found["data"]["items"][0]["item"]["id"]
    if len(found["data"]["items"]) > 1:
        raise TypeError(f"Error: more than one user found with email {email}")
    else:
        response = person.create()
        return f"CREATED contact: {email}", response["data"]["id"]


def update_person_organization(person_id, org_id, email, name):
    data = {
        "org_id": org_id,
        "email": email,
        "name": name,
    }
    person: PipedriveInvestorContact = PipedriveInvestorContact(id=person_id)
    return person.update(data)


def add_notes_to_created_entities(org_id, person_id):
    PipedriveInvestorNote.create_organization_note(
        "",
        f"[Core to Pipedrive]: Organization created due an Investor onboarding. Person: https://oneragtimeinvestors.pipedrive.com/person/{person_id} is linked to this organization",
        org_id,
    )
    PipedriveInvestorNote.create_contact_note(
        person_id,
        f"[Core to Pipedrive]: Person: https://oneragtimeinvestors.pipedrive.com/person/{person_id} created due an Investor onboarding, is linked to the following organization: https://oneragtimeinvestors.pipedrive.com/organization/{org_id}",
    )


def is_human_action(data):
    return data["meta"]["change_source"] == "app"
