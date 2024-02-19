from django.urls import path

from pipedrive.app.views.pipedrive_webhook.view_deal_webhook import (
    PipedriveInvestorWebhook,
)


app_name = "pipedrive-sdk"

pipedrive_sdk: list = [
    path(
        "pipedrive-sdk/investors/",
        PipedriveInvestorWebhook.as_view(),
        name="pipedrive-investors-webhook",
    )
]
