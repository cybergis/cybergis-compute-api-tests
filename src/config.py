"""
Config file for putting useful information that is used across tests.
"""
import base64
import json
import requests


class Secrets():
    def __init__(self):
        """Loads the secrets"""
        secret_dict = json.loads(open("secrets.json").read())
        self.__dict__ = secret_dict
        self.hashed_token = base64.b64encode((f"{self.jupyter_host}@{self.jupyter_token}").encode('ascii')).decode('utf-8')


secrets = Secrets()


def get(route, body=None, auth=True):
    """Sends a get request the api with auth token"""
    if body is None:
        del body  # pytest is being weird and copying this
        body = {}
    uri = secrets.api_url + route
    headers = {'Content-type': 'application/json'}
    if auth:
        body["jupyterhubApiToken"] = secrets.hashed_token
    # print(uri, body)
    return requests.get(
        uri,
        headers=headers,
        data=json.dumps(body)
    )


def post(route, body=None, auth=True):
    """Sends a post request to the api with auth token"""
    if body is None:
        body = {}
    uri = secrets.api_url + route
    headers = {'Content-type': 'application/json'}
    if auth:
        body["jupyterhubApiToken"] = secrets.hashed_token
    return requests.post(
        uri,
        headers=headers,
        data=json.dumps(body)
    )


def put(route, body=None, auth=True):
    """Sends a put request to the api with auth token"""
    if body is None:
        body = {}
    uri = secrets.api_url + route
    headers = {'Content-type': 'application/json'}
    if auth:
        body["jupyterhubApiToken"] = secrets.hashed_token
    return requests.put(
        uri,
        headers=headers,
        data=json.dumps(body)
    )


if __name__ == "__main__":
    """It's helpful to use this file for debugging and seeing what API output looks lik"""
    # x = get("/job/1653062379l80l3")
    # x = get("/folder", auth=False)
    x = requests.get("https://cgjobsup-test.cigi.illinois.edu/v2/job/1653062379l80l3/result-folder-content")
    # x = requests.get("https://cgjobsup-test.cigi.illinois.edu/v2/job/1653062379l80l3/result-folder-content")
    print(x.status_code)
    print(json.dumps(json.loads(x.content), indent=4))
