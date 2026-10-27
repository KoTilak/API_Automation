import pytest
from utils.excel_reader import ExcelReader

excel_reader = ExcelReader()
PROJECT_TEST_DATA = excel_reader.get_test_data("get_projects")


@pytest.mark.parametrize(
    "test_data",
    PROJECT_TEST_DATA,
    ids=[row["test_case_id"] for row in PROJECT_TEST_DATA]
)
def test_get_projects(
    api_client,
    unauthenticated_api_client,
    test_data
):
    is_authenticated = (
        str(test_data["authenticated"]).strip().lower()
        in ("true", "yes", "1")
    )

    if is_authenticated:
        client = api_client
    else:
        client = unauthenticated_api_client

    endpoint = client.get_endpoint("get_projects")
    response = client.get(endpoint)

    assert response.status_code == int(
        test_data["expected_status"]
    )

    if is_authenticated:
        response_data = response.json()

        assert response_data["success"] is True
        assert isinstance(
            response_data["data"]["projects"], list
        )
