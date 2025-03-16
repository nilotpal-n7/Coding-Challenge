import csv
import numpy as np
import matplotlib.pyplot as plt
from arr import arr1, arr2, arr3, arr4

def cubic_bezier(P0, P1, P2, P3, t):
    return (((1 - t) ** 3) * P0 + 3 * ((1 - t) ** 2) * t * P1 + 3 * (1 - t) * (t ** 2) * P2 + (t ** 3) * P3)

def smooth_points_with_bezier(points, num_interpolation_points=7):
    points = np.array(points)    
    smoothed_points = []
    
    for i in range(0, len(points) - 3, 3):
        P0 = points[i]
        P1 = points[i + 1]
        P2 = points[i + 2]
        P3 = points[i + 3]
        
        for t in np.linspace(0, 1, num_interpolation_points):
            smoothed_points.append(cubic_bezier(P0, P1, P2, P3, t))
    
    smoothed_points = np.array(smoothed_points)    
    return smoothed_points

def save_smoothed_points(smoothed_points, filename='smoothed.npy'):
    np.save(filename, smoothed_points)
    print(f"Smoothed points saved to {filename}")

points = []
with open("input.csv") as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        points.append(row)

def start(points, n):
    smoothed_points = points

    if(n>0):
        smoothed_points = smooth_points_with_bezier(points)
        print(n, len(smoothed_points))        
        smoothed_points = start(smoothed_points, n-1)

    return smoothed_points

points = arr3
points = np.array(points)
smoothed_points = start(points, 1)
save_smoothed_points(smoothed_points)
points = np.array(points)
print(len(smoothed_points))

plt.figure(figsize=(9, 5))
plt.plot(points[:, 0], points[:, 1], 'ro-', label='Original Points')
plt.plot(smoothed_points[:, 0], smoothed_points[:, 1], 'b-', label='Smoothed Bezier Curve')
plt.legend()
plt.show()
