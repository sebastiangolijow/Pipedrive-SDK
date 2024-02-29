from unittest.mock import call
from unittest.mock import patch

import pytest
from django.db.models import signals
from factory.django import mute_signals

from cashflow.bill.fakers.faker_bill import BillFaker
from core_auth.models.user import CustomUser
from core_management.fakers.faker_account import UserFaker
from core_management.fakers.faker_relationships import UserInvestorRelationshipFaker
from core_management.fakers.fakers import FundraisingFaker
from core_management.models import Fundraising
from core_management.signals.signals_investment import (
    insert_investment_to_investment_historical_value,
)
from dealflow.investment.faker_investment import InvestmentFaker
from dealflow.investment.faker_investment import InvestmentWithDocumentFaker
from dealflow.investment.models.model_investhistvalue import InvestmentHistoricalValue
from dealflow.investment.models.models import Investment
from dealflow.investment.models.models_choices import InvestmentStatusChoices
from entities.investor.fakers.faker_investor import InvestorFaker
from entities.investor.models.models import Investor
from entities.startup.tests.fakers.faker_startup import StartupFaker
from ort_files.document.fakers import FakeDocumentFactory


@pytest.fixture(scope="function")
def investment_instance():
    investor = InvestorFaker()
    user = UserFaker()
    UserInvestorRelationshipFaker(account=user, investor=investor)
    startup = StartupFaker()
    fundraising = FundraisingFaker(startup=startup)

    investment = InvestmentFaker(
        committed_amount=30000,
        fundraising=fundraising,
        status="validated",
        investor=investor,
    )
    investment.save()
    yield investment
    investment.delete()


@patch(
    "core_management.signals.signals_investment._insert_investment_to_investment_historical_value",
    autospec=True,
)
@pytest.mark.django_db
def test_signal_trigged(mock):
    user = UserFaker()
    investor = InvestorFaker()
    UserInvestorRelationshipFaker(account=user, investor=investor)
    startup = StartupFaker()
    fundraising = FundraisingFaker(
        startup=startup,
    )

    investment = InvestmentFaker(
        committed_amount=30000,
        fundraising=fundraising,
        status="validated",
        investor=investor,
    )
    investment.save()
    mock.assert_called_once()


@pytest.mark.django_db
@mute_signals(signals.post_save, signals.pre_save, signals.pre_delete)
def test_create_investment_historical_value_with_correct_attr(investment_instance):
    insert_investment_to_investment_historical_value(
        Investment, investment_instance, created=True
    )
    investment_historical_qs = InvestmentHistoricalValue.objects.filter(
        investment=investment_instance
    )
    assert investment_historical_qs
    investment_historical = investment_historical_qs.first()
    assert investment_historical.investment == investment_instance
    assert investment_instance.investor == investment_instance.investor
    assert investment_historical.fundraising == investment_instance.fundraising
    assert investment_historical.startup == investment_instance.fundraising.startup
    assert investment_historical.currency == investment_instance.fundraising.currency


@pytest.mark.django_db
class TestInvestmentSignalPipedriveIntegration:

    def test_signal_integration_create_deal(self):
        fundraising: Fundraising = FundraisingFaker(name="Hive Series A 2023 #3")
        user: CustomUser = UserFaker()
        investor: Investor = InvestorFaker()
        UserInvestorRelationshipFaker(account=user, investor=investor)
        with patch(
            "pipedrive.sdk.investors.sdk_integration.integrations.PipedriveDealUpdateIntegration.create_deal"
        ) as task:
            investment = Investment.objects.create(
                fundraising=fundraising, investor=investor, committed_amount=1000
            )
        create_deal_body: dict = task.call_args[0][0]
        assert create_deal_body["id"] == investment.id
        assert create_deal_body["investor_id"] == investor.id
        assert create_deal_body["user_id"] == user.id
        assert create_deal_body["committed_amount"] == investment.committed_amount
        assert create_deal_body["status"] == InvestmentStatusChoices.requested.name
        assert create_deal_body["fundraising_name"] == fundraising.name
        assert create_deal_body["title"] == f"{fundraising.name} Deal"
        assert create_deal_body["fees_percentage"] == investment.fees_percentage
        task.assert_called_once()

    def test_signal_integration_delete_deal(self):
        fundraising: Fundraising = FundraisingFaker(name="Hive Series A 2023 #3")
        user: CustomUser = UserFaker()
        investor: Investor = InvestorFaker()
        UserInvestorRelationshipFaker(account=user, investor=investor)
        with patch(
            "pipedrive.sdk.investors.sdk_integration.integrations.PipedriveDealUpdateIntegration.create_deal"
        ) as task_create:
            investment: Investment = Investment.objects.create(
                fundraising=fundraising, investor=investor, committed_amount=1000
            )
        task_create.assert_called()
        with patch(
            "pipedrive.sdk.investors.sdk_integration.integrations.PipedriveDealUpdateIntegration.delete_deal"
        ) as task_delete, patch(
            "pipedrive.sdk.investors.sdk_integration.integrations.PipedriveDealUpdateIntegration.check_trigger"
        ) as mock_check_deal_existence:
            mock_check_deal_existence.return_value = True
            investment.delete()
        task_delete.assert_called()

    def test_signal_integration_update_deal_status(self):
        fundraising: Fundraising = FundraisingFaker(name="Hive Series A 2023 #3")
        user: CustomUser = UserFaker()
        investor: Investor = InvestorFaker()
        UserInvestorRelationshipFaker(account=user, investor=investor)
        with patch(
            "pipedrive.sdk.investors.sdk_integration.integrations.PipedriveDealUpdateIntegration.create_deal"
        ) as task_create:
            investment = Investment.objects.create(
                id=2168,
                fundraising=fundraising,
                investor=investor,
                committed_amount=1000,
                status=InvestmentStatusChoices.intentional.name,
            )
        task_create.assert_called()
        with patch(
            "pipedrive.sdk.investors.sdk_integration.integrations.PipedriveDealUpdateIntegration.update_status"
        ) as task_update, patch(
            "pipedrive.sdk.investors.sdk_integration.integrations.PipedriveDealUpdateIntegration.check_trigger"
        ) as mock_check_deal_existence:
            mock_check_deal_existence.return_value = True
            investment.status = InvestmentStatusChoices.validated.name
            investment.save()
        update_deal_body: dict = task_update.call_args
        assert (
            update_deal_body[0][1]["status"] == InvestmentStatusChoices.validated.name
        )
        task_update.assert_called()

    def test_signal_integration_update_deal_sa(self):
        fundraising: Fundraising = FundraisingFaker(name="Hive Series A 2023 #3")
        investor: Investor = InvestorFaker()
        user: CustomUser = UserFaker()
        UserInvestorRelationshipFaker(account=user, investor=investor)
        with patch(
            "pipedrive.sdk.investors.sdk_integration.integrations.PipedriveDealUpdateIntegration.create_deal"
        ) as task_create:
            investment = Investment.objects.create(
                id=2168,
                fundraising=fundraising,
                investor=investor,
                committed_amount=1000,
                status=InvestmentStatusChoices.intentional.name,
            )
        task_create.assert_called()
        with patch(
            "pipedrive.sdk.investors.sdk_integration.integrations.PipedriveDealUpdateIntegration.update_status"
        ) as update_status:
            investment.document_subscription_agreement = FakeDocumentFactory()
            investment.save()
        with patch(
            "pipedrive.sdk.investors.sdk_integration.integrations.PipedriveDealUpdateIntegration.update_sa"
        ) as update_sa:
            BillFaker(investment=investment)
            investment.status = InvestmentStatusChoices.transfered.name
            investment.save()

        update_status_body: dict = update_status.call_args[0][1]
        update_status.assert_called()
        assert update_status_body["status"] == InvestmentStatusChoices.sa_signed.name
        update_sa.assert_called()
        assert (
            update_sa.call_args[0][1]["status"]
            == InvestmentStatusChoices.transfered.name
        )

    def test_signal_integration_update_deal_status_sa(self):
        fundraising: Fundraising = FundraisingFaker(name="Hive Series A 2023 #3")
        user: CustomUser = UserFaker()
        investor: Investor = InvestorFaker()
        UserInvestorRelationshipFaker(account=user, investor=investor)
        with patch(
            "pipedrive.sdk.investors.sdk_integration.integrations.PipedriveDealUpdateIntegration.create_deal"
        ) as task_create:
            investment = Investment.objects.create(
                id=2168,
                fundraising=fundraising,
                investor=investor,
                committed_amount=1000,
                status=InvestmentStatusChoices.intentional.name,
            )
        task_create.assert_called()
        with patch(
            "pipedrive.sdk.investors.sdk_integration.integrations.PipedriveDealUpdateIntegration.update_status"
        ) as task_update, patch(
            "pipedrive.sdk.investors.sdk_integration.integrations.PipedriveDealUpdateIntegration.check_trigger"
        ) as mock_check_deal_existence:
            mock_check_deal_existence.return_value = True
            investment.status = InvestmentStatusChoices.sa_sent.name
            investment.save()
        update_deal_body: dict = task_update.call_args
        assert update_deal_body[0][1]["status"] == InvestmentStatusChoices.sa_sent.name
        task_update.assert_called()

    def test_signal_integration_update_deal_status_auto(self):
        fundraising: Fundraising = FundraisingFaker(name="Hive Series A 2023 #3")
        investor: Investor = InvestorFaker()
        user: CustomUser = UserFaker()
        UserInvestorRelationshipFaker(account=user, investor=investor)
        with patch(
            "pipedrive.sdk.investors.sdk_integration.integrations.PipedriveDealUpdateIntegration.create_deal"
        ) as task_create:
            investment = Investment.objects.create(
                id=2168,
                fundraising=fundraising,
                investor=investor,
                committed_amount=1000,
                status=InvestmentStatusChoices.intentional.name,
            )
        task_create.assert_called()
        with patch(
            "pipedrive.sdk.investors.sdk_integration.integrations.PipedriveDealUpdateIntegration.update_status"
        ) as update_status:
            investment.document_subscription_agreement = FakeDocumentFactory()
            investment.save()
        update_status_body: dict = update_status.call_args[0][1]
        update_status.assert_called()
        assert update_status_body["status"] == InvestmentStatusChoices.sa_signed.name
