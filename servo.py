from machine import Pin, PWM
from time import sleep
from filter import MedianFilter, EMAFilter, FilterPipeline

class SG90Servo:
    def __init__(self, pin, min_duty=2200, max_duty=7200, freq=50, alpha=0.5, buffer_size=6):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(freq)
        self.min_duty = min_duty
        self.max_duty = max_duty
        self.current_duty = min_duty
        self.pwm.duty_u16(self.current_duty)
        
        # Initialize Filter Pipeline
        self.filter_pipeline = FilterPipeline(buffer_size, [MedianFilter(), EMAFilter(alpha)])

    def set_angle(self, angle):
        angle = max(0, min(180, angle))  # Clamp angle between 0 and 180
        self.filter_pipeline.add_value(angle)
        filtered_angle = self.filter_pipeline.get_filtered_value()
        
        duty = int(self.min_duty + (self.max_duty - self.min_duty) * (filtered_angle / 180))
        self.current_duty = duty
        self.pwm.duty_u16(duty)

    def deinit(self):
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