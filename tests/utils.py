import os

from enverus_direct_access import (DirectAccessV2, DeveloperAPIv3)


def set_token():
    if not os.environ.get("DIRECTACCESS_TOKEN"):
        os.environ["DIRECTACCESS_TOKEN"] = DirectAccessV2(
            client_id=os.environ.get("DIRECTACCESS_CLIENT_ID"),
            client_secret=os.environ.get("DIRECTACCESS_CLIENT_SECRET"),
            api_key=os.environ.get("DIRECTACCESS_API_KEY"),
        ).access_token
    return


def set_token_v3():
    if not os.environ.get("DIRECTACCESSV3_TOKEN"):
        os.environ["DIRECTACCESSV3_TOKEN"] = DeveloperAPIv3(
            api_key=os.environ.get("DIRECTACCESSV3_API_KEY"),
        ).access_token
    return
