from manim import FadeToColor, RED, BLUE, WHITE, YELLOW


class ManimAnimations():

    def __init__(self) -> None:
        pass

    #state animations
    def animate_dead_branch_state(self, state):
        return FadeToColor(state, color=RED)

    def animate_state_to_default_color(self, state):
        return FadeToColor(state, color=BLUE)

    def animate_highlight_state(self, state):
        return FadeToColor(state, color=YELLOW)


    #transition animations
    def animate_transition_to_default_color(self, transition):
        return FadeToColor(transition, color=WHITE)

    def animate_highlight_transition(self, transition):
        return FadeToColor(transition, color=YELLOW)


    #input animations
    

    #subscript animations



