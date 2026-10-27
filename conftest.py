import pytest
from clients.api_client import ApiClient

@pytest.fixture
def api_client():
    return ApiClient(authenticated=True)

@pytest.fixture
def unauthenticated_api_client():
    return ApiClient(authenticated=False)

