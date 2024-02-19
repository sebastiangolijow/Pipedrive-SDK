from django.conf import settings


stage_pipedrive_potential_deal_id_sandbox: int = 5
stage_pipedrive_potential_deal_id_prod: int = 3
stage_pipedrive_potential_deal_id = (
    stage_pipedrive_potential_deal_id_sandbox
    if settings.ENVIRONMENT_NAME in ["local", "dev", "test", "staging"]
    or settings.TESTING_ENV == True
    else stage_pipedrive_potential_deal_id_prod
)
stage_pipedrive_call_organized_id_sandbox: int = 4
stage_pipedrive_call_organized_id_prod: int = 2
stage_pipedrive_call_organized_id = (
    stage_pipedrive_call_organized_id_sandbox
    if settings.ENVIRONMENT_NAME in ["local", "dev", "test", "staging"]
    or settings.TESTING_ENV == True
    else stage_pipedrive_call_organized_id_prod
)
stage_pipedrive_information_sent_id_sandbox: int = 3
stage_pipedrive_information_sent_id_prod: int = 1
stage_pipedrive_information_sent_id = (
    stage_pipedrive_information_sent_id_sandbox
    if settings.ENVIRONMENT_NAME in ["local", "dev", "test", "staging"]
    or settings.TESTING_ENV == True
    else stage_pipedrive_information_sent_id_prod
)


class TriggerAndActionMixin:
    """
    Base class that contains two functions:
    - check_trigger
    - execute_action
    """

    def __init__(
        self,
        response,
        user_data,
        investor_data,
        deal_id,
        investment_value,
        fundraising,
        missing_data,
        stage_pipedrive_call_organized_id,
        person_id,
        org_id,
    ) -> None:
        self.response = response
        self.user_data = user_data
        self.investor_data = investor_data
        self.deal_id = deal_id
        self.investment_value = investment_value
        self.fundraising = fundraising
        self.missing_data = missing_data
        self.stage_pipedrive_call_organized_id = stage_pipedrive_call_organized_id
        self.person_id = person_id
        self.org_id = org_id

    def check_trigger(self):
        pass

    def execute_action(self):
        pass


class NoActionNeeded(TriggerAndActionMixin):
    def check_trigger(self):
        return self.is_deal_just_created_or_previous_stage_info_sent()

    def execute_action(self):
        return self.no_action_needed()

    def deal_was_moved_back_to_call_organized_from_potential_deal(self):
        return (
            self.response["previous"]["stage_id"] == stage_pipedrive_potential_deal_id
            and self.response["current"]["stage_id"]
            == stage_pipedrive_call_organized_id
        )

    def deal_updated_with_no_differences_in_stage(self):
        return (
            self.response["previous"]["stage_id"]
            == self.response["current"]["stage_id"]
            and self.response["previous"]["status"]
            == self.response["current"]["status"]
        )

    def deal_move_from_info_sent_to_call_organized(self):
        return (
            self.response["current"]["stage_id"] == stage_pipedrive_call_organized_id
            and self.response["previous"]["stage_id"]
            == stage_pipedrive_information_sent_id
        )

    def deal_move_back_to_info_sent(self):
        return (
            self.response["current"]["stage_id"] == stage_pipedrive_information_sent_id
        )

    def deal_already_lost(self):
        return (
            self.response["current"]["status"] == "lost"
            and self.response["previous"]["status"] == "lost"
        )

    def deal_reopen(self):
        return (
            self.response["current"]["status"] == "open"
            and self.response["previous"]["status"] == "lost"
        )

    def is_deal_just_created_or_previous_stage_info_sent(self):
        is_valid = (
            not self.response["previous"]
            or self.deal_move_back_to_info_sent()
            or self.deal_was_moved_back_to_call_organized_from_potential_deal()
            or self.deal_updated_with_no_differences_in_stage()
            or self.deal_move_from_info_sent_to_call_organized()
            or self.deal_already_lost()
            or self.deal_reopen()
        )
        return is_valid

    def no_action_needed(self):
        return "No action needed"
