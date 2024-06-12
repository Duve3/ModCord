from libs import events as ev
from libs import ui
from libs import config
from libs.logger import LoggingBase
import pygame


class MsgsMenu(LoggingBase):
    def __init__(self, screen: ui.CScaleScreen, settings: config.Settings):
        super().__init__(settings.LEVEL)
        self.screen = screen

    def run(self):
        while True:
            self.screen.clock.tick(60)

            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    return

            gEvents = ev.getEvents()
            for ge in gEvents:
                if ge.type % 5 != 1:
                    continue

                ev.removeEvent(ge)
