# -*- coding: utf-8 -*-
import falcon
from falcon import testing
import pytest
from unittest.mock import mock_open, call

from pprint import pprint
from app.api.app import init_app


@pytest.fixture
def client():
    app = init_app()
    return testing.TestClient(app)


# pytest will inject the object returned by the "client" function
# as an additional parameter.
def test_get_ping(client):

    response = client.simulate_get('/v1/ping')
    pprint(response)
    assert response.status == falcon.HTTP_OK