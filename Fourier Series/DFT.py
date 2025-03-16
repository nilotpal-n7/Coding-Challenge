from manim import *
import numpy as np
import csv
from arr import arr4

class Epicycles(Scene):
    def construct(self):
#        results = np.loadtxt('images.txt')
#        results = np.load('smoothed.npy')
        results = arr4

        '''def sketch(t):
            x = (16 * np.sin(t)**3) / 10
            y = (13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)) / 10
            return np.array([x, y, 0])

        N = 100
        t_values = np.linspace(0, 2 * np.pi, N)
        points = np.array([sketch(t) for t in t_values])'''

        '''results = []
        with open("input.csv") as csvfile:
            reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
            for row in reader:
                results.append(row)'''
        
        points = np.array(results)
        N = len(points)
        print(N)
        n = int(N / 2)

        def Epicycles(points, n):
            coefficients = []

            for k in range(-n, n + 1):
                coef = np.sum(points * np.exp(-2j * np.pi * k * np.arange(N) / N)) / N
                coefficients.append((k, coef))
            
            return sorted(coefficients, key=lambda c: abs(c[1]), reverse=True)
        
        coefficients = Epicycles(points[ : , 0] + 1j * points[ : , 1], n)

        def draw_epicycles(center, time, coefficients):
            current_point = center
            circles = VGroup()
            lines = VGroup()

            for k, coef in coefficients:
                radius = abs(coef)
                angle = 2 * np.pi * k * time + np.angle(coef)

                circle = Circle(radius=radius, stroke_opacity=0.7, color=BLUE)
                circle.move_to(current_point)
                circles.add(circle)

                end_point = current_point + np.array([
                    radius * np.cos(angle),
                    radius * np.sin(angle),
                    0
                ])

                line = Line(current_point, end_point, stroke_width=1, color=YELLOW)
                lines.add(line)
                current_point = end_point

            return circles, lines, current_point

        path = VMobject(color=RED)
        path_points = []
        dt = 1 / N
        time = 0

        while(time < 1 - dt):
            circles, lines, current_point = draw_epicycles(ORIGIN, time, coefficients)
            path_points.append(current_point)
            path.set_points_as_corners(path_points)
            time += dt

            self.add(circles, lines, path)
            self.wait(1 / 30)
            self.remove(circles, lines, path)

        self.add(path)
        self.wait(2)

scene = Epicycles()
scene.render()
