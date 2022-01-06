from ossapi import OssapiV2, Ossapi, Grant, Scope

import os

client_id = os.environ.get("OSU_API_CLIENT_ID")
client_secret = os.environ.get("OSU_API_CLIENT_SECRET")
client_id_dev = os.environ.get("OSU_API_CLIENT_ID_DEV")
client_secret_dev = os.environ.get("OSU_API_CLIENT_SECRET_DEV")
key = os.environ.get("OSU_API_KEY")

if not client_id:
    client_id = input("Enter your api v2 client id: ")
if not client_secret:
    client_secret = input("Enter your api v2 client secret: ")
if not client_id_dev:
    client_id_dev = input("Enter your api v2 client id (dev server): ")
if not client_secret_dev:
    client_secret_dev = input("Enter your api v2 client secret (dev server): ")

client_id = int(client_id)
client_id_dev = int(client_id_dev)

class DevOssapiV2(OssapiV2):
    TOKEN_URL = "https://dev.ppy.sh/oauth/token"
    AUTH_CODE_URL = "https://dev.ppy.sh/oauth/authorize"
    BASE_URL = "https://dev.ppy.sh/api/v2"

# technically all scopes except Scope.DELEGATE, since I don't own a bot account
all_scopes = [Scope.CHAT_WRITE, Scope.FORUM_WRITE, Scope.FRIENDS_READ,
    Scope.IDENTIFY, Scope.PUBLIC]



api = OssapiV2(client_id, client_secret, strict=True,
    grant=Grant.CLIENT_CREDENTIALS)
api_full = OssapiV2(client_id, client_secret, strict=True,
    grant=Grant.AUTHORIZATION_CODE, scopes=all_scopes)
api_dev = DevOssapiV2(client_id_dev, client_secret_dev, strict=True,
    grant=Grant.AUTHORIZATION_CODE, scopes=all_scopes)
apiv1 = Ossapi(key)
