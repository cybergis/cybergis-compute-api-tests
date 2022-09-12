"""
This file is for testing that the API is up and public routes (no authentication)

    "/container",
    "/git",
    "/hpc",
    "/maintainer",
    "/statistic"
"""
import json
import pytest
import sys
sys.path.insert(0, "./src")
import config  # noqa


@pytest.mark.parametrize("test_input", [
    (""),
    ("/container"),
    ("/git"),
    ("/hpc"),
    ("/maintainer"),
    ("/statistic")
])
def test_can_access_page(test_input):
    """Tests that I can get the base url"""
    response = config.get(test_input, auth=False)
    assert response.status_code == 200


@pytest.mark.parametrize("test_input", [
    (""),
    ("/container"),
    ("/git"),
    ("/hpc"),
    ("/maintainer"),
    ("/statistic")
])
def test_can_load_json_response(test_input):
    """Tests that the content for /container can be loaded with JSON"""
    response = config.get(test_input, auth=False)
    content = response.content
    json.loads(content)
