import argparse
import websocket as ws
import threading
from settings import Settings

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('-t', '--token', dest="TOKEN", required=True, help='User token (login added later!)')
arg_parser.add_argument("-v", "--version", default="9", dest="VER", help="API Version (defaults to 9)")


def start_websocket(token, ver, settings):
    f = ws.Websocket(token, ver, settings)
    threading.Thread(target=f.connect, daemon=True).start()


if __name__ == "__main__":
    args = arg_parser.parse_args()

    if int(args.VER) < 8:
        # WARN: PRINT
        print("WARNING: This program will run into issues when using API versions BELOW 8")

    settings = Settings()

    start_websocket(args.TOKEN, args.VER, settings)

    while True:
        pass
        # TODO: implement the actual CLI (probably requires ANOTHER event system... sigh)
