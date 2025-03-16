import numpy as np
import matplotlib.pyplot as plt
from arr import arr1, arr2, arr3, arr4, arr5

def basis_function(i, k, t, knots):
    """Compute the B-spline basis function N_{i,k}(t) recursively."""
    if k == 1:
        return 1.0 if knots[i] <= t < knots[i + 1] else 0.0
    
    denom1 = knots[i + k - 1] - knots[i]
    denom2 = knots[i + k] - knots[i + 1]
    
    term1 = ((t - knots[i]) / denom1 * basis_function(i, k - 1, t, knots)) if denom1 != 0 else 0
    term2 = ((knots[i + k] - t) / denom2 * basis_function(i + 1, k - 1, t, knots)) if denom2 != 0 else 0
    
    return term1 + term2

def b_spline_curve(control_points, k, num_points=700):
    """Compute the B-spline curve for given control points and degree."""
    n = len(control_points) - 1  # Number of control points - 1
    m = n + k + 1  # Total number of knots
    knots = np.linspace(0, 1, m)  # Uniformly spaced knots
    t_values = np.linspace(knots[k - 1], knots[n + 1], num_points)
    
    curve = np.zeros((num_points, 3))  # Store (x, y, z) points of the curve with z=0
    for j, t in enumerate(t_values):
        point = np.zeros(3)
        for i in range(n + 1):
            coeff = basis_function(i, k, t, knots)
            point[:2] += coeff * np.array(control_points[i])  # Assign x, y values
        curve[j] = point
    
    return curve

# Example usage
control_pts = arr4
degree = 3
num_points = 700
curve_points = b_spline_curve(control_pts, degree, num_points)

# Plot
plt.figure(figsize=(9,5))
plt.plot(curve_points[:, 0], curve_points[:, 1], label='B-Spline Curve')
plt.scatter(*zip(*control_pts), color='red', label='Control Points')
plt.legend()
plt.title("Uniform B-Spline Curve")
plt.show()
