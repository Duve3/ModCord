"""
Heartbeat event system
Websocket -> Heartbeat
All evens are for websocket side, all odds are for heartbeat side
"""


class Event:
    TYPE: int


GLOBAL_events: list[Event] = []


class HeartbeatUpdate(Event):
    """
    Used to update the current sequence `s` value (d)
    """
    TYPE = 1

    def __init__(self, d):
        """
        d is the last s value
        :param d:
        """
        self.d = d


class HeartbeatForced(Event):
    """
    Used when the discord API forces us to send a heartbeat, rare, but possible!
    """
    TYPE = 3


def pull_events(evens: bool) -> list[Event]:
    if evens:
        return [e for e in GLOBAL_events if e.TYPE % 2 == 0]

    return [e for e in GLOBAL_events if e.TYPE % 2 == 1]


def dispatch_event(x: Event):
    GLOBAL_events.append(x)


def remove_event(x: Event):
    GLOBAL_events.remove(x)
