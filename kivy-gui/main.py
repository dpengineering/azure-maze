import os

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.image import Image
import os.path

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from kivy.animation import Animation
from kivy.config import Config

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
INSTRUCTIONS_SCREEN_NAME = 'instructions'
OPTIONS_SCREEN_NAME = 'options'

class CustomImage(Image):
    def __init__(self, *args, **kwargs):
        Image.__init__(self, *args, **kwargs)
        self.bind(texture=self._update_texture_filters)

    def _update_texture_filters(self, image, texture):
        texture.mag_filter = 'nearest'


class AzureMaze(App):
    """
    Class to handle running the GUI Application
    """


    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White 1280 x 1080
class MainScreen(Screen):
    def __init__(self, **kw):
        super(MainScreen, self).__init__(**kw)

class InstructionsScreen(Screen):
    def __init__(self, **kw):
        super(InstructionsScreen, self).__init__(**kw)

class OptionsScreen(Screen):
    def __init__(self, **kw):
        super(OptionsScreen, self).__init__(**kw)


"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(InstructionsScreen(name=INSTRUCTIONS_SCREEN_NAME))
SCREEN_MANAGER.add_widget(OptionsScreen(name=OPTIONS_SCREEN_NAME))



if __name__ == "__main__":
    Window.size = (1280, 1080)
    Window.borderless = 1
    AzureMaze().run()
