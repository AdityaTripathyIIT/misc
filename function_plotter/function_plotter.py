#!/bin/python
import matplotlib.pyplot as plt
import numpy as np

x_lower_bound, x_upper_bound = [float(x) for x in input(
    "plot for which x interval : ").split()]

y_lower_bound, y_upper_bound = [float(x) for x in input(
    "plot for which y interval : ").split()]


def func(x):
    return 1 / (np.pi * np.sqrt(x**4 + 6 * x**2 + 25))


def plot():
    x = np.linspace(x_lower_bound, x_upper_bound, 1000)
    # can also append to func(x) np.append(x, x) and np.append(func_1(x), func_2(x)))
    plt.plot(x, func(x))
    # plt.plot(x, func_2(x))
   # plt.plot(np.append(x, x), np.append(func(x), -func(x)))
    plt.xlim(x_lower_bound, x_upper_bound)
    plt.ylim(y_lower_bound, y_upper_bound)
    plt.grid()
    plt.show()


plot()
