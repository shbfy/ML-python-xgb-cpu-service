import falcon
import pytest
from falcon import testing

from app import number_of_workers


@pytest.fixture(scope="session")
def client():
    """Client to call tests against"""
    options = {
        'bind': '%s:%s' % ('0.0.0.0', '8080'),
        'workers': str(number_of_workers()),
    }
    return testing.TestClient(falcon.API(), options)
