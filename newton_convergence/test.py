import numpy as np
import matplotlib.pyplot as plt
from math import fabs

def f(x):
    return x**3 - 2*x - 5  # Example function

def f_derivative(x):
    return 3*x**2 - 2  # Derivative of the function

def run_newton_iterations(num_iter, upper_alarm, lower_alarm, init_point):
    points = [init_point]
    
    while True:
        if abs(f_derivative(init_point)) < lower_alarm:
            print("Failure")
            return -1, points
        
        save = init_point
        init_point -= f(init_point) / f_derivative(init_point)
        points.append(init_point)
        
        if abs((init_point - save) / init_point) < lower_alarm:
            print(f"Solution = {init_point}")
            return init_point, points
        
        if abs(init_point) > upper_alarm:
            print("x got too big")
            return -1, points

def plot_iterations(points):
    x_vals = np.arange(len(points))
    new = list()
    for i in range(1, len(points)) :
        new.append(fabs(points[i] - points[i-1]))
    plt.plot(x_vals[1:], new, marker='o', linestyle='-', color='b')
    plt.xlabel("Iteration")
    plt.ylabel("x value")
    plt.title("Newton's Method Iterations")
    plt.grid()
    plt.show()

# Example usage
solution, points = run_newton_iterations(100, 1000, 1e-6, 100.0)
plot_iterations(points)
