"""
@file Joystick.py File to interact with a joystick
"""
import pygame
import os


class Joystick:
    """
    Class to handle the joystick and getting current states
    """

    def __init__(self, number, ssh_deploy):
        """
        Initialize Joystick
        :param number: Joystick number
        :param ssh_deploy: True if deploying over ssh
        """
        if ssh_deploy:  # allow ssh deploy with pygame
            os.environ['SDL_VIDEODRIVER'] = "dummy"

        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(number)
        self.joystick.init()

        self.num_buttons = self.joystick.get_numbuttons()

    def get_axis(self, axis):
        """
        Get the axis (x or y) of the joystick.
        :raises: ValueError If the given axis isn't 'x' 'y'
        :param axis: axis to get value of
        :rtype: float
        :return: All the way to the right=1, fully up=-1
        """
        axis.lower()
        self.refresh()

        if axis == 'x':
            return self.joystick.get_axis(0)
        elif axis == 'y':
            return self.joystick.get_axis(1)

        else:
            raise ValueError("Axis must be of type str and either 'x' or 'y'")

    def get_both_axes(self):
        """
        Get the status of both axes (x and y)
        :return: An array of both axes, [x-axis, y-axis]
        """
        return [self.get_axis('x'), self.get_axis('y')]

    @staticmethod
    def refresh():
        """
        Refresh the joysticks current value
        :return: None
        """
        pygame.event.pump()

    def get_button_state(self, button_num):
        """
        Get the state of a button. This project uses the "Logitech Attack 3" which contains 11 physical buttons but are
        indexed 0-10
        :param button_num: Button number to get the state of
        :raises: ValueError if the given button number is not in the range of available buttons
        :rtype: int
        :return: 0 or 1 (1=button depressed)
        """
        self.refresh()

        if button_num not in range(self.num_buttons):
            raise ValueError("The button number given is not a button on the joystick, "
                             "must be in range (0-%s)" % self.num_buttons)
        else:
            return self.joystick.get_button(button_num)

    def button_combo_check(self, buttons):
        """
        Check to see if the given button numbers are all being pressed
        :param buttons: List of buttons to check
        :rtype: bool
        :return: True if ALL of the buttons are being pressed, false otherwise
        """
        self.refresh()

        for button in buttons:
            if not self.get_button_state(button):
                return False
        return True
