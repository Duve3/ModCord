"""
Essentially reverse engineering the discord API <- done check insomnia
"""
from websockets.sync.client import connect
import json
import time
import threading
import random
import Heartbeat_events as ev
from settings import Settings
import hashlib


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


def Resume_builder(token, session_id, seq) -> str:
    """
    Builds the RESUME (6) OPCODE
    :return:
    """
    resume = {
        "op": 6,
        "d": {
            "token": token,
            "session_id": session_id,
            "seq": seq
        }
    }

    return json.dumps(resume)


def debug_print(ver, data):
    print("DEBUG INFORMATION (GIVE THIS WITH YOUR ERROR REPORT!):\n")
    print(f"PAYLOAD_DATA =\n{data}")
    print("---------END---------")
    print(f"API_VERSION =\n{ver}")


def default_message_create(data: dict):
    pass


def message_create_handler(data: dict):
    # https://discord.com/developers/docs/resources/message#message-object-message-types
    # MESSAGE CREATE TYPES TO IMPLEMENT (priority order): 0, 19, 1, 2, 3, 4, 5, 6, 7, 20, 21, 18, rest just whenever

    match data["d"]["type"]:
        case 0:
            default_message_create(data)


class Websocket:
    def __init__(self, token, ver, settings):
        self.settings: Settings = settings
        self.token = token
        self.ver = ver

    def connect(self):
        with connect(f"wss://gateway.discord.gg/?ver={self.ver}?encoding=json") as websocket:
            print("Connected!")
            data = json.loads(websocket.recv())
            print(f"data recv:\n{data}")
            if data["op"] != 10:
                TypeError("Something went very wrong!")
                return

            hbi = data["d"]["heartbeat_interval"]

            threading.Thread(target=Heartbeat_loop, args=(hbi, websocket), daemon=True).start()

            attempt_resume = False
            if self.settings.last_session_id is not None and self.settings.token_hash == hashlib.sha256(
                    bytes(self.token, "utf-8")).hexdigest() and self.settings.seq is not None:
                attempt_resume = True

            if attempt_resume:
                print("we are attempting to resume!")
                websocket.send(Resume_builder(self.token, self.settings.last_session_id, self.settings.seq))

            else:
                websocket.send(Identify_builder(self.token))
                self.settings.token_hash = hashlib.sha256(
                                    bytes(self.token, "utf-8")).hexdigest()
                self.settings.write()

            while True:
                data = json.loads(websocket.recv())
                print(data)

                match data["op"]:
                    # https://discord.com/developers/docs/topics/opcodes-and-status-codes#gateway-gateway-opcodes
                    case 0:
                        # https://discord.com/developers/docs/topics/gateway-events#receive-events
                        ev.dispatch_event(ev.HeartbeatUpdate(d=data["s"]))  # update our heartbeat!
                        self.settings.seq = data["s"]
                        self.settings.write()  # WARN: this might be very inefficient...

                        match data["t"]:
                            case "MESSAGE_CREATE":
                                message_create_handler(data)

                            case "READY":
                                self.settings.last_session_id = data["d"]["session_id"]
                                self.settings.write()

                            case "RESUMED":
                                print("We have successfully resumed session!")

                            case "TYPING_START":
                                type_data = data["d"]





                    case 1:  # Heartbeat
                        # this means discord is wanting a heartbeat right now :rage:
                        ev.dispatch_event(ev.HeartbeatForced())

                    case 2 | 3 | 4 | 6 | 8:  # 5 currently is non-existent in documentation, assumed missing
                        # these are ALL sending events, and should never be sent our direction!
                        pass

                    case 7:  # Reconnect
                        # TODO: what do we do here
                        pass

                    case 9:  # Invalid session
                        # TODO: uhh what to do when
                        pass

                    case 10:  # Hello - we can ignore this due to how we get hello up top!
                        pass

                    case 11:  # Heartbeat Ack - most likely not necessary to read?
                        pass

                    case _:
                        debug_print(self.ver, data)
                        raise TypeError(
                            "*****REPORT THIS ON GITHUB!*****\nSomething went really wrong! We received a payload with an unknown OPCODE!\nDebug information is printed either below this or above this stacktrace!")
