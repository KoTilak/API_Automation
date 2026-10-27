import pytest
from utils.excel_reader import ExcelReader

excel_reader = ExcelReader()

TEST_DATA = excel_reader.get_test_data("get_test_case_details")


@pytest.mark.parametrize(
    "test_data",
    TEST_DATA,
    ids=[row["test_case_id"] for row in TEST_DATA]
)
def test_get_testcase_details(api_client, test_data):
    endpoint = api_client.get_endpoint("get_test_case_details")

    params = {
        "project_id": int(test_data["project_id"]),
        "test_case_id": test_data["test_case_id_value"],
        "test_suite_id": int(test_data["test_suite_id"]),
    }

    response = api_client.get(endpoint, params=params)

    print("Request parameters:", params)
    print("Response status:", response.status_code)
    print("Response body:", response.text)

    expected_status = int(test_data["expected_status"])
    assert response.status_code == expected_status

    response_data = response.json()

    if expected_status == 200:
        assert response_data["success"] is True
        assert "data" in response_data
        assert isinstance(
            response_data["data"]["test_case_details"], list
        )
    elif expected_status == 404:
        assert response_data["success"] is False

