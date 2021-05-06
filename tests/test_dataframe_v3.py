import os
import logging

from pandas.api.types import is_datetime64_ns_dtype, is_float_dtype, is_int64_dtype

from enverus_direct_access import DeveloperAPIv3
from tests.utils import set_token_v3

set_token_v3()


LOG_LEVEL = logging.DEBUG
if os.environ.get("GITHUB_SHA"):
    LOG_LEVEL = logging.ERROR
DIRECTACCESSV3_API_KEY = os.environ.get("DIRECTACCESSV3_API_KEY")
DIRECTACCESSV3_TOKEN = os.environ.get("DIRECTACCESSV3_TOKEN")


def test_dataframe_v3():
    d3 = DeveloperAPIv3(
        api_key=DIRECTACCESSV3_API_KEY,
        access_token=DIRECTACCESSV3_TOKEN,
        retries=5,
        backoff_factor=10,
        log_level=LOG_LEVEL
    )
    df = d3.to_dataframe("rigs", pagesize=10000, deleteddate="null")

    # Check index is set to API endpoint "primary key"
    assert df.index.names[0] == "CompletionID"
    assert df.index.names[1] == "WellID"

    # Check datetime64 dtypes
    assert is_datetime64_ns_dtype(df.DeletedDate)
    assert is_datetime64_ns_dtype(df.SpudDate)
    assert is_datetime64_ns_dtype(df.UpdatedDate)

    # Check Int64 dtypes
    assert is_int64_dtype(df.RatedWaterDepth)
    assert is_int64_dtype(df.RatedHP)

    # Check float dtypes
    assert is_float_dtype(df.RigLatitudeWGS84)
    assert is_float_dtype(df.RigLongitudeWGS84)

    return


if __name__ == "__main__":
    test_dataframe_v3()
