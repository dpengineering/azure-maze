import os

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

SCREEN_MANAGER = ScreenManager()
IDLE_SCREEN_NAME = 'idle'


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


class IdleScreen(Screen):
    pass


"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(IdleScreen(name=IDLE_SCREEN_NAME))



if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    AzureMaze().run()
