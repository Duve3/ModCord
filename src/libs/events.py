"""
Events system for events to travel throughout the application
While a layer design is ideal here, for speed/simplicity purposes we skip this and just give everyone all events.
(^ this means that events cannot be "eaten" or destroyed, all layers access everything.)

This file works by essentially making EventList into a singleton that is declared using the init call.
"""

GLOBAL_EventList = None


class Event:
    def __init__(self, eventType: int):
        self.__dict__ = {}  # reset everything yk
        self.type = eventType


# TODO: (random idea) make all even events for the renderer, and all odd for the other?
# example:
#   type_1 <- render related event
#   type_2 <- non visual related event
#   type_3 <- saved for other threads event (these are there when the non visual makes a new thread and needs to communicate with it)
#   type_4 <- saved for other threads event
#   type_5 <- saved for other threads event
#   now the system repeats (you can probably use a modulus call like `if event.type % 5 == 1: print("its render!")`
#   type_6 <- back to render related event (different code but render still care about)

class EventList:
    def __init__(self):
        if GLOBAL_EventList is not None:
            raise ValueError("Only one EventList is allowed! (init declaration!)")
        self.__events__ = []

    @property
    def events(self):
        return self.__events__

    @events.setter
    def events(self, x: Event):
        self.__events__.append(x)


def init():
    global GLOBAL_EventList
    GLOBAL_EventList = EventList()


def getEvents():
    return GLOBAL_EventList.events  # noqa ; we shall believe


def removeEvent(x: Event):
    global GLOBAL_EventList
    GLOBAL_EventList.__events__.remove(x)  # noqa ; we shall believe


def pushEvent(x: Event):
    GLOBAL_EventList.events = x


# event definitions
# 2 -> token event, informs the backend of our current token

class RequestToken(Event):
    """
    Requesting the token from the backend,
    """
    def __init__(self):
        super().__init__(7)  # backend event!


class LoginEvent(Event):
    def __init__(self, user, passw):
        super().__init__(12)
        self.user = user
        self.passw = passw


class TokenDataEvent(Event):
    """
    This event is sent whenever we need to transfer token data to either side
    """
    def __init__(self, t: int, token: str):
        if t not in [1, 2, 3, 4, 5]:
            raise ValueError("Must be 1 - 5 event!")
        super().__init__(t)  # could result in any thread event!
        self.token = token


class TransitionMenuEvent(Event):
    """
    Transition to another menu, a menu will ignore this and instead kill itself and save it for the primary renderer.
    """
    def __init__(self, MenuNum: int):
        super().__init__(6)  # renderer event!
        self.goto = MenuNum
