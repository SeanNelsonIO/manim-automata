from cmath import cos
from curses import tparm
from manim import *
from manim_automata import ManimAutomaton
from .automata_dependencies.automata import Transition

from .manim_state import ManimState

import math

class ManimTransition(Transition, VGroup):
    """A Manim Transition. A visual representation of a Transition instance

        Parameters
        ----------
        transition_from
            state at which the transition starts
        transition_to
            pass
        read_symbols
            pass
        ...
        kwargs
            Additional parameters for ``VMobject``.
    """
    def __init__(
        self,
        transition_from: ManimState,
        transition_to: ManimState,
        read_symbols: list,
        parent_automaton: ManimAutomaton,
        animation_style: dict,
        font_size = 100,
        **kwargs
    ) -> None:

        Transition.__init__(self, transition_from, transition_to)
        self.circle = None
        #manim settings for animations and colors
        self.animation_style = animation_style
        #store tex mobjects of read_symbols for transitions
        self.read_symbols = []

        self.parent_automaton = parent_automaton
        #create manim read symbols for transitition
        for read_symbol in read_symbols:
            #Create mobjects of read_symbol
            self.read_symbols.append(Tex(read_symbol, font_size=font_size))
        
        if self.transition_from == self.transition_to: #create transition that points to itself
            position_1, position_2 = self.calculate_circle_vertices()
            self.create_reflexive_arrow(position_1, position_2)
        elif self.transition_to.get_transition_by_transition_to_state_id(self.transition_from.id) is not None: #check if there already exists an arrow pointing the opposite way
            #pre-exising arrow transition converted to curved arrow
            opposite_transition = self.transition_to.get_transition_by_transition_to_state_id(self.transition_from.id)
            opposite_transition.convert_straight_arrow_to_curved_arrow()

            #create this(self) arrow
            self.construct_curved_arrow()


        else: #transition_from ----> transition_to
            self.arrow = Arrow(transition_from, transition_to, buff=0)
            self.position_text() #- this is causing errors

        
      
        VGroup.__init__(self, self.arrow, *self.read_symbols, **kwargs)

       

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
        # centre_x = self.transition_from
        # centre_y = 
        circle = self.transition_from.circle
        
        p1 = circle.point_at_angle(PI/4 + PI/2)
        p2 = circle.point_at_angle(PI/4)

        return p1, p2

    def create_reflexive_arrow(self, point1, point2) -> None:
        self.arrow = CurvedArrow(point2, point1, angle=1.5*PI)
        
        #used to position the read symbols
        center_of_arc = self.arrow.get_arc_center()
        radius = self.arrow.radius

        #positions the text above the reflexive arrow
        for index, read_symbol in enumerate(self.read_symbols):
            # positions symbols to be stacked on top of the reflexive arrow.
            read_symbol.move_to(center_of_arc).shift(UP*radius+[0, index+1, 0])

    def calculate_direction_of_arrow_label(self, normal_vector_choice: int = 1) -> list[int]:
        """Calculates the which side of the arrow the label should be placed"""

        x1 = self.transition_from.get_x()
        y1 = self.transition_from.get_y()

        x2 = self.transition_to.get_x()
        y2 = self.transition_to.get_y()

        difference_of_x = x2 - x1
        difference_of_y = y2 - y1

        normalised_values = normalize([difference_of_x, difference_of_y])

        #calculate normal of the line
        normal_vectors = {
            0: [-normalised_values[1], normalised_values[0], -1],
            1: [normalised_values[1], -normalised_values[0], -1]
        }
        
        return normal_vectors[normal_vector_choice]

    def position_text(self, buffer=0.5) -> None:
        """This function positions text next to the arrow as there was no good way to do it with the lib rary"""
        #Obtain coordinates for the centre of the line
        x1 = None
        y1 = None
        if type(self.transition_from) == list:
            x1 = self.transition_from[0]
            y1 = self.transition_from[1]
        else:
            x1 = self.transition_from.get_x()
            y1 = self.transition_from.get_y()

        x2 = self.transition_to.get_x()
        y2 = self.transition_to.get_y()

        #midpoint
        c1 = (x1 + x2) / 2
        c2 = (y1 + y2) / 2

        # normal_offset = [x for x in self.calculate_direction_of_arrow_label()]
        normal_offset = self.calculate_direction_of_arrow_label()
        for index, read_symbol in enumerate(self.read_symbols):
            #if there are multiple symbols then stack them
            read_symbol_offset_y = normal_offset[1] * (index+1 * buffer)
            read_symbol_offset_x = normal_offset[0] * (index+1 * buffer)
            # read_symbol_offset_x = normal_offset[0] * buffer
            #directional offset from the arrow line
            read_symbol_offset = [read_symbol_offset_x, read_symbol_offset_y]
            
            #apply offset to centre of line coordinates
            text_coordinates = [x + y for x, y in zip([c1, c2, 0], read_symbol_offset)]

            #apply offset coordinates to the mobject.
            read_symbol.set_x(text_coordinates[0])
            read_symbol.set_y(text_coordinates[1])


    def convert_straight_arrow_to_curved_arrow(self):
        """
        Converts a straight arrow transition to a curved arrow transition.
        This method is primarily used when there are two opposing transitions
        between two states.
        """
        #remove existing manim arrow
        self.remove(self.arrow) 

        #remove manim read symbols
        for read_symbol in self.read_symbols:
            self.remove(read_symbol)

        #create new curved arrow and read symbols
        self.construct_curved_arrow()
        self.add(self.arrow, *self.read_symbols)

    def construct_curved_arrow(self, buffer=0.5):
        #create a straight line and use the points locations to create curved arrow
        temp_arrow = Arrow(self.transition_from, self.transition_to)
        from_point = temp_arrow.start
        to_point = temp_arrow.end
        
        self.arrow = CurvedArrow(from_point, to_point)


        chord_center_x = (from_point[0] + to_point[0]) / 2
        chord_center_y = (from_point[1] + to_point[1]) / 2

        cx = self.arrow.get_arc_center()[0]
        cy = self.arrow.get_arc_center()[1]

        #get the point of curved arrow
        angle = math.atan2(chord_center_y - cy, chord_center_x - cx)
        temp_circle = Circle(self.arrow.radius, color=RED)
        temp_circle.move_arc_center_to(self.arrow.get_arc_center())
        center_point = temp_circle.point_at_angle(angle)

        normal_offset = self.calculate_direction_of_arrow_label()
        
        for index, read_symbol in enumerate(self.read_symbols):
            #if there are multiple symbols then stack them
            read_symbol_offset_y = normal_offset[1] * (index+1 * buffer)
            
            # read_symbol_offset_x = normal_offset[0] * buffer
            read_symbol_offset_x = normal_offset[0] * (index+1 * buffer)
            #directional offset from the arrow line
            read_symbol_offset = [read_symbol_offset_x, read_symbol_offset_y]
            
            #apply offset to centre of line coordinates
            text_coordinates = [x + y for x, y in zip([center_point[0], center_point[1], 0], read_symbol_offset)]

            #apply offset coordinates to the mobject.
            read_symbol.set_x(text_coordinates[0])
            read_symbol.set_y(text_coordinates[1])

    def check_transition_read_symbols(self, token):
        """Given a token, check there is a read_symbol that matches"""
        for read_symbol in self.read_symbols:
            if read_symbol.tex_string == token.tex_string:
                return True # There is a read_symbol that matches the given token
        return False #There are no read_symbols that match the given token

