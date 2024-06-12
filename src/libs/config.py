"""
Copied (then modified) from Arjun Launcher
"""
from pathlib import Path
import json


def findSettingsFile():  # notTODO: change this to write it in this file, or be a one time thing (maybe?)
    dots = "."
    while True:
        try:
            print(f"trying {dots}/settings.json")
            file = open(f"{dots}/settings.json")
        except FileNotFoundError:
            dots += "."

            if len(dots) >= 3:
                f = open("./settings.json", "w")
                f.write("{}")
                f.close()
                return str(Path(f"./settings.json").absolute())

            continue

        file.close()
        return str(Path(f"{dots}/settings.json").absolute())  # converting these dot paths into absolute values.


def findDirectory(name):
    import os
    dots = "."
    while True:
        print(f"trying {dots}/{name}")
        if os.path.isdir(f"{dots}/{name}"):
            return str(Path(f"{dots}/{name}").absolute())  # converting these dot paths into absolute values.
        dots += "."

        if len(dots) >= 3:  # this is to prevent actually finding a real example of this dir
            return None


class Config:
    template = {}

    def read(self):
        pass

    def write(self):
        pass


class Settings(Config):
    """
    Settings object
    """
    template = {
        "ASSET_DIR": str(),  # The path to the assets folder
        "DEBUG": bool()  # whether debug mode enabled.
    }

    def __init__(self):
        self.path = findSettingsFile()
        # bs values, used for type checking
        # ex: self.TOKEN = str() or None
        self.ASSET_DIR = str() or None
        self.DEBUG = bool() or None
        self.LEVEL = int()

        # following set in the main function based on values pulled.
        self.POPPINS = str()
        self.COMFORT = str()
        self.read()

        # notTODO: technically always wastes one write call on execution, possible fix? (if even worth)
        # ^ not worth.

        # set debug
        if self.DEBUG is None:
            self.DEBUG = False

        # find asset dir
        if self.ASSET_DIR is None:
            self.ASSET_DIR = findDirectory("assets")
            if self.ASSET_DIR is None:
                raise NotADirectoryError("Unable to find assets directory! (report this on the github!)")

        if not self.ASSET_DIR.endswith("\\"):
            self.ASSET_DIR += "\\"

        self.write()

    def read(self):
        # read data
        with open(self.path, "r") as sf:
            data: dict = json.loads(sf.read())

            # by using the get thing, we allow it to default incase values do not exist.
            self.ASSET_DIR = data.get("ASSET_DIR", self.ASSET_DIR)
            self.DEBUG = data.get("DEBUG", self.DEBUG)

    def write(self):
        # write data
        with open(self.path, "w") as sf:
            data = json.dumps({
                "ASSET_DIR": self.ASSET_DIR,
                "DEBUG": self.DEBUG
            })

            sf.write(data)
