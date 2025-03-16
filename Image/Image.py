from manim import *
import numpy as np
import sympy as sp
from scipy.special import comb
from arr import arr1, arr2, arr3, arr4, arr5
from bspline import b_spline_curve

class Image(Scene):
    def construct(self):

        def Bezier(arr, k, t):
            eq = 0

            for i in range(k + 1):
                eq += comb(k, i, exact=True) * pow((1 - t), (k - i)) * pow(t, i) * arr[i]

            return eq
        
        def smoother(arr, k, t):
            smoother_curve = []
            eq_arr = []

            for i in range(0, len(arr) - k, k):
                points = np.array(arr[i : (i + k + 1)][ : ])
                x = sp.symbols('x')
                eq = sp.sympify(Bezier(points, k, x))
                eq_arr.append(eq)

                for j in np.linspace(0, 1, t):
                    smoother_curve.append(eq.subs(x, j))
            
            return smoother_curve, eq_arr
        
        def start(arr, k, n, t, eq_a):
            smoother_curve = arr
            eq_arr = eq_a

            last = np.array([smoother_curve[-1]])
            num = k - ((len(smoother_curve)-1) % k)
            for i in range(num):
                smoother_curve = np.concat((smoother_curve, last), axis=0)

            if(n > 0):
                smoother_curve, eq_arr = smoother(smoother_curve, k, t)
                print(n, len(smoother_curve))
                smoother_curve, eq_arr = start(smoother_curve, k, n-1, t, eq_arr)
            
            return smoother_curve, eq_arr
        
        def differentiate(arr, t):
            diff_curve1 = []
            diff_curve2 = []
            x = sp.symbols('x')

            for eq in arr:
                eq1 = sp.diff(eq, x)
                eq2 = sp.diff(eq1, x)

                for j in np.linspace(0, 1, t):
                    diff_curve1.append(eq1.subs(x, j))
                    diff_curve2.append(eq2.subs(x, j))
            
            return np.array(diff_curve1, dtype=np.float32) / 150, np.array(diff_curve2, dtype=np.float32)/ 150
                        
        points = arr4
        k = 3
        n = 1
        t = 7
#        smoother_curve, eq_arr = start(points, k, n, t, [])
#        diff_curve1, diff_curve2 = differentiate(eq_arr, t * n)
#        smoother_curve = np.array(smoother_curve, dtype=np.float32)
        last = np.array([points[-1]])
        num = k - ((len(points)-1) % k)
        for i in range(num):
            points = np.concat((points, last), axis=0)
        smoother_curve = b_spline_curve(points, k, 2200)
        print(len(points), len(smoother_curve))

        N = len(smoother_curve)
        n = int(N / 2)

        def Fourier(arr, n):
            coefficients = []

            for k in range(-n, n + 1):
                coeff = np.sum(arr * np.exp(-2j * np.pi * k * np.arange(N) / N)) / N
                coefficients.append((k, coeff))

            return sorted(coefficients, key=lambda c: abs(c[1]), reverse=True)
        
        coefficients = Fourier(smoother_curve[ : , 0] + 1j * smoother_curve[ : , 1], n)
        
        def draw(center, time, coefficients):
            start = center
            circles = VGroup()
            lines = VGroup()

            for k, coeff in coefficients:
                radius = abs(coeff)
                angle = 2 * np.pi * k * time + np.angle(coeff)

                circle = Circle(radius=radius, stroke_opacity=0.7, color=BLUE)
                end = start + np.array([radius * np.cos(angle), radius * np.sin(angle), 0])
                line = Line(start, end, stroke_width=1, color=YELLOW)

                circle.move_to(start)
                circles.add(circle)
                lines.add(line)
                start = end

            return circles, lines, start
        
        path = VMobject(color=RED)
        path_points = []
        dt = 1 / N
        time = 0

        while(time < (1 - dt)):
            circles, lines, starting = draw(ORIGIN, time, coefficients)
            path_points.append(starting)
            path.set_points_as_corners(path_points)
            time += dt

            self.add(circles, lines, path)
            self.wait(1 / 30)
            self.remove(circles, lines, path)

        self.add(path)
        self.wait(2)

scene = Image()
scene.render()
