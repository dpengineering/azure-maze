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
from kivy.uix.button import Button
from kivy.properties import BooleanProperty

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
INSTRUCTIONS_SCREEN_NAME = 'instructions'
LEADERBOARD_SCREEN_NAME = 'leaderboard'
OPTIONS_SCREEN_NAME = 'options'
START_SCREEN_NAME = 'start'
CREDITS_SCREEN_NAME = 'credits'
GAME_SCREEN_NAME = 'game'
END_SCREEN_NAME = 'end'
ADMIN_SCREEN_NAME = 'admin'
PASSCODESCREEN_SCREEN_NAME = 'passCode'
class HoverBehavior(object):
    """Hover behavior.
    :Events:
        `on_enter`
            Fired when mouse enter the bbox of the widget.
        `on_leave`
            Fired when the mouse exit the widget
    """

    hovered = BooleanProperty(False)
    border_point= ObjectProperty(None)
    '''Contains the last relevant point received by the Hoverable. This can
    be used in `on_enter` or `on_leave` in order to know where was dispatched the event.
    '''

    def __init__(self, **kwargs):
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(HoverBehavior, self).__init__(**kwargs)

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return # do proceed if I'm not displayed <=> If have no parent
        pos = args[1]
        #Next line to_widget allow to compensate for relative layout
        inside = self.collide_point(*self.to_widget(*pos))
        if self.hovered == inside:
            #We have already done what was needed
            return
        self.border_point = pos
        self.hovered = inside
        if inside:
            self.dispatch('on_enter')
        else:
            self.dispatch('on_leave')

    def on_enter(self):
        pass

    def on_leave(self):
        pass

from kivy.factory import Factory
Factory.register('HoverBehavior', HoverBehavior)

# modified from opqopq/hoverable.py
class HoverButton(Button, HoverBehavior):
    def on_enter(self, *args):
        pass

    def on_leave(self, *args):
        pass


class CustomImage(Image):
    def __init__(self, *args, **kwargs):
        Image.__init__(self, *args, **kwargs)
        self.bind(texture=self._update_texture_filters)

    def _update_texture_filters(self, image, texture):
        texture.mag_filter = 'nearest'


dpea_button_kv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "", "DPEAButton.kv")
Builder.load_file(dpea_button_kv_path)


class CustomButton(Button):
    shadow_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "shadow.png")
    shadow_path = ObjectProperty(shadow_image_path)

    def __init__(self, **kwargs):
        """
        Specifies the background_color, background_normal, and size_hint for all instances
        :param kwargs: Arguments passed to the Button Instance
        """
        super(DPEAButton, self).__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        self.size_hint = (None, None)
        self.original_colors = list()

    def on_press(self):
        """
        Overrides the Button default on_press to darken the color of the button.
        :return: None
        """
        super(DPEAButton, self).on_press()
        self.original_colors = self.color
        self.color = [i * 0.7 for i in self.original_colors]

    def on_touch_up(self, touch):
        """
        Overrides the Button default on_touch_up to revert the buttons color back to its original color.
        NOTE: This method is called for every widget onscreen
        :return: None
        """
        super(DPEAButton, self).on_touch_up(touch)

        # If button hasn't been pressed self.original colors is empty and will make the button color be black
        # So if the length is empty it hasn't been pressed so we return
        if len(self.original_colors) == 0:
            return

        self.color = self.original_colors
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
PASSWORD = '7266'
USERPW = ''

passcode_screen_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "", "PassCodeScreen.kv")

Builder.load_file(passcode_screen_path)

ADMIN_EVENTS_SCREEN = None
TRANSITION_BACK_SCREEN = 'main'

class PassCodeScreen(Screen):
    """
    Class used to enter the PassCodeScreen to enter the admin screen
    """

    def __init__(self, **kw):
        super(PassCodeScreen, self).__init__(**kw)

    def initialize(self):
        curr_app = App.get_running_app()
        print("wait")

    def add_num(self, num):
        """
        Add a number to the current password entry
        :param num: Number to add
        :return: None
        """
        global USERPW

        self.ids.pw.color = 0.392, 0.537, 0.631 , 1
        self.ids.pw.text += '* '
        USERPW += str(num)

    def remove_num(self):
        """
        Remove a number from the current password entry
        :return: None
        """
        global USERPW
        self.ids.pw.text = self.ids.pw.text[:len(self.ids.pw.text) - 2]
        USERPW = USERPW[:len(USERPW) - 1]

    def check_pass(self):
        """
        Check to see if the password was entered correctly
        :return: None
        """
        global USERPW
        if PASSWORD == USERPW:
            self.ids.pw.text = ' '
            USERPW = ''

            if ADMIN_EVENTS_SCREEN is None:
                print("Specify the admin screen name by calling PassCodeScreen.set_admin_events_screen")
                return

            self.parent.current = ADMIN_EVENTS_SCREEN

    def transition_back(self):
        """
        Transition back to given transition back scren
        :return: None
        """
        self.ids.pw.text = ""
        self.parent.current = TRANSITION_BACK_SCREEN

    @staticmethod
    def set_admin_events_screen(screen):
        """
        Set the name of the screen to transition to when the password is correct
        :param screen: Name of the screen to transition to
        :return: None
        """
        global ADMIN_EVENTS_SCREEN
        ADMIN_EVENTS_SCREEN = screen

    @staticmethod
    def set_transition_back_screen(screen):
        """
        Set the screen to transition back to when the "Back to Game" button is pressed
        :param screen: Name of the screen to transition back to
        :return: None
        """
        global TRANSITION_BACK_SCREEN
        TRANSITION_BACK_SCREEN = screen

    @staticmethod
    def set_password(pswd):
        """
        Change the default password
        :param pswd: New password
        :return: None
        """
        global PASSWORD
        PASSWORD = pswd

    @staticmethod
    def change_main_screen_name(name):
        """
        Change the name of the screen to add the hidden button to go to the admin screen

        NOTE: This only needs to be run ONCE, once it is called with the new name you can remove the call from your code
        :param name: Name of the main screen of the UI
        :return: None
        """
        if name == '':
            return

        with open(passcode_screen_path) as file:
            data = file.readlines()

        # This needs to be updated every time there are line changes in the PassCodeScreen.kv
        # TODO implement a better way to dynamically change the main screen name
        data[134] = '<' + name + '>\n'

        with open(passcode_screen_path, 'w') as file:
            file.writelines(data)


class MainScreen(Screen):
    pass


class StartScreen(Screen):
    global num
    num = 5
    global event1
    def countstart(self):
        global event1
        sleep(0.3);
        event1 = Clock.schedule_interval(self.countdown, 1)
        self.ids.number.text = "%d" % num
    def countdown(self,dt):
        global num
        global event1
        if num >= 2:
            num = num - 1
            print("%d" % num)
            self.ids.number.text = "%d" % num
        else:
            num = 5
            SCREEN_MANAGER.current = GAME_SCREEN_NAME
            Clock.unschedule(event1)
            self.ids.number.text = "Ready"


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


class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()
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
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))


if __name__ == "__main__":
    Window.size = (1280, 1080)
    Window.borderless = 1
    AzureMaze().run()
