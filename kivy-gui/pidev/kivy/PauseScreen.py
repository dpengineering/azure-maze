from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.clock import Clock
import os.path
from kivy.app import App

pause_screen_kv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "", "PauseScreen.kv")
Builder.load_file(pause_screen_kv_path)


class PauseScreen(Screen):
    """
    Class used to pause the UI
    """
    white_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "white.png")

    @staticmethod
    def pause(pause_scene_name, transition_back_scene, text, pause_duration):
        """
        Pause the UI for a given amount of time
        :param pause_scene_name: The name of the PauseScreen when added as a widget
        :param transition_back_scene: The name of the scene (when added as a widget) to transition back to when complete
        :param text: The text to display on screen while paused
        :param pause_duration: The number of seconds to pause the UI for
        :return: None
        """
        screen_manager = App.get_running_app().root

        screen_manager.current = pause_scene_name
        screen_manager.get_screen(pause_scene_name).ids.pause_text.text = text

        load = Animation(size=(10, 10), duration=0) + \
                    Animation(size=(150, 10), duration=pause_duration)
        load.start(screen_manager.get_screen(pause_scene_name).ids.progress_bar)

        Clock.schedule_once(lambda dt: PauseScreen.transition_back(transition_back_scene), pause_duration)
        return

    @staticmethod
    def transition_back(screen_name):
        """
        Transition the UI back from the PauseScreen
        :param screen_name: The name of the screen to transition back to
        :return: None
        """
        App.get_running_app().root.current = screen_name
