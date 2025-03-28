from math import *

r1, r2 = 1, 1
phi, a, b, c = 0, 0, 0, 0
x = (r2 + r1 * cos(phi)) * (cos(c) * cos(b) + sin(a) * sin(c) * sin(b)) - r1 * cos(a) * sin(c) * sin(phi)
y = (r2 + r1 * cos(phi)) * (cos(b) * sin(c) - cos(c) * sin(a) * sin(b)) + r1 * cos(a) * cos(c) * sin(phi)
z = (r2 + r1 * cos(phi)) * cos(a) * sin(b) + r1 * sin(a) * sin(phi)
