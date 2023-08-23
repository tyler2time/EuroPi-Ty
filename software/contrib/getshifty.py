'''
This is an EuroPi script that acts as a sampling sequential shift register. On a trigger or gate it will sample ain
and output the value on cv1. The value will be shifted to cv2 on the next trigger or gate, and so on. when the shift
register is full, it will drop the oldest value and shift the rest of the values down.
'''

from europi import *
from europi_script import EuroPiScript
from time import sleep_ms

import random

try:
    # local dev
    from software.firmware.europi import (
        MAX_INPUT_VOLTAGE,
        OLED_HEIGHT,
        OLED_WIDTH,
        ain,
        b1,
        b2,
        cv1,
        cv2,
        cv4,
        din,
        k1,
        k2,
        oled,
    )
except ImportError:
    from europi import MAX_INPUT_VOLTAGE, OLED_HEIGHT, OLED_WIDTH, ain, b1, b2, cv1, cv2, cv4, din, k1, k2, oled

MAX_RATE = OLED_WIDTH
Y_TRUE = int(OLED_HEIGHT / 3 * 2)
Y_FALSE = int(OLED_HEIGHT / 3)
D_WAVE_HEIGHT = Y_TRUE - Y_FALSE + 1
RIGHT_EDGE = OLED_WIDTH - 1
Y_PIXELS = OLED_HEIGHT - 1

# Create a list to hold the values. To avoid errors we will populate the list with random values
values = [random.uniform(0, 1) for _ in range(6)]
# Create a variable to hold the current voltage
current_voltage = 0

offset = 0
scale = 1

flag = False

class GetShifty(EuroPiScript):
    def __init__(self):
        super().__init__()

    def oled_display(self):
        global current_voltage, values, offset, scale, old_value
        self.handle_knobs()
        oled.fill(0)       
        # Draw the current voltage
        location_y = 0
        location_x = 0
        oled.fill(0)
        y_value = 0
        for i in range(len(values)):
            location_y = 10
            y_value = (values[i] * 3)
            location_x = i * 18
            oled.fill_rect(location_x, location_y, 18, round(y_value), 1)
            oled.rect(location_x, location_y, 18, 32, 0)
        # Draw the current voltage
        oled.text(str(current_voltage), 0, 0, 1)
        # Draw the offset
        oled.text("O: " + str(offset), 40, 0, 1)
        # Draw the scale
        oled.text("Scl: " + str(scale), 80, 0, 1)

        oled.show()
    
  

    def handle_knobs(self):
        global current_voltage, values, offset, scale
        # Handle knob 1
        offset = k1.choice([-3, -2, -1, 0, 1, 2, 3])
        # Handle knob 2
        scale = k2.choice([0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2])

    def get_voltage(self):
        global current_voltage, values, offset, scale
        self.handle_knobs()
        current_voltage = ain.read_voltage()
        current_voltage = current_voltage + offset
        current_voltage = current_voltage * scale
        #current_voltage = current_voltage * scale
        # If the array is full, remove the oldest value
        if len(values) > 6:
            values.pop(0)
        # Add the current voltage to the array
        values.append(current_voltage)
        cv1.voltage(values[5])
        cv2.voltage(values[4])
        cv3.voltage(values[3])
        cv4.voltage(values[2])
        cv5.voltage(values[1])
        cv6.voltage(values[0])
        self.oled_display()


    def main(self):
        global current_voltage, values, old_value
        old_value = din.value()
        @din.handler
        def on_rising_clock():
            self.get_voltage()

        @b1.handler
        def on_b1_press():
            self.get_voltage()
        
        @b2.handler
        def on_b2_press():
            values = [0] * 6
            self.get_voltage()
        while True:
            self.oled_display()
            sleep_ms(10)
        

        #self.oled_display(current_voltage, values)
            


if __name__ == '__main__':
    GetShifty().main()



  
