from manim import *
from src.manim_automata.mobjects import *
from src.manim_automata.mobjects.automaton_mobject import ManimAutomaton



automaton_json = {
    'structure': {
        'type': 'fa',
        'automaton': {
            'state': [
                {'@id': '0', '@name': 'q0', 'x': '84.0', 'y': '122.0', 'initial': None},
                {'@id': '1', '@name': 'q1', 'x': '218.0', 'y': '175.0'},
                {'@id': '2', '@name': 'q2', 'x': '386.0', 'y': '131.0', 'final': None},
                {'@id': '3', '@name': 'q3', 'x': '227.0', 'y': '36.0'}
            ],
            'transition': [
                {'from': '0', 'to': '1', 'read': '0'},
                {'from': '0', 'to': '1', 'read': '1'},
                {'from': '2', 'to': '3', 'read': '0'},
                {'from': '1', 'to': '2', 'read': '1'},
                {'from': '3', 'to': '0', 'read': '1'},
                {'from': '3', 'to': '0', 'read': '0'}
            ]
        }
    }
}


class Automata(MovingCameraScene):
    
    def construct(self):
        manim_automaton = ManimAutomaton(automata_templete=automaton_json, xml_file='testmachine2.jff', camera_follow=True)

         #creates a frame around manim-automaton
        self.camera.frame.set_width(manim_automaton.width + 2)
        self.camera.frame.set_height(manim_automaton.height + 10)
        self.camera.frame.move_to(manim_automaton)

        self.play(DrawBorderThenFill(manim_automaton))

        input_string = "11"
        # input_string = {
        #     "input": "11",
        #     "x": 0,
        #     "y": 0
        # }

        automaton_input = manim_automaton.construct_automaton_input(input_string)

        for sequence in manim_automaton.play_string(automaton_input):
            for step in sequence:
                try:
                    self.play(step, run_time=1)
                except Exception as e:
                    print(step)
                    print(e)
                    exit()


        
class Sandbox(MovingCameraScene):
    def construct(self):
        value = 0.2

        point1 = np.array([value, 0, 0])
        point2 = np.array([-value, 0, 0])
        control1 = np.array([-(point1[0]+0.5), point1[1] + 1, 0])
        control2 = np.array([point2[0]+0.5, point2[1] + 1, 0])
        
        bezier = CubicBezier(point1, control2, control1, point2)

        #visual display of vertices
        # dot1 = Dot(point=point1).set_color(BLUE)
        dotcontrol1 = Dot(point=control1).set_color(ORANGE)
        dot2 = Dot(point=point1).set_color(BLUE)
        dotcontrol2 = Dot(point=control2).set_color(RED)


        triangle = Triangle(color=GREEN, fill_color=GREEN, fill_opacity=1).rotate(60*DEGREES).scale(0.1)
        triangle.set_x(point2[0])
        triangle.set_y(point2[1])
    
        dot_group = VGroup(bezier, triangle, dotcontrol1, dot2,  dotcontrol2)
        self.play(FadeIn(dot_group.scale(2)))



class Test(MovingCameraScene):
    def construct(self):
        value = 1
        arrow = ArcBetweenPoints([value, 0, 0], [-value, 0, 0], angle=1.5*PI, tip_style={'stroke_width': 5})
        arrow.add_tip()
        self.add(arrow)

        self.play(FadeIn(arrow))


def border_function():
    rectangle = Rectangle(width=width_of_scene, height=height, color=ORANGE)
    #set centre of rectangle to the centre of manim_automaton
    rectangle.set_x(manim_automaton.get_x())
    rectangle.set_y(manim_automaton.get_y())
    print("rectangle:", rectangle.get_x(), rectangle.get_y())
    # self.play(FadeIn(manim_automaton))
    self.play(DrawBorderThenFill(manim_automaton))
    self.play(DrawBorderThenFill(rectangle))