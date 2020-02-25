"""
@file stepper.py
File containing stepper class to interface with stepper motors on the Slush Engine
"""
import sys
from collections import OrderedDict
import Slush
from Slush.Devices import L6470Registers as LReg
from Slush.Devices import L6480Registers as LReg6480
from .slush_manager import slush_board as slush_board

CHIP_STATUSES_XLT = OrderedDict([  # MSB to LSB of motor controller status and index of the associated bit (16 bit number)
        ('SCK_MOD', 0),
        ('STEP_LOSS_B\\', 1),
        ('STEP_LOSS_A\\', 2),
        ('OCD\\', 3),
        ('TH_SD\\', 4),
        ('TH_WRN\\', 5),
        ('UVLO\\', 6),
        ('WRONG_CMD', 7),
        ('NOTPERF_CMD', 8),
        ('MOT_STATUS', (9, 10)),
        ('DIR', 11),
        ('SW_EVEN', 12),
        ('SW_F', 13),
        ('BUSY\\', 14),
        ('HiZ', 15)])

CHIP_STATUSES_D = OrderedDict([ # MSB to LSB of motor controller status and the number of associated bits
        ('STEP_LOSS_B\\', 0),
        ('STEP_LOSS_A\\', 1),
        ('OCD\\', 2),
        ('TH_STATUS', (3, 4)),
        ('UVLO_ADC\\', 5),
        ('UVLO\\', 6),
        ('STCK_MOD', 7),
        ('CMD_ERROR', 8),
        ('MOT_STATUS', (9, 10)),
        ('DIR', 11),
        ('SW_EVN', 12),
        ('SW_F', 13),
        ('BUSY', 14),
        ('HiZ', 15)
    ])


class stepper(Slush.Motor):
    """
    DPEA stepper implementation, extended from Slush.Motor
    Reference Slush.Motor for additional functionality
    """
    instances = []

    def __init__(self, port=0, micro_steps=64, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
                 steps_per_unit=200/25.4, speed=1):
        """
        Constructor for the stepper class
        :param port: port the stepper is connected to. 0-3 on XLT, 0-6 on D. Default:0
        :param micro_steps: how much each step is subdivided. (1,2,4,8,16,32,64,128) Default:64
        :param hold_current: amount of current when motor is holding in place. Default:20
        :param run_current: amount of current when motor is moving at constant speed. Default:20
        :param accel_current: amount of current when motor is accelerating. Default:20
        :param deaccel_current: amount of current when motor is decelerating. Default:20
        :param steps_per_unit: amount of steps per unit. used so you can control motors by linear distance (with lead
               screws) or by revolutions if the motor rotates something Default:200/25.4 (used to move in mm on 8mm/turn lead screws)
        :param speed: how fast the stepper moves in units
        """
        super().__init__(port)
        self.port = port
        self.resetDev()
        self.micro_steps = micro_steps
        self.set_micro_steps(self.micro_steps)
        self.setCurrent(hold_current,
                        run_current,
                        accel_current,
                        deaccel_current)
        self.steps_per_unit = steps_per_unit
        self.speed = speed
        self.set_speed(self.speed)
        if self.boardInUse == 1:
            self.setParam(LReg6480.GATECFG1, 0x5F)
            self.setParam(LReg6480.OCD_TH, 0x1F)

    def _get_status_byte(self):
        """
        Get the status byte as a String
        :return: String of the status byte
        """
        byte = '{0:b}'.format(self.getStatus())

        if len(byte) != 16:  # Add leading zeroes to the byte to make it 16 bits
            diff = 16 - len(byte)
            byte = "0" * diff + byte
        return byte

    def print_status(self):
        """
        Print all of the registers status for the L6470 chipset, if a status has a \ means it is active low
        :return: None
        """
        byte = self._get_status_byte()

        print("The byte for ", str(self), "is: ", byte)

        if self.boardInUse == 0:  # if the slush board is not the model D
            for status in CHIP_STATUSES_XLT:
                byte_index = CHIP_STATUSES_XLT.get(status)

                if isinstance(byte_index, tuple):
                    print(status + " " + str(byte[byte_index[0]]) + str(byte[byte_index[1]]))
                else:
                    print(status + " " + str(byte[byte_index]))
        else:
            for status in CHIP_STATUSES_D:
                byte_index = CHIP_STATUSES_D.get(status)

                if isinstance(byte_index, tuple):
                    print(status + " " + str(byte[byte_index[0]]) + str(byte[byte_index[1]]))
                else:
                    print(status + " " + str(byte[byte_index]))

    def get_specific_status(self, status_register):
        """
        Get the specific status of a register
        :param status_register: The register status you want to check
        :return: String of the status. This is necessary as some statuses are 2 bits and a string ensures no truncation
        """
        byte = self._get_status_byte()

        if self.boardInUse == 0:
            data = CHIP_STATUSES_XLT.get(status_register)
            if data is None:
                raise ValueError("Invalid status register try adding the active low flag '\\\\' to the parameter")

            if isinstance(data, tuple):
                return str(byte[data[0]]) + str(byte[data[1]])
            else:
                return str(byte[data])
        else:
            data = CHIP_STATUSES_D.get(status_register)
            if data is None:
                raise ValueError("Invalid status register try adding the active low flag '\\\\' to the parameter")

            if isinstance(data, tuple):
                return str(byte[data[0]]) + str(byte[data[1]])
            else:
                return str(byte[data])

    def get_micro_steps(self):
        """
        Get the number of microsteps the stepper motor is running at
        :return:
        """
        return self.micro_steps

    def set_micro_steps(self, micro_steps):
        """
        Set the number of microsteps the stepper motor runs at
        :param micro_steps: Number of microsteps of base 2 up to a maximum of 128
        :return: None
        """
        if micro_steps > 128:
            sys.exit("ERROR: Slush Engine only supports microstepping values of base 2 up to a maximum of 128")

        self.micro_steps = micro_steps
        self.setMicroSteps(micro_steps)

    def set_speed(self, speed_in_units):
        """
        Set the speed the stepper motor runs at in units
        :param speed_in_units: Speed the motor will run at in units
        :return: None
        """
        self.speed = speed_in_units * self.steps_per_unit
        self.set_max_speed(self.speed)

    def set_speed_in_steps(self, speed):
        """
        set the speed the stepper motor runs at in steps
        :param speed: Speed the motor will run at in steps
        :return: None
        """
        self.set_max_speed(speed)
    def set_accel(self, acceleration):
        """
        Set the acceleration of the motor
        :param acceleration: Acceleration amount
        :return: None
        """
        self.setAccel(acceleration)

    def set_deaccel(self, deceleration):
        """
        Set the deceleration for the motor
        :param deceleration: Deceleration amount
        :return: None
        """
        self.setDecel(deceleration)

    def home(self, direction):
        """
        Home the motor
        :param direction: Direction (0 or 1) the motor should spin when homing 0-clockwise
        :return: None
        """
        self.run(direction, self.speed)

        while not self.read_switch():
            continue

        self.hard_stop()
        self.set_as_home()

    def read_switch(self):
        """
        Read the stepper motors corresponding switch
        :return: None
        """
        if self.getStatus() & 0x4:
            return 1
        else:
            return 0

    def relative_move(self, distance_in_units):
        """
        Moves a certain distance in units (defined by steps_per_unit in constructor) with MOVEMENTS BLOCKED (synchronise)
        :param distance_in_units: a distance in units
        :return:
        """
        number_of_steps = distance_in_units * self.micro_steps * self.steps_per_unit
        self.move(int(number_of_steps))
        self.wait_move_finish()

    def start_relative_move(self, distance_in_units):
        """
        Starts moving a certain distance in units (defined by steps_per_unit in constructor) WITHOUT BLOCKING MOVEMENTS (a-synchronise)
        :param distance_in_units: a distance in units
        :return:
        """
        number_of_steps = distance_in_units * self.micro_steps * self.steps_per_unit
        self.move(int(number_of_steps))

    def go_to_position(self, position_in_units):
        """
        Goes to a set position in units (defined by steps_per_unit in constructor) WITH BLOCKING (synchronise)
        :param position_in_units: position to move to in units
        :return: None
        """
        position_in_steps = position_in_units * self.micro_steps * self.steps_per_unit
        self.go_to(int(position_in_steps))
        self.wait_move_finish()

    def start_go_to_position(self, position_in_units):
        """
        begins going to a set position in units (defined by steps_per_unit in constructor) WITHOUT BLOCKING (a-synchronise)
        :param position_in_units: position to move to in units
        :return: None
        """
        position_in_steps = position_in_units * self.micro_steps * self.steps_per_unit
        self.go_to(int(position_in_steps))

    @staticmethod
    def get_GPIO_state(port, pin):
        """
        Get the state of one of the GPIO pins
        :param port: GPIO port a=0, b=1
        :param pin: Pin to check, first pin=0 incrementing by one
        :return:
        """
        return slush_board.getIOState(port, pin)

    @staticmethod
    def set_GPIO_state(port, pin, state):
        """
        Set the state of one of the GPIO pins
        :param port: GPIO port a=0, b=1
        :param pin: Pin to set, first pin=0 incrementing by one
        :param state: State you want to set the pin at
        :return: None
        """
        return slush_board.setIOState(port, pin, state)

    def set_limit_hardstop(self, stop):
        """
        Set whether the Slush Engine should stop moving the stepper motor when it hits the limit switch
        :param stop: True motor with stop when sensor is high (Should be used in cases where there is a mechanical stop)
                     False motor will continue past sensor (Should be used when motor can rotate freely)
        :return: None
        """
        try:
            self.setLimitHardStop(stop)
        except AttributeError:
            sys.exit("Update SlushEngine Code (DPEA Fork), this feature is only on recent versions")

    def stop(self):
        """
        Stops the motor, same as performing a hard stop
        :return: None
        """
        self.hard_stop()

    def hard_stop(self):
        """
        Hard stop the motor
        :return: None
        """
        self.hardStop()

    def go_to(self, number_of_steps):
        """
        Make the stepper go to a position in steps
        :param number_of_steps: Number of steps to move
        :return: None
        """
        self.goTo(number_of_steps)

    def wait_move_finish(self):
        """
        Wait for the move to finish
        :return: None
        """
        self.waitMoveFinish()

    def set_as_home(self):
        """
        Set the current position as home
        :return: None
        """
        self.setAsHome()

    def set_max_speed(self, speed):
        """
        Set the max speed the stepper motor can run at
        :param speed: The maximum speed
        :return: None
        """
        self.setMaxSpeed(speed)

    def move_steps(self, steps):
        """
        Move the stepper motor a set amount of steps including microstepping. Forwards the call to Slush Motor move()
        :param steps: Number of steps to move (multiplied by microstepping amount)
        :return: None
        """
        self.move(steps * self.micro_steps)

    def go_until_press(self, dir, speed):
        """
        Move the stepper until it hits a sensor
        :param dir: The direction 1 or 0
        :param speed: Speed in steps per second
        :return: None
        """
        if self.read_switch() is 0:
            self.goUntilPress(1, dir, speed)

    def is_busy(self):
        """
        Checks if the stepper is moving
        :return: True or False
        """
        return self.isBusy()

    def get_position(self):
        """
        Gets the position of the stepper in steps
        :return: position in steps
        """
        return self.getPosition()

    def get_position_in_units(self):
        """
        Gets the position of the stepper in units
        :return: position in units
        """
        return self.get_position() / self.steps_per_unit / self.micro_steps

    @staticmethod
    def free_all():
        """
        Free all of the instantiated stepper motors
        :return: None
        """
        for stp in stepper.instances:
            stp.free()

    def __repr__(self):
        """
        Returns string representation of the stepper object
        :return: "stepper on port" with the corresponding port number
        """
        return "stepper on port " + str(self.port)
