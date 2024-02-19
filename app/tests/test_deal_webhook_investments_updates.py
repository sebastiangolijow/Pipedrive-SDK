from unittest.mock import patch

import pytest
from django.urls import reverse
from faker import Faker

from cashflow.cashcalls.fakers.faker_kyc import KYCFaker
from core_auth.models.user import CustomUser
from core_management.fakers.faker_account import UserFaker
from core_management.fakers.faker_relationships import UserInvestorRelationshipFaker
from core_management.fakers.fakers import FundraisingFaker
from core_management.fakers.fakers import InvestmentFaker
from core_management.fakers.fakers import InvestorFaker
from core_management.models import KYC
from dealflow.investment.faker_investment import InvestmentWithDocumentFaker
from dealflow.investment.models.models import Investment
from dealflow.investment.models.models_choices import InvestmentStatusChoices
from entities.investor.choices import KYCStatusChoices
from entities.investor.models.models import Investor
from entities.startup.models.models import Startup
from entities.startup.tests.fakers.faker_startup import StartupFaker


fake = Faker()

test_data: dict = {
    "v": 1,
    "matches_filters": {"current": [1]},
    "meta": {
        "action": "updated",
        "change_source": "app",
        "company_id": 12175019,
        "host": "oneragtimeinvestors-sandbox.pipedrive.com",
        "id": 9526,
        "is_bulk_update": False,
        "matches_filters": {"current": [1]},
        "object": "deal",
        "permitted_user_ids": [17557976, 17611667],
        "pipedrive_service_name": False,
        "timestamp": 1693485777,
        "timestamp_micro": 1693485777197050,
        "prepublish_timestamp": 1693485777372,
        "trans_pending": False,
        "user_id": 17557976,
        "v": 1,
        "webhook_id": "2435470",
    },
    "current": {
        "email_messages_count": 0,
        "cc_email": "oneragtimeinvestors-sandbox+deal9526@pipedrivemail.com",
        "products_count": 0,
        "next_activity_date": None,
        "next_activity_type": None,
        "next_activity_duration": None,
        "id": 9525,
        "person_id": 15292,
        "creator_user_id": 17557976,
        "expected_close_date": None,
        "owner_name": "Investor Team",
        "participants_count": 1,
        "stage_id": 6,
        "probability": None,
        "undone_activities_count": 0,
        "active": True,
        "person_name": "Sebas golijow",
        "last_activity_date": None,
        "close_time": None,
        "org_hidden": False,
        "next_activity_id": None,
        "weighted_value_currency": "USD",
        "b184a4616a39b675c78ea5644a7374be150db0a1": None,
        "stage_order_nr": 4,
        "next_activity_subject": None,
        "rotten_time": None,
        "user_id": 17557976,
        "visible_to": "3",
        "org_id": 15075,
        "notes_count": 0,
        "next_activity_time": None,
        "formatted_value": "$1,000",
        "status": "open",
        "formatted_weighted_value": "$1,000",
        "first_won_time": None,
        "last_outgoing_mail_time": None,
        "b6923458151406bf97a3f694a051f063f6d3506b": "16",
        "title": "Jonathan Robinson deal",
        "last_activity_id": None,
        "update_time": "2023-08-31 12:42:57",
        "activities_count": 0,
        "pipeline_id": 2,
        "lost_time": None,
        "currency": "USD",
        "weighted_value": 1000,
        "org_name": "Jonathan Robinson",
        "value": 1000,
        "person_hidden": False,
        "next_activity_note": None,
        "files_count": 0,
        "last_incoming_mail_time": None,
        "label": None,
        "lost_reason": None,
        "deleted": False,
        "won_time": None,
        "followers_count": 1,
        "stage_change_time": "2023-08-31 12:42:57",
        "add_time": "2023-08-28 08:31:35",
        "done_activities_count": 0,
    },
    "previous": {
        "email_messages_count": 0,
        "cc_email": "oneragtimeinvestors-sandbox+deal9526@pipedrivemail.com",
        "products_count": 0,
        "next_activity_date": None,
        "next_activity_type": None,
        "next_activity_duration": None,
        "id": 9526,
        "person_id": 15292,
        "creator_user_id": 17557976,
        "expected_close_date": None,
        "owner_name": "Investor Team",
        "participants_count": 1,
        "stage_id": 8,
        "probability": None,
        "undone_activities_count": 0,
        "active": True,
        "person_name": "Seba golijow",
        "last_activity_date": None,
        "close_time": None,
        "org_hidden": False,
        "next_activity_id": None,
        "weighted_value_currency": "USD",
        "b184a4616a39b675c78ea5644a7374be150db0a1": None,
        "stage_order_nr": 2,
        "next_activity_subject": None,
        "rotten_time": None,
        "user_id": 17557976,
        "visible_to": "3",
        "org_id": 15075,
        "notes_count": 0,
        "next_activity_time": None,
        "formatted_value": "$1,000",
        "status": "open",
        "formatted_weighted_value": "$1,000",
        "first_won_time": None,
        "last_outgoing_mail_time": None,
        "b6923458151406bf97a3f694a051f063f6d3506b": None,
        "title": "Jonathan Robinson deal",
        "last_activity_id": None,
        "update_time": "2023-08-31 12:41:04",
        "activities_count": 0,
        "pipeline_id": 2,
        "lost_time": None,
        "currency": "USD",
        "weighted_value": 1000,
        "org_name": "Jonathan Robinson",
        "value": 1000,
        "person_hidden": False,
        "next_activity_note": None,
        "files_count": 0,
        "last_incoming_mail_time": None,
        "label": None,
        "lost_reason": None,
        "deleted": False,
        "won_time": None,
        "followers_count": 1,
        "stage_change_time": "2023-08-31 12:41:04",
        "add_time": "2023-08-28 08:31:35",
        "done_activities_count": 0,
    },
    "event": "updated.deal",
    "retry": 0,
}

test_data_3: dict = {
    "v": 1,
    "matches_filters": {"current": [2]},
    "meta": {
        "action": "updated",
        "change_source": "app",
        "company_id": 12175019,
        "host": "oneragtimeinvestors-sandbox.pipedrive.com",
        "id": 13844,
        "is_bulk_update": False,
        "matches_filters": {"current": [2]},
        "object": "deal",
        "permitted_user_ids": [17557976, 17611667],
        "pipedrive_service_name": False,
        "timestamp": 1696240655,
        "timestamp_micro": 1696240655173189,
        "prepublish_timestamp": 1696240655326,
        "trans_pending": False,
        "user_id": 17557976,
        "v": 1,
        "webhook_id": "2561507",
    },
    "current": {
        "email_messages_count": 0,
        "cc_email": "oneragtimeinvestors-sandbox+deal13844@pipedrivemail.com",
        "5bdf85cbab2f8630cad1a962d6ba420e26db83f8": "",
        "products_count": 0,
        "next_activity_date": None,
        "next_activity_type": None,
        "next_activity_duration": None,
        "id": 13844,
        "person_id": 23058,
        "creator_user_id": 17557976,
        "expected_close_date": None,
        "owner_name": "Investor Team",
        "participants_count": 0,
        "stage_id": 7,
        "probability": None,
        "undone_activities_count": 0,
        "active": False,
        "person_name": "Sebastian Testing",
        "last_activity_date": None,
        "close_time": "2023-10-02 09:57:35",
        "org_hidden": False,
        "next_activity_id": None,
        "weighted_value_currency": "USD",
        "b184a4616a39b675c78ea5644a7374be150db0a1": None,
        "stage_order_nr": 2,
        "next_activity_subject": None,
        "rotten_time": None,
        "user_id": 17557976,
        "visible_to": "3",
        "org_id": 20647,
        "notes_count": 0,
        "next_activity_time": None,
        "formatted_value": "$48,000",
        "status": "won",
        "formatted_weighted_value": "$48,000",
        "first_won_time": "2023-09-27 09:38:16",
        "last_outgoing_mail_time": None,
        "b6923458151406bf97a3f694a051f063f6d3506b": "335",
        "title": "Keli Network Seed 2017 #3 (721)",
        "last_activity_id": None,
        "update_time": "2023-10-02 09:57:35",
        "activities_count": 0,
        "pipeline_id": 1,
        "lost_time": None,
        "currency": "USD",
        "weighted_value": 48000,
        "org_name": "Rémy Teuma",
        "value": 48000,
        "person_hidden": False,
        "next_activity_note": None,
        "files_count": 0,
        "last_incoming_mail_time": None,
        "label": None,
        "lost_reason": None,
        "deleted": False,
        "won_time": "2023-10-02 09:57:35",
        "followers_count": 1,
        "stage_change_time": "2023-09-28 07:35:12",
        "add_time": "2023-09-27 09:38:16",
        "done_activities_count": 0,
    },
    "previous": {
        "email_messages_count": 0,
        "cc_email": "oneragtimeinvestors-sandbox+deal13844@pipedrivemail.com",
        "5bdf85cbab2f8630cad1a962d6ba420e26db83f8": "",
        "products_count": 0,
        "next_activity_date": None,
        "next_activity_type": None,
        "next_activity_duration": None,
        "id": 13844,
        "person_id": None,
        "creator_user_id": 17557976,
        "expected_close_date": None,
        "owner_name": "Investor Team",
        "participants_count": 0,
        "stage_id": 5,
        "probability": None,
        "undone_activities_count": 0,
        "active": True,
        "person_name": "Sebastian Testing",
        "last_activity_date": None,
        "close_time": None,
        "org_hidden": False,
        "next_activity_id": None,
        "weighted_value_currency": "USD",
        "b184a4616a39b675c78ea5644a7374be150db0a1": None,
        "stage_order_nr": 2,
        "next_activity_subject": None,
        "rotten_time": None,
        "user_id": 17557976,
        "visible_to": "3",
        "org_id": 20647,
        "notes_count": 0,
        "next_activity_time": None,
        "formatted_value": "$48,000",
        "status": "open",
        "formatted_weighted_value": "$48,000",
        "first_won_time": "2023-09-27 09:38:16",
        "last_outgoing_mail_time": None,
        "b6923458151406bf97a3f694a051f063f6d3506b": "335",
        "title": "Keli Network Seed 2017 #3 (721)",
        "last_activity_id": None,
        "update_time": "2023-10-02 09:57:27",
        "activities_count": 0,
        "pipeline_id": 1,
        "lost_time": None,
        "currency": "USD",
        "weighted_value": 48000,
        "org_name": "Rémy Teuma",
        "value": 48000,
        "person_hidden": False,
        "next_activity_note": None,
        "files_count": 0,
        "last_incoming_mail_time": None,
        "label": None,
        "lost_reason": None,
        "deleted": False,
        "won_time": None,
        "followers_count": 1,
        "stage_change_time": "2023-09-28 07:35:12",
        "add_time": "2023-09-27 09:38:16",
        "done_activities_count": 0,
    },
    "event": "updated.deal",
    "retry": 0,
}

test_data_6: dict = {
    "v": 1,
    "matches_filters": {"current": [2]},
    "meta": {
        "action": "updated",
        "change_source": "app",
        "company_id": 12175019,
        "host": "oneragtimeinvestors-sandbox.pipedrive.com",
        "id": 13844,
        "is_bulk_update": False,
        "matches_filters": {"current": [2]},
        "object": "deal",
        "permitted_user_ids": [17557976, 17611667],
        "pipedrive_service_name": False,
        "timestamp": 1696240655,
        "timestamp_micro": 1696240655173189,
        "prepublish_timestamp": 1696240655326,
        "trans_pending": False,
        "user_id": 17557976,
        "v": 1,
        "webhook_id": "2561507",
    },
    "current": {
        "email_messages_count": 0,
        "cc_email": "oneragtimeinvestors-sandbox+deal13844@pipedrivemail.com",
        "5bdf85cbab2f8630cad1a962d6ba420e26db83f8": "",
        "products_count": 0,
        "next_activity_date": None,
        "next_activity_type": None,
        "next_activity_duration": None,
        "id": 13844,
        "person_id": 23058,
        "creator_user_id": 17557976,
        "expected_close_date": None,
        "owner_name": "Investor Team",
        "participants_count": 0,
        "stage_id": 7,
        "probability": None,
        "undone_activities_count": 0,
        "active": False,
        "person_name": "Sebastian Testing",
        "last_activity_date": None,
        "close_time": "2023-10-02 09:57:35",
        "org_hidden": False,
        "next_activity_id": None,
        "weighted_value_currency": "USD",
        "b184a4616a39b675c78ea5644a7374be150db0a1": None,
        "stage_order_nr": 2,
        "next_activity_subject": None,
        "rotten_time": None,
        "user_id": 17557976,
        "visible_to": "3",
        "org_id": 20647,
        "notes_count": 0,
        "next_activity_time": None,
        "formatted_value": "$48,000",
        "status": "lost",
        "formatted_weighted_value": "$48,000",
        "first_won_time": "2023-09-27 09:38:16",
        "last_outgoing_mail_time": None,
        "b6923458151406bf97a3f694a051f063f6d3506b": "335",
        "title": "Keli Network Seed 2017 #3 (721)",
        "last_activity_id": None,
        "update_time": "2023-10-02 09:57:35",
        "activities_count": 0,
        "pipeline_id": 1,
        "lost_time": None,
        "currency": "USD",
        "weighted_value": 48000,
        "org_name": "Rémy Teuma",
        "value": 48000,
        "person_hidden": False,
        "next_activity_note": None,
        "files_count": 0,
        "last_incoming_mail_time": None,
        "label": None,
        "lost_reason": None,
        "deleted": False,
        "won_time": "2023-10-02 09:57:35",
        "followers_count": 1,
        "stage_change_time": "2023-09-28 07:35:12",
        "add_time": "2023-09-27 09:38:16",
        "done_activities_count": 0,
    },
    "previous": {
        "email_messages_count": 0,
        "cc_email": "oneragtimeinvestors-sandbox+deal13844@pipedrivemail.com",
        "5bdf85cbab2f8630cad1a962d6ba420e26db83f8": "",
        "products_count": 0,
        "next_activity_date": None,
        "next_activity_type": None,
        "next_activity_duration": None,
        "id": 13844,
        "person_id": None,
        "creator_user_id": 17557976,
        "expected_close_date": None,
        "owner_name": "Investor Team",
        "participants_count": 0,
        "stage_id": 5,
        "probability": None,
        "undone_activities_count": 0,
        "active": True,
        "person_name": "Sebastian Testing",
        "last_activity_date": None,
        "close_time": None,
        "org_hidden": False,
        "next_activity_id": None,
        "weighted_value_currency": "USD",
        "b184a4616a39b675c78ea5644a7374be150db0a1": None,
        "stage_order_nr": 2,
        "next_activity_subject": None,
        "rotten_time": None,
        "user_id": 17557976,
        "visible_to": "3",
        "org_id": 20647,
        "notes_count": 0,
        "next_activity_time": None,
        "formatted_value": "$48,000",
        "status": "open",
        "formatted_weighted_value": "$48,000",
        "first_won_time": "2023-09-27 09:38:16",
        "last_outgoing_mail_time": None,
        "b6923458151406bf97a3f694a051f063f6d3506b": "335",
        "title": "Keli Network Seed 2017 #3 (721)",
        "last_activity_id": None,
        "update_time": "2023-10-02 09:57:27",
        "activities_count": 0,
        "pipeline_id": 1,
        "lost_time": None,
        "currency": "USD",
        "weighted_value": 48000,
        "org_name": "Rémy Teuma",
        "value": 48000,
        "person_hidden": False,
        "next_activity_note": None,
        "files_count": 0,
        "last_incoming_mail_time": None,
        "label": None,
        "lost_reason": None,
        "deleted": False,
        "won_time": None,
        "followers_count": 1,
        "stage_change_time": "2023-09-28 07:35:12",
        "add_time": "2023-09-27 09:38:16",
        "done_activities_count": 0,
    },
    "event": "updated.deal",
    "retry": 0,
}


@pytest.mark.django_db
class TestDealWebhookInvestmentUpdates:
    def url(self) -> str:
        return reverse("api:pipedrive-investors-webhook")

    def test_url(self):
        assert "/api/v2/pipedrive-sdk/investors/" == self.url()

    @patch("services.email.sendinblue_mail.SendInBlueMail.send")
    def test_deal_updated_to_won(self, send, client):
        user: CustomUser = UserFaker(
            email="test@test.com", first_name="Sebastian", last_name="Testing"
        )
        startup: Startup = StartupFaker(name="test")
        fundraising = FundraisingFaker(
            name="Keli Network Seed 2017 #3", startup=startup
        )
        kyc: KYC = KYCFaker(
            email="test@test.com", status=KYCStatusChoices.waiting_submit.name
        )
        investor: Investor = InvestorFaker(name="Sebastian Testing", kyc=kyc)
        UserInvestorRelationshipFaker(account=user, investor=investor)
        investment = InvestmentWithDocumentFaker(
            investor=investor,
            fundraising=fundraising,
            id=773,
            status=InvestmentStatusChoices.sa_sent.name,
        )
        investments_count: int = Investment.objects.count()
        users_count: int = CustomUser.objects.count()
        investor_count: int = Investor.objects.count()
        response = client.post(self.url(), test_data_3, format="json")
        assert (
            response.json()
            == "[Pipedrive Update] Investment: https://core.oneragtime.com/investments/773 updated status to SA Signed as Deal: https://oneragtimeinvestors.pipedrive.com/deal/13844 has been moved to Won"
        )
        assert investment.status == InvestmentStatusChoices.sa_sent.name
        assert Investment.objects.count() == investments_count
        assert CustomUser.objects.count() == users_count
        assert Investor.objects.count() == investor_count
        send.assert_called

    @patch("services.email.sendinblue_mail.SendInBlueMail.send")
    def test_deal_updated_to_won_no_investment_sa_in_core(self, send, client):
        user: CustomUser = UserFaker(
            email="test@test.com", first_name="Sebastian", last_name="Testing"
        )
        startup: Startup = StartupFaker(name="test")
        fundraising = FundraisingFaker(
            name="Keli Network Seed 2017 #3", startup=startup
        )
        kyc: KYC = KYCFaker(
            email="test@test.com", status=KYCStatusChoices.waiting_submit.name
        )
        investor: Investor = InvestorFaker(name="Sebastian Testing", kyc=kyc)
        UserInvestorRelationshipFaker(account=user, investor=investor)
        investment = InvestmentFaker(
            investor=investor,
            fundraising=fundraising,
            id=773,
            status=InvestmentStatusChoices.sa_sent.name,
        )
        investments_count: int = Investment.objects.count()
        users_count: int = CustomUser.objects.count()
        investor_count: int = Investor.objects.count()
        response = client.post(self.url(), test_data_3, format="json")
        assert "[Pipedrive Update Error]" in response.json()
        assert investment.status == InvestmentStatusChoices.sa_sent.name
        assert Investment.objects.count() == investments_count
        assert CustomUser.objects.count() == users_count
        assert Investor.objects.count() == investor_count
        send.assert_called

    @patch("services.email.sendinblue_mail.SendInBlueMail.send")
    def test_view_investment_delete_on_deal_update_to_lost(self, send, client):
        user: CustomUser = UserFaker(
            email="test@test.com", first_name="Sebastian", last_name="Testing"
        )
        startup: Startup = StartupFaker(name="test")
        fundraising = FundraisingFaker(
            name="Keli Network Seed 2017 #3", startup=startup
        )
        kyc: KYC = KYCFaker(
            email="test@test.com", status=KYCStatusChoices.waiting_submit.name
        )
        investor: Investor = InvestorFaker(name="Sebastian Testing", kyc=kyc)
        UserInvestorRelationshipFaker(account=user, investor=investor)
        InvestmentFaker(investor=investor, fundraising=fundraising, id=773)
        investments_count: int = Investment.objects.count()
        response = client.post(self.url(), test_data_6, format="json")
        assert (
            response.json()
            == f"[Pipedrive Update] Investment with id: 773 successfully deleted"
        )
        assert Investment.objects.count() == investments_count - 1
        send.assert_called

    @pytest.mark.skip(reason="not running in test env")
    @patch("services.email.sendinblue_mail.SendInBlueMail.send")
    def test_view_fail_slack_message(self, send, client):
        email = fake.email()
        user: CustomUser = UserFaker(email=email)
        startup: Startup = StartupFaker(name="test")
        FundraisingFaker(name="Sonio Seed", startup=startup)
        kyc: KYC = KYCFaker(email=email, status=KYCStatusChoices.waiting_submit.name)
        investor: Investor = InvestorFaker(name="Test case3", kyc=kyc)
        UserInvestorRelationshipFaker(account=user, investor=investor)

    @pytest.mark.skip(reason="not running in test env")
    @patch("services.email.sendinblue_mail.SendInBlueMail.send")
    def test_view_fail_slack_message_2(self, send, client):
        email = fake.email()
        user: CustomUser = UserFaker(email=email)
        startup: Startup = StartupFaker(name="test")
        FundraisingFaker(name="Sonio Seed", startup=startup)
        kyc: KYC = KYCFaker(email=email, status=KYCStatusChoices.waiting_submit.name)
        investor: Investor = InvestorFaker(name="Test case3", kyc=kyc)
        UserInvestorRelationshipFaker(account=user, investor=investor)

    @pytest.mark.skip(
        reason="Skip because in sandbox club deal pipeline id is different from master, to run this test go to utils and inside the function check_if_deal_pipeline_is_clubdeal_and_return_core_url replace the club_deal_pipeline_id for club_deal_pipeline_id_sandbox"
    )
    def test_investment_club_deal_aready_exists_and_update_core_url_in_pipedrive_deal(
        self, client
    ):
        user: CustomUser = UserFaker(
            email="test@test.com", first_name="Sebastian", last_name="Testing"
        )
        startup: Startup = StartupFaker(name="test")
        fundraising = FundraisingFaker(name="Sonio Seed", startup=startup)
        kyc: KYC = KYCFaker(
            email="test@test.com", status=KYCStatusChoices.waiting_submit.name
        )
        investor: Investor = InvestorFaker(name="Sebastian Testing", kyc=kyc)
        UserInvestorRelationshipFaker(account=user, investor=investor)
        InvestmentFaker(fundraising=fundraising, investor=investor)
        investments_count: int = Investment.objects.count()
        users_count: int = CustomUser.objects.count()
        investor_count: int = Investor.objects.count()
        response = client.post(self.url(), test_data_3, format="json")
        assert response.json() == "successfully created"
        assert Investment.objects.count() == investments_count
        assert CustomUser.objects.count() == users_count
        assert Investor.objects.count() == investor_count
