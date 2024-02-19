import requests

from pipedrive.sdk.investors.models.abstract_model import BaseInvestorFileModel


class PipedriveInvestorFile(BaseInvestorFileModel):
    def create(self, **kwargs):
        if kwargs:
            headers = {
                "X-Api-Token": self.params["api_token"],
                "User-Agent": "Testing",
                "Cache-Control": "no-cache",
                "Host": "api.pipedrive.com",
            }
            file = kwargs.pop("file")
            response = requests.post(
                self.url,
                headers=headers,
                data=kwargs,
                files=file,
            )
            return response.json()

    def delete(self, **kwargs):
        if kwargs:
            response = requests.delete(
                f"{self.url}/{kwargs.get('id')}", params=self.params
            )
        return response.json()
