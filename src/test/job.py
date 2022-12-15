"""
Tests for the job-oriented routes

    "/job" (POST)
    "/job/:jobId" (GET, PUT)
    "/job/:jobId/events" (GET)
    "/job/:jobId/logs" (GET)
    "/job/:jobId/result-folder-content" (GET)
    "/job/:jobId/submit" (POST)

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


@pytest.mark.parametrize("test_input", [
    ("/job/{}"),
    ("/job/{}/events")
])
def test_cant_access_job_get_routes_without_auth(test_input):
    """Tests that the /user routes are inaccessible without the auth token"""
    jobid = helpers.get_user_jobid()
    route = test_input.format(jobid)  # fill in job id if there is a space
    response = config.get(route, auth=False)
    assert response.status_code == 402


def test_cant_access_job_route_without_auth():
    """Tests that the /job route are inaccessible without the auth token"""
    response = config.post("/job", auth=False)
    assert response.status_code == 402


def test_can_create_null_job():
    """Tests that given auth, we can access /job and get a JSON response

    TODO: add more assertions to this test.
    """
    response = config.post("/job")
    assert response.status_code == 200
    content = response.content
    json.loads(content)


def test_can_get_job_info_for_id():
    """Tests that given auth, we can access /job/:id and get a JSON response"""
    response = config.get(f"/job/{helpers.get_user_jobid()}")
    assert response.status_code == 200
    content = response.content
    json.loads(content)

def test_can_get_info_for_result_folder():
    response = config.get(f"/job/{helpers.get_user_jobid()}/result-folder-content")
    assert response.status_code == 200
    content = response.content
    json.loads(content)

def test_can_get_info_for_result_folder():
    config.get(f"/job/{helpers.get_user_jobid()}/submit")
    response = config.get(f"/job/{helpers.get_user_jobid()}/submit")
    assert response.status_code == 404

def cancel_route_exists():
    response = config.get(f"/job/{helpers.get_user_jobid()}/cancel")
    assert response.status_code == 200

def pause_route_exists():
    response = config.get(f"/job/{helpers.get_user_jobid()}/pause")
    assert response.status_code == 200

def resume_route_exists():
    response = config.get(f"/job/{helpers.get_user_jobid()}/resume")
    assert response.status_code == 200

def can_access_logs_with_auth():
    response = config.get(f"/job/{helpers.get_user_jobid()}/logs")
    assert response.status_code == 200
    content = response.content
    json.loads(content)