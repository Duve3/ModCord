"""
Essentially reverse engineering the discord API <- done check insomnia
"""
from unittest import case

from websockets.sync.client import connect
import json
import time
import threading
import random
import Heartbeat_events as ev


def Heartbeat_loop(interval, ws):
    iden = 1
    end_time = 0
    while True:
        for event in ev.pull_events(True):
            if event.TYPE == ev.HeartbeatUpdate:
                iden = event.d

                ev.remove_event(event)

            elif event.TYPE == ev.HeartbeatForced:
                end_time = time.time() - 1  # this would IMMEDIATELY make end_time < time.time()

                ev.remove_event(event)

        if end_time <= time.time():
            ws.send(json.dumps({
                "op": 1,
                "d": iden
            }
            ))

            end_time = time.time() + (
                        interval * random.random()) // 1000  # after checking docs, this SHOULD be safe rounding


def Identify_builder(token, os="windows", large_thres=250) -> str:
    """
    Builds the IDENTIFY (2) OPCODE
    :return:
    """
    iden = {
        "op": 2,
        "d": {
            "token": token,
            "properties": {
                "os": os,
                "browser": "disco",
                "device": "disco"
            },
            "large_threshold": large_thres
        },
        "s": None,
        "t": None
    }

    return json.dumps(iden)


class Websocket:
    def __init__(self, token, ver):
        self.token = token
        self.ver = ver

    def connect(self):
        with connect(f"wss://gateway.discord.gg/?ver={self.ver}?encoding=json") as websocket:
            print("Connected!")
            data = json.loads(websocket.recv())
            print(f"data recv:\n{data}")
            if data["op"] != 10:
                print("Something went wrong!")
                return

            hbi = data["d"]["heartbeat_interval"]

            threading.Thread(target=Heartbeat_loop, args=(hbi, websocket), daemon=True).start()

            websocket.send(Identify_builder(self.token))

            while True:
                data = json.loads(websocket.recv())
                print(data)

                match data["op"]:
                    # https://discord.com/developers/docs/topics/opcodes-and-status-codes#gateway-gateway-opcodes
                    case 1:  # Heartbeat
                        # this means discord is wanting a heartbeat right now :rage:
                        ev.dispatch_event(ev.HeartbeatForced())

                    case 0 | 2 | 3 | 4 | 5 | 6 | 8:  # 5 currently is non-existent in documentation, assumed missing
                        # these are ALL sending events, and should never be sent our direction!
                        pass

                    case 7:  # Reconnect
                        # TODO: what do we do here
                        pass

                    case 9:  # Invalid session
                        # TODO: uhh what to do when
                        pass

                    case 10:  # we can ignore this due to how we get hello up top!
                        pass

                    case 11:  # most likely not necessary to read?
                        pass
