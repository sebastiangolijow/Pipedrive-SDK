import django_fsm
from django.db import models
from django.db import transaction
from django.dispatch import Signal
from django.dispatch import receiver

from cashflow.bill.models.models import Bill
from core_auth.models.user import CustomUser
from core_management.utils import RequestTypeChoices
from dealflow.investment.factory_investment_historical_value import (
    InvestmentHistoricalValueFactory,
)
from dealflow.investment.models.model_investhistvalue import InvestmentHistoricalValue
from dealflow.investment.models.models import Investment
from dealflow.valuations.models.models import Valuation
from entities.investor.models.models import Investor
from pipedrive.sdk.investors.sdk_integration.integrations import (
    PipedriveDealUpdateIntegration,
)
from pipedrive.sdk.investors.sdk_integration.integrations import (
    PipedriveInvestorIntegration,
)


def _insert_investment_to_investment_historical_value(instance: Investment):
    investment_historical: InvestmentHistoricalValue = InvestmentHistoricalValueFactory(
        investment=instance,
        investor=instance.investor,
        startup=instance.fundraising.startup,
        currency=instance.fundraising.currency,
        fundraising=instance.fundraising,
    )
    if Valuation.objects.filter(fundraising=instance.fundraising).exists():
        investment_historical.set_attributes_according_investment()


@receiver(models.signals.post_save, sender=Investment)
def insert_investment_to_investment_historical_value(
    sender, instance: Investment, created=False, **kwargs
):
    investment_historical_qs = InvestmentHistoricalValue.objects.filter(
        investment=instance
    )
    if not investment_historical_qs:
        _insert_investment_to_investment_historical_value(instance)


sa_signed_signal = Signal()


@receiver(models.signals.pre_save, sender=Investment)
def pipedrive_deal_integration_investment_update_deal(
    sender, instance: Investment, created=False, **kwargs
):
    """Signal to update Deal on Pipedrive when Investment is updated"""
    sa_signed_signal.send(sender=sender, instance=instance)


@receiver(django_fsm.signals.post_transition, sender=Investment)
def pipedrive_deal_integration_investment_update_deal_on_transition(
    sender, instance: Investment, created=False, **kwargs
):
    """Signal to update Deal on Pipedrive when Investment is updated"""
    sa_signed_signal.send(sender=sender, instance=instance)


@receiver(sa_signed_signal, sender=Investment)
def pipedrive_update_receiver(sender, instance, **kwargs):
    previous_instance_data: None = None
    try:
        previous_instance = sender.objects.get(pk=instance.pk)
        bill_count: int = Bill.objects.filter(investment=previous_instance).count()
        previous_instance_data: dict = {
            "status": previous_instance.status,
            "committed_amount": previous_instance.committed_amount,
            "fundraising_name": previous_instance.fundraising.name,
            "subscription_agreement": previous_instance.document_subscription_agreement,
            "bill_count": bill_count,
        }
    except Exception as e:
        print("Investment not found.", e)
    if previous_instance_data:
        investor: Investor = instance.investor
        try:
            if instance.creator_relationship:
                user: CustomUser = instance.creator_relationship.account
            else:
                user: CustomUser = investor.relationships.first().account
            bill_count: int = Bill.objects.filter(investment=instance).count()
            instance_data: dict = {
                "id": instance.id,
                "investor_name": investor.name,
                "investor_id": investor.id,
                "user_id": user.id,
                "user_name": f"{user.first_name} {user.last_name}",
                "committed_amount": instance.committed_amount,
                "status": instance.status,
                "fundraising_name": instance.fundraising.name,
                "document_subscription_agreement": instance.document_subscription_agreement,
                "title": f"{instance.fundraising.name} Deal",
                "fees_percentage": instance.fees_percentage,
                "bill_count": bill_count,
            }
            PipedriveInvestorIntegration.sync(investor, user)
            PipedriveDealUpdateIntegration.sync(
                instance_data, RequestTypeChoices.UPDATE.name, previous_instance_data
            )
            models.signals.post_save.disconnect(
                pipedrive_deal_integration_investment_create_deal, sender=Investment
            )
        except Exception as e:
            print(e)
    else:
        models.signals.post_save.connect(
            pipedrive_deal_integration_investment_create_deal, sender=Investment
        )


@receiver(models.signals.post_save, sender=Investment)
def pipedrive_deal_integration_investment_create_deal(
    sender, instance: Investment, created=False, **kwargs
):
    """Signal to create Deal on Pipedrive when Investment is updated"""
    investor: Investor = instance.investor
    try:
        if instance.creator_relationship:
            user: CustomUser = instance.creator_relationship.account
        else:
            user: CustomUser = investor.relationships.first().account
        PipedriveInvestorIntegration.sync(investor, user)
        instance_data: dict = {
            "id": instance.id,
            "investor_name": investor.name,
            "investor_id": investor.id,
            "user_id": user.id,
            "user_name": f"{user.first_name} {user.last_name}",
            "committed_amount": instance.committed_amount,
            "status": instance.status,
            "fundraising_name": instance.fundraising.name,
            "document_subscription_agreement": instance.document_subscription_agreement,
            "title": f"{instance.fundraising.name} Deal",
            "fees_percentage": instance.fees_percentage,
        }
        PipedriveDealUpdateIntegration.sync(
            instance_data, RequestTypeChoices.CREATE.name
        )
    except Exception as e:
        print(e)


@receiver(models.signals.pre_delete, sender=Investment)
def pipedrive_deal_integration_investment_delete_deal(
    sender, instance: Investment, created=False, **kwargs
):
    """Signal to create Deal on Pipedrive when Investment is updated"""
    instance_data: dict = {
        "id": instance.id,
        "committed_amount": instance.committed_amount,
        "status": instance.status,
        "fundraising_name": instance.fundraising.name,
        "document_subscription_agreement": instance.document_subscription_agreement,
        "title": f"{instance.fundraising.name} Deal",
        "fees_percentage": instance.fees_percentage,
    }
    PipedriveDealUpdateIntegration.sync(instance_data, RequestTypeChoices.DELETE.name)
