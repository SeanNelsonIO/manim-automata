from manim import Transform, FadeToColor, RED, BLUE, WHITE, YELLOW, FadeIn


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
    def animate_input_token_spent(self, token):
        return token.animate.set_opacity(0.5)

    def animate_highlight_input_token(self, token):
        return FadeToColor(token, color=YELLOW)

    def animate_display_input(self, input):
        return FadeIn(input)

    #subscript animations
    def animate_transform_to_new_subscript_object(self, initial_subscript, new_subscript):
        return Transform(initial_subscript, new_subscript)



