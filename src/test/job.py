"""
Tests for the job-oriented routes

    "/job" (POST)
    "/job/:jobId" (GET, PUT)
    "/job/:jobId/events" (GET)
    "/job/:jobId/logs" (GET)
    "/job/:jobId/result-folder-content" (GET)
    "/job/:jobId/submit" (POST)
    "/statistic/job/:jobId (GET)

Not fully implemented, but routes exist
    "/job/:jobId/cancel" (PUT)
    "/job/:jobId/pause" (PUT)
    "/job/:jobId/resume" (PUT)

We use pytest fixtures for some info like job ids. For more info see:
https://docs.pytest.org/en/6.2.x/fixture.html
"""
import json
import pytest
import sys
sys.path.insert(0, "./src")
import config  # noqa
import helpers  # noqa

"""
Testing /job (POST) 
"""
def test_cant_access_job_post_route_without_auth():
    """Tests that the /job route is inaccessible without the auth token"""
    response = config.post("/job", auth=False)
    assert response.status_code == 402 # 402 error because no authentication
    assert json.loads(response.content)['error'] == 'invalid input' # correct error message

def test_can_create_null_job():
    """Tests that given auth, we can access /job and get a JSON response"""
    response = config.post("/job")
    assert response.status_code == 200 # makes sure request is successful
    content = response.content
    formatted = json.loads(content)
    assert helpers.confirm_job_format(formatted) # makes sure the information rtecieved has correct attributes

"""
Testing /job/:jobId (PUT)
"""
def test_cant_access_job_id_put_route_without_auth():
    """Tests that the /job/:jobId route is inaccessible without the auth token"""
    jobid = helpers.get_user_jobid()
    route = "/job/{}".format(jobid)  # fill in job id if there is a space
    response = config.put(route, auth=False)
    assert response.status_code == 402 # 402 error because no authentication
    assert json.loads(response.content)['error'] == 'invalid input' # correct error message

def test_cant_access_job_id_put_route_with_auth():
    """Tests that the /job/:jobId route is inaccessible without the auth token"""
    jobid = helpers.get_user_jobid()
    route = "/job/{}".format(jobid)  # fill in job id if there is a space
    response = config.put(route)
    assert response.status_code == 403 # 403 error because no content
    assert json.loads(response.content)['error'] == 'internal error'

"""
Testing /job/:jobId (GET), /job/:jobId/events (GET), /job/:jobId/logs (GET), and /job/:jobId/result-folder-content (GET) with no authorization
"""
@pytest.mark.parametrize("test_input", [
    ("/job/{}"),
    ("/job/{}/events"),
    ("/job/{}/logs"), # as of 02/20/2023 returns 200 when should be 402 but correct error message
    ("/job/{}/result-folder-content") # as of 02/20/2023 returns 200 when should be 402 but correct error message
])
def test_cant_access_job_id_get_routes_without_auth(test_input):
    jobid = helpers.get_user_jobid()
    route = test_input.format(jobid)  # fill in job id if there is a space
    response = config.get(route, auth=False)
    assert response.status_code == 402 # 402 error because no authentication
    assert json.loads(response.content)['error'] == 'invalid input' # correct error message

"""
Testing /job/:jobId (GET) with authorization
"""
def test_can_get_job_info_for_id():
    """Tests that given auth, we can access /job/:id and get a JSON response"""
    response = config.get(f"/job/{helpers.get_user_jobid()}")
    assert response.status_code == 200 # makes sure request is successful
    content = response.content
    formatted = json.loads(content)
    assert helpers.confirm_job_format(formatted) # confirms data can be loaded and is reasonable

"""
Testing /job/:jobId/events (GET) with authorization
"""
def test_can_access_job_id_events_get_route_with_auth():
    jobid = helpers.get_user_jobid()
    route = "/job/{}/events".format(jobid)  # fill in job id if there is a space
    response = config.get(route)
    assert response.status_code == 200 # makes sure request is successful
    content = response.content
    formatted = json.loads(content)
    assert len(formatted) > 0
    for i in formatted:
        assert helpers.confirm_job_event_format(i) # confirms data can be loaded and is reasonable

"""
Testing /job/:jobId/logs (GET) with authorization
"""
def test_can_access_logs_with_auth():
    response = config.get(f"/job/{helpers.get_user_jobid()}/logs")
    assert response.status_code == 200 # makes sure request is successful
    content = response.content
    formatted = json.loads(content)
    assert len(formatted) > 0
    for i in formatted:
        assert(helpers.confirm_logs_format(i)) # confirms data can be loaded and is reasonable


"""
Testing /job/:jobId/result-folder-content (GET) with authorization
"""
def test_can_get_info_for_result_folder():
    response = config.get(f"/job/{helpers.get_user_jobid()}/result-folder-content")
    assert response.status_code == 200 # makes sure request is successful
    content = response.content
    formatted = json.loads(content)
    assert(len(formatted) > 0) # confirms data can be loaded and is reasonable


"""
Testing /job/:jobId/submit" (POST) 
"""
def test_can_post_using_submit():
    response = config.post(f"/job/{helpers.get_user_jobid()}/submit")
    assert response.status_code == 401 # uses a previous job ID so results in error
    assert json.loads(response.content)['error'] == 'job already submitted or in queue' # correct error message

def test_cant_post_using_submit_without_auth():
    response = config.post(f"/job/{helpers.get_user_jobid()}/submit", auth=False)
    assert response.status_code == 402
    assert json.loads(response.content)['error'] == 'invalid input' # correct error message


"""
Testing /statistic/job/:jobId (GET)
"""
def test_cant_access_job_stats_with_auth():
    response = config.get(f"/statistic/job/{helpers.get_user_jobid()}", auth=False)
    assert response.status_code == 402 # 402 error because no authentication
    assert json.loads(response.content)['error'] == 'invalid input' # correct error message

def test_can_access_job_stats_with_auth():
    response = config.get(f"/statistic/job/{helpers.get_user_jobid()}")
    assert response.status_code == 200 # makes sure request is successful
    content = response.content
    formatted = json.loads(content)
    assert 'runtime_in_seconds' in formatted # confirms data can be loaded and is reasonable


"""
These paths are not yet implemented, and if run the user will get a 504 error from it timing out
"""
# @pytest.mark.parametrize("test_input", [
#     ("/job/{}/cancel"),
#     ("/job/{}/pause"),
#     ("/job/{}/resume")
# ])
# def test_cancel_pause_resume_put_routes_exists(test_input):
#     response = config.put(test_input.format(helpers.get_user_jobid()))
#     assert response.status_code == 200