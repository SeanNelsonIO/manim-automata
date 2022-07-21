from manim import *
from src.manim_automata.mobjects import *
from src.manim_automata.mobjects.automaton_mobject import ManimAutomaton


class Automata(MovingCameraScene):
    def construct(self):
        manim_automaton = ManimAutomaton(xml_file='x_contains_a_1_in_third_final_position.jff', camera_follow=True)

        width_of_scene = manim_automaton.width
        height = manim_automaton.height
        rectangle = Rectangle(width=width_of_scene, height=height, color=ORANGE)
        #set centre of rectangle to the centre of manim_automaton
        rectangle.set_x(manim_automaton.get_x())
        rectangle.set_y(manim_automaton.get_y())
        print("rectangle:", rectangle.get_x(), rectangle.get_y())
        
        # setup cameara
        self.play(
            self.camera.frame.animate.move_to(manim_automaton)
        )

        #creates a frame around manim-automaton
        self.camera.frame.set_width(width_of_scene + 2)
        self.camera.frame.set_height(height + 10)
        # self.play(FadeIn(manim_automaton))
        self.play(DrawBorderThenFill(manim_automaton))
        self.play(DrawBorderThenFill(rectangle))
        
        input_string = "01110"

        for sequence in manim_automaton.play_string(input_string):
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

