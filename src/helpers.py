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

def get_user_folderid():
    """Gets the the ID of a user's folder"""
    return get_user_job()['remoteExecutableFolder']['id']

def confirm_job_format(job):
    to_return = 'id' in job
    to_return = to_return and 'userId' in job
    to_return = to_return and 'secretToken' in job
    to_return = to_return and 'slurmId' in job
    to_return = to_return and 'maintainer' in job
    to_return = to_return and 'hpc' in job
    to_return = to_return and 'remoteExecutableFolder' in job
    to_return = to_return and 'remoteDataFolder' in job
    to_return = to_return and 'remoteResultFolder' in job
    to_return = to_return and 'localExecutableFolder' in job
    to_return = to_return and 'localDataFolder' in job
    to_return = to_return and 'param' in job
    to_return = to_return and 'env' in job
    to_return = to_return and 'slurm' in job
    to_return = to_return and 'createdAt' in job
    to_return = to_return and 'updatedAt' in job
    to_return = to_return and 'deletedAt' in job
    to_return = to_return and 'initializedAt' in job
    to_return = to_return and 'finishedAt' in job
    to_return = to_return and 'isFailed' in job
    to_return = to_return and 'events' in job
    to_return = to_return and 'logs' in job
    return to_return

def confirm_logs_format(logs):
    to_return = 'id' in logs
    to_return = to_return and 'jobId' in logs
    to_return = to_return and 'message' in logs
    to_return = to_return and 'createdAt' in logs
    to_return = to_return and 'updatedAt' in logs
    to_return = to_return and 'deletedAt' in logs
    return to_return

def confirm_job_event_format(event):
    return confirm_logs_format(event) and 'type' in event

def confirm_valid_folder(folder):
    to_return = 'id' in folder
    to_return = to_return and 'name' in folder
    to_return = to_return and 'hpc' in folder
    to_return = to_return and 'hpcPath' in folder
    to_return = to_return and 'globusPath' in folder
    to_return = to_return and 'userId' in folder
    to_return = to_return and 'isWritable' in folder
    to_return = to_return and 'createdAt' in folder
    to_return = to_return and 'updatedAt' in folder
    to_return = to_return and 'deletedAt' in folder
    return to_return