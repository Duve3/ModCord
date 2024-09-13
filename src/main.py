import argparse
import websocket as ws
import threading

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('-t', '--token', dest="TOKEN", required=True, help='User token (login added later!)')
arg_parser.add_argument("-v", "--version", default="9", dest="VER", help="API Version (defaults to 9)")


def start_websocket(token, ver):
    f = ws.Websocket(token, ver)
    threading.Thread(target=f.connect, daemon=True).start()


if __name__ == "__main__":
    args = arg_parser.parse_args()

    start_websocket(args.TOKEN, args.VER)

    while True:
        pass
        # TODO: implement the actual CLI (probably requires ANOTHER event system... sigh)
