"""
Helpers that are used across multiple files
"""
import json
import sys
sys.path.insert(0, "./src")
import config  # noqa


def get_user_jobs():
    """
    Grabs the user jobs so we have job ids for testing
    """
    return json.loads(config.get("/user/job").content)


def get_user_job():
    """Gets the first job from the job data"""
    return get_user_jobs()["job"][0]


def get_user_jobid():
    """Gets the job id for a user job"""
    return get_user_job()["id"]
