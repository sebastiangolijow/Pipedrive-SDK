from core_auth.models.user import CustomUser
from entities.investor.models.models import Investor
from pipedrive.sdk.investors.models.organization_model import (
    PipedriveInvestorOrganization,
)
from pipedrive.sdk.investors.models.person_model import PipedriveInvestorContact


def delete_pipedrive_entities(user: CustomUser) -> None:
    investor: Investor = Investor.objects.last()
    name: str = f"{user.first_name} {user.last_name}"
    contact_response = PipedriveInvestorContact(
        name=name,
        email=user.email,
    ).check_user_existence_return_id()
    investor_name: str = (
        investor.name if investor else f"{user.first_name} {user.last_name}"
    )
    org_response = PipedriveInvestorOrganization(
        name=investor_name,
    ).check_org_existence_return_id()
    contact_response = (
        contact_response if isinstance(contact_response, int) else contact_response[0]
    )
    if isinstance(contact_response, int):
        contact = PipedriveInvestorContact(id=contact_response)
        contact.delete()
    if org_response != "Org not found":
        org_response = (
            org_response if isinstance(org_response, int) else org_response[0]
        )
        org = PipedriveInvestorOrganization(id=org_response)
        org.delete()
    else:
        org_response = PipedriveInvestorOrganization(
            name=name,
        ).check_org_existence_return_id()
        if org_response != "Org not found":
            org_response = (
                org_response if isinstance(org_response, int) else org_response[0]
            )
            if isinstance(org_response, int):
                org = PipedriveInvestorOrganization(id=org_response)
                org.delete()
