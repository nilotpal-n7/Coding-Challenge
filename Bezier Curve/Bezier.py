from manim import *
import numpy as np
import csv
from scipy.special import binom, comb

class Bezier(Scene):
    def construct(self):

        points = np.array([[-6,1,0], [-5,3,0], [-4,-1,0], [-2,2,0], [3,2,0], [5,0,0], [1,-1,0]])

        def Bezier(arr, t):
            k = len(arr) - 1
            eq = 0

            for i in range(k + 1):
                eq += comb(k, i, exact=True) * np.pow((1 - t), (k - i)) * np.pow(t, i) * arr[i]

            return eq
        
        def Lines(arr, d_c=GRAY, l_c=BLUE_C):
            dots = VGroup()
            lines = VGroup()
            n = len(arr)

            for i in range(n):
                dot = Dot(arr[i], radius=0.07, color=d_c)
                dots.add(dot)

            for i in range(n-1):
                line = Line(arr[i], arr[i+1], stroke_width=3, color=l_c)
                lines.add(line)

            return dots, lines
        
        def moving_lines(arr, t):
            n = len(arr)
            moving_dot = VGroup()
            moving_line = VGroup()
            moving_points = []

            if(n>1):
                for i in range(n-1):
                    point = Bezier([arr[i], arr[i+1]], t)
                    moving_points.append(point)

                moving_dot, moving_line = Lines(moving_points)
                get_dot, get_line, md = moving_lines(moving_points, t)
                moving_dot.add(get_dot)                    
                moving_line.add(get_line)
            else:
                md = arr[0]

            return moving_dot, moving_line, md

        path = VMobject(color=RED, stroke_width=10)
        dot, line = Lines(points, DARK_BROWN, YELLOW_E)
        self.add(line, dot)
        path_points = []
        dt = 1 / 120
        t = 0

        while(t <= 1):
            moving_dot, moving_line, md = moving_lines(points, t)
            path_points.append(md)
            dot0 = Dot(md, radius=0.13, color=LIGHT_PINK)
            path.set_points_as_corners(path_points)
            t += dt

            self.add(moving_line, moving_dot, path, dot0)
            self.wait(1 / 30)
            if(t <= 1):
                self.remove(dot0, path, moving_dot, moving_line)
        
        self.wait(6)
        print(path_points)
