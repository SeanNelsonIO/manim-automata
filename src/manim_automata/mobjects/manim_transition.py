from manim import *
from .automata_dependencies.automata import Transition


class ManimTransition(VGroup):
    """A Manim Transition. A visual representation of a Transition instance

        Parameters
        ----------
        transition
            Positions of pendulum bobs.
        start_state
            state at which the transition sta
        end_state
            Parameters for ``Line``.
        label
            Parameters for ``Circle``.
        kwargs
            Additional parameters for ``VMobject``.
        Examples - do I need this.
        --------
        .. manim:: ManimTransitionExample

            from manim_physics import *
            class MultiPendulumExample(SpaceScene):
                def construct(self):
                    p = MultiPendulum(RIGHT, LEFT)
                    self.add(p)
                    self.make_rigid_body(p.bobs)
                    p.start_swinging()
                    self.add(TracedPath(p.bobs[-1].get_center, stroke_color=BLUE))
                    self.wait(10)
        """
    def __init__(
        self,
        transition: Transition,
        start_state: "ManimState",
        end_state: "ManimState",
        read_symbols: list,
        animation_style: dict,
        **kwargs
    ) -> None:

        self.animation_style = animation_style
        self.transition = transition

        self.start_state = start_state
        self.end_state = end_state
        #create text objects for read_symbols
        self.manim_read_symbols = []
        for read_symbol in read_symbols:
            self.manim_read_symbols.append(Text(read_symbol, font_size=100))
        

        if start_state == end_state: #create transition that points to itself
            position_1, position_2 = self.calculate_circle_vertices()
            self.create_reflexive_arrow(position_1, position_2)
        else: #start_state ----> end_state
            self.arrow = Arrow(start_state, end_state, buff=0)
            self.position_text()
            
        super().__init__(self.arrow, *self.manim_read_symbols, **kwargs)
        


    def animate_transition(self, transition_result: bool):
        """Animates the arrow of a ManimTransition, color depends on if the transition
        accepts the input token """
        animation_function = self.animation_style["animate_transition"]["animation_function"]
        run_time = self.animation_style["animate_transition"]["run_time"]
        time_width = self.animation_style["animate_transition"]["time_width"]

        if transition_result: 
            color = self.animation_style["animate_transition"]["accept_color"]
        else:
            color = self.animation_style["animate_transition"]["reject_color"]
            

        return animation_function(self.arrow.copy().set_color(color), run_time=run_time, time_width=time_width)


    def calculate_circle_vertices(self) -> tuple[int]:
        # centre_x = self.start_state
        # centre_y = 
        circle = self.start_state.circle
        
        p1 = circle.point_at_angle(PI/4 + PI/2)
        p2 = circle.point_at_angle(PI/4)

        return p1, p2

    def create_reflexive_arrow(self, point1, point2) -> None:
        self.arrow = CurvedArrow(point2, point1, angle=1.5*PI)
        
        center_of_arc = self.arrow.get_arc_center()
        radius = self.arrow.radius

        #positions the text above the reflexive arrow
        self.text.move_to(center_of_arc).shift(UP*radius*1.5)

    def calculate_direction_of_arrow_label(self, normal_vector_choice: int = 0) -> list[int]:
        """Calculates the which side of the arrow the label should be placed"""
        # direction_of_arrow = [self.arrow.get_x(), self.arrow.get_y()]
        # direction = self.arrow.line.get_normal_vector()
        #difference of the arrow
        x1 = None
        y1 = None
        if type(self.start_state) == list:
            x1 = self.start_state[0]
            y1 = self.start_state[1]
        else:
            x1 = self.start_state.get_x()
            y1 = self.start_state.get_y()

        x2 = self.end_state.get_x()
        y2 = self.end_state.get_y()

        difference_of_x = x2 - x1
        difference_of_y = y2 - y1

        normalised_values = normalize([difference_of_x, difference_of_y])

        #calculate normal of the line
        normal_vectors = {
            0: [-normalised_values[1], normalised_values[0], -1],
            1: [normalised_values[1], -normalised_values[0], -1]
        }
        
        return normal_vectors[normal_vector_choice]

    def position_text(self) -> None:
        """This function positions text next to the arrow as there was no good way to do it with the lib rary"""
        #Obtain coordinates for the centre of the line
        x1 = None
        y1 = None
        if type(self.start_state) == list:
            x1 = self.start_state[0]
            y1 = self.start_state[1]
        else:
            x1 = self.start_state.get_x()
            y1 = self.start_state.get_y()

        x2 = self.end_state.get_x()
        y2 = self.end_state.get_y()

        #midpoint
        c1 = (x1 + x2) / 2
        c2 = (y1 + y2) / 2

        # normal_offset = [x for x in self.calculate_direction_of_arrow_label()]
        normal_offset = self.calculate_direction_of_arrow_label()

        for index, manim_read_symbol in enumerate(self.manim_read_symbols):
            buffer = 0.1 #buffer between read_symbols
            normal_offset[1] = normal_offset[1] * (index+1 + buffer)

            text_coordinates = [x + y for x, y in zip([c1, c2, 0], normal_offset)]

            manim_read_symbol.set_x(text_coordinates[0])
            manim_read_symbol.set_y(text_coordinates[1])
        