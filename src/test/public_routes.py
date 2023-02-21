"""
This file is for testing that the API is up and public routes (no authentication)

    "/",
    "/container",
    "/git",
    "/hpc",
    "/maintainer",
    "/statistic",
    "/whitelist"
"""
import json
import pytest
import sys
sys.path.insert(0, "./src")
import config  # noqa


"""
Testing (GET) for /, /container, /git, /hpc, /maintainer, /statistic, and /whitelist
"""
@pytest.mark.parametrize("test_input", [
    (""),
    ("/container"),
    ("/git"),
    ("/hpc"),
    ("/maintainer"),
    ("/statistic"),
    ("/whitelist")
])
def test_can_access_page_and_load_response(test_input):
    """Tests that base url is accessible and that the content for each path can be loaded with JSON with or without a token"""
    response = config.get(test_input, auth=False)
    response2 = config.get(test_input)
    assert response.content == response2.content # same response with and without auth
    assert response.status_code == 200 
    assert response2.status_code == 200 # successful requests
    content = response.content
    content2 = response2.content
    assert json.loads(content) is not None
    assert json.loads(content2) is not None # something is recieved for data
