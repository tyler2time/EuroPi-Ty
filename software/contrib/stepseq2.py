
from time import sleep_ms
from europi import *
from machine import Timer
from europi_script import EuroPiScript

# Initialize step array
num_steps = 8
step_array = [0] * num_steps
current_step = 0
selected_step = 0
step_size = 1
divide = 0
gate_timer = Timer()


class StepSeq2(EuroPiScript):
    def __init__(self):
        super().__init__()
        
    # Define callback function for timer
    def trigger_gate(self):
        global current_step, step_array, cv1, cv2, cv3, gate_timer
        if step_array[current_step]:
            print('gate on')
            cv1.on()
            if current_step % 2:
                cv2.on()
            else:
                cv2.off()
            if current_step % 3:
                cv3.on()
            else:
                cv3.off()
        else:
            print('gate off')
            cv1.off()
            cv2.off()
            cv3.off()
    # Modify output function to use timer
    def output(self):
        global current_step, step_size, num_steps, gate_timer
        current_step += step_size
        if current_step >= num_steps:
            current_step = 0
        elif current_step < 0:
            current_step = num_steps - 1
        gate_timer.init(period=2, mode=Timer.PERIODIC, callback=self.trigger_gate)

    # Define oled display
    def oled_display(self):
        global current_step, step_array, selected_step, step_size, num_steps
        selected_step = k1.range(num_steps)
        self.k2_handler()
        oled.fill(0)
        selected_step_txt = selected_step + 1
        # Draw 8 steps
        for i in range(num_steps):
            step_x = i * 16
            step_y = 20
            if step_array[i] == 1:
                oled.fill_rect(step_x, step_y, 16, 8, 1)
            elif i == selected_step:
                oled.hline(step_x, step_y + 2, 16, 1)
            else:
                oled.rect(step_x, step_y, 16, 8, 1)
        # Draw current step
        current_step_x = current_step * 16
        current_step_y = 30
        oled.fill_rect(current_step_x, current_step_y, 16, 8, 1)
        oled.text("Nora", 0, 0)
        oled.hline(0, 10, 36, 1)
        oled.text("SelStep " + str(selected_step_txt), 40, 0)
        oled.text("StepSz " + str(step_size), 50, 10)
        oled.show()
    # Knob 2 will select the number of steps the sequencer will proceed forward or backward.  
    # 12 o'clock will be 1 step, 3 o'clock will be 2 steps and 9 o'clock will be 2 steps back
    #

    def k2_handler(self):
        global step_size, current_step, num_steps
        step_size = k2.choice([-3, -2, -1, 1, 2, 3])
        oled.fill(0)
        if current_step >= num_steps:
            current_step = 0
        elif current_step < 0:
            current_step = num_steps - 1


    # Define button handlers
    @b1.handler
    # Button 1 will enable the selected step
    def b1_handler():
        global step_array, selected_step
        if step_array[selected_step] == 1:
            step_array[selected_step] = 0
        else:
            step_array[selected_step] = 1

    @b2.handler
    def b2_handler():
        global step_array, current_step
        current_step = 0

    # Digital input will advance the step.  If the step is enabled, it will send a trigger
    @din.handler
    def din_handler(self):
        global current_step, step_array, gate_timer, divide
        if divide == 1:
            cv5.on()
            sleep_ms(20)
            cv5.off()
            divide = 0
        else:
            divide = 1  
        cv4.on()
        sleep_ms(20)
        cv4.off()
        self.k2_handler()
        self.output()
        #Main loop
    def main(self):
        while True:
            global num_steps, current_step, step_size
            
            step_size = 1
            self.oled_display()

if __name__ == "__main__":
    StepSeq2().main()

        




