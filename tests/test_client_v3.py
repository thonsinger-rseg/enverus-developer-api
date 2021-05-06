import os
import logging
from tempfile import TemporaryFile

from enverus_direct_access import (
    DeveloperAPIv3,
    DADatasetException,
    DAQueryException,
    DAAuthException,
)
from tests.utils import set_token_v3

set_token_v3()


LOG_LEVEL = logging.DEBUG
if os.environ.get("GITHUB_SHA"):
    LOG_LEVEL = logging.ERROR
DIRECTACCESSV3_API_KEY = os.environ.get("DIRECTACCESSV3_API_KEY")
DIRECTACCESSV3_TOKEN = os.environ.get("DIRECTACCESSV3_TOKEN")


def test_query_v3():
    d3 = DeveloperAPIv3(
        api_key=DIRECTACCESSV3_API_KEY,
        access_token=DIRECTACCESSV3_TOKEN,
        retries=5,
        backoff_factor=10,
        log_level=LOG_LEVEL
    )

    query = d3.query("casings", pagesize=100, deleteddate="null")
    records = list()
    for i, row in enumerate(query, start=1):
        # print(row)
        records.append(row)
        if i % 10 == 0:
            break
    assert records


test_query_v3()


def test_docs_v3():
    d3 = DeveloperAPIv3(
        api_key=DIRECTACCESSV3_API_KEY,
        access_token=DIRECTACCESSV3_TOKEN,
        retries=5,
        backoff_factor=10,
        log_level=LOG_LEVEL
    )
    docs = d3.docs("casings")
    assert docs
    assert isinstance(docs, list)


#test_docs_v3()


def test_ddl_v3():
    d3 = DeveloperAPIv3(
        api_key=DIRECTACCESSV3_API_KEY,
        access_token=DIRECTACCESSV3_TOKEN,
        retries=5,
        backoff_factor=10,
        log_level=LOG_LEVEL
    )
    ddl = d3.ddl("casings", database="pg")
    with TemporaryFile(mode="w+") as f:
        f.write(ddl)
        f.seek(0)
        for line in f:
            assert line.startswith("CREATE TABLE casings")
            break

    # Neg - test ddl with invalid database parameter
    try:
        ddl = d3.ddl("casings", database="invalid")
    except DAQueryException:
        pass

    return


#test_ddl_v3()


def test_count_v3():
    d3 = DeveloperAPIv3(
        api_key=DIRECTACCESSV3_API_KEY,
        access_token=DIRECTACCESSV3_TOKEN,
        retries=5,
        backoff_factor=10,
        log_level=LOG_LEVEL
    )
    count = d3.count("rigs", deleteddate="null")
    assert count is not None
    assert isinstance(count, int)

    # Neg - test count for invalid dataset
    try:
        count = d3.count("invalid")
    except DADatasetException as e:
        pass
    return


#test_count_v3()


def test_token_refresh_v3():
    d3 = DeveloperAPIv3(
        api_key=DIRECTACCESSV3_API_KEY,
        access_token="invalid",
        retries=5,
        backoff_factor=10,
        log_level=LOG_LEVEL
    )
    invalid_token = d3.access_token
    count = d3.count("rigs", deleteddate="null")
    query = d3.query("rigs", pagesize=10000, deleteddate="null")
    assert len([x for x in query]) == count
    assert invalid_token != d3.access_token

    # Test client with no credentials
    try:
        d3 = DeveloperAPIv3(
            api_key=None, log_level=LOG_LEVEL
        )
    except DAAuthException as e:
        pass

    return


#test_token_refresh_v3()
