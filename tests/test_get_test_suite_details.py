import pytest
from utils.excel_reader import ExcelReader

excel_reader = ExcelReader()
TEST_DATA = excel_reader.get_test_data("get_test_suite_details")


@pytest.mark.parametrize(
    "test_data",
    TEST_DATA,
    ids=[row["test_case_id"] for row in TEST_DATA]
)
def test_get_test_suite_details(api_client, test_data):
    # Get endpoint from config.ini
    endpoint = api_client.get_endpoint("get_test_suite_details")

    # Build query parameters from Excel
    params = {
        "project_id": int(test_data["project_id"]),
        "user_id": str(test_data["user_id"]),
        "test_suite_id": int(test_data["test_suite_id"]),
        "page_size": int(test_data["page_size"]),
        "page": int(test_data["page"]),
    }

    # Send GET request
    response = api_client.get(endpoint, params=params)

    # Validate HTTP status code
    assert response.status_code == int(test_data["expected_status"]), (
        f"Test case: {test_data['test_case_id']}; "
        f"Expected: {test_data['expected_status']}; "
        f"Actual: {response.status_code}; "
        f"Response: {response.text}"
    )

    # Validate successful response structure
    if response.status_code == 200:
        response_data = response.json()

        assert response_data["success"] is True
        assert "data" in response_data
        assert "test_case_pagination" in response_data["data"]
        assert isinstance(response_data["data"]["test_cases"], list)

    # Validate expected error for nonexistent suite
    elif response.status_code == 404:
        response_data = response.json()
        assert response_data["success"] is False
        assert "not found" in response_data["message"].lower()

