from manim import *

__all__ = ["DotGrid"]


class DotGrid(VMobject):
    def __init__(self):
        super().__init__()
        dot1 = Circle().shift(LEFT)
        dot2 = Circle()
        dot3 = Circle().shift(RIGHT)
        self.dotgrid = VGroup(dot1, dot2, dot3)
        self.add(self.dotgrid)

    def update_dot(self):
        self.dotgrid.become(self.dotgrid.shift(UP))