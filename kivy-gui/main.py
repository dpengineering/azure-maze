import os

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.config import Config

SCREEN_MANAGER = ScreenManager()
LEADERBOARD_SCREEN_NAME = 'leaderboard'
IDLE_SCREEN_NAME = 'idle'
GAME_SCREEN_NAME = 'game'


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
class LeaderScreen(Screen):
    pass
class IdleScreen(Screen):
    pass
class GameScreen(Screen):
    pass


"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(LeaderScreen(name=LEADERBOARD_SCREEN_NAME))



if __name__ == "__main__":
    # send_event("Project Initialized")
    Config.set('graphics', 'window_state', 'visible')
    Config.write()
    Window.size = (1280, 1024)
    #Window.borderless = 1
    AzureMaze().run()
