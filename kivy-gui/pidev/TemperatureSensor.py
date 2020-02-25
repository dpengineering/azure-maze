import sys
try:
    import smbus
except ImportError:
    sys.exit("Install smbus with sudo apt-get install python3-smbus")


class TemperatureSensor:
    """
    Class to interact with the add on temperature sensor on the Slush Engine
    """

    def __init__(self):
        """
        Constructs a new temperature sensor Object
        """
        self.bus = smbus.SMBus(1)
        self.config = [0x00, 0x00]
        self.bus.write_i2c_block_data(0x18, 0x01, self.config)
        self.bus.write_byte_data(0x18, 0x08, 0x03)
        self.data = self.bus.read_i2c_block_data(0x18, 0x05, 2)

    def update_data(self):
        """
        Update the current data read off the temperature sensor
        :return: None
        """
        self.data = self.bus.read_i2c_block_data(0x18, 0x05, 2)

    def get_temperature_in_fahrenheit(self):
        """
        Get the current temperature in Fahrenheit
        :return: Current temperature in Fahrenheit (Float)
        """
        self.update_data()
        ftemp = ((self.data[0] & 0x1F) * 256) + self.data[1]
        
        if ftemp > 4095:
            ftemp -= 8192
        
        return ftemp * 0.0625 * 1.8 + 32

    def get_temperature_in_celsius(self):
        """
        Get the current temperature in Celsius
        :return: Current temperature in Celsius (Float)
        """
        self.update_data()
        ctemp = ((self.data[0] & 0x1F) * 256) + self.data[1]
        
        if ctemp > 4095 :
            ctemp -= 8192
        
        return ctemp * 0.0625
