import requests
import json


class DiscordRequestProcessor:
    """
    Wraps around the `requests` library to make it easier for us to make requests...
    """
    ALL_BASE_URLS = {
        "v6": "https://discord.com/api/v6/",
        "v7": "https://discord.com/api/v7/",
        "v8": "https://discord.com/api/v8/",
        "v9": "https://discord.com/api/v9/",
        "v10": "https://discord.com/api/v10/"
    }

    def __init__(self, base_url: str, x_super: str = None,
                 sec_ca_ua: str = "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"", platform: str = "Windows"):
        self.base_url = base_url

        if self.base_url not in self.ALL_BASE_URLS:
            raise TypeError("base_url must be one of {}".format(list(self.ALL_BASE_URLS.values())))

        if x_super is None:
            # predefined string from the Windows official discord client running newest version on a stable channel.
            x_super = "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MTYzIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJ4NjQiLCJzeXN0ZW1fbG9jYWxlIjoiZW4tVVMiLCJicm93c2VyX3VzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBkaXNjb3JkLzEuMC45MTYzIENocm9tZS8xMjQuMC42MzY3LjI0MyBFbGVjdHJvbi8zMC4yLjAgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjMwLjIuMCIsIm9zX3Nka192ZXJzaW9uIjoiMTkwNDUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjozMjkyNDQsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjUyMTUzLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="

        """
        Explanation of Predefined Headers:
        The predefined header has data fields that are filled beforehand,
        this is to make it so you aren't trackable + it becomes harder for discord to know if its official or not.
        
        There are some settings that 
        WARN: do NOT use `sec-cha-ua-platform = platform.system()` UNLESS the x_super is updated to match!
        """
        self.predefined_header = {  # all data-based ones are made up and mainly inaccurate.
            "accept": "*/*",
            "accept-language": "en-US",
            "x-super-properties": x_super,
            "sec-ch-ua": sec_ca_ua,
            "sec-ch-ua-mobile": "?0",
            "sec-cha-ua-platform": f"\"{platform}\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-discord-timezone": "America/Los_Angeles",  # might be wrong too but im a lazy bum
            "referrerPolicy": "strict-origin-when-cross-origin",
            "mode": "cors",
            "credentials": "include"
        }

    def post(self, path, body, token: str = None):
        if not token:
            nhead = self.predefined_header
        else:
            nhead = self.predefined_header[:]
            nhead["token"] = token

        return requests.post(self.base_url + path, json=body, headers=nhead)

    def get(self, path, token: str = None):
        if not token:
            nhead = self.predefined_header
        else:
            nhead = self.predefined_header[:]
            nhead["token"] = token

        return requests.get(self.base_url + path, headers=nhead, json=None)


def get_channel(drp: DiscordRequestProcessor, cid: int, token: str = None):
    return drp.get(f"channels/{cid}", token=token)
