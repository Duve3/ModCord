from visual_application import Application
from libs import events as ev
from libs.logger import setupLogging, logging
import threading
import time
from libs.config import Settings


def main():
    ev.init()

    settings = Settings()  # WARN: DO NOT MODIFY WHEN WE SEPARATE THREADS TO AVOID DATA RACES!
    # ^ we can modify as main-thread (if this doesn't work create an event to inform)

    settings.POPPINS = settings.ASSET_DIR + "POPPINS.ttf"
    settings.COMFORT = settings.ASSET_DIR + "COMFORT.ttf"

    settings.LEVEL = logging.DEBUG

    app = Application(settings)

    nVthread = threading.Thread(target=nonVisualCode, args=(settings,), daemon=True)

    nVthread.start()

    app.run()


def nonVisualCode(settings: Settings):
    """
    This function runs EVERYTHING other than visuals and rendering (it does send events between to talk to each-other!)
    :return:
    """
    token = ""
    ev.pushEvent(ev.TransitionMenuEvent(0))  # GOTO LOGIN
    while True:
        gEvents = ev.getEvents()

        for ge in gEvents:
            if ge.type % 5 != 2:
                # not our type of event
                continue

            if ge.type == 2:
                ge: ev.TokenDataEvent
                token = ge.token

            elif ge.type == 7:
                ge: ev.RequestToken
                ev.pushEvent(ev.TokenDataEvent(1, token))

            ev.removeEvent(ge)

        time.sleep(0.1)  # to prevent overloading!


if __name__ == '__main__':
    main()
