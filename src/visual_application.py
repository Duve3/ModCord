from libs import events as ev
from libs import config
from libs import ui
from libs.logger import LoggingBase
import pygame
from zMENU_login import LoginMenu
from zMENU_msgs import MsgsMenu


class Application(LoggingBase):
    def __init__(self, settings: config.Settings):
        super().__init__(settings.LEVEL)
        pygame.init()
        self.settings = settings

        self.screen = ui.CScaleScreen(size=(1080, 720), caption="ModCord (Made by Duve3)", scrap=True, clock=True)
        # ^ clock is used for ensuring videos, and gifs don't go too fast or too slow.

        self.menus = [
            LoginMenu(self.screen, settings),
            MsgsMenu(self.screen, settings)
        ]

        self.prepareSwitch: int = -1

    def run(self):
        """
        This run loop has zero visual code, it simply just handles events
        :return:
        """
        while True:
            gevents = ev.getEvents()
            for ge in gevents:
                if ge.type % 5 != 1:
                    # this event is not meant for the render!
                    continue

                if ge.type == 1:
                    pass  # we don't really care :shrug: <- but we also want to eat up the event!

                elif ge.type == 6:
                    ge: ev.TransitionMenuEvent
                    self.prepareSwitch = ge.goto

                ev.removeEvent(ge)

            if self.prepareSwitch != -1:
                runFunc = self.menus[self.prepareSwitch].run
                self.prepareSwitch = -1

                runFunc()
