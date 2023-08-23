from europi import *
from europi_script import EuroPiScript
import random
from time import sleep_ms

# Initialize the number of steps, repeats, and change
numSteps = 8
numRepeats = 16
numChange = 1

# Initialize the sequence and other variables
sequence = [1, 0, 0, 0, 1, 0, 0, 0] 
repeats = 0
changed = 0
currentStep = 0
currentChange = 0
currentRepeat = 0

drop_speed = 0
class GenSeq(EuroPiScript):
    def __init__(self):
        super().__init__()

    def oled_update(self):
        global sequence, repeats, changed, currentStep, currentChange, currentRepeat, numSteps, numRepeats, numChange, drop_speed
        self.handle_knobs()
        oled.fill(0)
        '''
        # Create Raindrop animation based on the differnt parameters
        total_drops = numSteps * numChange
        drop_spacing = 128 / total_drops
        drop_speed += 1
        if drop_speed > 32:
            drop_speed = 0
        drops = []
        for i in range(total_drops):
            # Create a random number from 1 to 5
            random_num = random.randint(1, 5)
            drops.append([int(i * drop_spacing), random_num, drop_speed])
        for drop in drops:
            drop[1] += drop[2]
            if drop[1] > 32:
                drop[1] = 0
            oled.pixel(int(drop[0]), int(drop[1]), 1)
            '''
        # Draw a cool animation based on the number of steps
        
        # Draw contents of sequence with rectangles at the bottom of the screen. 0 is black, 1 is white
        for i in range(numSteps):
            if sequence[i] == 0:
                if numSteps > 16:
                    oled.rect(i * 8, 28, 8, 4, 0)
                else:    
                    oled.rect(i * 16, 28, 16, 4, 0)
            else:
                if numSteps > 16:
                    oled.rect(i * 8, 28, 8, 4, 1)
                else:
                    oled.rect(i * 16, 28, 16, 4, 1)
        # List the number of steps, repeats, and changes
        oled.text("Steps" + str(currentRepeat) + "/" + str(numRepeats), 0, 0, 1)
        oled.text("Upcoming Changes" +str(numChange), 0, 10, 1)
        oled.show()
        print("OLED updated")

    def sequence_clear(self):
        global sequence, repeats, changed, currentStep, currentChange, currentRepeat, numSteps, numRepeats, numChange
        # clear all the steps and unpredictability values and counters to start fresh
        sequence = [0, 0, 0, 0, 0, 0, 0, 0]
        repeats = 0
        changed = 0
        currentStep = 0
        currentChange = 0
        currentRepeat = 0
        print("Sequence cleared")

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
        print("Sequence changed")

    def sequence_play(self):
        global sequence, repeats, changed, currentStep, currentChange, currentRepeat, numSteps, numRepeats, numChange, lockedSequence
        # if the current step is 1 then turn on the gate
        if sequence[currentStep] == 1:
            cv1.on()
            cv4.on()
            sleep_ms(40)
            cv1.off()
            cv4.off()
        # if the current step is 0 then play the off beat on cv2 and cv5
        else:
            cv2.on()
            cv5.on()
            sleep_ms(40)
            cv2.off()
            cv5.off()
        # Play the locked sequence if the current step is 1
        if lockedSequence[currentStep] == 1:
            cv3.on()
            cv6.on()
            sleep_ms(40)
            cv3.off()
            cv6.off()
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
        if currentRepeat > numRepeats:
            currentRepeat = 0
            self.sequence_change()
        # increment the number of repeats that have happened
        repeats += 1
        # if the number of repeats that have happened is equal to the number of repeats set by the user
        # then reset the number of repeats that have happened to 0
        if repeats > numRepeats:
            repeats = 0
        print("Sequence played")

    # Define a function to lock the sequence
    def sequence_lock(self):
        global sequence, repeats, changed, currentStep, currentChange, currentRepeat, numSteps, numRepeats, numChange, lockedSequence
        # copy current sequence to locked sequence
        lockedSequence = sequence

    def handle_knobs(self):
        global sequence, repeats, changed, currentStep, currentChange, currentRepeat, numSteps, numRepeats, numChange
        # use knob 2 to set the number of repeats before the sequence can change
        numRepeats = k1.choice([8, 16, 32, 64, 128, 256, 512])
        numChange = k2.choice([1, 2, 3, 4, 5, 6, 7, 8])

        print("Knobs handled")

    def main(self):
        global sequence, repeats, changed, currentStep, currentChange, currentRepeat, numSteps, numRepeats, numChange, lockedSequence
       
        # Play the sequence if a gate signal is received or button 1 is pressed
        @din.handler
        def on_gate():
            self.sequence_play()
            self.oled_update()
        @b1.handler
        def on_b1():
            self.sequence_lock()
        # Increase number of steps if b2 is pushed
        @b2.handler
        def num_steps_up():
            global numSteps, sequence
            numSteps += 1
            # Add a 0 to the sequence
            sequence.extend([0])
            if numSteps > 32:
                numSteps = 1
                sequence = [0]
            self.oled_update()
        print("Main loop started")

if __name__ == '__main__':
    GenSeq().main()


