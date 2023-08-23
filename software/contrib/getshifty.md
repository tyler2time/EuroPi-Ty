**EuroPi - Get Shifty**

Get Shifty is a simple shift register that samples the input voltage on a gate or trigger and shifts previous values through the CV outputs.  
This functionality can be achieved through other scripts and patching but I wanted a simple sampling shift register with that functionality from the get go.
The incoming voltages can be scaled an offset. 0 to 10 volts are the minimum and maximum.

AIN: Input voltage to be sampled
DIN: Trigger or gate here will sample the voltage and output value to CV1 and shift previous voltage to CV2-CV6
Knob 1: Offset(-3 to +3)
Knob 2: Scale(.25 to 2)
Button 1: Same function as DIN
Button 2: Will clear register and sample AIN
CV1-CV6: Sampled voltages
