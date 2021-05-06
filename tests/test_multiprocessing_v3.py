import os
import logging
from multiprocessing import Process

from enverus_direct_access import DeveloperAPIv3
from tests.utils import set_token_v3

set_token_v3()


LOG_LEVEL = logging.DEBUG
if os.environ.get("GITHUB_SHA"):
    LOG_LEVEL = logging.ERROR
DIRECTACCESSV3_API_KEY = os.environ.get("DIRECTACCESSV3_API_KEY")
DIRECTACCESSV3_TOKEN = os.environ.get("DIRECTACCESSV3_TOKEN")


def query(endpoint, access_token, **options):
    """
    Query method target for multiprocessing child processes.

    :param endpoint: a valid Direct Access API dataset endpoint
    :param access_token: a Direct Access API access token
    :param options: kwargs of valid query parameters for the dataset endpoint
    :return:
    """
    client = DeveloperAPIv3(
        api_key=DIRECTACCESSV3_API_KEY,
        access_token=DIRECTACCESSV3_TOKEN,
        retries=5,
        backoff_factor=5,
        log_level=LOG_LEVEL
    )

    resp = client.query(endpoint, **options)
    next(resp)
    assert resp
    return


def test_multiple_processes_v3():
    """
    Launch two child processes, one for rigs and one for casings.
    :return:
    """
    procs = list()
    a = Process(
        target=query, kwargs=dict(endpoint="rigs", access_token=DIRECTACCESSV3_TOKEN)
    )
    procs.append(a)

    b = Process(
        target=query, kwargs=dict(endpoint="casings", access_token=DIRECTACCESSV3_TOKEN)
    )
    procs.append(b)

    [x.start() for x in procs]
    [x.join() for x in procs]
    return


if __name__ == "__main__":
    test_multiple_processes_v3()
