# -*- coding: utf-8 -*-
'''
3.
Задайте функцию штрафа как A - g(x, 0, sigma), где g(x, 0, sigma) -- гаусова
функцию с матожиданием в нуле. Чему разумно задать константу A и
среднеквадратичное отклонение (sigma)?
'''
import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
import matplotlib.pyplot as plt
from math import sqrt, pi, exp


def gaussian(x, A, sigma):
    return (A - (np.exp(-(x)**2/(2*sigma**2))/(sigma*np.sqrt(2*np.pi))))

def polynom(x, a, b, c, d, e):
    return a*x**4 + b*x**3 + c*x**2 + d*x + e


if __name__ == '__main__':
    data = pd.read_csv('regression_x_y.2.csv', ';')
    x = data['X']
    y = data['Y']

    # как вариант
    #best_vals = np.polyfit(x=x, y=y, deg=4)

    plt.figure()
    plt.plot(x, y, 'ro')
    best_vals, covar = curve_fit(polynom, x, y)
    plt.plot(x, polynom(x, best_vals[0], best_vals[1], best_vals[2], best_vals[3], best_vals[4]))
    best_vals, covar = curve_fit(gaussian, x, y)
    plt.plot(x, gaussian(x, best_vals[0], best_vals[1]))

    plt.ylabel('Y')
    plt.xlabel('X')
    plt.show()
