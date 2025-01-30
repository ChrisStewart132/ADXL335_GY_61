from machine import ADC, Pin
import time
import math

class AccelerometerGY61:
    def __init__(self, pin_x=26, pin_y=27, pin_z=28):
        self.adc_x = ADC(Pin(pin_x))  # GP26 -> X axis
        self.adc_y = ADC(Pin(pin_y))  # GP27 -> Y axis
        self.adc_z = ADC(Pin(pin_z))  # GP28 -> Z axis

        self.ADC_MAX = 65535  # Maximum ADC value (16-bit)
        self.VREF = 3.3       # Reference voltage
        self.ZERO_G_VOLTAGE = 1.65  # Voltage at 0g (assuming 3.3V supply)
        self.SENSITIVITY = 0.33  # Sensitivity in V/g (typical for GY-61)

    # Function to convert ADC value to acceleration in g
    def adc_to_g(self, adc_value):
        voltage = (adc_value / self.ADC_MAX) * self.VREF
        acceleration = (voltage - self.ZERO_G_VOLTAGE) / self.SENSITIVITY
        return acceleration

    # Function to calculate orientation (roll and pitch) in degrees
    def calculate_orientation(self, x, y, z):
        roll = math.atan2(y, math.sqrt(x * x + z * z)) * (180 / math.pi)
        pitch = math.atan2(x, math.sqrt(y * y + z * z)) * (180 / math.pi)
        return roll, pitch

    # Function to normalize the XYZ acceleration values
    def normalize_vector(self, x, y, z):
        magnitude = math.sqrt(x * x + y * y + z * z)
        if magnitude == 0:
            return 0, 0, 0  # Avoid division by zero
        return x / magnitude, y / magnitude, z / magnitude

    # Method to read and return accelerometer data
    def read_acceleration(self):
        x_value = self.adc_x.read_u16()
        y_value = self.adc_y.read_u16()
        z_value = self.adc_z.read_u16()

        x_accel = self.adc_to_g(x_value)
        y_accel = self.adc_to_g(y_value)
        z_accel = self.adc_to_g(z_value)

        roll, pitch = self.calculate_orientation(x_accel, y_accel, z_accel)

        up_x, up_y, up_z = self.normalize_vector(x_accel, y_accel, z_accel)

        return x_value, y_value, z_value, x_accel, y_accel, z_accel, roll, pitch, up_x, up_y, up_z
    
    def __str__(self):
        x_val, y_val, z_val, x_acc, y_acc, z_acc, roll, pitch, up_x, up_y, up_z = self.read_acceleration()
        return (f"X: {x_val} (Accel: {x_acc:.2f} g)")+(f"Y: {y_val} (Accel: {y_acc:.2f} g)")\
               +(f"\nZ: {z_val} (Accel: {z_acc:.2f} g)")\
               +(f"\nRoll: {roll:.2f}°, Pitch: {pitch:.2f}°")\
               +(f"\nUp Vector: ({up_x:.2f}, {up_y:.2f}, {up_z:.2f})")\
                +("\n-----------------------------")


# Example usage:
if __name__ == "__main__":
    accelerometer = AccelerometerGY61()

    while True:
        x_val, y_val, z_val, x_acc, y_acc, z_acc, roll, pitch, up_x, up_y, up_z = accelerometer.read_acceleration()
        print(accelerometer)

        time.sleep(0.05)
