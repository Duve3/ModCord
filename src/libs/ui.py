"""
ui.py
Contains UI objects and essentially the entire UI system.
(This file is used in multiple projects, this is NOT stolen code, these projects are owned/operated by me)
ModCord Version (based upon ArjunLauncher Version)
"""
import pathlib
import math
import pygame.freetype
from typing import Sequence, Callable, Tuple, Union, Optional

RGBAOutput = Tuple[int, int, int, int]
ColorValue = Union[pygame.Color, int, Tuple[int, int, int], RGBAOutput, Sequence[int]]  # no strings allowed
Coordinate = Union[Tuple[float, float], Sequence[float]]
STYLE_DEFAULT = pygame.freetype.STYLE_DEFAULT


class CUColor(pygame.Color):
    """
    A superior version of the pygame built in color.
    (This function will always use the fourth value of a tuple over the alpha value)
    :param color: The color tuple you want to set (if it includes alpha then that will be used instead of the param).
    :param alpha: The alpha value of the color (optional defaults to 255).
    :return:
    """

    def __init__(self, color: ColorValue, alpha: int = 255) -> None:
        if isinstance(color, pygame.Color):
            super().__init__(color.r, color.g, color.b, color.a)
        elif isinstance(color, tuple) or isinstance(color, list):
            super().__init__(color[0], color[1], color[2], color[3]) if len(color) == 4 else super().__init__(*color,
                                                                                                              alpha)
        else:
            raise TypeError("Unable to bind current value to a valid color type! (just try using a tuple or a list)")

        self.color = (*color, alpha)  # a tuple which will look like this: (r, g, b, a)

    def darken(self, offset: int, retColor: bool = False) -> ColorValue:
        """
        Returns darkened version of the color (based on offset).
        :param int offset: The integer value of how much to darken the color.
        :param bool retColor: The option to return a CUColor instead of a tuple.
        :return ColorValue: Either a tuple or a CUColor of the new color.
        """
        darkColor = []
        for color in self.color[:3]:
            put = color - offset
            if put < 0:
                put = 0

            darkColor.append(put)

        darkColor.append(self.color[3])
        darkColor = tuple(darkColor)

        return darkColor if not retColor else CUColor(darkColor)

    def lighten(self, offset: int, retColor: bool = False) -> ColorValue:
        """
        Returns lightened version of the color (based on offset).
        :param int offset: The integer value of how much to darken the color.
        :param bool retColor: The option to return a CUColor instead of a tuple.
        :return ColorValue: Either a tuple or a CUColor of the new color.
        """
        lightColor = [c + offset for c in self.color]
        lightColor[3] = self.color[3]
        lightColor = tuple(lightColor)

        return lightColor if not retColor else CUColor(lightColor)

    # some constants to help out with easy colors
    @staticmethod
    def WHITE():
        return CUColor((255, 255, 255), 255)

    @staticmethod
    def BLACK():
        return CUColor((0, 0, 0), 255)

    @staticmethod
    def RED():
        return CUColor((255, 0, 0), 255)

    @staticmethod
    def BLUE():
        return CUColor((0, 0, 255), 255)

    @staticmethod
    def GREEN():
        return CUColor((0, 255, 0), 255)

    @staticmethod
    def YELLOW():
        return CUColor((255, 230, 0), 255)

    @staticmethod
    def ORANGE():
        return CUColor((255, 110, 0), 255)

    @staticmethod
    def PURPLE():
        return CUColor((205, 0, 255), 255)

    @staticmethod
    def CYAN():
        return CUColor((55, 240, 240), 255)

    @staticmethod
    def GREY():
        return CUColor((165, 165, 165), 255)

    @staticmethod
    def GRAY():
        return CUColor.GREY()


class CUIFont(pygame.freetype.Font):
    """
    A Font class that works better in most scenarios.
    :param str location: The file path of the font file.
    :param float fontSize: The size to render the font at.
    :param CUColor fgColor: The foreground color of the text.
    :param CUColor bgColor: The background color of the text (optional defaults to None).
    :param int font_index: The font index (same as pygame.freetype.font) (defaults to 0)
    :param int resolution: The resolution of the font (same as pygame.freetype.font) (defaults to 0)
    :param int ucs4: The ucs4 (same as pygame.freetype.font) (defaults to False)
    :param list[CUColor] ColorList: The list of colors to use when multiline rendering (very specific use case but can be more efficient/effective) (defaults to None)
    """

    def __init__(self, location: str, fontSize: Union[float, Tuple[float, float]],
                 fgColor: CUColor,
                 bgColor: CUColor = None,
                 font_index: int = 0, resolution: int = 0, ucs4: int = False, ColorList: list[
                CUColor] = None) -> None:

        newLoc = pathlib.Path(location)
        super().__init__(newLoc.absolute(), size=fontSize, font_index=font_index, resolution=resolution, ucs4=ucs4)
        self.fgcolor = fgColor
        if bgColor is not None:
            self.bgcolor = bgColor
        self.ColorList = ColorList

    def multiline_render_to(self, surf: pygame.Surface, dest, text: str, fgcolor: Optional[CUColor] = None,
                            bgcolor: Optional[CUColor] = None, style: int = STYLE_DEFAULT, rotation: int = 0,
                            size: float = 0) -> list[pygame.rect.Rect]:
        """
        Render to a surface using the multiline render.
        :param Surface surf: The pygame.Surface.
        :param Coordinate dest: The position/rect of where to place the text.
        :param str text: The text the font is rendering (use \n for next line).
        :param CUColor fgcolor: The foreground color of the text (optional defaults to the one defined on creation).
        :param CUColor bgcolor: The background color of the text (optional defaults to the one defined on creation).
        :param int style:
        :param int rotation:
        :param float size:
        :return: list[pygame.rect.Rect]
        """
        ListText = text.splitlines()
        ListRects = []
        useColorList = True if self.ColorList is not None else False
        for i, line in enumerate(ListText):
            if useColorList:
                self.fgcolor = self.ColorList[i % len(self.ColorList)]
            rect = self.render_to(surf=surf, dest=(dest[0], dest[1] + (i * self.size + 10)), text=line, fgcolor=fgcolor,
                                  bgcolor=bgcolor, style=style, rotation=rotation, size=size)
            ListRects.append(rect)

        return ListRects

    def multiline_render(self, text: str, fgcolor: Optional[CUColor] = None, bgcolor: Optional[CUColor] = None,
                         style: int = STYLE_DEFAULT, rotation: int = 0, size: float = 0) -> list[
                         Tuple[pygame.Surface, pygame.rect.Rect]]:
        """
        Render a surface containing multiple lines of text.
        :param str text: The text the font is rendering (use \n for next line).
        :param CUColor fgcolor: The foreground color of the text (optional defaults to the one defined on creation).
        :param CUColor bgcolor: The background color of the text (optional defaults to the one defined on creation).
        :param int style:
        :param int rotation:
        :param float size:
        :return: list[Tuple[Surface, pygame.rect.Rect]]
        """
        ListText = text.splitlines()
        ListSurfs = []
        for i, line in enumerate(ListText):
            surfRect = self.render(text=line, fgcolor=fgcolor, bgcolor=bgcolor, style=style, rotation=rotation,
                                   size=size)
            ListSurfs.append(surfRect)

        return ListSurfs

    def get_center(self, surf: pygame.Surface, text: str, style: int = STYLE_DEFAULT, rotation: int = 0,
                   size: float = 0,
                   x: bool = True, y: bool = False) -> pygame.rect.Rect:
        """

        :param surf:
        :param text:
        :param style:
        :param rotation:
        :param size:
        :param x:
        :param y:
        :return:
        """
        rect = self.get_rect(text=text, style=style, rotation=rotation, size=size)
        if x:
            rect.centerx = surf.get_rect().centerx

        if y:
            rect.centery = surf.get_rect().centery

        return rect


class BaseObject:
    """
    This class is just meant to be the base of all basic objects like lines and circles.
    """

    def draw(self, screen: pygame.Surface):
        pass


class CRect(pygame.FRect):
    """
    A custom rectangle that has more information stored inside it, allowing for easier use.
    :param float x: A float containing the X coordinate of the rect.
    :param float y: A float containing the Y coordinate of the rect.
    :param float width: A float containing the width of the rect.
    :param float height: A float containing the height of the rect.
    :param CUColor color: A Custom UI Color, used for storing color information.
    """

    def __init__(self, x: float, y: float, width: float, height: float, color: CUColor, draw_width: int = 0,
                 draw_border_radius: int = -1,
                 draw_border_top_left_radius: int = -1,
                 draw_border_top_right_radius: int = -1,
                 draw_border_bottom_left_radius: int = -1,
                 draw_border_bottom_right_radius: int = -1):
        super().__init__(x, y, width, height)
        self.color = color
        self.draw_width = draw_width
        self.draw_border_radius = draw_border_radius
        self.draw_border_top_left_radius = draw_border_top_left_radius
        self.draw_border_top_right_radius = draw_border_top_right_radius
        self.draw_border_bottom_left_radius = draw_border_bottom_left_radius
        self.draw_border_bottom_right_radius = draw_border_bottom_right_radius

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the rectangle on the provided surface.
        :param screen: A Surface to draw onto.
        """
        pygame.draw.rect(screen, self.color, self, self.draw_width, self.draw_border_radius,
                         self.draw_border_top_left_radius, self.draw_border_top_right_radius,
                         self.draw_border_bottom_left_radius, self.draw_border_bottom_right_radius)


class CLine(BaseObject):
    """
    A custom line which stores more information, allowing for easier use.
    :param Sequence[float] start: The starting position of the line.
    :param Sequence[float] end: The ending position of the line.
    :param CUColor color: The color of the line.
    :param int width: The width of the line.
    """

    def __init__(self, start: Sequence[float], end: Sequence[float], color: CUColor, width: int = 1):
        self.start = [start[0], start[1]]
        self.end = [end[0], end[1]]
        self.length = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
        self.color = color
        self.draw_width = width

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws a line on the provided surface.
        :param screen: A Surface to draw onto.
        """
        pygame.draw.line(screen, self.color, self.start, self.end, self.draw_width)  # noqa ; seq[float] != seq[float]??

    def set_pos(self, x: float, y: float):
        """
        Set the position of the line using only one point.
        WARN: This method just assumes that the point provided is the top and the bottom is below it.
        :param float x:
        :param float y:
        :return:
        """
        # TODO: fix this function to figure out the proper angle and stuff, because defaulting to down should be illegal
        self.start = [x, y]
        self.end = [x, y + self.length]


class CCircle(BaseObject):
    """
    A custom circle that has more information stored inside.
    :param Sequence[float] center: The center of the circle.
    :param float radius: The radius of the circle.
    :param CUColor color: The color of the circle.
    """

    def __init__(self, center: Sequence[float], radius: float, color: CUColor, draw_width: int = 0,
                 draw_top_right: bool = False, draw_top_left: bool = False, draw_bottom_left: bool = False,
                 draw_bottom_right: bool = False):
        self.center = [center[0], center[1]]
        self.radius = radius
        self.diameter = radius * 2
        self.color = color
        self.draw_width = draw_width
        self.draw_top_right = draw_top_right
        self.draw_top_left = draw_top_left
        self.draw_bottom_left = draw_bottom_left
        self.draw_bottom_right = draw_bottom_right

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, self.center, self.radius, self.draw_width, self.draw_top_right,  # noqa
                           self.draw_top_left, self.draw_bottom_left,
                           self.draw_bottom_right)
        # ^ above noqa is because it's saying the self.center is type Sequence[float] which is not Sequence[float]????


class CUIObject(CRect):
    """
    The base Custom UI object. Used for every Custom UI object.
    :param float x: A float containing the X coordinate of the rect.
    :param float y: A float containing the Y coordinate of the rect.
    :param float width: A float containing the width of the rect.
    :param float height: A float containing the height of the rect.
    :param CUColor color: A Custom UI Color, used for color information.
    """

    def __init__(self, x: float, y: float, width: float, height: float, color: CUColor, **kwargs):
        super().__init__(x, y, width, height, color, **kwargs)

        self.registeredEvents = []
        self.hasDrawn = False  # used for defining if has been drawn
        self.tag = ""  # id tag, set externally.

    def subscribe_event(self, event: pygame.Event):
        """
        Add to events to be listened by this Custom UI object.
        Do not touch this unless you know what you are doing, it could affect performance greatly!
        :param event: The pygame.Event to subscribe to.
        :return:
        """
        self.registeredEvents.append(event)

    def unsubscribe_event(self, event: pygame.Event):
        """
        Remove from events to be listened by this Custom UI object.
        Do not touch this unless you are using know what you are doing, it could break the UI object!
        :param event: The pygame.Event to unsubscribe to.
        :return:
        """
        if event in self.registeredEvents:
            self.registeredEvents.remove(event)

    def tick(self, event: pygame.Event, mouse_pos: tuple[int, int]):
        self.hasDrawn = False

    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        self.hasDrawn = True


class CUIButton(CUIObject):
    """
    A Custom UI Object that functions just like a button. Currently, not very customizable.
    :param float x: A float containing the X coordinate of the rect.
    :param float y: A float containing the Y coordinate of the rect.
    :param float width: A float containing the width of the rect.
    :param float height: A float containing the height of the rect.
    :param CUColor defaultColor: A Custom UI Color for the default color.
    :param CUColor pressedColor: A Custom UI Color for the on pressed color.
    :param CUColor highlightColor: A Custom UI Color for the on hover color.
    :param Callable onPress: A function to call
    :param **kwargs: Everything else that should be passed to the CUIObject constructor.
    """

    def __init__(self, x: float, y: float, width: float, height: float, defaultColor: CUColor,
                 pressedColor: CUColor = None, highlightColor: CUColor = None, onPress: Callable = None,
                 **kwargs):
        super().__init__(x, y, width, height, defaultColor, **kwargs)
        self._defaultColor = defaultColor
        if pressedColor is None:
            pressedColor = defaultColor.darken(20, retColor=True)
        self.pressedColor = pressedColor
        if highlightColor is None:
            highlightColor = defaultColor.darken(40, retColor=True)
        self.highlightColor = highlightColor

        self.registeredEvents = [pygame.MOUSEMOTION,
                                 pygame.MOUSEBUTTONDOWN]  # this is used by the manager, not by the actual tick method.

        self.isPressed = False
        self.isHovered = False
        if onPress:
            self.func = onPress

    @property
    def defaultColor(self):
        return self._defaultColor

    @defaultColor.setter
    def defaultColor(self, x):
        self._defaultColor = x
        self.pressedColor = x.darken(20, retColor=True)
        self.highlightColor = x.darken(40, retColor=True)

    def tick(self, event: pygame.Event, mouse_pos: tuple[int, int]):
        """
        Ticks the button to listen to an event to update the button.
        Try avoiding sending every event to this method.
        :param event: The pygame event.
        :param mouse_pos: Mouse position currently.
        :return:
        """
        if event.type == pygame.MOUSEMOTION:
            if self.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.color = self.highlightColor
                self.isHovered = True
            else:
                self.color = self.defaultColor
                self.isHovered = False

            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.color = self.pressedColor
                self.isPressed = True
                if getattr(self, 'func', False):
                    self.func()
            else:
                self.color = self.defaultColor
                self.isPressed = False

            return

        super().tick(event, mouse_pos)


class CUITextButton(CUIButton):
    """
    Same as the CUIButton but with an added text feature.
    :param float x: A float containing the X coordinate of the rect.
    :param float y: A float containing the Y coordinate of the rect.
    :param float width: A float containing the width of the rect.
    :param float height: A float containing the height of the rect.
    :param CustomColor defaultColor: A custom color from the pygame_wrapper library.
    :param Font font: A pygame_wrapper library font object.
    :param String text: The text to display on the screen.
    :param Sequence[float] indentation: A sequence of floats containing the indentation vectors for the text.
    :param CustomColor pressedColor: A custom color from the pygame_wrapper library.
    :param CustomColor highlightColor: A custom color from the pygame_wrapper library.
    :param Callable onPress: A function to call
    :param **kwargs: Everything else that should be passed to the CUIObject constructor.
    """

    def __init__(self, x: float, y: float, width: float, height: float, defaultColor: CUColor, font: CUIFont,
                 text: str, pressedColor: CUColor = None,
                 highlightColor: CUColor = None, onPress: Callable = None, **kwargs):
        super().__init__(x, y, width, height, defaultColor, pressedColor, highlightColor, onPress, **kwargs)
        self.font = font
        self._text = text
        self.text_pos = (self.centerx - self.font.get_rect(text, size=self.font.size).width // 2,
                         self.centery - self.font.get_rect(text, size=self.font.size).height // 2)

        if len(text.split("\n")) > 1:
            self.multiline = True
        else:
            self.multiline = False

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.text_pos = (self.centerx - self.font.get_rect(self._text, size=self.font.size).width // 2,
                         self.centery - self.font.get_rect(self._text, size=self.font.size).height // 2)

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        if self.multiline:
            self.font.multiline_render_to(screen, self.text_pos, self.text)
        else:
            self.font.render_to(screen, self.text_pos, self.text)


class CUILabel(CUIObject):
    """
    A Text label to put text on to the screen.
    :param float x: The x coordinate of the label.
    :param float y: The y coordinate of the label.
    :param Font font: The pygame_wrapper Font to use when displaying the label.
    :param String text: The text to put on the screen.
    """

    def __init__(self, x: float, y: float, font: CUIFont, text: str):
        super().__init__(x, y, 1, 1, CUColor((0, 0, 0)))  # bs props since this isn't needed.
        self.font = font
        self.text = text
        self.registeredEvents = []  # prevent wasting time due to accidental addiction to manager

        if len(self.text.split("\n")) > 1:
            self.multiline = True
        else:
            self.multiline = False

    def draw(self, screen: pygame.Surface) -> None:
        if self.multiline:
            self.font.multiline_render_to(screen, (self.x, self.y), self.text)
        else:
            self.font.render_to(screen, (self.x, self.y), self.text)


class CUITextInput(CUIButton):
    """
    Just a button that records the key presses.
    :param float x: The x position of the object.
    :param float y: The y position of the object.
    :param float width: The width of the object.
    :param float height: The height of the object.
    :param CUColor defaultColor: The Custom UI Color for the object.
    :param Font font: The Font for the object.
    :param str placeholder_text: The string for the placeholder text.
    :param CUColor pressedColor: Optional pressed color, defaults to defaultColor.darken(20)
    :param CUColor highlightColor: Optional highlighted color, defaults to defaultColor.darken(40)
    :param int charLimit: The maximum number of characters that can be inputted into the textbox.
    :param list allowedKeys: The keys that are allowed to be typed - defaults to all.
    :param Callable onTextUpdate: The function to call upon the text being updated.
    """

    def __init__(self, x: float, y: float, width: float, height: float, defaultColor: CUColor, font: CUIFont,
                 placeholder_text: str, pressedColor: CUColor = None, highlightColor: CUColor = None,
                 charLimit: int = 20, allowedKeys: list = None, onTextUpdate: Callable = None, shrink: bool = False):
        super().__init__(x, y, width, height, defaultColor, pressedColor=pressedColor, highlightColor=highlightColor,
                         draw_width=5, draw_border_radius=5)

        self.font = font
        self.placeholder_text = placeholder_text
        self.placeholder_font = self.font
        self.placeholder_font.fgcolor = CUColor(self.placeholder_font.fgcolor).darken(20)
        self.text = ""
        self.history = [""]
        self.registeredEvents = [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION, pygame.KEYDOWN, pygame.KEYUP]
        self.ctrlPressed = False
        self.character_limit = charLimit
        self.allowed_keys = allowedKeys
        self.textUpdateFunc = onTextUpdate  # WARN: DO NOT NAME self.func BREAKS BC OF SUPER BUTTON
        self.shrink = shrink

    def tick(self, event: pygame.Event, mouse_pos: tuple[int, int]):
        if event.type == pygame.KEYDOWN and self.isPressed:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.isPressed = False
                self.isHovered = False
            elif event.key == pygame.K_LCTRL:
                self.ctrlPressed = True

            elif event.key == pygame.K_v and self.ctrlPressed:
                if pygame.scrap.has_text():
                    self.text += pygame.scrap.get_text()
            elif event.key == pygame.K_z and self.ctrlPressed:
                self.text = self.history[-1]
                if len(self.history) > 1:
                    del self.history[-1]

            elif len(self.text) < self.character_limit:
                if self.allowed_keys:
                    if event.unicode not in self.allowed_keys:
                        return

                self.text += event.unicode
                self.history.append(self.text)

                self.textUpdateFunc(self.text)

                if self.font.get_rect(self.text).width >= self.width:
                    if self.font.size > 1:
                        self.font.size -= 1

            return

        if event.type == pygame.KEYUP and self.isPressed:
            if event.key == pygame.K_LCTRL and self.ctrlPressed:
                self.ctrlPressed = False

            return

        super().tick(event, mouse_pos)

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        self.text = str(self.text)  # str needed :shrug: "well-designed language"
        if len(self.text) <= 0 and not self.isPressed:
            t = self.placeholder_text
            self.placeholder_font.render_to(screen, (
                self.centerx - self.font.get_rect(t, size=self.font.size).width // 2,
                self.centery - self.font.get_rect(t, size=self.font.size).height // 2), t)
        else:
            t = self.text
            self.font.render_to(screen, (self.centerx - self.font.get_rect(t, size=self.font.size).width // 2,
                                         self.centery - self.font.get_rect(t, size=self.font.size).height // 2), t)


class CUIManager:
    """
    Simple UI manager for objects.
    :param list[CUIObject] objects: List of UI (CUIObject based) objects.
    :param bool onSurface: Whether the object is on a surface.
    :param tuple[float, float] pos: The position of the surface (offset)
    """

    def __init__(self, objects: list[CUIObject], onSurface: bool = False, pos: tuple[float, float] = None):
        self.ui_objects = objects
        self.offset = None

        if onSurface:
            if pos is None:
                raise TypeError("Missing pos value for onSurface type! (required value!)")
            self.offset = pos

    def add_object(self, obj: CUIObject) -> None:
        """
        Adds UI objects.
        :param obj: Any UI object.
        :return: None
        """
        if obj not in self.ui_objects:
            self.ui_objects.append(obj)

    def update_object(self, obj: CUIObject) -> None:
        """
        Updates UI objects.
        :param obj: Any UI object.
        :return: None
        """
        if obj in self.ui_objects:
            i = self.ui_objects.index(obj)
            self.ui_objects[i] = obj

    def remove_object(self, obj: CUIObject) -> None:
        """
        Remove an object from the current UI objects.
        :param obj: Any UI object.
        :return:
        """
        if obj in self.ui_objects:
            self.ui_objects.remove(obj)

    def tick(self, events: list[pygame.Event]):
        mp = pygame.mouse.get_pos()
        mp = [mp[0], mp[1]]
        if self.offset:  # ensures offset is used
            mp[0] -= self.offset[0]
            mp[1] -= self.offset[1]

        for obj in [obj for obj in self.ui_objects if obj.hasDrawn]:  # redefined to only tick visible objects.
            ne = [event for event in events if
                  event.type in obj.registeredEvents]  # only keeps events that are important.
            if len(ne) == 0:
                continue

            for e in ne:
                obj.tick(e, mp)  # noqa ; tuple[int, int] basically list[int]


class CGClock:
    """
    Initializes a Custom Game Clock, with FPS preloaded.
    Due to pygame not allowing subclassing of pygame.time.Clock(), some methods may be missing.
    :param int fps: The fps value
    """

    def __init__(self, fps: int):
        self._clock = pygame.time.Clock()
        self.fps = fps

    def tick(self, framerate: int = None):
        """
        Ticks the clock to ensure the FPS.
        Provide a custom framerate param here if needed.
        :param int framerate: The custom framerate value.
        :return int: The milliseconds since last tick.
        """
        if framerate is None:
            return self._clock.tick(self.fps)
        else:
            return self._clock.tick(framerate)

    def tick_busy_loop(self, framerate: int = None):
        """
        Ticks the clock in a busy loop.
        Provide a custom framerate param here if needed.
        :param int framerate: The custom framerate value.
        :return int: The milliseconds since last tick.
        """
        if framerate is None:
            return self._clock.tick_busy_loop(self.fps)
        else:
            return self._clock.tick_busy_loop(framerate)

    def get_fps(self):
        """
        Gets the current FPS.
        :return float: Current FPS
        """
        return self._clock.get_fps()

    def get_time(self):
        """
        :shrug:
        :return int: The milliseconds used in the last tick.
        """
        return self._clock.get_time()

    def get_rawtime(self):
        """
        :shrug:
        :return int: The milliseconds actual time used in the last tick.
        """
        return self._clock.get_rawtime()


class CUIGroup:
    """
    Essentially a pygame.Surface that stores objects.
    :param size: Size of the surface.
    :param flags: Flags to pass to the pygame.Surface.
    """

    def __init__(self, size: Sequence[float] = (0, 0), flags: int = 0):
        if size == (0, 0):
            size = (800, 600)

        if flags == 0:
            flags = pygame.SRCALPHA

        self.surface = pygame.Surface(size, flags=flags)
        self.surface.fill(CUColor((255, 255, 255), 0))

        self.do_rotate = [False, 0]

        self.pos = [0, 0]
        self.objs: list[CUIObject] = []

    def add_obj(self, obj: Union[CUIObject, BaseObject]):
        """
        Add an object to the Group.
        :param CUIObject obj: Any UI object.
        :return:
        """
        if obj not in self.objs:
            self.objs.append(obj)

    def remove_obj(self, obj):
        """
        Remove an object from the Group.
        :param CUIObject obj: Any UI object.
        :return:
        """
        if obj in self.objs:
            del self.objs[self.objs.index(obj)]

    def draw(self, screen):
        """
        Draw the Group of UI objects to the screen.
        :param screen: A CScreen to draw to.
        :return:
        """
        self.surface.fill(CUColor((255, 255, 255), 0))
        for obj in self.objs:
            obj.draw(self.surface)

        if self.do_rotate[0]:
            surface = pygame.transform.rotate(self.surface, self.do_rotate[1])
            self.do_rotate = [False, 0]
        else:
            surface = self.surface

        screen.draw(surface, self.pos)

    def connect_manager(self, manager: CUIManager):
        """
        Connects a CUIManager to all the objects currently in the Group.
        :param CUIManager manager: A UI Manager.
        :return:
        """
        for obj in self.objs:
            manager.update_object(obj)

    def rotate(self, degree: float):
        """
        Rotates the surface within the group.
        This function works by tasking the rotation to happen later (right before draw call)
        :param float degree: The angle to rotate by (in degrees).
        """
        self.do_rotate = [True, degree]


class CScreen:
    """
    A custom implementation of the pygame screen object, allowing more versatility and easier usage.

    :param Sequence[float] size: The size of the display defaults to (800, 600).
    :param int flags: The pygame flags to pass to the creation of the screen
    :param int display: Unknown what this really does, not listed in any documentation.
    :param int vsync: Whether to have vsync, if OPENGL parameter is sent -1 vsync will turn on adaptive vsync.
    :param str caption: The caption to put as the title.
    :param str icon: The icon for the window (note in development, this won't show up in the taskbar).
    :param bool scrap: Whether to initialize the scrap (clipboard) module.
    :param bool clock: Whether to add a clock to the object.
    :param int fps: Sets the FPS for the clock, defaults to 60.
    """

    def __init__(self, size: Sequence[float] = (0, 0), flags: int = 0, display: int = 0,
                 vsync: int = 0, caption: str = "No Caption Provided", icon: str = None, scrap: bool = False,
                 clock: bool = False, fps: int = 60):
        if size == (0, 0):
            size = (800, 600)

        if flags == 0:
            flags = pygame.SRCALPHA

        self.surface = pygame.display.set_mode(size=size, flags=flags, display=display, vsync=vsync)

        pygame.display.set_caption(caption)

        if icon is not None:
            pygame.display.set_icon(pygame.image.load(icon))

        if scrap:
            pygame.scrap.init()

        if clock:
            self.clock: CGClock = CGClock(fps)

    def fill(self, color: CUColor):
        """
        Fills the screen with a certain color.
        :param CUColor color: The Custom UI Color to fill the screen with.
        """
        self.surface.fill(color=color)

    def draw(self, obj, pos: Sequence[float] = None) -> None:
        """
        Draw any type of object to the screen.
        :param obj: The object to put on the screen.
        :param pos: Optional argument depending on if you are putting a rectangle or not.
        :return: None
        """
        if isinstance(obj, (CUIObject, CRect, BaseObject, pygame.FRect, pygame.Rect)):
            # check if its FRect or normal rect, if so then run just a default call.
            if type(obj) is pygame.FRect or type(obj) is pygame.Rect:
                pygame.draw.rect(self.surface, (255, 255, 255), obj)
                print("WARNING: Attempted to draw a pygame FRect/Rect onto a CScreen! (Resulted in default draw call!")
                return

            obj.draw(self.surface)

        elif isinstance(obj, CUIGroup):  # since CUIGroups are surfaces, they will be in here as well.
            obj.draw(self)
            return

        elif isinstance(obj, pygame.Surface):
            if pos is None:
                raise TypeError("Missing required positional argument, 'pos'! (required for pygame.Surface)")

            self.surface.blit(obj, pos)  # noqa:unexpected_types ; its saying "Sequence[float] is not Sequence[float]"

        else:
            raise TypeError("Object is not any drawable object!")

    @staticmethod
    def close(kill: bool = True) -> None:
        """
        Closes pygame, and possibly the entire program.
        :param kill: Whether to kill the program. Defaults to True.
        :return: None
        """
        pygame.quit()
        if kill:
            import sys
            sys.exit(1)

    def tick(self):
        """
        Ticks using the screens CGClock.
        Will not work without a CGClock defined.
        :return:
        """

        if getattr(self, "clock", False):
            return self.clock.tick()
        else:
            print("ERROR: Attempted to call tick() without a clock defined!")
            return 0


class CScaleScreen(CScreen):
    """
    A custom implementation of the pygame screen object, allowing more versatility and easier usage.
    WARN: You should NEVER attempt to go inside and take the direct screen! (it will FAIL)
    ^ instead take the `prescaledSurface` object

    :param Sequence[float] size: The STARTING size of the display defaults to (800, 600).
    :param int flags: The pygame flags to pass to the creation of the screen
    :param int display: Unknown what this really does, not listed in any documentation.
    :param int vsync: Whether to have vsync, if OPENGL parameter is sent -1 vsync will turn on adaptive vsync.
    :param str caption: The caption to put as the title.
    :param str icon: The icon for the window (note in development, this won't show up in the taskbar).
    :param bool scrap: Whether to initialize the scrap (clipboard) module.
    :param bool clock: Whether to add a clock to the object.
    :param int fps: Sets the FPS for the clock, defaults to 60.
    """
    def __init__(self, size: Sequence[float] = (0, 0), flags: int = 0, display: int = 0,
                 vsync: int = 0, caption: str = "No Caption Provided", icon: str = None, scrap: bool = False,
                 clock: bool = False, fps: int = 60):
        super().__init__(size, flags | pygame.RESIZABLE, display, vsync, caption, icon, scrap, clock, fps)
        # some odd fix that patches prescaled not using updated size from the super func
        if size == (0, 0):
            self.size = (800, 600)
        else:
            self.size = size

        self.prescaledSurface = pygame.Surface((self.size[0], self.size[1]), flags)

    def draw(self, obj, pos: Sequence[float] = None) -> None:
        if isinstance(obj, (CUIObject, CRect, BaseObject, pygame.FRect, pygame.Rect)):
            # check if its FRect or normal rect, if so then run just a default call.
            if type(obj) is pygame.FRect or type(obj) is pygame.Rect:
                pygame.draw.rect(self.prescaledSurface, (255, 255, 255), obj)
                print("WARNING: Attempted to draw a pygame FRect/Rect onto a CScreen! (Resulted in default draw call)!")
                return

            obj.draw(self.prescaledSurface)

        elif isinstance(obj, CUIGroup):  # since CUIGroups are surfaces, they will be in here as well.
            raise ValueError("CUIGroups are currently not implemented correctly for this (bypasses scaler)")
            # obj.draw(self)
            # return self._post_draw()

        elif isinstance(obj, pygame.Surface):
            if pos is None:
                raise TypeError("Missing required positional argument, 'pos'! (required for pygame.Surface)")

            self.prescaledSurface.blit(obj, pos)  # noqa:unexpected_types ; its saying "Sequence[float] is not Sequence[float]"

        else:
            raise TypeError("Object is not any drawable object!")

    def before_flip(self):
        """
        MUST BE USED BEFORE FLIPPING THE SCREEN OTHERWISE YOU JUST HAVE A BLACK SCREEN!
        :return:
        """
        size = self.surface.get_size()

        scaled = pygame.transform.scale(self.prescaledSurface, size)

        self.surface.blit(scaled, (0, 0))

    def fill(self, color: CUColor):
        """
        Fills the screen with a certain color.
        :param CUColor color: The Custom UI Color to fill the screen with.
        """
        self.prescaledSurface.fill(color=color)


class CGCamera:
    """
    A game camera
    :param pygame.Surface surface: The surface to render to.
    """

    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self._x = 0
        self._y = 0

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, x: float):
        self._x = x

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, y: float):
        self._y = y

    def render(self, obj: Union[CRect, CUIGroup, BaseObject, pygame.Surface], pos: Sequence[float] = None):
        """
        Renders objects onto the screen based off the camera.
        :param CRect obj: Any CRect, CUIObject, or any object higher in the object chain.
        :param Sequence[float] pos: The position to place the object. Optional for all except surfaces.
        :return:
        """
        # this function is named 'render' instead of 'draw' because it is actively modifying things before drawing.
        if isinstance(obj, CUIGroup):
            # these objects work differently as it is just a group of objects
            for o in obj.objs:
                self.render(o)
            return

        elif isinstance(obj, CLine):
            # these objects work differently, as it is a line that we have to move
            os = [obj.start[0], obj.start[1]]
            oe = [obj.end[0], obj.end[1]]
            obj.start[0] -= self.x
            obj.end[0] -= self.x
            obj.start[1] -= self.y
            obj.end[1] -= self.y

            obj.draw(self.surface)

            obj.start = os
            obj.end = oe
            return

        elif isinstance(obj, CCircle):
            # these objects work differently
            oc = [obj.center[0], obj.center[1]]
            obj.center[0] -= self.x
            obj.center[1] -= self.y

            obj.draw(self.surface)

            obj.center = oc
            return

        elif isinstance(obj, pygame.Surface):
            if pos is None:
                raise TypeError("Missing required positional argument, 'pos'! (required for pygame.Surface)")

            npos = [pos[0], pos[1]]
            npos[0] -= self.x
            npos[1] -= self.y

            self.surface.blit(obj, npos)
            return

        # save pos for later restore
        ox = obj.x
        oy = obj.y

        # move obj
        obj.x -= self.x
        obj.y -= self.y

        obj.draw(self.surface)

        # restore pos
        obj.x = ox
        obj.y = oy


def init():
    """
    Initializes anything required for the UI system.
    WARNING: pygame.scrap is NOT initialized here! It requires a window to initialize!
    :return: None
    """
    pygame.init()
    print("initialized pygame-ce based UI system.")


if __name__ == "__main__":
    # import time
    # from settings import find_filepath
    #
    # delay = 0.5
    # pygame.init()
    # screen = CScreen()
    # rect = CRect(0, 0, 100, 100, CustomColor((255, 0, 0)))x
    # pygame.display.flip()
    #
    # time.sleep(delay)
    # screen.draw_to(rect)
    # pygame.display.flip()
    #
    # time.sleep(delay)
    # img = pygame.image.load(find_filepath("assets") + "/testing_img.png", "testing_img")
    # screen.draw(img, (100, 100))
    # pygame.display.flip()
    # time.sleep(delay)
    # ----------------------------------------- #
    # pygame.init()
    # screen = CScreen()
    # button = CUIButton(20, 20, 300, 50, CustomColor((0, 0, 255)))
    #
    # manager = CUIManager([button])
    #
    # while True:
    #     evnts = pygame.event.get()
    #     for evnt in evnts:
    #         if evnt.type == pygame.QUIT:
    #             screen.close(kill=True)
    #     manager.tick(evnts)
    #
    #     screen.draw(button)
    #     pygame.display.flip()
    # -------------------------------------- #
    # camera test
    # cscreen = CScreen(clock=True, fps=60)
    # camera = CGCamera(cscreen)
    #
    # rectangle = CRect(100, 100, 200, 50, CUColor.BLUE())
    #
    # offscreen_rectangle = CRect(-100, 100, 10, 100, CUColor.ORANGE())
    #
    # static_rectangle = CRect(200, 200, 50, 100, CUColor.RED())
    #
    # while True:
    #     cscreen.tick()
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             cscreen.close(kill=True)
    #
    #     if pygame.key.get_pressed()[pygame.K_w]:
    #         camera.y -= 10
    #
    #     if pygame.key.get_pressed()[pygame.K_s]:
    #         camera.y += 10
    #
    #     if pygame.key.get_pressed()[pygame.K_a]:
    #         camera.x -= 10
    #
    #     if pygame.key.get_pressed()[pygame.K_d]:
    #         camera.x += 10
    #
    #     cscreen.fill(CUColor.WHITE())
    #
    #     camera.render(rectangle)
    #
    #     camera.render(offscreen_rectangle)
    #
    #     cscreen.draw(static_rectangle)
    #
    #     pygame.display.flip()

    pass
