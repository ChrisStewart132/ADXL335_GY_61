from machine import ADC, Pin, SPI
import time
import math

from accelerometer import AccelerometerGY61
from nokia5110 import Nokia5110
from neo7m import NEO7M
from servo import SG90Servo

def main():
    spi = SPI(0, baudrate=1000000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3))  
    dc = 19  # Data/Command pin
    rst = 18  # Reset pin
    cs = 20  # Chip Select pin
    lcd = Nokia5110(spi, dc, rst, cs)
    lcd.clear()

    acc = AccelerometerGY61()
    gps = NEO7M()
    right_aileron = SG90Servo(14)
    left_aileron = SG90Servo(15) 
    right_aileron.set_angle(90)
    left_aileron.set_angle(90)

    tick = 0
    while True: 
        x_val, y_val, z_val, x_acc, y_acc, z_acc, roll, pitch, up_x, up_y, up_z = acc.read_acceleration()
        #print(acc)
        
        aileron = (-roll*2)+60
        right_aileron.set_angle(aileron)
        left_aileron.set_angle(aileron)
        
        gps.read_data()
        if gps.is_valid():
            print("Latitude:", gps.get_location()[0])
            print("Longitude:", gps.get_location()[1])
            print("Altitude:", gps.get_altitude(), "m")
            print("Speed:", gps.get_speed(), "km/h")
            print("Course:", gps.get_course(), "degrees")
            print("Satellites:", gps.get_satellites())
            
        try:
            lcd.clear()
            lcd.write_text_at_position(f"tick: {tick}", 0, 0)
            lcd.write_text_at_position(f"Roll: {roll:.2f}°", 0, 1)
            lcd.write_text_at_position(f"Pitch: {pitch:.2f}°", 0, 2)
        except Exception as e:
            print(e)  
        tick += 1
        
        time.sleep(0.05)
try:
    main()
except:
    right_aileron.set_angle(90)
    left_aileron.set_angle(90)