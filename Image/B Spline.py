from manim import *
import numpy as np

class B_Spline(Scene):
    def construct(self):

        def basis_function(i, k, t, knots):
            if k == 1:
                return 1.0 if knots[i] <= t < knots[i + 1] else 0.0

            denom1 = knots[i + k - 1] - knots[i]
            denom2 = knots[i + k] - knots[i + 1]

            term1 = ((t - knots[i]) / denom1 * basis_function(i, k - 1, t, knots)) if denom1 != 0 else 0
            term2 = ((knots[i + k] - t) / denom2 * basis_function(i + 1, k - 1, t, knots)) if denom2 != 0 else 0

            return term1 + term2

        def b_spline_curve(control_points, k, num_points=700):
            n = len(control_points) - 1
            m = n + k + 1
            knots = np.linspace(0, 1, m)
            t_values = np.linspace(knots[k - 1], knots[n + 1], num_points)

            curve = np.zeros((num_points, 3))
            for j, t in enumerate(t_values):
                point = np.zeros(3)
                for i in range(n + 1):
                    coeff = basis_function(i, k, t, knots)
                    point[:2] += coeff * np.array(control_points[i])
                curve[j] = point

            return curve
        
        def Lines(arr, d_c=GRAY, l_c=BLUE_C):
            arr1 = np.zeros([len(arr), 3])
            arr1[:,0:2] =  arr[:,0:2]
            dots = VGroup()
            lines = VGroup()
            n = len(arr)

            for i in range(n):
                dot = Dot(arr1[i], radius=0.07, color=d_c)
                dots.add(dot)

            for i in range(n-1):
                line = Line(arr1[i], arr1[i+1], stroke_width=3, color=l_c)
                lines.add(line)

            return dots, lines
        
        points = np.array([[-6,1], [-5,3], [-4,-1], [-2,2], [3,2], [5,0], [1,-1]])
        num = 120
        md = b_spline_curve(points, 3, num)
        
        path = VMobject(color=RED, stroke_width=10)
        dot, line = Lines(points, DARK_BROWN, YELLOW_E)
        self.add(line, dot)
        path_points = []
        t = 0

        while(t < num):
            path_points.append(md[t])
            dot0 = Dot(md[t], radius=0.13, color=LIGHT_PINK)
            path.set_points_as_corners(path_points)
            t += 1

            self.add(path, dot0)
            self.wait(1 / 30)
            if(t < num):
                self.remove(dot0, path)
        
        self.wait(2)
        print(path_points)
