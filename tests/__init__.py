import os
from unittest import TestCase

from ossapi import OssapiV2, Ossapi, Grant, Scope


# technically all scopes except Scope.DELEGATE, since I don't own a bot account
ALL_SCOPES = [Scope.CHAT_WRITE, Scope.FORUM_WRITE, Scope.FRIENDS_READ,
    Scope.IDENTIFY, Scope.PUBLIC]
UNIT_TEST_MESSAGE = ("unit test from ossapi "
    "(https://github.com/circleguard/ossapi/), please ignore")

headless = os.environ.get("OSSAPI_TEST_HEADLESS", False)


class DevOssapiV2(OssapiV2):
    TOKEN_URL = "https://dev.ppy.sh/oauth/token"
    AUTH_CODE_URL = "https://dev.ppy.sh/oauth/authorize"
    BASE_URL = "https://dev.ppy.sh/api/v2"

def get_env(name):
    val = os.environ.get(name)
    if not val:
        val = input(f"Enter a value for {name}: ")
    return val

def setup_api_v1():
    key = get_env("OSU_API_KEY")
    return Ossapi(key)

def setup_api_v2():
    client_id = int(get_env("OSU_API_CLIENT_ID"))
    client_secret = get_env("OSU_API_CLIENT_SECRET")
    api_v2 = OssapiV2(client_id, client_secret, strict=True,
        grant=Grant.CLIENT_CREDENTIALS)

    if headless:
        api_v2_full = None
    else:
        redirect_uri = get_env("OSU_API_REDIRECT_URI")
        api_v2_full = OssapiV2(client_id, client_secret, redirect_uri,
            strict=True, grant=Grant.AUTHORIZATION_CODE, scopes=ALL_SCOPES)

    return (api_v2, api_v2_full)

def setup_api_v2_dev():

    if headless or not get_env("OSSAPI_TEST_RUN_DEV"):
        return None

    client_id = int(get_env("OSU_API_CLIENT_ID_DEV"))
    client_secret = get_env("OSU_API_CLIENT_SECRET_DEV")

    redirect_uri = get_env("OSU_API_REDIRECT_URI_DEV")
    return DevOssapiV2(client_id, client_secret, redirect_uri, strict=True,
        grant=Grant.AUTHORIZATION_CODE, scopes=ALL_SCOPES)

api_v1 = setup_api_v1()
api_v2, api_v2_full = setup_api_v2()
api_v2_dev = setup_api_v2_dev()


class TestCaseAuthorizationCode(TestCase):
    def setUp(self):
        if not api_v2_full:
            self.skipTest("Running in headless mode because "
                "OSSAPI_TEST_HEADLESS was set; skipping authorization code "
                "test.")

class TestCaseDevServer(TestCase):
    def setUp(self):
        if not api_v2_dev:
            self.skipTest("Dev api not set up; either OSSAPI_TEST_HEADLESS was "
                "set, or OSSAPI_TEST_RUN_DEV was not set.")
