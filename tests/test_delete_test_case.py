import json
import pytest
from utils.excel_reader import ExcelReader

excel_reader = ExcelReader()
DELETE_TESTCASE_DATA = excel_reader.get_test_data("delete_test_case")


@pytest.mark.parametrize(
    "test_data",
    DELETE_TESTCASE_DATA,
    ids=[row["test_case_id"] for row in DELETE_TESTCASE_DATA]
)
def test_delete_testcase(api_client, test_data):
    endpoint = api_client.get_endpoint("delete_test_case")

    request_body = {
        "project_id": int(test_data["project_id"]),
        "test_suite_id": int(test_data["test_suite_id"])
    }

    # Include test_case_ids only when Excel contains a value.
    test_case_ids = test_data.get("test_case_ids")

    if test_case_ids is not None and str(test_case_ids).strip():
        if isinstance(test_case_ids, str):
            test_case_ids = json.loads(test_case_ids)

        request_body["test_case_ids"] = test_case_ids

    response = api_client.delete(
        endpoint,
        json=request_body
    )

    expected_status = int(test_data["expected_status"])

    assert response.status_code == expected_status, (
        f"Test case: {test_data['test_case_id']}; "
        f"Expected status: {expected_status}; "
        f"Actual status: {response.status_code}; "
        f"Response: {response.text}"
    )

    response_data = response.json()

    if expected_status == 200:
        assert response_data["success"] is True
        assert response_data["message"] == "Test cases deleted successfully"
        assert response_data["status_code"] == 200
        assert response_data["data"] is None

    else:
        assert response_data["success"] is False
        assert isinstance(response_data.get("message"), str)
        assert response_data["message"].strip() != ""
        assert response_data["status_code"] == expected_status

