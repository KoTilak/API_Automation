import pytest
from utils.excel_reader import ExcelReader

# Read test cases from Excel
excel_reader = ExcelReader()
TEST_SUITE_TEST_DATA = excel_reader.get_test_data("get_test_suites")


@pytest.mark.parametrize(
    "test_data",
    TEST_SUITE_TEST_DATA,
    ids=[row["test_case_id"] for row in TEST_SUITE_TEST_DATA]
)
def test_get_test_suites(api_client, test_data):
    # Get the endpoint from config.ini
    endpoint = api_client.get_endpoint("get_test_suites")

    # Build query parameters from Excel.
    # Empty cells are omitted from the request.
    params = {}

    for key in (
        "status_filter",
        "page",
        "page_size",
        "sort_by",
        "sort_order",
        "project_id"
    ):
        value = test_data.get(key)

        if value is not None and str(value).strip() != "":
            if key in ("page", "page_size", "project_id"):
                value = int(value)

            params[key] = value

    # Send the GET request
    response = api_client.get(endpoint, params=params)
    print("Request parameters:",params)
    print("Response body:",response.text)

    # Validate the HTTP status code
    assert response.status_code == int(test_data["expected_status"]), (
        f"Test case: {test_data['test_case_id']}. "
        f"Expected status: {test_data['expected_status']}, "
        f"Actual status: {response.status_code}. "
        f"Response: {response.text}"
    )

    # Validate the response for successful requests
    if response.status_code == 200:
        response_data = response.json()

        assert response_data["success"] is True
        assert "data" in response_data
        assert "pagination_details" in response_data["data"]

