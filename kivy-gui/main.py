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


Window.clearcolor = (1, 1, 1, 1)  # White
class MainScreen(Screen):
     pass
class InstructionScreen(Screen):
    pass


"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(InstructionScreen(name=INSTRUCTIONS_SCREEN_NAME))



if __name__ == "__main__":
    Window.size = (1280, 1080)
    Window.borderless = 1
    AzureMaze().run()
