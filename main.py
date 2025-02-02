import time
from accelerometer import AccelerometerGY61
from servo import SG90Servo

def main():

    acc = AccelerometerGY61()
    
    # alpha (0-1, lower for more smoothness), buffer_size (1-inf, lower for responsiveness, higher for less noise/bad inputs)
    alpha, buffer_size = 0.4, 5

    right_aileron = SG90Servo(14, alpha=alpha, buffer_size=buffer_size)
    left_aileron = SG90Servo(15, alpha=alpha, buffer_size=buffer_size) 
    right_aileron.set_angle(90)
    left_aileron.set_angle(90)

    while True: 
        x_val, y_val, z_val, x_acc, y_acc, z_acc, roll, pitch, up_x, up_y, up_z = acc.read_acceleration()
        #print(acc)

        # roll trim
        roll += 1
        
        print(roll)
        
        # calculate a roll angle amplitude using a quadratic amplitude = a.roll + b.roll**2
        amplitude = abs(roll) + roll*roll/10
        
        # clamp amplitude
        amplitude = min(amplitude, 90)
        
        
        aileron = (amplitude*-1)+90 if roll > 0 else amplitude+90
        right_aileron.set_angle(aileron)
        left_aileron.set_angle(aileron)

        time.sleep(0.02)

main()


