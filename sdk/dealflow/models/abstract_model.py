import requests

from pipedrive.sdk.abstracts.pipe_abstract_model import PipedriveActivitiesAbstract
from pipedrive.sdk.abstracts.pipe_abstract_model import PipedriveActivitiesTypesAbstract
from pipedrive.sdk.abstracts.pipe_abstract_model import PipedriveContactAbstract
from pipedrive.sdk.abstracts.pipe_abstract_model import PipedriveFileAbstract
from pipedrive.sdk.abstracts.pipe_abstract_model import PipedriveLeadsAbstract
from pipedrive.sdk.abstracts.pipe_abstract_model import PipedriveNoteAbstract
from pipedrive.sdk.abstracts.pipe_abstract_model import PipedriveOrganizationAbstract
from pipedrive.sdk.abstracts.pipe_field_abstract_model import (
    PipedriveActivityFieldAbstract,
)
from pipedrive.sdk.abstracts.pipe_field_abstract_model import (
    PipedriveContactFieldsAbstract,
)
from pipedrive.sdk.abstracts.pipe_field_abstract_model import (
    PipedriveOrganizationFieldAbstract,
)
from pipedrive.sdk.secrets import settings


class DealflowMixin:
    api_token = settings.PIPEDRIVE_DEALFLOW_API_TOKEN

    def get_or_create(self):
        email: str = self.data.dict()["email"]
        found = self.filter(email=email)
        if len(found["data"]["items"]) == 1:
            return found["data"]["items"][0]["item"]
        if len(found["data"]["items"]) > 1:
            raise TypeError(f"Error: more than one user found with email {email}")
        else:
            response = self.create()
            return response["data"]

    def get_activities(self, **kwargs):
        self.url = f"{self.url}/{self.data.id}/activities"
        if kwargs:
            self.url = (
                f"{self.url}?start={kwargs.get('start')}&limit={kwargs.get('limit')}"
            )
        response = requests.get(self.url, params=self.params)
        return response.json()

    def add_picture(self, **kwargs):
        img = requests.get(kwargs.get("link"))
        if img:
            files = {"file": (kwargs.get("name"), img.content, "image/png")}
            headers = {"Accept": "application/json"}
            response = requests.post(
                f"{self.url}/{self.data.id}/picture",
                params=self.params,
                headers=headers,
                files=files,
            )
            return response.json()
        return TypeError("Img not found")

    def check_user_existence_return_id(self):
        try:
            email: str = self.data.dict()["email"]
            found = self.get(email=email)
            if len(found["data"]["items"]) == 1:
                return found["data"]["items"][0]["item"]["id"]
            if len(found["data"]["items"]) > 1:
                ids = []
                for person in found["data"]["items"]:
                    ids.append(person["item"]["id"])
                return ids
        except:
            name: str = self.data.dict()["name"]
            found = self.filter(name=name)
            if len(found["data"]["items"]) == 1:
                return found["data"]["items"][0]["item"]["id"]
            if len(found["data"]["items"]) > 1:
                ids = []
                for person in found["data"]["items"]:
                    ids.append(person["item"]["id"])
                return ids
        return "User not found"

    def check_org_existence_return_id(self):
        name: str = self.data.dict()["name"]
        found = self.filter(name=name)
        if len(found["data"]["items"]) == 1:
            return found["data"]["items"][0]["item"]["id"]
        if len(found["data"]["items"]) > 1:
            ids = []
            for person in found["data"]["items"]:
                ids.append(person["item"]["id"])
            return ids
        return "Org not found"


class BaseDealflowContactModel(DealflowMixin, PipedriveContactAbstract):
    pass


class BaseDealflowOrganizationModel(DealflowMixin, PipedriveOrganizationAbstract):
    pass


class BaseDealflowContactModelField(DealflowMixin, PipedriveContactFieldsAbstract):
    pass


class BaseDealflowOrganizationModelField(
    DealflowMixin, PipedriveOrganizationFieldAbstract
):
    pass


class BaseDealflowNoteModel(DealflowMixin, PipedriveNoteAbstract):
    pass


class BaseDealflowActivityModel(DealflowMixin, PipedriveActivitiesAbstract):
    pass


class BaseDealflowActivityTypeModel(DealflowMixin, PipedriveActivitiesTypesAbstract):
    pass


class BaseDealflowLeadModel(DealflowMixin, PipedriveLeadsAbstract):
    pass


class BaseDealflowOActivityModelField(DealflowMixin, PipedriveActivityFieldAbstract):
    pass


class BaseDealflowFileModel(DealflowMixin, PipedriveFileAbstract):
    pass
