# -*- coding: utf-8 -*-
'''
1.
Просмотрите данные в regression_x_y.csv файле. Постройте график по точкам.
'''
import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
import matplotlib.pyplot as plt

def polynom(x, a, b, c, d, e):
    return a*x**4 + b*x**3 + c*x**2 + d*x + e

if __name__ == '__main__':
    data = pd.read_csv('regression_x_y.csv', ';')
    x = data['X']
    y = data['Y']

    best_vals, covar = curve_fit(polynom, x, y)

    plt.figure()
    plt.plot(data['X'], data['Y'], 'ro')
    plt.plot(x, polynom(x, best_vals[0], best_vals[1], best_vals[2], best_vals[3], best_vals[4]))
    plt.title('Regression')
    plt.ylabel('Y')
    plt.xlabel('X')
    plt.show()
