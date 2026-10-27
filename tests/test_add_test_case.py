import pytest
from utils.excel_reader import ExcelReader

excel_reader = ExcelReader()
ADD_TESTCASES_DATA = excel_reader.get_test_data("add_testcases")


@pytest.mark.parametrize(
    "test_data",
    ADD_TESTCASES_DATA,
    ids=[row["test_case_id"] for row in ADD_TESTCASES_DATA]
)
def test_add_testcases(api_client, test_data):
    endpoint = api_client.get_endpoint("add_test_case")
    # Prepare request body from Excel
    test_case_ids = test_data.get("test_case_ids")

    if isinstance(test_case_ids, str):
        import json
        test_case_ids = json.loads(test_case_ids)

    request_body = {
        "project_id": int(test_data["project_id"]),
        "test_suite_id": int(test_data["test_suite_id"]),
        "test_case_ids": test_case_ids
    }

    response = api_client.post(endpoint, json=request_body)

    # Validate HTTP status code
    expected_status = int(test_data["expected_status"])
    assert response.status_code == expected_status, (
        f"Expected {expected_status}, got {response.status_code}. "
        f"Response: {response.text}"
    )

    # Validate response body
    response_data = response.json()

    if expected_status == 200:
        assert response_data["success"] is True
        assert "data" in response_data
        assert isinstance(response_data["data"], list)

        returned_ids = [
            item["test_case_id"]
            for item in response_data["data"]
        ]
        assert test_case_ids[0] in returned_ids

    else:
        assert response_data["success"] is False
        assert isinstance(response_data.get("message"), str)
        assert response_data["message"].strip() != ""

