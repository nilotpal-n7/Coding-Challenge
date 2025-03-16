from manim import *
import numpy as np
import torch

class DFT(Scene):
    def construct(self):

        def sketch(t):
            x = (16 * torch.sin(t)**3) / 10
            y = (13 * torch.cos(t) - 5 * torch.cos(2*t) - 2 * torch.cos(3*t) - torch.cos(4*t)) / 10
            return torch.tensor([x, y, 0])

        N_POINTS = 100
        t_points = torch.linspace(0, 2 * torch.pi, N_POINTS)
        points = torch.zeros([N_POINTS, 3])
        for t, t_v in enumerate(t_points):
            points[t] = sketch(t_v)

        def dft(points, n_terms):
            N = len(points)
            coefficients = torch.zeros([2 * n_terms], dtype=torch.complex128)
            for k in range(-n_terms, n_terms + 1):
                coefficients[k] = torch.sum(points * torch.exp(-2j * k * torch.pi * torch.arange(N) / N)) / N

            return coefficients

        N_TERMS = 50
        coefficients = dft(points[ : , 0] + 1j * points[ : , 1], N_TERMS)

        def draw(center, time, coefficients):
            live_point = center
            epi_circles = VGroup()
            epi_lines = VGroup()

            for k, c in enumerate(coefficients):
                c = c.numpy()
                frequency = k - N_TERMS
                radius = abs(c)
                phase = np.angle(c)

                epi_circle = Circle(radius=radius, stroke_opacity=0.5, color=BLUE)
                epi_circles.move_to(live_point)
                epi_circles.add(epi_circle)

                ter_point = live_point + np.array([
                    radius * np.cos(2 * np.pi * frequency * time + phase),
                    radius * np.sin(2 * np.pi * frequency * time + phase),
                    0
                ])

                epi_line = Line(live_point, ter_point, stroke_opacity=0.7, color=YELLOW)
                epi_lines.add(epi_line)
                live_point = ter_point

            return epi_circles, epi_lines, live_point

        point0 = points[0].numpy()
        path = VMobject(color=RED)
        path.set_points_as_corners([point0])
        path_points = [point0]
        dt = 1 / 60
        time = 0

        for t in range(N_POINTS):
            time += dt
            epi_circles, epi_lines, live_point = draw(ORIGIN, time, coefficients)
            path_points.append(live_point)
            path.set_points_as_corners(path_points)

            self.clear()
            self.add(epi_circles, epi_lines, path)
            self.wait(dt)

scene = DFT()
scene.render()
