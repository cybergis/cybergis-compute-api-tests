"""
Tests for the folder-oriented routes

    "/folder" (GET)
    "/folder/:folderId" (GET/DELETE/PUT)
    "/folder/:folderId/download/globus-init" (POST)
    "/folder/:folderId/download/globus-status" (GET)
"""
import json
import sys
sys.path.insert(0, "./src")
import config  # noqa
import helpers #noqa


def test_cant_access_folder_route_without_auth():
    """Tests that the /folder routes are inaccessible without the auth token"""
    response = config.get("/folder", auth=False)
    assert response.status_code == 402


def test_can_create_null_job():
    """Tests that given auth, we can access /job and create a job"""
    response = config.get("/folder")
    assert response.status_code == 200
    content = response.content
    json.loads(content)