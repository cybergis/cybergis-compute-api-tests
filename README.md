# CyberGIS-Compute API Tests

**Authors:** CyberGIS-Compute Development Team. Alexander Michels, Taylor Ziegler, Mit Kotak.

This repository is designed to house a variety of tests for check that a CyberGIS-Compute Core API is functioning correctly. We use it as part of our development process to ensure that all routes are functional and returning reasonable results.

## Quickstart:

Configure key information in `secrets.json` (API url, username, token, etc.) and then from the root of the repo run:

```
> pytest src/test/*
```

## Overview:

The layout is relatively simple. All of the code is contained in `src/` and all of the tests are in `src/test`. There are a few key files for our testing framework:

* `src/config.py` - this offers configuration and a few helper functions for all tests. The Secrets class loads the configuration from `secrets.json` for use by tests. The helper functions it defines add the hashed token and appropriate header to the get/put/post call for simplicity. It is also helpful for manually inspecting API calls.
* `src/helpers.py` - Helpers to provide information required by other tests. For example, job Ids for jobid routes. These were originally [pytest fixtures](https://docs.pytest.org/en/6.2.x/fixture.html), but it was too complex to use fixtures from another file with parameterized functions. I tried a few things and they all failed.

The tests are in `src/test` and grouped logically.

* [`public_routes.py`](src/test/public_routes.py) tests public routes (i.e. ones that do not request authentication) like /git and /container.
* [`user.py`](src/test/user.py) tests /user and other user-centric routes.
* [`job.py`](src/test/job.py) tests /job and job-centric routes.
* [`folder.py`](src/test/folder.py) tests /folder and folder-centric routes.


## Notes:

* pytest was being weird when I set `body={}` as a default argument in the config functions because it was persisting the auth.