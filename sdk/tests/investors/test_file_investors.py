import os

import pytest

from pipedrive.sdk.investors.models.file_model import PipedriveInvestorFile


@pytest.mark.skip(reason="Skip it to no create files constantly on Pipedrive")
def test_file_model_create():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_name = "result.json"  # Replace with your actual JSON file name
    file_path = os.path.join(script_directory, file_name)

    files = {"file": ("new_file.json", open(file_path, "rb"), "file")}
    data = {"person_id": 15842, "file": files}

    file: PipedriveInvestorFile = PipedriveInvestorFile()
    response = file.create(**data)
    data = response["data"]
    assert response["success"] == True


@pytest.mark.skip(reason="Skip it to no delete files constantly on Pipedrive")
def test_file_model_delete():
    file: PipedriveInvestorFile = PipedriveInvestorFile()
    data: dict = {"id": 855}
    response = file.delete(**data)
    data = response["data"]
    assert response["success"] == True
