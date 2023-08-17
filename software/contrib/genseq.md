# EuroPi GenSeq - A Somewhat Generative Gate\Trigger Sequencer

author: Tyler Relyt (github.com/tyler2time)

date: 2023-08-17

labels: sequencer, gates, triggers, randomness, generative

**Work in Progress**

GenSeq is a simple generative trigger sequencer that has some randomness to it and 
probability is controlled by parameters chosen by user. I love adding randomness and unpredictability 
to my patches but I often find the randomness comes in or changes at inopportune times (it's called random for a reason!).
Some modules get around this by adding a looping or locking mechanism to the randomness but I also wanted a way to be able to tell the
randomness when to come in. There are ways to patch this functionality but I wanted a sequencer that I could "schedule" the randomness.

To achieve this GenSeq has a Repeats parameter. Since music is structured into beats and bars this is a pretty easy task to calculate.
GenSeg counts the number of times it receives a clock sig (or other gate\cv on DIN) and does not change the sequence until the number of Repeats
that are set are hit. The options for repeats are 4, 8, 16, 32, 64, 128, 256. In a 4/4 time signature this would translate to 1 bar, 2 bars, 4 bars, 8 bars etc.
Once the number of Repeats is met GenSeq will flip a random step (or steps) from the current sequence.

I also wanted to be able to control the amount of randomness that is applied so gave it a Change parameter.  This parameter will tell GenSeq how
many steps to change when the number of Repeats is met. This is currently set to 1 to 8. If set to 1, GenSeq will flip 1 step at random. If set to 8, it will flip all steps.

Note: I know there are some "random" purest out there that would argue this is not random at all and I totally agree with you.

**To-do:**  
-  The display animation is not finished and I may need to rethink my initial idea and stick to something simpler.
-  Add a Freshness or Age parameter\attribute, where a step is more likely to change the older it is.
-  A Chaos parameter in which some steps are flipped outside of the Repeats threshhold.
-  Make the number of steps in the sequence configurable.
-  Add preset sequences or ability to program initial sequence.  Right now; initial sequence is set to random and when reset (Button2) is
pushed it starts with empty sequence.
-  Add functionality to AIN 



Credits:
- The Europi hardware and firmware was designed by Allen Synthesis:
https://github.com/Allen-Synthesis/EuroPi
- This code is heavily inspired by all the other contributors to the EuroPi platform. Thank you to all of you!

# Controls

- digital_in: Clock\Trigger in
- analog_in: Mode 1: TBD

- knob_1: Select the number of repeats threshhold.
- knob_2: Select the number of steps to flip.

- button_1: Send a trigger to advance sequence.  This was mainly set for testing purposes and will re-assign later.
- button_2: Resets all parameters and sequence to 0.  Again, mainly used for testing and will change later.

- output_1: Gate signal from active\on steps in sequence 
- output_2: Gate signal from inactive steps.
- output_3: Random voltage 0-10 Volts
- output_4: Gate signal from active\on steps in sequence 
- output_5: Gate signal from inactive steps.
- output_6: Random voltage 0-10 Volts



# Known bugs / Interesting features
In some situations, when the Repeats, Change and active steps are just right, the sequence will get stuck and will not change no matter what the parameters
are set to.  Reset will also not work.  I believe it is getting stuck in a for loop.  Need to add some type of logic to prevent this.
