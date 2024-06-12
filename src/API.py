"""
This file handles all (except websocket) interactions with Discord
"""
import enum
import requests


class VERSION(enum.StrEnum):
    V9 = "https://discord.com/api/v9",
    CDN = "https://cdn.discordapp.com"


class LOGIN(enum.StrEnum):
    INVALID = "INVALID_LOGIN"


class Request:
    """
    Represents a Discord API request

    TODO: update this to be better docs
    Only thing that matters is that version is the version (enum above) and route is the /blah/blah to the location.
    """

    def __init__(self, version: VERSION, method: str, route: str, params=None, headers: dict = None, json=None):
        self.version = version
        self.method = method.upper()
        self.route = route
        self.params = params if params else ""
        self.headers = headers if headers else {}
        self.json = json

    def execute(self):
        url = self.version.value + self.route
        return _request(self.method, url, headers=self.headers, json=self.json, params=self.params)


def _request(method: str, url: str, params=None, headers: dict = None, json=None) -> requests.Response:
    req = requests.request(method, url, params=params, headers=headers, json=json)

    return req


def login(username: str, password: str) -> LOGIN | str:
    """
    Login to Discord (in the future will support 2FA, but currently not supported.
    :param username:
    :param password:
    :return: Token in string format (or ERROR)
    """
    headers = {
        "accept": "*/*",
        "accept-language": "en-US",
        "content-type": "application/json",
        "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-debug-options": "bugReporterEnabled",
        "x-discord-locale": "en-US",
        "x-discord-timezone": "America/Los_Angeles",
        "x-fingerprint": "1244718084334551139.OFak6GfmfKdYW5NEtoAB9gCC4GY",
        "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJwdGIiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC4xMDgyIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJ4NjQiLCJzeXN0ZW1fbG9jYWxlIjoiZW4tVVMiLCJicm93c2VyX3VzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBkaXNjb3JkLzEuMC4xMDgyIENocm9tZS8xMjAuMC42MDk5LjI5MSBFbGVjdHJvbi8yOC4yLjEwIFNhZmFyaS81MzcuMzYiLCJicm93c2VyX3ZlcnNpb24iOiIyOC4yLjEwIiwiY2xpZW50X2J1aWxkX251bWJlciI6Mjk2NDU4LCJuYXRpdmVfYnVpbGRfbnVtYmVyIjo0ODE2NiwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiZGVzaWduX2lkIjowfQ=="
    }

    payload = {
        "login": username,
        "password": password,
        "undelete": False,
        "captcha": None,
        "login_source": None,
        "gift_code_sku_id": None
    }

    req = Request(VERSION.V9, "POST", "/auth/login", headers=headers, json=payload)

    res = req.execute()

    json_res = res.json()
    print(json_res)

    if res.status_code != 200:
        # assume login error (there's a possibility it's an captcha error but that's a later me issue!
        # TODO: (read above)
        errs = json_res["errors"]["login"]["_errors"]

        for e in errs:
            if e["code"] == "INVALID_LOGIN":
                return LOGIN.INVALID

    return json_res["token"]


if __name__ == "__main__":
    # test code
    with open("./testpass.secret", "r") as f:
        email, passw = f.read().split(";")

    print(login(email, passw))
