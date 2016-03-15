# -*- coding: utf-8 -*-
'''
4.
Известно, что функция регрессии представляет собой полином четвертой степени.
Напишите функцию штрафа, которая принимает на вход коэфициенты полинома, а на
выходе выдает штраф по точкам.
'''
import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
import matplotlib.pyplot as plt
from math import sqrt, pi, exp


def polynom(x, a, b, c, d, e):
    return a*x**4 + b*x**3 + c*x**2 + d*x + e

def penalty(x, y, coeff):
    pen = 0
    for i,j in zip(x,y):
        pen += abs(j - polynom(i, coeff[0], coeff[1], coeff[2], coeff[3], coeff[4]))
    return pen

if __name__ == '__main__':
    data = pd.read_csv('regression_x_y.2.csv', ';')
    x = data['X']
    y = data['Y']

    a = penalty(x, y, [  2.00161138,   -90.0489400,    1332.52062,   -7124.16618,    9612.19685])
    print 'общий штраф:  ', a


    # как вариант
    #best_vals = np.polyfit(x=x, y=y, deg=4)

    # best_vals, covar = curve_fit(polynom, x, y)
    # plt.plot(x, polynom(x, best_vals[0], best_vals[1], best_vals[2], best_vals[3], best_vals[4]))
