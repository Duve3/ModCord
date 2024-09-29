from pathlib import Path
import json
import copy


def find_settings():  # notTODO: change this to write it in this file, or be a one time thing (maybe?)
    dots = "."
    while True:
        try:
            print(f"trying {dots}/settings.json")
            file = open(f"{dots}/settings.json")

            if len(dots) > 5:
                return None
        except FileNotFoundError:
            dots += "."
            continue

        file.close()
        return str(Path(f"{dots}/settings.json").absolute())  # converting these dot paths into absolute values.


class Settings:
    """
    A wrapper around the settings.json object
    """
    TEMPLATE = {
        "last_session_id": str | None,
        "token_hash": str | None,
        "seq": int | None
    }

    def __init__(self):
        self.path = find_settings()

        if self.path is None:
            with open("./settings.json", "w") as sf:
                sf.write(json.dumps(self.TEMPLATE))
                self.path = find_settings()  # re-call because im lazy

        # data values
        self.last_session_id = str | None
        self.token_hash = str | None
        self.seq = int | None

        self.read()

    def read(self):
        with open(self.path, 'r') as sf:
            d = sf.read()

            nd = json.loads(d)

            self.last_session_id = nd.get("last_session_id", None)
            self.token_hash = nd.get("token_hash", None)
            self.seq = nd.get("seq", None)

    def write(self):
        with open(self.path, 'w') as sf:
            d = copy.deepcopy(self.TEMPLATE)

            d["last_session_id"] = self.last_session_id
            d["token_hash"] = self.token_hash
            d["seq"] = self.seq

            nd = json.dumps(d)

            sf.write(nd)

