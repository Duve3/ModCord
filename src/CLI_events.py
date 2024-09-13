"""
CLI Event system
CLI -> Websocket
All evens are for CLI side, all odds are for websocket side
"""


class Event:
    TYPE: int


GLOBAL_events: list[Event] = []


def pull_events(evens: bool) -> list[Event]:
    if evens:
        return [e for e in GLOBAL_events if e.TYPE % 2 == 0]

    return [e for e in GLOBAL_events if e.TYPE % 2 == 1]


def dispatch_event(x: Event):
    GLOBAL_events.append(x)


def remove_event(x: Event):
    GLOBAL_events.remove(x)
