"""
Tests for the user-oriented routes

(All GET so far)
    "/user",
    "/user/job"
    "/user/jupyter-globus",
    "/user/slurm-usage"
"""
import pytest
import sys
sys.path.insert(0, "./src")
import config  # noqa
import json


"""
Testing (GET) for /user, /user/job, /user/jupyter-globus, and /user/slurm-usage
"""
@pytest.mark.parametrize("test_input", [
    ("/user"),
    ("/user/job"),
    ("/user/jupyter-globus"),
    ("/user/slurm-usage")
])
def test_cant_access_user_routes_without_auth(test_input):
    """Tests that the /user routes are inaccessible without the auth token"""
    response = config.get(test_input, auth=False)
    assert response.status_code == 402 # makes sure request is successful
    assert json.loads(response.content)['error'] == 'invalid input' # correct error


@pytest.mark.parametrize("test_input", [
    ("/user"),
    ("/user/job"),
    ("/user/jupyter-globus"),
    ("/user/slurm-usage")
])
def test_can_access_with_auth(test_input):
    """Tests that we get a 200 status from route with authentication"""
    response = config.get(test_input)
    assert response.status_code == 200 # makes sure request is successful
    content = response.content
    assert json.loads(content) is not None # ensures something is retrieved
