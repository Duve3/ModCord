"""
The menu for logging into discord
"""
from libs import ui
from libs import config
from libs import events as ev
from libs.logger import LoggingBase
import pygame
from API import login, LOGIN


class LoginMenu(LoggingBase):
    def __init__(self, screen: ui.CScaleScreen, settings: config.Settings):
        super().__init__()
        self.screen = screen

        self.LABEL_title = ui.CUILabel(340, 200, ui.CUIFont(settings.COMFORT, 30, ui.CUColor.WHITE()),
                                       "Login to Discord (NO 2FA)")

        basic_font = ui.CUIFont(settings.COMFORT, 20, ui.CUColor.WHITE())
        self.TEXTBOX_email = ui.CUITextInput(440, 350, 200, 75, ui.CUColor((88, 101, 242)).darken(20, retColor=True),
                                             basic_font, "Email", onTextUpdate=lambda x: x, charLimit=100)
        self.TEXTBOX_pass = ui.CUITextInput(440, 450, 200, 75, ui.CUColor((88, 101, 242)).darken(20, retColor=True),
                                            basic_font, "Password", onTextUpdate=lambda x: x, charLimit=100)

        self.BUTTON_login = ui.CUITextButton(500, 550, 75, 25, ui.CUColor((88, 101, 242)).darken(20, retColor=True),
                                             basic_font, "Login", onPress=self.login)

        self.manager = ui.CUIManager([self.TEXTBOX_email, self.TEXTBOX_pass, self.BUTTON_login])

    def login(self):
        t: LOGIN | str = login(self.TEXTBOX_email.text, self.TEXTBOX_pass.text)

        if t != LOGIN.INVALID:
            ev.pushEvent(ev.TokenDataEvent(1, t))  # inform our own program
            ev.pushEvent(ev.TokenDataEvent(2, t))  # inform backend

            ev.pushEvent(ev.TransitionMenuEvent(1))
            return
        else:
            pass  # TODO: what happens when it fails!!1111 (push event upon ourself?)

    def run(self):
        while True:
            self.screen.clock.tick(60)

            events = pygame.event.get()
            self.manager.tick(events)

            for event in events:
                if event.type == pygame.QUIT:
                    return

            gevents = ev.getEvents()
            for ge in gevents:
                if ge.type % 5 != 1:  # WE ARE STILL CONNECTED TO RENDERING!
                    continue

                if ge.type == 1:
                    continue  # WE WANT FUTURE RENDERS TO DEAL WITH THIS, NOT US!

                if ge.type == 6:
                    return  # not only do we force a higher renderer to deal with it, we also allow it to handle it properly.

                ev.removeEvent(ge)

            self.screen.fill(ui.CUColor((88, 101, 242)))  # bg color

            self.LABEL_title.draw(self.screen.prescaledSurface)

            self.TEXTBOX_email.draw(self.screen.prescaledSurface)
            self.TEXTBOX_pass.draw(self.screen.prescaledSurface)

            self.BUTTON_login.draw(self.screen.prescaledSurface)

            self.screen.before_flip()
            pygame.display.flip()
