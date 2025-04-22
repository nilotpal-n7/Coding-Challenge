from manim import *
from random import *

class Fern(Scene):
    def construct(self):

        def fun1(x, y):
            return (0, 0.16 * y)
        def fun2(x, y):
            return (0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6)
        def fun3(x, y):
            return (0.2 * x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6)
        def fun4(x, y):
            return -0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44
        
        x, y = 0, 0
        t = 60000
        funs = [fun1, fun2, fun3, fun4]

        dots = VGroup()
        dot = Dot([x, y - 5, 0], radius=0.01)
        dots.add(dot)
        
        while t:
            r = random()
            dot = Dot([x, (y - 5)/1.5, 0], radius=0.006, color=GREEN)
            dots.add(dot)

            if(t % 100 == 0):
                self.add(dots)
                self.wait(1 / 60)

            fun = choices(funs, weights=[0.01, 0.85, 0.07, 0.07], k=1)
            x, y = fun[0](x, y)
            t -= 1
