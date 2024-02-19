from datetime import datetime
from datetime import timedelta

from pipedrive.sdk.investors.models.organization_model import (
    PipedriveInvestorOrganization,
)
from pipedrive.sdk.investors.models.person_model import PipedriveInvestorContact
from pipedrive.sdk.investors.models.recent_model import PipedriveInvestorRecent


def delete_last_entities(time, entity) -> None:
    original_date = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    new_date = original_date - timedelta(hours=1)
    data: dict = {
        "since_timestamp": new_date.strftime("%Y-%m-%d %H:%M:%S"),
        "items": entity,
    }
    recent_investor = PipedriveInvestorRecent(**data)
    response = recent_investor.get()
    filtered_list: list = extract_item_id(response["data"])
    for item in filtered_list:
        if item["item"] == "person":
            delete_contact(item["id"])
        else:
            delete_organization(item["id"])


def extract_item_id(data_list) -> list:
    result = []
    if data_list != None:
        for item_data in data_list:
            item_id_dict = {"item": item_data["item"], "id": item_data["id"]}
            result.append(item_id_dict)

    return result


def delete_contact(id) -> None:
    person = PipedriveInvestorContact(id=id)
    person.delete()


def delete_organization(id) -> None:
    org = PipedriveInvestorOrganization(id=id)
    org.delete()
