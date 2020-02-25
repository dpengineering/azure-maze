"""
@file LidarSensor.py file containing class to easily interact with Lidar Sensor while using the i2c multiplexer
"""

import adafruit_vl6180x
import board
import busio
from smbus import SMBus as Bus


class LidarSensor:
    """
    Class to interact with Lidar Sensors, specifically while using the i2c multiplexer
    """

    def __init__(self, port, threshold=25, address_offset=0b000, address_default=0x70):
        """
        Initialize a Lidar Sensor
        :param port: Port the lidar sensor is connected to on the i2c multiplexer
        :param threshold: Threshold distance, object is considered to be detected if distance is less
        than or equal to the threshold distance
        :param address_offset: i2c address offset, defaults to 0b000
        :param address_default: i2c address default of the i2c multiplexer, defaults to 0x70
        """
        self.port = port
        self.threshold = threshold
        self.delay_time = 0.001
        self.address = address_offset + address_default
        self.detected = False
        self.last_read = self.threshold + 10

        self.i2c_smbus = Bus(1)
        self.port_select(port=self.port)
        self.i2c_circuit_python = busio.I2C(board.SCL, board.SDA)  # creates circuit python i2c instance
        self.sensor = adafruit_vl6180x.VL6180X(self.i2c_circuit_python)  # creates sensor instance on circuit python i2c

    def port_select(self, port):
        """
        Writes a bit in the position given by the port to the multiplexer control register
        :param port: Port on multiplexer to talk to
        :return: None
        """
        self.i2c_smbus.write_byte(self.address, 1 << port)

    def distance(self):
        """
        Get the current distance from the lidar sensor and store this value as last_read
        :rtype: int
        :return: Range read from the sensor
        """
        self.port_select(port=self.port)
        self.last_read = self.sensor.range
        self.detected_object()

        return self.last_read

    def detected_object(self):
        """
        Check if the distance sensed by the sensor is less than or equal to the threshold.
        Note this makes use of the last read field which is updated by distance.
        :rtype: bool
        :return: True if the distance is less than or equal to the threshold distance
        """
        # TODO simplify logic statements
        if self.detected:  # if previously detected return True
            return True
        elif self.last_read <= self.threshold:
            self.detected = True
            return True
        else:
            return False

    def reset(self):
        """
        Reset the sensors detected status and last_read
        :return: None
        """
        self.detected = False
        self.last_read = self.threshold + 10  # Set last read to be over threshold

    def refresh_last_read(self):
        """
        Refresh the sensors reading by simply calling distance()
        :return: None
        """
        self.distance()
