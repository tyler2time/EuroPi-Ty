from europi import *
from europi_script import EuroPiScript
import random
from time import sleep_ms

# Set the minimum and maximum number of steps in the sequence
minSteps = 2
maxSteps = 16

# Set the minimum and maximum number of repeats before the sequence can change
minRepeats = 2
maxRepeats = 32

# Set the minimum and maximum number of steps that can change when the sequence changes
minChange = 1
maxChange = 4

# Initialize the number of steps, repeats, and change
numSteps = 8
numRepeats = 16
numChange = 1

# Initialize the sequence and populate it with 0s
sequence = [1, 0, 0, 0, 1, 0, 0, 0] 

# Initialize the number of repeats that have happened
repeats = 0

# Initialize the number of steps that have changed
changed = 0

# Initialize the current step
currentStep = 0

# Initialize the current change
currentChange = 0

# Initialize the current repeat
currentRepeat = 0

class GenerativeGate(EuroPiScript):
    def __init__(self):
        super().__init__()

    def oled_update(self):
        global sequence, repeats, changed, currentStep, currentChange, currentRepeat, numSteps, numRepeats, numChange
        oled.fill(0)
        # Create Raindrop animation based on the differnt parameters
        total_drops = numSteps * numChange
        drop_spacing = 128 / total_drops
        drop_speed = 3 - (numChange / 2)
        drops = []
        for i in range(total_drops):
            drops.append([int(i * drop_spacing), 0, drop_speed])
        for drop in drops:
            drop[1] += drop[2]
            if drop[1] > 63:
                drop[1] = 0
            oled.pixel(int(drop[0]), int(drop[1]), 1)
        oled.show()

    def sequence_clear(self):
        global sequence, repeats, changed, currentStep, currentChange, currentRepeat, numSteps, numRepeats, numChange
        # clear all the steps and unpredictability values and counters to start fresh
        sequence = [0, 0, 0, 0, 0, 0, 0, 0]
        repeats = 0
        changed = 0
        currentStep = 0
        currentChange = 0
        currentRepeat = 0
    '''
    def sequence_select(self):
        global sequence, repeats, changed, currentStep, currentChange, currentRepeat, numSteps, numRepeats, numChange
        # use knob 1 to select the preset sequence
        sel_preset = k2.choice(['1', '2', '3', '4', '5', '6', '7', '8'])
        if sel_preset == '1':
            sequence = [1, 0, 1, 0, 1, 0, 1, 0]
        elif sel_preset == '2':
            sequence = [1, 0, 0, 0, 1, 0, 0, 0]
        elif sel_preset == '3':
            sequence = [0, 1, 0, 1, 0, 1, 0, 1]
        elif sel_preset == '4':
            sequence = [0, 1, 1, 1, 0, 1, 1, 1]
        elif sel_preset == '5':
            sequence = [1, 1, 1, 1, 1, 1, 1, 1]
        elif sel_preset == '6':
            sequence = [0, 0, 0, 0, 0, 0, 0, 0]
        elif sel_preset == '7':
            sequence = [1, 1, 0, 0, 1, 1, 0, 0]
        elif sel_preset == '8':
            sequence = [0, 0, 1, 1, 0, 0, 1, 1]
    '''
    def sequence_change(self):
        global sequence, repeats, changed, currentStep, currentChange, currentRepeat, numSteps, numRepeats, numChange
        # change the sequence by the number of steps set by the user
        for i in range(numChange):
            # choose a random step to change
            changeStep = random.randint(0, numSteps - 1)
            # change the step to the opposite of what it was
            if sequence[changeStep] == 0:
                sequence[changeStep] = 1
            else:
                sequence[changeStep] = 0
            # increment the number of steps that have changed
            changed += 1
            # if the number of steps that have changed is equal to the number of steps in the sequence
            # then reset the number of steps that have changed to 0
            if changed == numSteps:
                changed = 0
            

    def sequence_play(self):
        global sequence, repeats, changed, currentStep, currentChange, currentRepeat, numSteps, numRepeats, numChange
        # if the current step is 1 then turn on the gate
        if sequence[currentStep] == 1:
            cv1.on()
            cv4.on()
            sleep_ms(40)
            cv1.off()
            cv4.off()
        # if the current step is 0 then turn off the gate
        else:
            cv2.on()
            cv5.on()
            sleep_ms(40)
            cv2.off()
            cv5.off()
        # give a random value to cv3 and cv6
        cv3.value(random.randint(0, 10))
        cv6.value(random.randint(0, 10))
        # increment the current step
        currentStep += 1
        # if the current step is goes beyond the number of steps in the sequence
        # then reset the current step to 0 and increment the current change
        if currentStep == numSteps:
            currentStep = 0
        # increment the current repeat
        currentRepeat += 1
        # if the current repeat is equal to the number of repeats set by the user
        # then reset the current repeat to 0 and change the sequence
        if currentRepeat == numRepeats:
            currentRepeat = 0
            self.sequence_change()
        # increment the number of repeats that have happened
        repeats += 1
        # if the number of repeats that have happened is equal to the number of repeats set by the user
        # then reset the number of repeats that have happened to 0
        if repeats == numRepeats:
            repeats = 0
    

    def handle_knobs(self):
        global sequence, repeats, changed, currentStep, currentChange, currentRepeat, numSteps, numRepeats, numChange
        # use knob 2 to set the number of repeats before the sequence can change
        numRepeats = k1.choice([32, 64, 128, 256, 512])
        numChange = k2.choice([1, 2, 3, 4, 5, 6, 7, 8])
        self.oled_update()
        
    def main(self):
        global sequence, repeats, changed, currentStep, currentChange, currentRepeat, numSteps, numRepeats, numChange
        # Reset the sequence if button 2 is pressed
        @b2.handler
        def on_press():
            self.sequence_clear()
            self.oled_update()

        # Check the knobs and buttons
        self.handle_knobs()
        
        @din.handler
        def on_gate():
            self.sequence_play()
            self.oled_update()
        @b1.handler
        def on_b1():
            self.sequence_play()
            self.oled_update()
        
        


if __name__ == '__main__':
    GenerativeGate().main()



