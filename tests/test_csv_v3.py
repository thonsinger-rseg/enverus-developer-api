import os
import csv
import logging
from tempfile import mkdtemp

from enverus_direct_access import DeveloperAPIv3
from tests.utils import set_token_v3

set_token_v3()


LOG_LEVEL = logging.DEBUG
if os.environ.get("GITHUB_SHA"):
    LOG_LEVEL = logging.ERROR
DIRECTACCESSV3_API_KEY = os.environ.get("DIRECTACCESSV3_API_KEY")
DIRECTACCESSV3_TOKEN = os.environ.get("DIRECTACCESSV3_TOKEN")


def test_csv_v3():
    """
    Write Direct Access query results to CSV

    :return:
    """
    tempdir = mkdtemp()
    path = os.path.join(tempdir, "rigs.csv")
    d3 = DeveloperAPIv3(
        api_key=DIRECTACCESSV3_API_KEY,
        access_token=DIRECTACCESSV3_TOKEN,
        retries=5,
        backoff_factor=10,
        log_level=LOG_LEVEL
    )

    dataset = "rigs"
    options = dict(pagesize=10000, deleteddate="null")
    count = d3.count(dataset, **options)
    query = d3.query(dataset, **options)
    d3.to_csv(
        query, path=path, log_progress=True, delimiter=",", quoting=csv.QUOTE_MINIMAL
    )

    with open(path, mode="r") as f:
        reader = csv.reader(f)
        row_count = len([x for x in reader])
        assert row_count == (count + 1)


if __name__ == "__main__":
    test_csv_v3()
