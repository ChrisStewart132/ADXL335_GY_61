from machine import UART, Pin
import utime

class NEO7M:
    def __init__(self, uart_id=0, baudrate=9600, tx_pin=12, rx_pin=13):
        """
        Initialize the NEO-7M GPS module using UART.
        
        :param uart_id: UART ID (default is 0 for UART0)
        :param baudrate: Baud rate for communication (default is 9600)
        :param tx_pin: TX pin 
        :param rx_pin: RX pin 
        """
        self.uart = UART(uart_id, baudrate=baudrate, tx=Pin(tx_pin), rx=Pin(rx_pin))
        self.uart.init(baudrate=baudrate, bits=8, parity=None, stop=1)
        self.buffer = bytearray(255)
        self.latitude = None
        self.longitude = None
        self.satellites = None
        self.altitude = None
        self.speed = None
        self.course = None
        self.valid = False

    def read_data(self):
        """
        Read data from the GPS module and parse NMEA sentences.
        """
        if self.uart.any():
            self.buffer = self.uart.readline()
            try:
                #print(self.buffer)
                nmea_sentence = self.buffer.decode('utf-8').strip()
                if nmea_sentence.startswith('$GPGGA'):
                    self.parse_gpgga(nmea_sentence)
                elif nmea_sentence.startswith('$GPRMC'):
                    self.parse_gprmc(nmea_sentence)
            except UnicodeError:
                pass

    def parse_gpgga(self, sentence):
        """
        Parse the GPGGA NMEA sentence to extract latitude, longitude, altitude, and satellites.
        """
        parts = sentence.split(',')
        if len(parts) >= 10:
            try:
                self.latitude = self.convert_to_degrees(parts[2], parts[3])
                self.longitude = self.convert_to_degrees(parts[4], parts[5])
                self.altitude = float(parts[9])
                self.satellites = int(parts[7])
                self.valid = parts[6] != '0'
            except ValueError:
                pass

    def parse_gprmc(self, sentence):
        """
        Parse the GPRMC NMEA sentence to extract speed and course.
        """
        parts = sentence.split(',')
        if len(parts) >= 8:
            try:
                self.speed = float(parts[7]) * 1.852  # Convert knots to km/h
                self.course = float(parts[8])
            except ValueError:
                pass

    def convert_to_degrees(self, raw_value, direction):
        """
        Convert raw NMEA latitude/longitude values to degrees.
        """
        try:
            degrees = float(raw_value[:2]) + float(raw_value[2:]) / 60.0
            if direction in ['S', 'W']:
                degrees = -degrees
            return degrees
        except ValueError:
            return None

    def get_location(self):
        """
        Get the current location (latitude, longitude).
        """
        return self.latitude, self.longitude

    def get_altitude(self):
        """
        Get the current altitude.
        """
        return self.altitude

    def get_speed(self):
        """
        Get the current speed in km/h.
        """
        return self.speed

    def get_course(self):
        """
        Get the current course.
        """
        return self.course

    def get_satellites(self):
        """
        Get the number of satellites in view.
        """
        return self.satellites

    def is_valid(self):
        """
        Check if the GPS data is valid.
        """
        return self.valid


if __name__ == "__main__":
    # Example usage
    gps = NEO7M()

    while True:
        gps.read_data()
        if gps.is_valid():
            print("Latitude:", gps.get_location()[0])
            print("Longitude:", gps.get_location()[1])
            print("Altitude:", gps.get_altitude(), "m")
            print("Speed:", gps.get_speed(), "km/h")
            print("Course:", gps.get_course(), "degrees")
            print("Satellites:", gps.get_satellites())
        utime.sleep(1)
