[![Finite State Machine in Manim]([https://img.youtube.com/vi/YOUTUBE_VIDEO_ID_HERE/0](https://www.youtube.com/watch?v=Lfq6XD3-aUw).jpg)]([https://www.youtube.com/watch?v=YOUTUBE_VIDEO_ID_HER](https://www.youtube.com/watch?v=Lfq6XD3-aUw)E)


Notes
=====
The manim-automata plugin currently relies on JFLAP files, future updates will enable the user to create automata without JFLAP.
[JFLAP](https://www.jflap.org) is software for experimenting with formal languages topics.

Installation
============
To install manim-automata plugin run:

   pip install manim-automata

To see which version of manim-automata you have:

    manim-automata

or

    pip list


Importing
=========
To use manim-automata in your project, you can:

* Add ``from manim_automata import *`` to your script.
Once manim-automata has been imported, you can use the ManimAutomata class to create automata.

How To Use
==========





Example
=======
```python
class Automaton(MovingCameraScene):
    def construct(self):
        manim_automaton = ManimAutomaton(xml_file='example_machine.jff')

        #Adjust camera frame to fit ManimAutomaton in scene
        self.camera.frame.set_width(manim_automaton.width + 10)
        self.camera.frame.set_height(manim_automaton.height + 10)
        self.camera.frame.move_to(manim_automaton)

        #Create an mobject version of input for the manim_automaton
        automaton_input = manim_automaton.construct_automaton_input("110011")

        #Position automaton_input on the screen.
        automaton_input.shift(LEFT * 2)
        automaton_input.shift(UP * 10)

        self.play(
                DrawBorderThenFill(manim_automaton),
                FadeIn(automaton_input)
            )

        #Play all the animations generate from .play_string()
        for sequence in manim_automaton.play_string(automaton_input):
            for step in sequence:
                self.play(step, run_time=1)
               
```
To run the code and generate the video, run:
   manim -pqh <name_of_script.py> Automaton plugins = manim_automata

XML file used:
```
<?xml version="1.0" encoding="UTF-8" standalone="no"?><!--Created with JFLAP 7.1.--><structure>
	<type>fa</type>
	<automaton>
		<!--The list of states.-->
		<state id="0" name="q0">
			<x>40.0</x>
			<y>53.0</y>
			<initial/>
		</state>
		<state id="1" name="q1">
			<x>484.0</x>
			<y>39.0</y>
			<final/>
		</state>
		<state id="2" name="q2">
			<x>138.0</x>
			<y>130.0</y>
		</state>
		<state id="3" name="q3">
			<x>205.0</x>
			<y>186.0</y>
		</state>
		<state id="4" name="q4">
			<x>142.0</x>
			<y>239.0</y>
			<final/>
		</state>
		<state id="5" name="q5">
			<x>236.0</x>
			<y>120.0</y>
		</state>
		<state id="6" name="q6">
			<x>343.0</x>
			<y>178.0</y>
			<final/>
		</state>
		<state id="7" name="q7">
			<x>379.0</x>
			<y>101.0</y>
			<final/>
		</state>
		<!--The list of transitions.-->
		<transition>
			<from>0</from>
			<to>0</to>
			<read>0</read>
		</transition>
		<transition>
			<from>5</from>
			<to>7</to>
			<read>0</read>
		</transition>
		<transition>
			<from>0</from>
			<to>2</to>
			<read>1</read>
		</transition>
		<transition>
			<from>1</from>
			<to>0</to>
			<read>0,1</read>
		</transition>
		<transition>
			<from>6</from>
			<to>7</to>
			<read>0</read>
		</transition>
		<transition>
			<from>5</from>
			<to>6</to>
			<read>1</read>
		</transition>
		<transition>
			<from>3</from>
			<to>4</to>
			<read>0</read>
		</transition>
		<transition>
			<from>3</from>
			<to>4</to>
			<read>1</read>
		</transition>
		<transition>
			<from>2</from>
			<to>3</to>
			<read>0</read>
		</transition>
		<transition>
			<from>4</from>
			<to>2</to>
			<read>1</read>
		</transition>
		<transition>
			<from>4</from>
			<to>0</to>
			<read>0</read>
		</transition>
		<transition>
			<from>7</from>
			<to>1</to>
			<read>0,1</read>
		</transition>
		<transition>
			<from>2</from>
			<to>5</to>
			<read>1</read>
		</transition>
		<transition>
			<from>5</from>
			<to>5</to>
			<read>1</read>
		</transition>
	</automaton>
</structure>
```

