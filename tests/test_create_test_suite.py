import pytest
from utils.excel_reader import ExcelReader

excel_reader = ExcelReader()
TEST_DATA = excel_reader.get_test_data("create_test_suite")


@pytest.mark.parametrize(
    "test_data",
    TEST_DATA,
    ids=[row["test_case_id"] for row in TEST_DATA]
)
def test_create_test_suite(api_client, test_data):
    endpoint = api_client.get_endpoint("create_test_suite")

    expected_status = int(test_data["expected_status"])

    payload = {
        "test_suite_name": test_data.get("test_suite_name"),
        "created_by": test_data.get("created_by"),
        "updated_by": test_data.get("updated_by"),
        "project_id": str(test_data.get("project_id")),
        "description": test_data.get("description"),
        "tool": test_data.get("tool"),
        "browser": test_data.get("browser"),
        "language": test_data.get("language"),
        "scheduled_test_suite": None
    }

    # Remove optional fields that are blank in Excel.
    payload = {
        key: value
        for key, value in payload.items()
        if value is not None and str(value).strip() != ""
    }

    # For the missing-name test, omit the required field entirely.
    if str(test_data["scenario"]).lower().find("without") >= 0:
        payload.pop("test_suite_name", None)

    response = api_client.post(endpoint, json=payload)

    assert response.status_code == expected_status, (
        f"Expected HTTP {expected_status}, got {response.status_code}. "
        f"Response: {response.text}"
    )

    response_data = response.json()

    if expected_status == 200:
        assert response_data["success"] is True
        assert response_data["data"]["test_suite_id"] is not None
        assert response_data["data"]["test_suite_name"] == payload["test_suite_name"]

    elif expected_status == 422:
        assert response_data["success"] is False

    elif expected_status == 400:
        assert response_data["success"] is False
        assert "already exists" in response_data["message"].lower()
