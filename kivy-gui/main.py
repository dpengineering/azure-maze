#Written by Andrew Xie and Kogan Sam, December 2020, for the DPEA
import os

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.label import Label
from kivy.uix.image import Image
import os.path

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from kivy.animation import Animation
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.config import Config
from threading import Thread
from time import sleep

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
INSTRUCTIONS_SCREEN_NAME = 'instructions'
LEADERBOARD_SCREEN_NAME = 'leaderboard'
OPTIONS_SCREEN_NAME = 'options'
START_SCREEN_NAME = 'start'
CREDITS_SCREEN_NAME = 'credits'
GAME_SCREEN_NAME = 'game'
END_SCREEN_NAME = 'end'

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
    pass


class StartScreen(Screen):
    global num
    num = 10
    global event1
    def countstart(self):
        global event1
        event1 = Clock.schedule_interval(self.countdown, 1)
    def countdown(self,dt):
        global num
        global event1
        if num >= 2:
            num = num - 1
            print("%d" % num)
            self.ids.number.text = "%d" % num
        else:
            num = 10
            SCREEN_MANAGER.current = GAME_SCREEN_NAME
            Clock.unschedule(event1)
            self.ids.number.text = "%d" % num


class GameScreen(Screen):
    pass


class EndScreen(Screen):
    pass


class LeaderboardScreen(Screen):
    pass


class InstructionsScreen(Screen):
    pass


class OptionsScreen(Screen):
    pass

class CreditsScreen(Screen):
    pass


"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(StartScreen(name=START_SCREEN_NAME))
SCREEN_MANAGER.add_widget(GameScreen(name=GAME_SCREEN_NAME))
SCREEN_MANAGER.add_widget(EndScreen(name=END_SCREEN_NAME))
SCREEN_MANAGER.add_widget(LeaderboardScreen(name=LEADERBOARD_SCREEN_NAME))
SCREEN_MANAGER.add_widget(InstructionsScreen(name=INSTRUCTIONS_SCREEN_NAME))
SCREEN_MANAGER.add_widget(OptionsScreen(name=OPTIONS_SCREEN_NAME))
SCREEN_MANAGER.add_widget(CreditsScreen(name=CREDITS_SCREEN_NAME))



if __name__ == "__main__":
    Window.size = (1280, 1080)
    Window.borderless = 1
    AzureMaze().run()
