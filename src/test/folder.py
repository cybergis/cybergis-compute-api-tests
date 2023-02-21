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
import config  #noqa
import helpers #noqa

"""
Testing /folder (GET)
"""
def test_cant_access_folder_route_without_auth():
    """Tests that the /folder routes are inaccessible without the auth token"""
    response = config.get("/folder", auth=False)
    assert response.status_code == 402 # 402 error because no authentication
    assert json.loads(response.content)['error'] == 'invalid input' # correct error message

def test_can_access_folders():
    """Tests that given auth, we can access /folder and get a list of the user's folders"""
    response = config.get("/folder")
    assert response.status_code == 200 # makes sure request is successful
    content = response.content
    # makes sure recieved data is correct form
    assert "folder" in json.loads(content)
    assert len(json.loads(content)["folder"]) > 0 
    for i in json.loads(content)["folder"]:
        assert helpers.confirm_valid_folder(i)


"""
Testing /folder/:folderId (GET/PUT)
"""
def test_can_access_get_folder_folderid():
    """Tests that given auth, we can access a specific folder and load contents"""
    response = config.get(f"/folder/{helpers.get_user_folderid()}")
    assert response.status_code == 200 # makes sure request is successful
    content = response.content
    assert helpers.confirm_valid_folder(json.loads(content)[0])

def test_cant_access_get_folder_folderid_without_auth():
    """Tests that without auth, we cannot access a specific folder"""
    response = config.get(f"/folder/{helpers.get_user_folderid()}", auth=False)
    assert response.status_code == 402 # 402 error because no authentication
    assert json.loads(response.content)['error'] == 'invalid input' # correct error message

def test_can_access_put_folder_folderid():
    """Tests that given auth, we can access the put route but get an error because there is no body"""
    response = config.put(f"/folder/{helpers.get_user_folderid()}")
    assert response.status_code == 401 # 401 because no message body in put request
    assert json.loads(response.content)['error'] == 'encountered error: UpdateValuesMissingError: Cannot perform update query because update values are not defined. Call "qb.set(...)" method to specify updated values.' # ensures correct error

def test_cant_access_put_folder_folderid_without_auth():
    """Tests that given auth, we can access the put route but get an error because there is no body"""
    response = config.put(f"/folder/{helpers.get_user_folderid()}", auth=False)
    assert response.status_code == 402 # 402 error because no authentication
    assert json.loads(response.content)['error'] == 'invalid input' # correct error message


"""
Testing /folder/:folderId/download/globus-init (POST)
"""
def test_can_post_globus_init():
    """Tests that the globus init route is accessible but results in 402 invalid input error"""
    response = config.post(f"/folder/{helpers.get_user_folderid()}/download/globus-init")
    assert response.status_code == 402 # 402 because no content
    assert json.loads(response.content)['error'] == 'invalid input'
    assert json.loads(response.content)['messages'][0] != 'requires property "jupyterhubApiToken"' # confirms is not auth error

def test_cant_post_globus_init_without_auth():
    """Tests that the globus init route is accessible but results in 402 invalid input error"""
    response = config.post(f"/folder/{helpers.get_user_folderid()}/download/globus-init", auth=False)
    assert response.status_code == 402 # 402 error because no authentication
    assert json.loads(response.content)['error'] == 'invalid input'
    assert json.loads(response.content)['messages'][0] == 'requires property "jupyterhubApiToken"' # correct error


"""
Testing /folder/:folderId/download/globus-status (GET)
"""
def test_can_get_globus_status():
    """Tests that the globus status route is accessible and that contents can be loaded"""
    response = config.get(f"/folder/{helpers.get_user_folderid()}/download/globus-status")
    assert response.status_code == 200 # makes sure request is successful
    content = response.content
    assert json.loads(content) is not None # something is recieved

def test_cant_get_globus_status_without_auth():
    """Tests that the globus status route is accessible and that contents can be loaded"""
    response = config.get(f"/folder/{helpers.get_user_folderid()}/download/globus-status", auth=False)
    assert response.status_code == 402 # makes sure request is successful
    assert json.loads(response.content)['error'] == 'invalid input' # correct error