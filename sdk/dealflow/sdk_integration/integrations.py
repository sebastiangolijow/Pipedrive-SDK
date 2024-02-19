from core_auth.models.user import CustomUser
from core_management.models import BusinessModel
from core_management.models import GoToMarket
from core_management.models import GrowthStage
from entities.startup.models.models import Startup
from ort_files.document.models import Document
from ort_files.document.models import DocumentFile
from ort_files.general.utils.s3_utils import download_from_s3
from pipedrive.app.utils.utils import map_option
from pipedrive.sdk.abstracts.core_to_pipedrive_integration import (
    CoreToPipedriveIntegration,
)
from pipedrive.sdk.dealflow.models.file_model import PipedriveDealflowFile
from pipedrive.sdk.dealflow.models.note_model import PipedriveDealflowNote
from pipedrive.sdk.dealflow.models.organization_model import (
    PipedriveDealflowOrganization,
)
from pipedrive.sdk.dealflow.models.person_model import PipedriveDealflowContact
from pipedrive.sdk.dealflow.sdk_integration.integration_serializers import (
    StartuptoOrganizationSerializer,
)
from pipedrive.sdk.investors.sdk_integration.serializers import return_correct_option
from services.slack.choices import MessageChoices
from services.slack.main import DealFlowSlackSender


class StartupOnboardingIntegration(CoreToPipedriveIntegration):
    """this class will take as input the data from the StartOnboarding class and it will
    create the corresponding entities in Pipedrive
    data e.g: {
            "user_id": 6322,
            "startup_name": "test",
            "location": 11, ## City id
            "website": "www.test.com",
            "sectors_of_interest": [],
            "business_models": [15],
            "go_to_markets": [11],
            "tagline": "asdasdasdasdsad",
            "company_description": "asdasdsadsadsad",
            "growth_stage": 11, ## GrowthStageId
            "total_round": "11",
            "employer": "test",
            "position": "dev",
            "pitch_deck_document": pitch_deck.id,
            "address": "test 21",
        }"""

    @classmethod
    def sync(cls, startup_data: dict, data):
        """Main entry of integration class, in charge of verify data with serializer,
        check trigger if needed and perform the corresponding action"""
        try:
            if cls.verify_data(data) and cls.check_trigger():
                cls.perform_action(startup_data, data)
        except BaseException as e:
            print("Pipedrive error: ", e)

    @classmethod
    def verify_data(cls, data) -> bool:
        """Verify if data is correct in serializer"""
        startup_data = StartuptoOrganizationSerializer(data=data)
        return startup_data.is_valid()

    @classmethod
    def check_trigger(cls):
        return True

    @classmethod
    def perform_action(cls, startup_data: dict, data) -> None:
        """Creates Organization from startup and contact from User"""
        user: CustomUser = startup_data["account"]
        org_response: dict = cls.create_organization_dealflow_pipedrive(
            startup_data, data
        )
        org_id: int = org_response["data"]["id"]
        person_response: dict = cls.create_person_dealflow_pipedrive(
            user, org_id, startup_data
        )
        person_id: int = person_response["data"]["id"]
        cls.add_pitch_dec_to_pipedrive(data, org_id, person_id)
        cls.add_notes_to_entities(person_id, org_id)

    @classmethod
    def create_organization_dealflow_pipedrive(
        cls, startup_data: dict, data: dict
    ) -> dict:
        data: dict = {
            "name": startup_data["startup__name"],
            "source": [230],
            "event": [],  ### Empty cause as is it created from the onboarding the event should be empty
            "website": startup_data["startup__links__website"],
            "linkedin_url": (
                startup_data["linkedin_url"]
                if "linkedin_url" in startup_data.keys()
                else ""
            ),
            "address": (
                startup_data["address"] if "address" in startup_data.keys() else ""
            ),
            "business_model": cls.return_business_model(data),
            "sector": data["sectors_of_interest"],  ### map option
            "go_to_markets": [],  ### Not in pipedrive, should we add it ?
            "stage": cls.return_stage(data),
            "tagline": startup_data["startup__tagline"],
        }
        org: PipedriveDealflowOrganization = PipedriveDealflowOrganization(**data)
        org_response: dict = org.create()
        slack_sender = DealFlowSlackSender(
            startup_id=Startup.objects.last().id,
            startup_name=startup_data["startup__name"],
            org_id=org_response["data"]["id"],
        )
        slack_sender.send(MessageChoices.startup_onboarding_org_created.name)
        return org_response

    @classmethod
    def create_person_dealflow_pipedrive(
        cls, user: CustomUser, org_id: int, startup_data: dict
    ) -> dict:
        person_name: str = f"{user.first_name} {user.last_name}"
        data: dict = {
            "name": person_name,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "org_id": org_id,
        }
        person: PipedriveDealflowContact = PipedriveDealflowContact(**data)
        person_response: dict = person.create()
        slack_sender = DealFlowSlackSender(
            startup_id=Startup.objects.last().id,
            startup_name=startup_data["startup__name"],
            person_name=person_name,
            user_name=person_name,
            person_id=person_response["data"]["id"],
            user_id=user.id,
        )
        slack_sender.send(MessageChoices.startup_onboarding_user_created.name)
        return person_response

    @classmethod
    def map_data_option(cls, id, options) -> str:
        for item in options:
            if item["id"] == id:
                return item["name"]

    @classmethod
    def return_go_to_market(cls, data):
        go_to_markets_id: int = (
            data["go_to_markets"][0] if len(data["go_to_markets"]) > 0 else []
        )
        if isinstance(go_to_markets_id, int):
            name = GoToMarket.objects.get(id=go_to_markets_id).name
            map_option(name, return_correct_option(""))

    @classmethod
    def return_stage(cls, data):
        stage_id: int = (
            data["growth_stage"] if isinstance(data["growth_stage"], int) else []
        )
        if isinstance(stage_id, int):
            name = GrowthStage.objects.get(id=stage_id).name
            return map_option(name, return_correct_option("stage"))
        return []

    @classmethod
    def return_business_model(cls, data):
        business_model_id: int = (
            data["business_models"][0] if len(data["business_models"]) > 0 else []
        )
        if isinstance(business_model_id, int):
            name = BusinessModel.objects.get(id=business_model_id).name
            return map_option(name, return_correct_option("business_models"))
        return []

    @classmethod
    def add_pitch_dec_to_pipedrive(cls, data, org_id, person_id):
        """Method used to create Pitch dec document in Pipedrive, related to Organization"""
        pitch_deck = Document.objects.get(id=data["pitch_deck_document"])
        pitch_deck_file = DocumentFile.objects.get(
            id=pitch_deck.current_document_file_id
        )
        s3_file = download_from_s3(
            str(pitch_deck_file.document_file._get_file()), pitch_deck.name
        )
        files = {
            "file": (
                pitch_deck.name,
                open(
                    s3_file,
                    "rb",
                ),
                "file",
            )
        }
        data = {"org_id": org_id, "person_id": person_id, "file": files}
        file: PipedriveDealflowFile = PipedriveDealflowFile()
        return file.create(**data)

    @classmethod
    def add_notes_to_entities(cls, person_id, org_id):
        cls.add_note_to_new_contact(person_id)
        cls.add_note_to_new_org(org_id)

    @classmethod
    def add_note_to_new_contact(cls, person_id):
        data: dict = {
            "person_id": person_id,
            "content": "[Core to Pipedrive automation] This contact has been created due an Startup onboarding",
        }
        note: PipedriveDealflowNote = PipedriveDealflowNote(**data)
        return note.create()

    @classmethod
    def add_note_to_new_org(cls, org_id):
        data: dict = {
            "org_id": org_id,
            "content": "[Core to Pipedrive automation] This Organization has been created due an Startup onboarding",
        }
        note: PipedriveDealflowNote = PipedriveDealflowNote(**data)
        return note.create()
