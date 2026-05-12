import copy
import importlib

from fastapi.testclient import TestClient

app_module = importlib.import_module("src.app")
BASE_ACTIVITIES = copy.deepcopy(app_module.activities)


def pytest_configure(config):
    # Ensure any module imports use the clean initial state for the app.
    app_module.activities = copy.deepcopy(BASE_ACTIVITIES)


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities = copy.deepcopy(BASE_ACTIVITIES)
    yield


@pytest.fixture
def client():
    return TestClient(app_module.app)
