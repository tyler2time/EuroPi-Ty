from time import sleep_ms
from europi import *
from machine import Timer
from europi_script import EuroPiScript


num_steps = 8

class StepSeq(EuroPiScript):
    def __init__(self):
        super().__init__()
        # Initialize step array
        global num_steps
        self.step_array = [0] * num_steps
        self.current_step = 0
        self.selected_step = 0
        self.step_size = 1
        self.divide = 0
        self.gate_timer = machine.Timer()
        #even_cvs = [cv2, cv4, cv6]
        #odd_cvs = [cv1, cv3, cv5]
        # Initialize step array
        self.step_array = [0] * num_steps
        print("StepSeq initialized")

    # Define callback function for timer
    def trigger_gate(self, current_step, step_array, cv1, cv2, cv3, gate_timer):
        print('triggering gate')
        if step_array[self.current_step]:
            print('gate on')
            cv1.on()
            if self.current_step % 2:
                cv2.on()
            else:
                cv2.off()
            if self.current_step % 3:
                cv3.on()
            else:
                cv3.off()
        else:
            print('gate off')
            cv1.off()
            cv2.off()
            cv3.off()

    # Modify output function to use timer
    def output(self, step_size, gate_timer):
        global num_steps, current_step #, step_size, StepSeq.num_steps, gate_timer
        self.current_step += step_size
        print('current_step: ', self.current_step)
        print('num_steps: ', num_steps)
        if self.current_step >= num_steps:
            self.current_step = 0
        elif self.current_step < 0:
            self.current_step = num_steps - 1
        print('current_step: ', self.current_step)
        gate_timer.init(period=2, mode=Timer.PERIODIC, callback=self.trigger_gate)

    # Define oled display
    def oled_display(self, current_step, step_size):
        global num_steps
        selected_step = k1.range(num_steps)
        # Draw step array on OLED display
        oled.fill(0)
        selected_step_txt = selected_step + 1
        print("Step: " + str(self.current_step))
        print("Sel_Step: " + str(selected_step))
        print("StepSz: " + str(step_size))
        for i in range(num_steps):
            if i == self.current_step:
                oled.rect(i*16, 20, 20, 8, 1)
            elif self.step_array[i]:
                oled.fill_rect(i*16, 20, 16, 8, 1)
            elif i == selected_step:
                oled.hline(i*16, 30, 16, 1)
            else:
                oled.rect(i*16, 20, 18, 8, 1)
        oled.text("Nora", 0, 0)
        oled.hline(0, 10, 36, 1)
        oled.text("SelStep " + str(selected_step_txt), 40, 0)
        oled.text("StepSz " + str(step_size), 50, 10)
            #oled.text("Sequencer")

        oled.show()
        '''
        for i in range(num_steps):
            if step_array[i]:
                cv1.on()
                sleep_ms(30)
                cv1.off()
            else:
                pass
        
        time.sleep_ms(30)
        '''
    # Define Knob handlers
    #def k1_handler():

    # Knob 2 will select the number of steps the sequencer will proceed forward or backward.  
    # 12 o'clock will be 1 step, 3 o'clock will be 2 steps and 9 o'clock will be 2 steps back
    #

    def k2_handler(self, oled_display, current_step, step_size):
        global num_steps
        self.step_size = k2.choice([-3, -2, -1, 1, 2, 3])
        print("current_step: {}".format(current_step))
        print("step_size: {}".format(step_size))
        oled.fill(0)
        if self.current_step >= num_steps:
            self.current_step = 0
        elif self.current_step < 0:
            self.current_step = num_steps - 1
        oled_display(self.current_step, self.step_size)

    # Define button handlers
    @b1.handler
    # Button 1 will enable the selected step
    def b1_handler(self, step_array, selected_step, oled_display):
        if step_array[selected_step]:
            step_array[selected_step] = 0
        else:
            step_array[selected_step] = 1
        oled_display(current_step, step_size)
        print("Step: " + str(selected_step))
        print("Value: " + str(step_array[selected_step]))

    @b2.handler
    def b2_handler(self):
        self.current_step = 0
        print("Step: " + str(self.current_step))


    # Digital input will advance the step.  If the step is enabled, it will send a trigger
    @din.handler
    def din_handler(self, divide, cv4, cv5, k2_handler, output):
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
        k2_handler()
        output()
        print("DIN handler")

        
    #Main loop
    def main(self):
        while True:
            global num_steps
            current_step = 0
            step_size = 1
            print("current step: " + str(current_step))
            print("step size: " + str(step_size))
            self.oled_display(current_step, step_size)
        
if __name__ == "__main__":
    StepSeq().main()
    



