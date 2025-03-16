from manim import *
import numpy as np
from scipy.special import binom, comb

class Writting(Scene):
    def construct(self):

        title = Text("Spline and Curve Fitting", font_size=48, color=BLUE).to_edge(UP)

        formula1 = MathTex(
            r"\mathbf{DFT:}\ X_k = \sum_{n=0}^{N-1} x_n e^{-2\pi i k n / N}",
            substrings_to_isolate=["X_k", "x_n", "e^{-2\pi i k n / N}"]
        ).to_edge(LEFT).shift(UP).set_color_by_gradient(BLUE, PINK)

        formula2 = MathTex(
            r"\mathbf{Bezier:\ }\mathbf{C}(t) = \sum_{i=0}^{n-1} (1 - t)\mathbf{P}_{i} + t\mathbf{P}_{i-1}",
            substrings_to_isolate=["\mathbf{C}(t)", "\mathbf{P}_0", "\mathbf{P}_1"]
        ).scale(0.7).to_edge(RIGHT).shift(DOWN * 2.7).shift(LEFT * 0.2).set_color_by_gradient(BLUE, PINK)

        formula3 = MathTex(
            r"\mathbf{B\ Spline:\ }\mathbf{C}(t) = \sum_{i=0}^{n} N_{i,k}(t) \mathbf{P}_i",
            substrings_to_isolate=["\mathbf{C}(t)", "N_{i,k}(t)", "\mathbf{P}_i"]
        ).scale(0.7).to_edge(LEFT).shift(DOWN * 2.7).shift(RIGHT * 0.5).set_color_by_gradient(BLUE, PINK)

        sq1 = Square().scale(3).to_edge(DL)
        sq2 = Square().scale(3).to_edge(DR)
        self.play(Write(title))
        self.play(Create(sq1), Create(sq2))
        self.play(Write(formula2), Write(formula3))



        def basis_function(i, k, t, knots):
            if k == 1:
                return 1.0 if knots[i] <= t < knots[i + 1] else 0.0

            denom1 = knots[i + k - 1] - knots[i]
            denom2 = knots[i + k] - knots[i + 1]

            term1 = ((t - knots[i]) / denom1 * basis_function(i, k - 1, t, knots)) if denom1 != 0 else 0
            term2 = ((knots[i + k] - t) / denom2 * basis_function(i + 1, k - 1, t, knots)) if denom2 != 0 else 0

            return term1 + term2

        def b_spline_curve(control_points, k, num_points=120):
            n = len(control_points) - 1
            m = n + k + 1
            knots = np.linspace(0, 1, m)
            t_values = np.linspace(knots[k - 1], knots[n + 1], num_points)

            curve = np.zeros((num_points, 3))
            for j, t in enumerate(t_values):
                point = np.zeros(3)
                for i in range(n + 1):
                    coeff = basis_function(i, k, t, knots)
                    point[:3] += coeff * np.array(control_points[i])
                curve[j] = point

            return curve
        


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
        

        
        points = np.array([[-6,1,0], [-5,3,0], [-4,-1,0], [-2,2,0], [3,2,0], [5,0,0], [1,-1,0]]) / 2
        num = 120
        shift_l = 3.3
        shift_r = 3.9

        md1 = b_spline_curve(points, 3, num)        
        path1 = VMobject(color=RED, stroke_width=10)
        dot1, line1 = Lines(points, DARK_BROWN, YELLOW_E)
        self.add(line1.shift(LEFT * shift_l), dot1.shift(LEFT * shift_l))
        path_points1 = []
        t = 0

        path2 = VMobject(color=RED, stroke_width=10)
        dot2, line2 = Lines(points, DARK_BROWN, YELLOW_E)
        self.add(line2.shift(RIGHT * shift_r), dot2.shift(RIGHT * shift_r))
        path_points2 = []
        dt = 1 / num
        time = 0



        while(t < num):
            moving_dot, moving_line, md2 = moving_lines(points, time)
            path_points2.append(md2)
            dot02 = Dot(md2, radius=0.13, color=LIGHT_PINK)
            path2.set_points_as_corners(path_points2)
            time += dt

            path_points1.append(md1[t])
            dot01 = Dot(md1[t], radius=0.13, color=LIGHT_PINK)
            path1.set_points_as_corners(path_points1)
            t += 1

            self.add(moving_line.shift(RIGHT * shift_r), moving_dot.shift(RIGHT * shift_r), path2.shift(RIGHT * shift_r), dot02.shift(RIGHT * shift_r), path1.shift(LEFT * shift_l), dot01.shift(LEFT * shift_l))
            self.wait(1 / 30)
            if(t < num):
                self.remove(dot01, path1, dot02, path2, moving_dot, moving_line)



        self.wait(2)
        self.remove(dot01, path1, dot02, path2, moving_dot, moving_line, line1, line2, dot1, dot2)
        self.play(FadeOut(formula2, formula3))
        self.play(Uncreate(sq1), Uncreate(sq2))
        self.play(FadeOut(title))
