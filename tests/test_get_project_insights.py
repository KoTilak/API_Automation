import pytest
from utils.excel_reader import ExcelReader

excel_reader = ExcelReader()
PROJECT_INSIGHTS_TEST_DATA = excel_reader.get_test_data(
    "get_project_insights"
)


@pytest.mark.parametrize(
    "test_data",
    PROJECT_INSIGHTS_TEST_DATA,
    ids=[row["test_case_id"] for row in PROJECT_INSIGHTS_TEST_DATA]
)
def test_get_project_insights(api_client, test_data):
    endpoint = api_client.get_endpoint("get_project_insights")

    params = {}
    project_id = test_data.get("project_id")

    if project_id is not None and str(project_id).strip() != "":
        params["project_id"] = int(project_id)

    response = api_client.get(endpoint, params=params)

    assert response.status_code == int(test_data["expected_status"]), (
        f"Test case: {test_data['test_case_id']}; "
        f"Expected: {test_data['expected_status']}; "
        f"Actual: {response.status_code}; "
        f"Response: {response.text}"
    )

    if response.status_code == 200:
        response_data = response.json()

        assert response_data["success"] is True
        assert response_data["data"]["project_id"] == int(project_id)
        assert isinstance(
            response_data["data"]["average_execution_time_minutes"],
            (int, float)
        )
