'''
This is an EuroPi script that acts as a sampling sequential shift register. On a trigger or gate it will sample ain
and output the value on cv1. The value will be shifted to cv2 on the next trigger or gate, and so on. when the shift
register is full, it will drop the oldest value and shift the rest of the values down.
'''

from europi import *
from europi_script import EuroPiScript

import random

# Create a list to hold the values. To avoid errors we will populate the list with random values
values = [random.uniform(0, 1) for _ in range(6)]
# Create a variable to hold the current voltage
current_voltage = 0

flag = False

class GetShifty(EuroPiScript):
    def __init__(self):
        super().__init__()

    def oled_display(self):
        global current_voltage, values
        location_y = 0
        location_x = 0
        oled.fill(0)
        for i in range(len(values)):
            location_x += 15
            location_y = 16
            if location_x > 128:
                location_x = 15

            shape_size = int(values[i] * 5 + 3)
            for x in range(location_x - shape_size//2, location_x + shape_size//2):
                for y in range(location_y - shape_size//2, location_y + shape_size//2):
                    if (x - location_x)**2 + (y - location_y)**2 <= (shape_size//2)**2:
                        oled.pixel(x, y, 1)
        oled.show()
    
        '''     
        def oled_display(self, current_voltage, values):
        location_y = 0
        location_x = 0
        oled.fill(0)
        for i in range(len(values)):
            location_x += 15
            if location_x > 128:
                location_x = 15
                location_y += 15
            shape_size = int(values[i] * 5)
            if i == 0:
                oled.rect(location_x, location_y, shape_size, 24, 1)
            elif i == 1:
                oled.rect(location_x, location_y, shape_size, 24, 1)
            elif i == 2:
                oled.rect(location_x, location_y, shape_size, 24, 1)
            elif i == 3:
                oled.rect(location_x, location_y, shape_size, 24, 1)
            elif i == 4:
                oled.rect(location_x, location_y, shape_size, 24, 1)
            elif i == 5:
                oled.rect(location_x, location_y, shape_size, 24, 1)
        oled.show()
        '''
        
    def get_voltage(self):
        global current_voltage, values
        current_voltage = ain.read_voltage()
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
        global current_voltage, values
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
        

        #self.oled_display(current_voltage, values)
            


if __name__ == '__main__':
    GetShifty().main()
