from machine import Pin, PWM
from time import sleep

class LowPassFilter:
    def __init__(self, alpha):
        """
        Initialize the low-pass filter.
        
        :param alpha: Smoothing factor (0 < alpha < 1). Smaller values = more smoothing.
        """
        self.alpha = alpha
        self.filtered_value = None

    def update(self, new_value):
        """
        Update the filter with a new value.
        
        :param new_value: The new raw input value.
        :return: The filtered value.
        """
        if self.filtered_value is None:
            self.filtered_value = new_value  # Initialize on first run
        else:
            # Apply the low-pass filter formula
            self.filtered_value = self.alpha * new_value + (1 - self.alpha) * self.filtered_value
        return self.filtered_value

class SG90Servo:
    def __init__(self, pin, min_duty=2500, max_duty=7500, freq=50, alpha=0.5):
        """
        Initialize the SG90 servo motor.
        
        :param pin: The GPIO pin connected to the servo signal line.
        :param min_duty: The minimum duty cycle for the servo (default is 2500 for 0 degrees).
        :param max_duty: The maximum duty cycle for the servo (default is 7500 for 180 degrees).
        :param freq: The frequency of the PWM signal (default is 50 Hz).
        :param alpha: Smoothing factor for the low-pass filter (default is 0.2).
        """
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(freq)
        self.min_duty = min_duty
        self.max_duty = max_duty
        self.current_duty = min_duty
        self.pwm.duty_u16(self.current_duty)
        
        # Initialize the low-pass filter
        self.filter = LowPassFilter(alpha)
        self.filtered_angle = None

    def set_angle(self, angle):
        """
        Set the servo to a specific angle.
        
        :param angle: The desired angle (0 to 180 degrees).
        """
        if angle < 0:
            angle = 0
        elif angle > 180:
            angle = 180
        
        # Apply low-pass filtering to the angle
        self.filtered_angle = self.filter.update(angle)
        
        # Map the filtered angle to the duty cycle range
        duty = int(self.min_duty + (self.max_duty - self.min_duty) * (self.filtered_angle / 180))
        self.current_duty = duty
        self.pwm.duty_u16(duty)

    def deinit(self):
        """
        Deinitialize the PWM signal and release the pin.
        """
        self.pwm.deinit()


if __name__ == "__main__":
    # Example usage
    servo = SG90Servo(15, alpha=0.5)  # Assuming the servo signal is connected to GPIO 15

    try:
        while True:
            print("Setting servo to 0 degrees")
            servo.set_angle(0)  # Move servo to 0 degrees
            sleep(1)

            print("Setting servo to 90 degrees")
            servo.set_angle(90)  # Move servo to 90 degrees
            sleep(1)

            print("Setting servo to 180 degrees")
            servo.set_angle(180)  # Move servo to 180 degrees
            sleep(1)

    except KeyboardInterrupt:
        print("Stopping servo and cleaning up...")
        servo.deinit()  # Release the servo