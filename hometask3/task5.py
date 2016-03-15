# -*- coding: utf-8 -*-
'''
5.
Методом перебора найдите функцию с наименьшим штрафом.
'''
import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
import matplotlib.pyplot as plt
from math import sqrt, pi, exp


def polynom(x, a, b, c, d, e):
    return a*x**4 + b*x**3 + c*x**2 + d*x + e


if __name__ == '__main__':
    data = pd.read_csv('regression_x_y.2.csv', ';')
    x = data['X']
    y = data['Y']

    # как вариант
    #best_vals = np.polyfit(x=x, y=y, deg=4)

    best_vals, covar = curve_fit(polynom, x, y)

    print 'коэффициенты для полинома 4ой степени'
    print 'a: ', best_vals[0]
    print 'b: ', best_vals[1]
    print 'c: ', best_vals[2]
    print 'd: ', best_vals[3]
    print 'e: ', best_vals[4]

    plt.figure()
    plt.plot(x, y, 'ro')
    plt.plot(x, polynom(x, best_vals[0], best_vals[1], best_vals[2], best_vals[3], best_vals[4]))
    plt.ylabel('Y')
    plt.xlabel('X')
    plt.show()
